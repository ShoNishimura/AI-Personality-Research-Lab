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
    experience_by_id,
    experience_ids,
    load_yaml,
    make_api_failure,
    parse_structured_response,
    render_generation_prompts,
    response_metadata,
    sha256_text,
    stimuli_for_split,
    write_jsonl,
    write_runtime_environment,
)


def build_manifest(config: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for rep in range(1, int(config["replicates"]) + 1):
        for stim in stimuli_for_split(config["stimulus_split"]):
            for exp_id in experience_ids():
                identity = {
                    "family_id": stim["family_id"],
                    "exp_id": exp_id,
                    "replicate_id": f"R{rep:03d}",
                }
                system, user = render_generation_prompts(stim, exp_id)
                rows.append({
                    "run_id": sha256_text(canonical_json(identity))[:16],
                    **identity,
                    "stimulus_id": stim["id"],
                    "prompt_sha256": sha256_text(system + "\n" + user),
                    "situation_sha256": sha256_text(stim["situation"]),
                    "experience_sha256": sha256_text(experience_by_id(exp_id)["packet"]),
                })
    random.Random(int(config["randomization_seed"])).shuffle(rows)
    return rows


def ensure_pretest(config: dict[str, Any]) -> None:
    if not config.get("require_pretest_pass", False):
        return
    path = ROOT / config["pretest_analysis_path"]
    if not path.exists():
        raise RuntimeError("pretest analysis not found; run python -m src.pretest and python -m src.pretest_analyze first")
    result = json.loads(path.read_text(encoding="utf-8"))
    if not result.get("all_gates_pass"):
        raise RuntimeError("pretest did not pass; main generation is prohibited")
    if result.get("design_hashes") != design_hashes():
        raise RuntimeError("design hashes changed after pretest; refusing main generation")


def generate(client: Any, config: dict[str, Any], row: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    stim = {s["id"]: s for s in stimuli_for_split(config["stimulus_split"])}[row["stimulus_id"]]
    system, user = render_generation_prompts(stim, row["exp_id"])
    started = datetime.now(UTC).isoformat()
    response = client.responses.create(
        model=config["model"],
        instructions=system,
        input=user,
        max_output_tokens=int(config["max_output_tokens"]),
        store=False,
        text={"format": {"type": "json_schema", "name": "aprl_pf_exp_0007_response", "strict": True, "schema": schema}},
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
        "parsed_output": parsed,
    }


def run(config_path: Path, dry_run: bool) -> int:
    config = load_yaml(config_path)
    manifest = build_manifest(config)
    manifest_path = ROOT / config["manifest_path"]
    results_path = ROOT / config["results_path"]
    write_jsonl(manifest_path, manifest, refuse_change=True)
    print(f"main manifest: {manifest_path} ({len(manifest)} runs)")
    if dry_run:
        print("dry-run: no API requests sent")
        return 0

    ensure_pretest(config)
    write_runtime_environment(ROOT / config["environment_path"])
    from openai import OpenAIError

    schema = json.loads((ROOT / config["output_schema"]).read_text(encoding="utf-8"))
    client = create_openai_client()
    completed = completed_ids(results_path, "run_id")
    errors = (OpenAIError, ResponseOutputError, json.JSONDecodeError, jsonschema.ValidationError, ValueError)
    halt = False

    for index, row in enumerate(manifest, start=1):
        if row["run_id"] in completed:
            print(f"[{index}/{len(manifest)}] skip {row['run_id']}")
            continue
        for attempt in range(1, int(config["max_retries"]) + 2):
            try:
                record = generate(client, config, row, schema)
                record["attempt"] = attempt
                append_jsonl(results_path, record)
                print(f"[{index}/{len(manifest)}] ok {row['run_id']}")
                break
            except errors as exc:
                append_jsonl(results_path, make_api_failure(exc, row, config, attempt))
                if attempt > int(config["max_retries"]):
                    print(f"[{index}/{len(manifest)}] failed {row['run_id']}: {type(exc).__name__}", file=sys.stderr)
                    halt = isinstance(exc, OpenAIError)
                else:
                    time.sleep(1)
        if halt:
            break

    expected = {r["run_id"] for r in manifest}
    succeeded = completed_ids(results_path, "run_id") & expected
    missing = expected - succeeded
    print(f"generation summary: planned={len(expected)} succeeded={len(succeeded)} missing={len(missing)}")
    return 0 if not missing else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Run PF-EXP-0007 main generation.")
    parser.add_argument("--config", type=Path, default=ROOT / "experiment.yaml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.config.resolve(), args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
