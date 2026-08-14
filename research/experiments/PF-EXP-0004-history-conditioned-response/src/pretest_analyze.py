from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any

from .common import ROOT, design_hashes, load_yaml, read_jsonl


def analyze_rows(rows: list[dict[str, Any]], thresholds: dict[str, Any]) -> dict[str, Any]:
    families = sorted({row["family_id"] for row in rows})
    if len(families) != 8:
        raise ValueError(f"expected 8 families; got {len(families)}")

    family_effects: dict[str, dict[str, float]] = {}
    for family in families:
        subset = [row for row in rows if row["family_id"] == family]
        plus = [row for row in subset if row["history_id"] == "H+"]
        minus = [row for row in subset if row["history_id"] == "H-"]
        if not plus or not minus:
            raise ValueError(f"{family}: missing H+ or H-")
        family_effects[family] = {
            "outcome_valence_separation": mean(row["outcome_valence"] for row in plus)
            - mean(row["outcome_valence"] for row in minus)
        }

    plus_all = [row for row in rows if row["history_id"] == "H+"]
    minus_all = [row for row in rows if row["history_id"] == "H-"]
    separation = mean(row["outcome_valence"] for row in plus_all) - mean(
        row["outcome_valence"] for row in minus_all
    )
    directiveness = [float(row["current_response_directiveness"]) for row in rows]
    trait = [float(row["trait_labeling"]) for row in rows]
    correct_families = sum(value["outcome_valence_separation"] > 0 for value in family_effects.values())

    gates = {
        "P1_outcome_separation": {
            "pass": separation >= float(thresholds["min_outcome_valence_separation"]),
            "observed": separation,
            "threshold": float(thresholds["min_outcome_valence_separation"]),
        },
        "P2_no_directiveness": {
            "pass": (
                mean(directiveness) <= float(thresholds["max_mean_current_response_directiveness"])
                and max(directiveness) <= float(thresholds["max_single_current_response_directiveness"])
            ),
            "mean": mean(directiveness),
            "max": max(directiveness),
            "thresholds": {
                "max_mean": float(thresholds["max_mean_current_response_directiveness"]),
                "max_single": float(thresholds["max_single_current_response_directiveness"]),
            },
        },
        "P3_no_trait_labeling": {
            "pass": (
                mean(trait) <= float(thresholds["max_mean_trait_labeling"])
                and max(trait) <= float(thresholds["max_single_trait_labeling"])
            ),
            "mean": mean(trait),
            "max": max(trait),
            "thresholds": {
                "max_mean": float(thresholds["max_mean_trait_labeling"]),
                "max_single": float(thresholds["max_single_trait_labeling"]),
            },
        },
        "P4_family_direction": {
            "pass": correct_families >= int(thresholds["min_families_correct_valence_direction"]),
            "correct_families": correct_families,
            "threshold": int(thresholds["min_families_correct_valence_direction"]),
        },
    }
    return {
        "record_count": len(rows),
        "family_count": len(families),
        "outcome_valence_separation": separation,
        "family_effects": family_effects,
        "gates": gates,
        "all_gates_pass": all(gate["pass"] for gate in gates.values()),
    }


def analyze(config: dict[str, Any]) -> dict[str, Any]:
    manifest = read_jsonl(ROOT / config["pretest_manifest_path"])
    results = [row for row in read_jsonl(ROOT / config["pretest_results_path"]) if row.get("status") == "succeeded"]
    expected = {row["pretest_id"] for row in manifest}
    by_id = {row["pretest_id"]: row for row in results}
    if set(by_id) != expected:
        raise ValueError(f"pretest incomplete: expected={len(expected)} succeeded={len(set(by_id) & expected)}")
    if len(expected) != 16:
        raise ValueError(f"expected 16 pretest records; got {len(expected)}")

    rows = [{**item, **by_id[item["pretest_id"]]["scores"]} for item in manifest]
    thresholds = load_yaml(ROOT / config["thresholds"])["pretest"]
    result = analyze_rows(rows, thresholds)
    return {
        "experiment_id": config["experiment_id"],
        "phase": config["phase"],
        **result,
        "design_hashes": design_hashes(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze PF-EXP-0004 history pretest.")
    parser.add_argument("--config", type=Path, default=ROOT / "experiment.yaml")
    args = parser.parse_args()
    config = load_yaml(args.config.resolve())
    result = analyze(config)
    path = ROOT / config["pretest_analysis_path"]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["all_gates_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
