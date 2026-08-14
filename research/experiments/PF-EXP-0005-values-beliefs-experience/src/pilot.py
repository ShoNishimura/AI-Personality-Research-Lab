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
    design_hashes,
    load_yaml,
    make_api_failure,
    parse_structured_response,
    render_generation_prompts,
    response_metadata,
    sha256_text,
    stimuli_for_split,
    values_beliefs_by_id,
    vb_ids,
    write_jsonl,
    write_runtime_environment,
)


def build_manifest(config: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for replicate in range(1, int(config["replicates"]) + 1):
        for stimulus in stimuli_for_split(config["stimulus_split"]):
            for vb_id in vb_ids():
                system, user = render_generation_prompts(stimulus, vb_id)
                identity = {
                    "family_id": stimulus["family_id"],
                    "vb_id": vb_id,
                    "replicate_id": f"R{replicate:03d}",
                }
                rows.append(
                    {
                        "run_id": sha256_text(canonical_json(identity))[:16],
                        **identity,
                        "stimulus_id": stimulus["id"],
                        "prompt_sha256": sha256_text(system + "\n" + user),
                        "situation_sha256": sha256_text(stimulus["situation"]),
                        "perception_sha256": sha256_text(stimulus["perception"]),
                        "vb_sha256": sha256_text(values_beliefs_by_id(vb_id)["packet"]),
                    }
                )
    random.Random(int(config["randomization_seed"])).shuffle(rows)
    return rows


def require_pretest_pass(config: dict[str, Any]) -> None:
    if not config.get("require_pretest_pass", False):
        return
    path = ROOT / config["pretest_analysis_path"]
    if not path.exists():
        raise RuntimeError(f"pretest gate result not found: {path}; run python -m src.pretest_analyze first")
    result = json.loads(path.read_text(encoding="utf-8"))
    if not result.get("all_gates_pass", False):
        raise RuntimeError("pretest gates did not all pass; do not start main generation")
    if result.get("design_hashes") != design_hashes():
        raise RuntimeError("design files changed after successful pretest; rerun pretest before main generation")


def execute_run(client: Any, config: dict[str, Any], row: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    stimuli = {item["id"]: item for item in stimuli_for_split(config["stimulus_split"])}
    stimulus = stimuli[row["stimulus_id"]]
    system, user = render_generation_prompts(stimulus, row["vb_id"])
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
                "name": "aprl_pf_exp_0005_experience",
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
    from openai import OpenAIError

    schema = json.loads((ROOT / config["output_schema"]).read_text(encoding="utf-8"))
    client = create_openai_client()
    errors = (OpenAIError, ResponseOutputError, json.JSONDecodeError, jsonschema.ValidationError, ValueError)
    completed = completed_ids(results_path, "run_id")
    halt = False

    for index, row in enumerate(manifest, start=1):
        if row["run_id"] in completed:
            print(f"[{index}/{len(manifest)}] skip {row['run_id']}")
            continue
        for attempt in range(1, int(config["max_retries"]) + 2):
            try:
                record = execute_run(client, config, row, schema)
                record["attempt"] = attempt
                append_jsonl(results_path, record)
                print(f"[{index}/{len(manifest)}] ok {row['run_id']}")
                break
            except errors as exc:
                append_jsonl(results_path, make_api_failure(exc, row, config, attempt))
                if attempt > int(config["max_retries"]):
                    print(f"[{index}/{len(manifest)}] failed {row['run_id']}: {type(exc).__name__}", file=sys.stderr)
                    if isinstance(exc, OpenAIError):
                        halt = True
                else:
                    time.sleep(1)
        if halt:
            break

    expected = {row["run_id"] for row in manifest}
    succeeded = completed_ids(results_path, "run_id") & expected
    missing = expected - succeeded
    print(f"generation summary: planned={len(expected)} succeeded={len(succeeded)} missing={len(missing)}")
    return 0 if not missing else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Run PF-EXP-0005 Experience generation.")
    parser.add_argument("--config", type=Path, default=ROOT / "experiment.yaml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.config.resolve(), args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
