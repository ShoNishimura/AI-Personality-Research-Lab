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
    load_yaml,
    make_api_failure,
    parse_structured_response,
    relationship_by_id,
    relationship_ids,
    response_metadata,
    sha256_text,
    stimuli_for_split,
    write_jsonl,
    write_runtime_environment,
)

REL_PRETEST = "relationship_quality"
BOUNDARY_PRETEST = "perception_boundary"


def render_pretest_prompts(stimulus: dict[str, Any], kind: str, rel_id: str | None = None) -> tuple[str, str]:
    system = (ROOT / "prompts/pretest-system.md").read_text(encoding="utf-8")
    if kind == REL_PRETEST:
        if rel_id is None:
            raise ValueError("relationship_quality pretest requires rel_id")
        mode = "RELATIONSHIP_QUALITY"
        perception = "[not shown in RELATIONSHIP_QUALITY mode]"
        vb = "[not shown in RELATIONSHIP_QUALITY mode]"
        relationship = relationship_by_id(rel_id)["packet"]
    elif kind == BOUNDARY_PRETEST:
        if rel_id is not None:
            raise ValueError("perception_boundary pretest must not receive rel_id")
        mode = "PERCEPTION_BOUNDARY"
        perception = stimulus["perception"]
        vb = "[not shown in PERCEPTION_BOUNDARY mode]"
        relationship = "[not shown in PERCEPTION_BOUNDARY mode]"
    else:
        raise ValueError(f"unknown pretest kind: {kind}")

    user = (ROOT / "prompts/pretest-task.md").read_text(encoding="utf-8").format(
        pretest_mode=mode,
        situation=stimulus["situation"],
        perception=perception,
        values_beliefs=vb,
        relationship=relationship,
    )
    return system, user


def build_pretest_manifest(config: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for rep in range(1, int(config["pretest_replicates"]) + 1):
        for stim in stimuli_for_split(config["stimulus_split"]):
            for rel_id in relationship_ids():
                system, user = render_pretest_prompts(stim, REL_PRETEST, rel_id)
                identity = {
                    "pretest_kind": REL_PRETEST,
                    "family_id": stim["family_id"],
                    "rel_id": rel_id,
                    "replicate_id": f"R{rep:03d}",
                }
                rows.append({
                    "pretest_id": sha256_text(canonical_json(identity))[:16],
                    **identity,
                    "stimulus_id": stim["id"],
                    "prompt_sha256": sha256_text(system + "\n" + user),
                    "situation_sha256": sha256_text(stim["situation"]),
                    "relationship_sha256": sha256_text(relationship_by_id(rel_id)["packet"]),
                })

            system, user = render_pretest_prompts(stim, BOUNDARY_PRETEST)
            identity = {
                "pretest_kind": BOUNDARY_PRETEST,
                "family_id": stim["family_id"],
                "replicate_id": f"R{rep:03d}",
            }
            rows.append({
                "pretest_id": sha256_text(canonical_json(identity))[:16],
                **identity,
                "stimulus_id": stim["id"],
                "prompt_sha256": sha256_text(system + "\n" + user),
                "situation_sha256": sha256_text(stim["situation"]),
                "perception_sha256": sha256_text(stim["perception"]),
            })

    random.Random(int(config["pretest_randomization_seed"])).shuffle(rows)
    return rows


def evaluate_packet(client: Any, config: dict[str, Any], row: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    stimuli = {s["id"]: s for s in stimuli_for_split(config["stimulus_split"])}
    stim = stimuli[row["stimulus_id"]]
    rel_id = row.get("rel_id") if row["pretest_kind"] == REL_PRETEST else None
    system, user = render_pretest_prompts(stim, row["pretest_kind"], rel_id)
    started = datetime.now(UTC).isoformat()
    response = client.responses.create(
        model=config["pretest_model"],
        instructions=system,
        input=user,
        max_output_tokens=int(config["pretest_max_output_tokens"]),
        store=False,
        text={"format": {"type": "json_schema", "name": "aprl_pf_exp_0006_pretest", "strict": True, "schema": schema}},
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
    rel_count = sum(r["pretest_kind"] == REL_PRETEST for r in manifest)
    boundary_count = sum(r["pretest_kind"] == BOUNDARY_PRETEST for r in manifest)
    print(f"pretest manifest: {manifest_path} ({len(manifest)} runs: relationship={rel_count}, boundary={boundary_count})")
    if dry_run:
        print("dry-run: no API requests sent")
        return 0

    write_runtime_environment(ROOT / config["environment_path"])
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
    parser = argparse.ArgumentParser(description="Run PF-EXP-0006 split pretest.")
    parser.add_argument("--config", type=Path, default=ROOT / "experiment.yaml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.config.resolve(), args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
