from __future__ import annotations

import argparse
import random
from pathlib import Path
from typing import Any

from .common import ROOT, load_yaml, read_jsonl, sha256_text, write_jsonl


def build_blind_files(config: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    results = [row for row in read_jsonl(ROOT / config["results_path"]) if row.get("status") == "succeeded"]
    manifest = read_jsonl(ROOT / config["manifest_path"])
    expected = {row["run_id"] for row in manifest}
    succeeded = {row["run_id"] for row in results}
    if succeeded != expected:
        missing = sorted(expected - succeeded)
        extra = sorted(succeeded - expected)
        raise ValueError(f"generation incomplete or mismatched: missing={len(missing)} extra={len(extra)}")

    blind_rows: list[dict[str, Any]] = []
    key_rows: list[dict[str, Any]] = []
    salt = str(config["blind_randomization_seed"])
    for row in results:
        blind_id = sha256_text(f"{salt}:{row['run_id']}")[:16]
        interpretation = row["parsed_output"]["interpretation"]
        blind_rows.append({"blind_id": blind_id, "interpretation": interpretation})
        key_rows.append(
            {
                "blind_id": blind_id,
                "run_id": row["run_id"],
                "condition_id": row["condition_id"],
                "stimulus_id": row["stimulus_id"],
                "stimulus_class": row["stimulus_class"],
                "replicate_id": row["replicate_id"],
            }
        )

    random.Random(int(config["blind_randomization_seed"])).shuffle(blind_rows)
    return blind_rows, key_rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Create PF-EXP-0001 blind evaluation files.")
    parser.add_argument("--config", type=Path, default=ROOT / "experiment.yaml")
    args = parser.parse_args()
    config = load_yaml(args.config.resolve())
    blind_rows, key_rows = build_blind_files(config)
    write_jsonl(ROOT / config["blind_set_path"], blind_rows)
    write_jsonl(ROOT / config["blind_key_path"], key_rows)
    print(f"blind set: {len(blind_rows)} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
