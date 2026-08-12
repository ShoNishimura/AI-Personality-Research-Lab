from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path

from src.pilot import ROOT, canonical_json, load_yaml, write_jsonl


def blind_id(run_id: str, salt: str) -> str:
    return hashlib.sha256(f"{salt}:{run_id}".encode()).hexdigest()[:16]


def build_blind_files(results_path: Path, seed: int, salt: str) -> tuple[list[dict], list[dict]]:
    stimuli = {item["id"]: item for item in load_yaml(ROOT / "stimuli.yaml")["stimuli"]}
    evaluations: list[dict] = []
    key: list[dict] = []
    with results_path.open(encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            if record.get("status") != "succeeded":
                continue
            blinded = blind_id(record["run_id"], salt)
            evaluations.append({
                "blind_id": blinded,
                "experience": stimuli[record["stimulus_id"]]["text"],
                "interpretation": record["parsed_output"]["interpretation"]["summary"],
                "action": record["parsed_output"]["response"]["action"],
                "ratings": None,
            })
            key.append({
                "blind_id": blinded,
                "run_id": record["run_id"],
                "condition_id": record["condition_id"],
                "stimulus_id": record["stimulus_id"],
            })
    random.Random(seed).shuffle(evaluations)
    return evaluations, key


def main() -> int:
    parser = argparse.ArgumentParser(description="Create condition-masked files for independent human review.")
    parser.add_argument("results", type=Path, nargs="?", default=ROOT / "runs/pilot-002/results.jsonl")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "runs/pilot-002/blind")
    parser.add_argument("--seed", type=int, default=20260811)
    parser.add_argument("--salt", required=True, help="Private run-specific salt; do not commit it.")
    args = parser.parse_args()
    evaluations, key = build_blind_files(args.results, args.seed, args.salt)
    write_jsonl(args.output_dir / "evaluation.jsonl", evaluations)
    write_jsonl(args.output_dir / "key.jsonl", key)
    print(canonical_json({"blinded": len(evaluations)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
