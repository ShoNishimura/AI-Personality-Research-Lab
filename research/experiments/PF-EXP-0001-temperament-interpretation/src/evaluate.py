from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import jsonschema

from .common import ROOT, append_jsonl, completed_ids, load_yaml, read_jsonl, render_evaluator_prompts
from .pilot import create_openai_client, usage_dict


def evaluate_one(client: Any, config: dict[str, Any], row: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    system, user = render_evaluator_prompts(row["interpretation"])
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
                "name": "aprl_pf_exp_0001_blind_score",
                "strict": True,
                "schema": schema,
            }
        },
    )
    raw_text = response.output_text
    parsed = json.loads(raw_text)
    jsonschema.validate(parsed, schema)
    return {
        "blind_id": row["blind_id"],
        "status": "succeeded",
        "started_at": started,
        "completed_at": datetime.now(UTC).isoformat(),
        "model_requested": config["evaluation_model"],
        "model_returned": getattr(response, "model", None),
        "response_id": getattr(response, "id", None),
        "x_request_id": getattr(response, "_request_id", None),
        "http_status": 200,
        "store": False,
        "scores": parsed,
        "usage": usage_dict(response),
    }


def run(config_path: Path, dry_run: bool) -> int:
    config = load_yaml(config_path)
    blind_path = ROOT / config["blind_set_path"]
    rows = read_jsonl(blind_path)
    if not rows:
        raise FileNotFoundError(f"blind set not found or empty: {blind_path}; run python -m src.blind first")
    if dry_run:
        print(f"evaluation dry-run: {len(rows)} blind records; no API requests sent")
        return 0

    from openai import APIStatusError, OpenAIError

    schema = json.loads((ROOT / config["evaluation_schema"]).read_text(encoding="utf-8"))
    output_path = ROOT / config["evaluation_results_path"]
    completed = completed_ids(output_path, "blind_id")
    client = create_openai_client()
    technical_errors = (OpenAIError, json.JSONDecodeError, jsonschema.ValidationError, ValueError)
    failures = 0
    halt_new_requests = False

    for index, row in enumerate(rows, start=1):
        if row["blind_id"] in completed:
            print(f"[{index}/{len(rows)}] skip {row['blind_id']}")
            continue
        for attempt in range(int(config["max_retries"]) + 1):
            try:
                record = evaluate_one(client, config, row, schema)
                record["attempt"] = attempt + 1
                append_jsonl(output_path, record)
                print(f"[{index}/{len(rows)}] ok {row['blind_id']}")
                break
            except technical_errors as exc:
                failure_record = {
                    "blind_id": row["blind_id"],
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
                append_jsonl(output_path, failure_record)
                if attempt >= int(config["max_retries"]):
                    failures += 1
                    print(
                        f"[{index}/{len(rows)}] failed {row['blind_id']}: {type(exc).__name__}",
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
    parser = argparse.ArgumentParser(description="Blind-evaluate PF-EXP-0001 interpretations.")
    parser.add_argument("--config", type=Path, default=ROOT / "experiment.yaml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.config.resolve(), args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
