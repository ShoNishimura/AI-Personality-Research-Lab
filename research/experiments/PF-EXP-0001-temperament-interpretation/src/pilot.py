from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import jsonschema

from .common import (
    ROOT,
    append_jsonl,
    canonical_json,
    completed_ids,
    load_yaml,
    render_generation_prompts,
    sha256_text,
    write_jsonl,
)


def build_manifest(config: dict[str, Any]) -> list[dict[str, Any]]:
    conditions = load_yaml(ROOT / "conditions.yaml")["conditions"]
    stimuli = [
        item
        for item in load_yaml(ROOT / "stimuli.yaml")["stimuli"]
        if item["split"] == config["stimulus_split"]
    ]
    rows: list[dict[str, Any]] = []
    for replicate in range(1, int(config["replicates"]) + 1):
        for condition in conditions:
            for stimulus in stimuli:
                system, user = render_generation_prompts(condition, stimulus)
                identity = {
                    "condition_id": condition["id"],
                    "stimulus_id": stimulus["id"],
                    "replicate_id": f"R{replicate:03d}",
                }
                rows.append(
                    {
                        "run_id": sha256_text(canonical_json(identity))[:16],
                        **identity,
                        "stimulus_class": stimulus["class"],
                        "prompt_sha256": sha256_text(system + "\n" + user),
                        "temperament_prompt_sha256": sha256_text(user.split("\n\n", 1)[0]),
                        "stimulus_sha256": sha256_text(stimulus["text"]),
                    }
                )
    random.Random(int(config["randomization_seed"])).shuffle(rows)
    max_runs = config.get("max_runs")
    return rows[: int(max_runs)] if max_runs is not None else rows


def create_openai_client() -> Any:
    from openai import OpenAI

    client = OpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        base_url="https://api.openai.com/v1",
    )
    client.organization = None
    client.project = None
    return client


def usage_dict(response: Any) -> dict[str, Any]:
    usage = getattr(response, "usage", None)
    if usage is None:
        return {}
    return usage.model_dump(mode="json") if hasattr(usage, "model_dump") else dict(usage)


def execute_run(client: Any, config: dict[str, Any], row: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    conditions = {item["id"]: item for item in load_yaml(ROOT / "conditions.yaml")["conditions"]}
    stimuli = {item["id"]: item for item in load_yaml(ROOT / "stimuli.yaml")["stimuli"]}
    system, user = render_generation_prompts(conditions[row["condition_id"]], stimuli[row["stimulus_id"]])
    started = datetime.now(UTC).isoformat()
    response = client.responses.create(
        model=config["model"],
        instructions=system,
        input=user,
        max_output_tokens=int(config["max_output_tokens"]),
        store=False,
        text={
            "format": {
                "type": "json_schema",
                "name": "aprl_pf_exp_0001_interpretation",
                "strict": True,
                "schema": schema,
            }
        },
    )
    raw_text = response.output_text
    parsed = json.loads(raw_text)
    jsonschema.validate(parsed, schema)
    return {
        **row,
        "status": "succeeded",
        "started_at": started,
        "completed_at": datetime.now(UTC).isoformat(),
        "model_requested": config["model"],
        "model_returned": getattr(response, "model", None),
        "response_id": getattr(response, "id", None),
        "x_request_id": getattr(response, "_request_id", None),
        "http_status": 200,
        "store": False,
        "raw_output": raw_text,
        "parsed_output": parsed,
        "usage": usage_dict(response),
    }


def run(config_path: Path, dry_run: bool) -> int:
    config = load_yaml(config_path)
    manifest = build_manifest(config)
    manifest_path = ROOT / config["manifest_path"]
    results_path = ROOT / config["results_path"]
    write_jsonl(manifest_path, manifest, refuse_change=True)
    print(f"manifest: {manifest_path} ({len(manifest)} runs)")
    if dry_run:
        print("dry-run: no API requests sent")
        return 0

    from openai import APIStatusError, OpenAIError

    schema = json.loads((ROOT / config["output_schema"]).read_text(encoding="utf-8"))
    client = create_openai_client()
    technical_errors = (OpenAIError, json.JSONDecodeError, jsonschema.ValidationError, ValueError)
    completed = completed_ids(results_path, "run_id")
    failures = 0
    halt_new_requests = False

    for index, row in enumerate(manifest, start=1):
        if row["run_id"] in completed:
            print(f"[{index}/{len(manifest)}] skip {row['run_id']}")
            continue
        for attempt in range(int(config["max_retries"]) + 1):
            try:
                record = execute_run(client, config, row, schema)
                record["attempt"] = attempt + 1
                append_jsonl(results_path, record)
                print(f"[{index}/{len(manifest)}] ok {row['run_id']}")
                break
            except technical_errors as exc:
                failure_record = {
                    **row,
                    "status": "failed",
                    "attempt": attempt + 1,
                    "failed_at": datetime.now(UTC).isoformat(),
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
                if isinstance(exc, APIStatusError):
                    body = exc.body if isinstance(exc.body, dict) else {}
                    detail = body.get("error", body) if isinstance(body, dict) else {}
                    failure_record.update(
                        {
                            "http_status": exc.status_code,
                            "api_error_type": detail.get("type") if isinstance(detail, dict) else None,
                            "api_error_code": detail.get("code") if isinstance(detail, dict) else None,
                            "x_request_id": (
                                exc.response.headers.get("x-request-id") if exc.response is not None else None
                            ),
                        }
                    )
                append_jsonl(results_path, failure_record)
                if attempt >= int(config["max_retries"]):
                    failures += 1
                    print(
                        f"[{index}/{len(manifest)}] failed {row['run_id']}: {type(exc).__name__}",
                        file=sys.stderr,
                    )
                    if isinstance(exc, OpenAIError):
                        halt_new_requests = True
                else:
                    time.sleep(1)
        if halt_new_requests:
            break
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run PF-EXP-0001 pilot generation.")
    parser.add_argument("--config", type=Path, default=ROOT / "experiment.yaml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.config.resolve(), args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
