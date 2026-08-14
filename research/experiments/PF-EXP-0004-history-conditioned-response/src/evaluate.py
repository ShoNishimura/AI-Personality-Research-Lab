from __future__ import annotations

import argparse
import json
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
    completed_ids,
    create_openai_client,
    load_yaml,
    parse_structured_response,
    read_jsonl,
    render_evaluator_prompts,
    response_metadata,
    write_runtime_environment,
)


def evaluate_one(client: Any, config: dict[str, Any], row: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    system, user = render_evaluator_prompts(row)
    started = datetime.now(UTC).isoformat()
    response = client.responses.create(
        model=config["evaluation_model"],
        instructions=system,
        input=user,
        max_output_tokens=int(config["evaluation_max_output_tokens"]),
        store=False,
        text={
            "format": {
                "type": "json_schema",
                "name": "aprl_pf_exp_0004_blind_response_score",
                "strict": True,
                "schema": schema,
            }
        },
    )
    parsed = parse_structured_response(response, schema)
    return {
        "blind_id": row["blind_id"],
        "experiment_phase": config["phase"],
        "status": "succeeded",
        "started_at": started,
        "completed_at": datetime.now(UTC).isoformat(),
        "model_requested": config["evaluation_model"],
        **response_metadata(response),
        "store": False,
        "scores": parsed,
    }


def run(config_path: Path, dry_run: bool) -> int:
    config = load_yaml(config_path)
    rows = read_jsonl(ROOT / config["blind_set_path"])
    if not rows:
        raise FileNotFoundError("blind set not found or empty; run python -m src.blind first")
    if dry_run:
        print(f"evaluation dry-run: {len(rows)} blind records; no API requests sent")
        return 0

    write_runtime_environment(ROOT / config["environment_path"])
    from openai import APIStatusError, OpenAIError

    schema = json.loads((ROOT / config["evaluation_schema"]).read_text(encoding="utf-8"))
    output_path = ROOT / config["evaluation_results_path"]
    completed = completed_ids(output_path, "blind_id")
    client = create_openai_client()
    errors = (OpenAIError, ResponseOutputError, json.JSONDecodeError, jsonschema.ValidationError, ValueError)
    halt = False

    for index, row in enumerate(rows, start=1):
        if row["blind_id"] in completed:
            print(f"[{index}/{len(rows)}] skip {row['blind_id']}")
            continue
        for attempt in range(1, int(config["max_retries"]) + 2):
            try:
                record = evaluate_one(client, config, row, schema)
                record["attempt"] = attempt
                append_jsonl(output_path, record)
                print(f"[{index}/{len(rows)}] ok {row['blind_id']}")
                break
            except errors as exc:
                error_type = exc.error_type if isinstance(exc, ResponseOutputError) else type(exc).__name__
                failure: dict[str, Any] = {
                    "blind_id": row["blind_id"],
                    "experiment_phase": config["phase"],
                    "status": "failed",
                    "attempt": attempt,
                    "failed_at": datetime.now(UTC).isoformat(),
                    "error_type": error_type,
                    "error": str(exc),
                }
                if isinstance(exc, ResponseOutputError):
                    failure.update(exc.metadata)
                if isinstance(exc, APIStatusError):
                    body = exc.body if isinstance(exc.body, dict) else {}
                    detail = body.get("error", body) if isinstance(body, dict) else {}
                    failure.update(
                        {
                            "http_status": exc.status_code,
                            "api_error_type": detail.get("type") if isinstance(detail, dict) else None,
                            "api_error_code": detail.get("code") if isinstance(detail, dict) else None,
                            "x_request_id": exc.response.headers.get("x-request-id") if exc.response is not None else None,
                        }
                    )
                append_jsonl(output_path, failure)
                if attempt > int(config["max_retries"]):
                    print(f"[{index}/{len(rows)}] failed {row['blind_id']}: {error_type}", file=sys.stderr)
                    if isinstance(exc, OpenAIError):
                        halt = True
                else:
                    time.sleep(1)
        if halt:
            break

    expected = {row["blind_id"] for row in rows}
    succeeded = completed_ids(output_path, "blind_id") & expected
    missing = expected - succeeded
    print(f"evaluation summary: planned={len(expected)} succeeded={len(succeeded)} missing={len(missing)}")
    return 0 if not missing else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Blind-evaluate PF-EXP-0004 responses.")
    parser.add_argument("--config", type=Path, default=ROOT / "experiment.yaml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.config.resolve(), args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
