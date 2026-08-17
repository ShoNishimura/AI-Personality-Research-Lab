from __future__ import annotations

import argparse
import random
from pathlib import Path
from typing import Any

from .common import (
    ROOT,
    assert_frozen_design,
    canonical_json,
    load_yaml,
    read_jsonl,
    sha256_text,
    stimuli_for_split,
    write_jsonl,
)


def _latest(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        if row.get("status") == "succeeded" and key in row:
            out[str(row[key])] = row
    return out


def build_blind_set(config: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    assert_frozen_design(config)
    manifest = read_jsonl(ROOT / config["manifest_path"])
    successes = _latest(read_jsonl(ROOT / config["results_path"]), "run_id")
    missing = {str(r["run_id"]) for r in manifest} - set(successes)
    if missing:
        raise RuntimeError(f"main generation incomplete: {len(missing)} missing succeeded rows")

    stimuli = {s["id"]: s for s in stimuli_for_split(config["stimulus_split"])}
    blind_rows: list[dict[str, Any]] = []
    key_rows: list[dict[str, Any]] = []
    for manifest_row in manifest:
        run_id = str(manifest_row["run_id"])
        result = successes[run_id]
        stimulus = stimuli[manifest_row["stimulus_id"]]
        action = str(result["parsed_output"]["action"])
        evaluation_id = sha256_text(canonical_json({"run_id": run_id, "seed": config["blind_randomization_seed"]}))[:16]
        blind_rows.append({
            "evaluation_id": evaluation_id,
            "situation": stimulus["situation"],
            "action": action,
        })
        key_rows.append({
            "evaluation_id": evaluation_id,
            "run_id": run_id,
            "family_id": manifest_row["family_id"],
            "exp_id": manifest_row["exp_id"],
            "replicate_id": manifest_row["replicate_id"],
            "stimulus_id": manifest_row["stimulus_id"],
        })

    random.Random(int(config["blind_randomization_seed"])).shuffle(blind_rows)
    return blind_rows, key_rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Create blinded PF-EXP-0007 Action evaluation set.")
    parser.add_argument("--config", type=Path, default=ROOT / "experiment.yaml")
    args = parser.parse_args()
    config = load_yaml(args.config.resolve())
    blind_rows, key_rows = build_blind_set(config)
    write_jsonl(ROOT / config["blind_set_path"], blind_rows, refuse_change=True)
    write_jsonl(ROOT / config["blind_key_path"], key_rows, refuse_change=True)
    print(f"blind set: {len(blind_rows)} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
