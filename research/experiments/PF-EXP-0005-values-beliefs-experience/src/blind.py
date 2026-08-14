from __future__ import annotations

import argparse
import random
from pathlib import Path
from typing import Any

from .common import ROOT, canonical_json, load_yaml, read_jsonl, sha256_text, stimuli_for_split, write_jsonl


def _latest_success(rows: list[dict[str, Any]], id_key: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        if row.get("status") == "succeeded" and id_key in row:
            out[str(row[id_key])] = row
    return out


def build_blind_set(config: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    manifest = read_jsonl(ROOT / config["manifest_path"])
    successes = _latest_success(read_jsonl(ROOT / config["results_path"]), "run_id")
    expected = {str(row["run_id"]) for row in manifest}
    missing = expected - set(successes)
    if missing:
        raise RuntimeError(f"main generation incomplete: {len(missing)} missing succeeded rows")

    stimuli = {row["id"]: row for row in stimuli_for_split(config["stimulus_split"])}
    blind_rows: list[dict[str, Any]] = []
    key_rows: list[dict[str, Any]] = []
    for manifest_row in manifest:
        run_id = str(manifest_row["run_id"])
        result = successes[run_id]
        stimulus = stimuli[str(manifest_row["stimulus_id"])]
        experience = str(result["parsed_output"]["experience"])
        evaluation_id = sha256_text(canonical_json({"run_id": run_id, "seed": config["blind_randomization_seed"]}))[:16]
        blind_rows.append(
            {
                "evaluation_id": evaluation_id,
                "situation": stimulus["situation"],
                "perception": stimulus["perception"],
                "experience": experience,
            }
        )
        key_rows.append(
            {
                "evaluation_id": evaluation_id,
                "run_id": run_id,
                "family_id": manifest_row["family_id"],
                "vb_id": manifest_row["vb_id"],
                "replicate_id": manifest_row["replicate_id"],
                "stimulus_id": manifest_row["stimulus_id"],
            }
        )

    rng = random.Random(int(config["blind_randomization_seed"]))
    rng.shuffle(blind_rows)
    return blind_rows, key_rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Create blinded PF-EXP-0005 evaluation set.")
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
