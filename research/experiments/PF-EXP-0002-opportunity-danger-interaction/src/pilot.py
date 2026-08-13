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
    ResponseOutputError,
    append_jsonl,
    canonical_json,
    completed_ids,
    load_yaml,
    parse_structured_response,
    render_generation_prompts,
    response_metadata,
    sha256_text,
    write_jsonl,
    write_runtime_environment,
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
                        "family_id": stimulus["family_id"],
                        "opportunity": stimulus["opportunity"],
                        "danger": stimulus["danger"],
                        "prompt_sha256": sha256_text(system + "\n" + user),
                        "temperament_prompt_sha256": sha256_text(user.split("\n\n", 1)[0]),
                        "stimulus_sha256": sha256_text(stimulus["text"]),
                    }
                )
    random.Random(int(config["randomization_seed"])).shuffle(rows)
    return rows


def create_openai_client() -> Any:
    from openai import OpenAI

    client = OpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        base_url="https://api.openai.com/v1",
    )
    client.organization = None
    client.project = None
    return client


def require_pretest_pass(config: dict[str, Any]) -> None:
    if not config.get("require_pretest_pass", False):
        return
    path = ROOT / config["pretest_analysis_path"]
    if not path.exists():
        raise RuntimeError(
            f"pretest gate result not found: {path}; run python -m src.pretest_analyze first"
        )
    result = json.loads(path.read_text(encoding="utf-8"))
    if not result.get("all_gates_pass", False):
        raise RuntimeError("pretest gates did not all pass; do not start main generation")


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
                "name": "aprl_pf_exp_0002_interpretation",
                "strict": True,
                "schema": schema,
            }
        },
    )
    parsed = parse_structured_response(response, schema)
    return {
        **row,
        "experiment_phase": config["phase"],
        "status": "succeeded",
        "started_at": started,
        "completed_at": datetime.now(UTC).isoformat(),
        "model_requested": config["model"],
        **response_metadata(response),
        "store": False,
        "raw_output": response.output_text,
        "parsed_output": parsed,
    }


def print_generation_summary(manifest: list[dict[str, Any]], results_path: Path) -> int:
    expected = {row["run_id"] for row in manifest}
    succeeded = completed_ids(results_path, "run_id") & expected
    missing = expected - succeeded
    print("generation summary:")
    print(f"  planned:   {len(expected)}")
    print(f"  succeeded: {len(succeeded)}")
    print(f"  missing:   {len(missing)}")
    return len(missing)


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

    require_pretest_pass(config)
    write_runtime_environment(ROOT / config["environment_path"])

    from openai import APIStatusError, OpenAIError

    schema = json.loads((ROOT / config["output_schema"]).read_text(encoding="utf-8"))
    client = create_openai_client()
    technical_errors = (OpenAIError, ResponseOutputError, json.JSONDecodeError, jsonschema.ValidationError, ValueError)
    completed = completed_ids(results_path, "run_id")
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
                error_type = exc.error_type if isinstance(exc, ResponseOutputError) else type(exc).__name__
                failure_record = {
                    **row,
                    "experiment_phase": config["phase"],
                    "status": "failed",
                    "attempt": attempt + 1,
                    "failed_at": datetime.now(UTC).isoformat(),
                    "error_type": error_type,
                    "error": str(exc),
                }
                if isinstance(exc, ResponseOutputError):
                    failure_record.update(exc.metadata)
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
                    print(
                        f"[{index}/{len(manifest)}] failed {row['run_id']}: {error_type}",
                        file=sys.stderr,
                    )
                    if isinstance(exc, OpenAIError):
                        halt_new_requests = True
                else:
                    time.sleep(1)
        if halt_new_requests:
            break

    missing = print_generation_summary(manifest, results_path)
    return 0 if missing == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Run PF-EXP-0002 pilot generation.")
    parser.add_argument("--config", type=Path, default=ROOT / "experiment.yaml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.config.resolve(), args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
