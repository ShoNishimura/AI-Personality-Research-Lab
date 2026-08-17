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
    experience_by_id,
    experience_ids,
    load_yaml,
    make_api_failure,
    parse_structured_response,
    response_metadata,
    sha256_text,
    stimuli_for_split,
    write_jsonl,
    write_runtime_environment,
)

EXPERIENCE_PRETEST = "experience_quality"
SITUATION_PRETEST = "situation_affordance"


def render_pretest_prompts(stimulus: dict[str, Any], kind: str, exp_id: str | None = None) -> tuple[str, str]:
    system = (ROOT / "prompts/pretest-system.md").read_text(encoding="utf-8")
    if kind == EXPERIENCE_PRETEST:
        if exp_id is None:
            raise ValueError("experience_quality pretest requires exp_id")
        mode = "EXPERIENCE_QUALITY"
        experience = experience_by_id(exp_id)["packet"]
    elif kind == SITUATION_PRETEST:
        if exp_id is not None:
            raise ValueError("situation_affordance pretest must not receive exp_id")
        mode = "SITUATION_AFFORDANCE"
        experience = "[not shown in SITUATION_AFFORDANCE mode]"
    else:
        raise ValueError(f"unknown pretest kind: {kind}")

    user = (ROOT / "prompts/pretest-task.md").read_text(encoding="utf-8").format(
        pretest_mode=mode,
        situation=stimulus["situation"],
        experience=experience,
    )
    return system, user


def build_pretest_manifest(config: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for rep in range(1, int(config["pretest_replicates"]) + 1):
        for stim in stimuli_for_split(config["stimulus_split"]):
            for exp_id in experience_ids():
                system, user = render_pretest_prompts(stim, EXPERIENCE_PRETEST, exp_id)
                identity = {
                    "pretest_kind": EXPERIENCE_PRETEST,
                    "family_id": stim["family_id"],
                    "exp_id": exp_id,
                    "replicate_id": f"R{rep:03d}",
                }
                rows.append({
                    "pretest_id": sha256_text(canonical_json(identity))[:16],
                    **identity,
                    "stimulus_id": stim["id"],
                    "prompt_sha256": sha256_text(system + "\n" + user),
                    "situation_sha256": sha256_text(stim["situation"]),
                    "experience_sha256": sha256_text(experience_by_id(exp_id)["packet"]),
                })

            system, user = render_pretest_prompts(stim, SITUATION_PRETEST)
            identity = {
                "pretest_kind": SITUATION_PRETEST,
                "family_id": stim["family_id"],
                "replicate_id": f"R{rep:03d}",
            }
            rows.append({
                "pretest_id": sha256_text(canonical_json(identity))[:16],
                **identity,
                "stimulus_id": stim["id"],
                "prompt_sha256": sha256_text(system + "\n" + user),
                "situation_sha256": sha256_text(stim["situation"]),
            })

    random.Random(int(config["pretest_randomization_seed"])).shuffle(rows)
    return rows


def evaluate_packet(client: Any, config: dict[str, Any], row: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    stimuli = {s["id"]: s for s in stimuli_for_split(config["stimulus_split"])}
    stim = stimuli[row["stimulus_id"]]
    exp_id = row.get("exp_id") if row["pretest_kind"] == EXPERIENCE_PRETEST else None
    system, user = render_pretest_prompts(stim, row["pretest_kind"], exp_id)
    started = datetime.now(UTC).isoformat()
    response = client.responses.create(
        model=config["pretest_model"],
        instructions=system,
        input=user,
        max_output_tokens=int(config["pretest_max_output_tokens"]),
        store=False,
        text={"format": {"type": "json_schema", "name": "aprl_pf_exp_0007_pretest", "strict": True, "schema": schema}},
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
    exp_count = sum(r["pretest_kind"] == EXPERIENCE_PRETEST for r in manifest)
    situation_count = sum(r["pretest_kind"] == SITUATION_PRETEST for r in manifest)
    print(f"pretest manifest: {manifest_path} ({len(manifest)} runs: experience={exp_count}, situation={situation_count})")
    if dry_run:
        print("dry-run: no API requests sent")
        return 0

    write_runtime_environment(ROOT / config["pretest_environment_path"], refuse_change=True)
    from openai import OpenAIError

    schema = json.loads((ROOT / config["pretest_schema"]).read_text(encoding="utf-8"))
    client = create_openai_client()
    completed = completed_ids(results_path, "pretest_id")
    errors = (OpenAIError, ResponseOutputError, json.JSONDecodeError, jsonschema.ValidationError, ValueError)
    halt = False

    for index, row in enumerate(manifest, start=1):
        if row["pretest_id"] in completed:
            print(f"[{index}/{len(manifest)}] skip {row['pretest_id']}")
            continue
        for attempt in range(1, int(config["max_retries"]) + 2):
            try:
                record = evaluate_packet(client, config, row, schema)
                record["attempt"] = attempt
                append_jsonl(results_path, record)
                print(f"[{index}/{len(manifest)}] ok {row['pretest_id']} ({row['pretest_kind']})")
                break
            except errors as exc:
                append_jsonl(results_path, make_api_failure(exc, row, config, attempt))
                if attempt > int(config["max_retries"]):
                    print(f"[{index}/{len(manifest)}] failed {row['pretest_id']}: {type(exc).__name__}", file=sys.stderr)
                    halt = isinstance(exc, OpenAIError)
                else:
                    time.sleep(1)
        if halt:
            break

    expected = {r["pretest_id"] for r in manifest}
    succeeded = completed_ids(results_path, "pretest_id") & expected
    missing = expected - succeeded
    print(f"pretest summary: planned={len(expected)} succeeded={len(succeeded)} missing={len(missing)}")
    return 0 if not missing else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Run PF-EXP-0007 split pretest.")
    parser.add_argument("--config", type=Path, default=ROOT / "experiment.yaml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.config.resolve(), args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
