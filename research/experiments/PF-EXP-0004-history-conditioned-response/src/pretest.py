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
    create_openai_client,
    history_by_id,
    load_yaml,
    parse_structured_response,
    render_history,
    render_pretest_prompts,
    response_metadata,
    sha256_text,
    stimuli_for_split,
    write_jsonl,
    write_runtime_environment,
)


def build_pretest_manifest(config: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for replicate in range(1, int(config["pretest_replicates"]) + 1):
        for stimulus in stimuli_for_split(config["stimulus_split"]):
            for history in stimulus["histories"]:
                system, user = render_pretest_prompts(stimulus, history["id"])
                identity = {
                    "family_id": stimulus["family_id"],
                    "history_id": history["id"],
                    "replicate_id": f"R{replicate:03d}",
                }
                rows.append(
                    {
                        "pretest_id": sha256_text(canonical_json(identity))[:16],
                        **identity,
                        "stimulus_id": stimulus["id"],
                        "history_valence": history["valence"],
                        "prompt_sha256": sha256_text(system + "\n" + user),
                        "history_sha256": sha256_text(render_history(history)),
                    }
                )
    random.Random(int(config["pretest_randomization_seed"])).shuffle(rows)
    return rows


def evaluate_history(client: Any, config: dict[str, Any], row: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    stimuli = {item["id"]: item for item in stimuli_for_split(config["stimulus_split"])}
    stimulus = stimuli[row["stimulus_id"]]
    history = history_by_id(stimulus, row["history_id"])
    if history["valence"] != row["history_valence"]:
        raise ValueError("history metadata mismatch")
    system, user = render_pretest_prompts(stimulus, row["history_id"])
    started = datetime.now(UTC).isoformat()
    response = client.responses.create(
        model=config["pretest_model"],
        instructions=system,
        input=user,
        max_output_tokens=int(config["pretest_max_output_tokens"]),
        store=False,
        text={
            "format": {
                "type": "json_schema",
                "name": "aprl_pf_exp_0004_history_pretest",
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
        "model_requested": config["pretest_model"],
        **response_metadata(response),
        "store": False,
        "scores": parsed,
    }


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
        for attempt in range(1, int(config["max_retries"]) + 2):
            try:
                record = evaluate_history(client, config, row, schema)
                record["attempt"] = attempt
                append_jsonl(results_path, record)
                print(f"[{index}/{len(manifest)}] ok {row['pretest_id']}")
                break
            except errors as exc:
                error_type = exc.error_type if isinstance(exc, ResponseOutputError) else type(exc).__name__
                failure: dict[str, Any] = {
                    **row,
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
                append_jsonl(results_path, failure)
                if attempt > int(config["max_retries"]):
                    print(f"[{index}/{len(manifest)}] failed {row['pretest_id']}: {error_type}", file=sys.stderr)
                    if isinstance(exc, OpenAIError):
                        halt = True
                else:
                    time.sleep(1)
        if halt:
            break

    expected = {row["pretest_id"] for row in manifest}
    succeeded = completed_ids(results_path, "pretest_id") & expected
    missing = expected - succeeded
    print(f"pretest summary: planned={len(expected)} succeeded={len(succeeded)} missing={len(missing)}")
    return 0 if not missing else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Blind-pretest PF-EXP-0004 histories.")
    parser.add_argument("--config", type=Path, default=ROOT / "experiment.yaml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.config.resolve(), args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
