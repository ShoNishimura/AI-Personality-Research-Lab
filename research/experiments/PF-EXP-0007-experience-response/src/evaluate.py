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
    make_api_failure,
    parse_structured_response,
    read_jsonl,
    render_evaluator_prompts,
    response_metadata,
)


def evaluate_row(client: Any, config: dict[str, Any], row: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    system, user = render_evaluator_prompts(row)
    started = datetime.now(UTC).isoformat()
    response = client.responses.create(
        model=config["evaluation_model"],
        instructions=system,
        input=user,
        max_output_tokens=int(config["evaluation_max_output_tokens"]),
        store=False,
        text={"format": {"type": "json_schema", "name": "aprl_pf_exp_0007_evaluation", "strict": True, "schema": schema}},
    )
    parsed = parse_structured_response(response, schema)
    return {
        "evaluation_id": row["evaluation_id"],
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
    blind_path = ROOT / config["blind_set_path"]
    if not blind_path.exists():
        raise RuntimeError(f"blind set not found: {blind_path}; run python -m src.blind first")
    rows = read_jsonl(blind_path)
    if dry_run:
        print(f"blind evaluation manifest: {len(rows)} rows")
        print("dry-run: no API requests sent")
        return 0

    from openai import OpenAIError

    schema = json.loads((ROOT / config["evaluation_schema"]).read_text(encoding="utf-8"))
    client = create_openai_client()
    results_path = ROOT / config["evaluation_results_path"]
    completed = completed_ids(results_path, "evaluation_id")
    errors = (OpenAIError, ResponseOutputError, json.JSONDecodeError, jsonschema.ValidationError, ValueError)
    halt = False

    for index, row in enumerate(rows, start=1):
        if row["evaluation_id"] in completed:
            print(f"[{index}/{len(rows)}] skip {row['evaluation_id']}")
            continue
        for attempt in range(1, int(config["max_retries"]) + 2):
            try:
                record = evaluate_row(client, config, row, schema)
                record["attempt"] = attempt
                append_jsonl(results_path, record)
                print(f"[{index}/{len(rows)}] ok {row['evaluation_id']}")
                break
            except errors as exc:
                append_jsonl(results_path, make_api_failure(exc, row, config, attempt))
                if attempt > int(config["max_retries"]):
                    print(f"[{index}/{len(rows)}] failed {row['evaluation_id']}: {type(exc).__name__}", file=sys.stderr)
                    halt = isinstance(exc, OpenAIError)
                else:
                    time.sleep(1)
        if halt:
            break

    expected = {str(r["evaluation_id"]) for r in rows}
    succeeded = completed_ids(results_path, "evaluation_id") & expected
    missing = expected - succeeded
    print(f"evaluation summary: planned={len(expected)} succeeded={len(succeeded)} missing={len(missing)}")
    return 0 if not missing else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Blind-evaluate PF-EXP-0007 Actions.")
    parser.add_argument("--config", type=Path, default=ROOT / "experiment.yaml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.config.resolve(), args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
