from __future__ import annotations

import argparse
import json
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
    render_pretest_prompts,
    response_metadata,
    sha256_text,
    write_jsonl,
    write_runtime_environment,
)
from .pilot import create_openai_client


def build_pretest_manifest(config: dict[str, Any]) -> list[dict[str, Any]]:
    stimuli = [s for s in load_yaml(ROOT / "stimuli.yaml")["stimuli"] if s["split"] == config["stimulus_split"]]
    rows = []
    for replicate in range(1, int(config["pretest_replicates"]) + 1):
        for stimulus in stimuli:
            system, user = render_pretest_prompts(stimulus["text"])
            identity = {"stimulus_id": stimulus["id"], "replicate_id": f"R{replicate:03d}"}
            rows.append({
                "pretest_id": sha256_text(canonical_json(identity))[:16], **identity,
                "family_id": stimulus["family_id"], "opportunity": stimulus["opportunity"],
                "danger": stimulus["danger"], "prompt_sha256": sha256_text(system + "\n" + user),
                "stimulus_sha256": sha256_text(stimulus["text"]),
            })
    random.Random(int(config["pretest_randomization_seed"])).shuffle(rows)
    return rows


def evaluate_stimulus(client: Any, config: dict[str, Any], row: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    stimuli = {s["id"]: s for s in load_yaml(ROOT / "stimuli.yaml")["stimuli"]}
    system, user = render_pretest_prompts(stimuli[row["stimulus_id"]]["text"])
    started = datetime.now(UTC).isoformat()
    response = client.responses.create(
        model=config["pretest_model"], instructions=system, input=user,
        max_output_tokens=int(config["pretest_max_output_tokens"]), store=False,
        text={"format": {"type": "json_schema", "name": "aprl_pf_exp_0003_stimulus_pretest",
                         "strict": True, "schema": schema}},
    )
    parsed = parse_structured_response(response, schema)
    return {
        **row, "experiment_phase": config["phase"], "status": "succeeded",
        "started_at": started, "completed_at": datetime.now(UTC).isoformat(),
        "model_requested": config["pretest_model"], **response_metadata(response), "store": False, "scores": parsed,
    }


def _summary(manifest: list[dict[str, Any]], path: Path) -> int:
    expected = {r["pretest_id"] for r in manifest}
    succeeded = completed_ids(path, "pretest_id") & expected
    missing = expected - succeeded
    print("pretest summary:")
    print(f"  planned:   {len(expected)}")
    print(f"  succeeded: {len(succeeded)}")
    print(f"  missing:   {len(missing)}")
    return len(missing)


def run(config_path: Path, dry_run: bool) -> int:
    config = load_yaml(config_path)
    manifest = build_pretest_manifest(config)
    manifest_path = ROOT / config["pretest_manifest_path"]
    results_path = ROOT / config["pretest_results_path"]
    write_jsonl(manifest_path, manifest, refuse_change=True)
    print(f"pretest manifest: {manifest_path} ({len(manifest)} runs)")
    if dry_run:
        print("dry-run: no API requests sent")
        return 0
    write_runtime_environment(ROOT / config["environment_path"])
    from openai import APIStatusError, OpenAIError
    schema = json.loads((ROOT / config["pretest_schema"]).read_text(encoding="utf-8"))
    client = create_openai_client()
    errors = (OpenAIError, ResponseOutputError, json.JSONDecodeError, jsonschema.ValidationError, ValueError)
    completed = completed_ids(results_path, "pretest_id")
    halt = False
    for index, row in enumerate(manifest, start=1):
        if row["pretest_id"] in completed:
            print(f"[{index}/{len(manifest)}] skip {row['pretest_id']}")
            continue
        for attempt in range(int(config["max_retries"]) + 1):
            try:
                record = evaluate_stimulus(client, config, row, schema)
                record["attempt"] = attempt + 1
                append_jsonl(results_path, record)
                print(f"[{index}/{len(manifest)}] ok {row['pretest_id']}")
                break
            except errors as exc:
                error_type = exc.error_type if isinstance(exc, ResponseOutputError) else type(exc).__name__
                failure = {**row, "experiment_phase": config["phase"], "status": "failed",
                           "attempt": attempt + 1, "failed_at": datetime.now(UTC).isoformat(),
                           "error_type": error_type, "error": str(exc)}
                if isinstance(exc, ResponseOutputError):
                    failure.update(exc.metadata)
                if isinstance(exc, APIStatusError):
                    body = exc.body if isinstance(exc.body, dict) else {}
                    detail = body.get("error", body) if isinstance(body, dict) else {}
                    failure.update({
                        "http_status": exc.status_code,
                        "api_error_type": detail.get("type") if isinstance(detail, dict) else None,
                        "api_error_code": detail.get("code") if isinstance(detail, dict) else None,
                        "x_request_id": exc.response.headers.get("x-request-id") if exc.response is not None else None,
                    })
                append_jsonl(results_path, failure)
                if attempt >= int(config["max_retries"]):
                    print(f"[{index}/{len(manifest)}] failed {row['pretest_id']}: {error_type}", file=sys.stderr)
                    if isinstance(exc, OpenAIError):
                        halt = True
                else:
                    time.sleep(1)
        if halt:
            break
    missing = _summary(manifest, results_path)
    return 0 if missing == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Blind pretest PF-EXP-0003 stimuli.")
    parser.add_argument("--config", type=Path, default=ROOT / "experiment.yaml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.config.resolve(), args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
