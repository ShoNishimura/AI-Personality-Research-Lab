from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any

from .common import ROOT, load_yaml, read_jsonl


def analyze(config: dict[str, Any]) -> dict[str, Any]:
    manifest = read_jsonl(ROOT / config["pretest_manifest_path"])
    results = [
        row
        for row in read_jsonl(ROOT / config["pretest_results_path"])
        if row.get("status") == "succeeded"
    ]
    expected = {row["pretest_id"] for row in manifest}
    by_id = {row["pretest_id"]: row for row in results}
    if set(by_id) != expected:
        raise ValueError(
            f"pretest incomplete: expected={len(expected)} succeeded={len(set(by_id) & expected)}"
        )

    rows = []
    for item in manifest:
        score = by_id[item["pretest_id"]]["scores"]
        rows.append(
            {
                **item,
                "opportunity_value": score["opportunity_value"],
                "danger_value": score["danger_value"],
            }
        )

    families = sorted({row["family_id"] for row in rows})
    family_effects: dict[str, dict[str, float]] = {}
    for family in families:
        fr = [row for row in rows if row["family_id"] == family]
        opp_main = mean(r["opportunity_value"] for r in fr if r["opportunity"] == "high") - mean(
            r["opportunity_value"] for r in fr if r["opportunity"] == "low"
        )
        danger_main = mean(r["danger_value"] for r in fr if r["danger"] == "high") - mean(
            r["danger_value"] for r in fr if r["danger"] == "low"
        )
        opp_to_danger = mean(r["danger_value"] for r in fr if r["opportunity"] == "high") - mean(
            r["danger_value"] for r in fr if r["opportunity"] == "low"
        )
        danger_to_opp = mean(r["opportunity_value"] for r in fr if r["danger"] == "high") - mean(
            r["opportunity_value"] for r in fr if r["danger"] == "low"
        )
        family_effects[family] = {
            "opportunity_main": opp_main,
            "danger_main": danger_main,
            "opportunity_to_danger_cross": opp_to_danger,
            "danger_to_opportunity_cross": danger_to_opp,
        }

    opportunity_main = mean(v["opportunity_main"] for v in family_effects.values())
    danger_main = mean(v["danger_main"] for v in family_effects.values())
    opportunity_to_danger_cross_abs = mean(
        abs(v["opportunity_to_danger_cross"]) for v in family_effects.values()
    )
    danger_to_opportunity_cross_abs = mean(
        abs(v["danger_to_opportunity_cross"]) for v in family_effects.values()
    )
    opportunity_correct = sum(v["opportunity_main"] > 0 for v in family_effects.values())
    danger_correct = sum(v["danger_main"] > 0 for v in family_effects.values())

    thresholds = load_yaml(ROOT / config["thresholds"])["pretest"]
    gates = {
        "opportunity_manipulation": {
            "pass": opportunity_main >= float(thresholds["min_opportunity_main_effect"]),
            "observed": opportunity_main,
            "threshold": float(thresholds["min_opportunity_main_effect"]),
        },
        "danger_manipulation": {
            "pass": danger_main >= float(thresholds["min_danger_main_effect"]),
            "observed": danger_main,
            "threshold": float(thresholds["min_danger_main_effect"]),
        },
        "opportunity_cross_contamination": {
            "pass": opportunity_to_danger_cross_abs
            <= float(thresholds["max_opportunity_to_danger_cross_abs"]),
            "observed": opportunity_to_danger_cross_abs,
            "threshold": float(thresholds["max_opportunity_to_danger_cross_abs"]),
        },
        "danger_cross_contamination": {
            "pass": danger_to_opportunity_cross_abs
            <= float(thresholds["max_danger_to_opportunity_cross_abs"]),
            "observed": danger_to_opportunity_cross_abs,
            "threshold": float(thresholds["max_danger_to_opportunity_cross_abs"]),
        },
        "family_direction": {
            "pass": (
                opportunity_correct >= int(thresholds["min_families_correct_direction"])
                and danger_correct >= int(thresholds["min_families_correct_direction"])
            ),
            "opportunity_correct_families": opportunity_correct,
            "danger_correct_families": danger_correct,
            "threshold": int(thresholds["min_families_correct_direction"]),
        },
    }

    return {
        "experiment_id": config["experiment_id"],
        "phase": config["phase"],
        "record_count": len(rows),
        "family_count": len(families),
        "effects": {
            "opportunity_main": opportunity_main,
            "danger_main": danger_main,
            "opportunity_to_danger_cross_abs": opportunity_to_danger_cross_abs,
            "danger_to_opportunity_cross_abs": danger_to_opportunity_cross_abs,
        },
        "family_effects": family_effects,
        "gates": gates,
        "all_gates_pass": all(gate["pass"] for gate in gates.values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze PF-EXP-0002 stimulus pretest.")
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
