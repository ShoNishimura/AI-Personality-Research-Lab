from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from .common import ROOT, load_yaml, read_jsonl


def _mean(rows: list[dict[str, Any]], field: str) -> float:
    return mean(float(row[field]) for row in rows)


def _condition_has(condition_id: str, axis: str, level: str) -> bool:
    index = 1 if axis == "seeking" else 2
    expected = "1" if level == "high" else "0"
    return condition_id[index] == expected


def _difference(rows: list[dict[str, Any]], outcome: str, axis: str) -> float:
    high = [r for r in rows if _condition_has(r["condition_id"], axis, "high")]
    low = [r for r in rows if _condition_has(r["condition_id"], axis, "low")]
    return _mean(high, outcome) - _mean(low, outcome)


def join_scores(config: dict[str, Any]) -> list[dict[str, Any]]:
    key = {row["blind_id"]: row for row in read_jsonl(ROOT / config["blind_key_path"])}
    evaluations = [
        row
        for row in read_jsonl(ROOT / config["evaluation_results_path"])
        if row.get("status") == "succeeded"
    ]
    if len(evaluations) != len(key) or not key:
        raise ValueError(f"evaluation incomplete: key={len(key)} succeeded={len(evaluations)}")
    joined: list[dict[str, Any]] = []
    for row in evaluations:
        meta = key[row["blind_id"]]
        joined.append({**meta, **row["scores"]})
    return joined


def analyze(config: dict[str, Any]) -> dict[str, Any]:
    thresholds = load_yaml(ROOT / config["thresholds"])["gates"]
    rows = join_scores(config)
    by_class: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_class[row["stimulus_class"]].append(row)

    seeking_target = by_class["seeking-target"]
    negative_target = by_class["negative-target"]
    conflict = by_class["conflict"]
    neutral = by_class["neutral"]

    seeking_main = _difference(seeking_target, "seeking_activation", "seeking")
    negative_main = _difference(negative_target, "negative_activation", "negative")
    seeking_cross = _difference(seeking_target, "negative_activation", "seeking")
    negative_cross = _difference(negative_target, "seeking_activation", "negative")

    def ratio(cross: float, main: float) -> float:
        return abs(cross) / abs(main) if main != 0 else float("inf")

    g1_threshold = float(thresholds["G1_seeking_main_effect"]["min_mean_difference"])
    g2_threshold = float(thresholds["G2_negative_main_effect"]["min_mean_difference"])
    g3_threshold = float(thresholds["G3_discriminant_validity"]["max_cross_to_main_ratio"])

    t11_conflict = [r for r in conflict if r["condition_id"] == "T11"]
    g4 = thresholds["G4_conflict_coactivation"]
    joint_min = int(g4["joint_activation_min_score_each"])
    joint_rate = mean(
        1.0
        if r["seeking_activation"] >= joint_min and r["negative_activation"] >= joint_min
        else 0.0
        for r in t11_conflict
    )
    t11_seek_mean = _mean(t11_conflict, "seeking_activation")
    t11_neg_mean = _mean(t11_conflict, "negative_activation")

    condition_axis_means: dict[str, dict[str, float]] = {}
    for condition_id in sorted({r["condition_id"] for r in neutral}):
        subset = [r for r in neutral if r["condition_id"] == condition_id]
        condition_axis_means[condition_id] = {
            "seeking_activation": _mean(subset, "seeking_activation"),
            "negative_activation": _mean(subset, "negative_activation"),
        }
    seeking_range = max(v["seeking_activation"] for v in condition_axis_means.values()) - min(
        v["seeking_activation"] for v in condition_axis_means.values()
    )
    negative_range = max(v["negative_activation"] for v in condition_axis_means.values()) - min(
        v["negative_activation"] for v in condition_axis_means.values()
    )
    g5_threshold = float(thresholds["G5_neutrality"]["max_condition_mean_range_each_axis"])

    gates = {
        "G1": {"pass": seeking_main >= g1_threshold, "observed": seeking_main, "threshold": g1_threshold},
        "G2": {"pass": negative_main >= g2_threshold, "observed": negative_main, "threshold": g2_threshold},
        "G3": {
            "pass": ratio(seeking_cross, seeking_main) <= g3_threshold
            and ratio(negative_cross, negative_main) <= g3_threshold,
            "seeking_cross_to_main_ratio": ratio(seeking_cross, seeking_main),
            "negative_cross_to_main_ratio": ratio(negative_cross, negative_main),
            "threshold": g3_threshold,
        },
        "G4": {
            "pass": t11_seek_mean >= float(g4["min_t11_mean_seeking"])
            and t11_neg_mean >= float(g4["min_t11_mean_negative"])
            and joint_rate >= float(g4["min_joint_activation_rate"]),
            "t11_mean_seeking": t11_seek_mean,
            "t11_mean_negative": t11_neg_mean,
            "joint_activation_rate": joint_rate,
            "thresholds": g4,
        },
        "G5": {
            "pass": seeking_range <= g5_threshold and negative_range <= g5_threshold,
            "seeking_condition_mean_range": seeking_range,
            "negative_condition_mean_range": negative_range,
            "threshold": g5_threshold,
            "condition_means": condition_axis_means,
        },
    }
    return {
        "experiment_id": config["experiment_id"],
        "phase": config["phase"],
        "record_count": len(rows),
        "effects": {
            "seeking_main": seeking_main,
            "negative_main": negative_main,
            "seeking_cross_on_negative": seeking_cross,
            "negative_cross_on_seeking": negative_cross,
        },
        "gates": gates,
        "all_gates_pass": all(item["pass"] for item in gates.values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze PF-EXP-0001 pilot gates.")
    parser.add_argument("--config", type=Path, default=ROOT / "experiment.yaml")
    args = parser.parse_args()
    config = load_yaml(args.config.resolve())
    result = analyze(config)
    output_path = ROOT / config["analysis_path"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["all_gates_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
