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
    ROOT, ResponseOutputError, append_jsonl, completed_ids, load_yaml, parse_structured_response,
    read_jsonl, render_evaluator_prompts, response_metadata, write_runtime_environment,
)
from .pilot import create_openai_client


def evaluate_one(client: Any, config: dict[str, Any], row: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    system, user = render_evaluator_prompts(row["interpretation"])
    started = datetime.now(UTC).isoformat()
    response = client.responses.create(
        model=config["evaluation_model"], instructions=system, input=user,
        max_output_tokens=int(config["evaluation_max_output_tokens"]), store=False,
        text={"format": {"type": "json_schema", "name": "aprl_pf_exp_0003_blind_score",
                         "strict": True, "schema": schema}},
    )
    parsed = parse_structured_response(response, schema)
    return {
        "blind_id": row["blind_id"], "experiment_phase": config["phase"], "status": "succeeded",
        "started_at": started, "completed_at": datetime.now(UTC).isoformat(),
        "model_requested": config["evaluation_model"], **response_metadata(response), "store": False, "scores": parsed,
    }


def _summary(rows: list[dict[str, Any]], path: Path) -> int:
    expected = {r["blind_id"] for r in rows}
    succeeded = completed_ids(path, "blind_id") & expected
    missing = expected - succeeded
    print("evaluation summary:")
    print(f"  planned:   {len(expected)}")
    print(f"  succeeded: {len(succeeded)}")
    print(f"  missing:   {len(missing)}")
    return len(missing)


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
        for attempt in range(int(config["max_retries"]) + 1):
            try:
                record = evaluate_one(client, config, row, schema)
                record["attempt"] = attempt + 1
                append_jsonl(output_path, record)
                print(f"[{index}/{len(rows)}] ok {row['blind_id']}")
                break
            except errors as exc:
                error_type = exc.error_type if isinstance(exc, ResponseOutputError) else type(exc).__name__
                failure = {"blind_id": row["blind_id"], "experiment_phase": config["phase"], "status": "failed",
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
                append_jsonl(output_path, failure)
                if attempt >= int(config["max_retries"]):
                    print(f"[{index}/{len(rows)}] failed {row['blind_id']}: {error_type}", file=sys.stderr)
                    if isinstance(exc, OpenAIError):
                        halt = True
                else:
                    time.sleep(1)
        if halt:
            break
    missing = _summary(rows, output_path)
    return 0 if missing == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Blind-evaluate PF-EXP-0003 interpretations.")
    parser.add_argument("--config", type=Path, default=ROOT / "experiment.yaml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.config.resolve(), args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
