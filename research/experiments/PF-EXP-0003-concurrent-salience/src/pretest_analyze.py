from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any

from .common import ROOT, load_yaml, read_jsonl


def analyze(config: dict[str, Any]) -> dict[str, Any]:
    manifest = read_jsonl(ROOT / config["pretest_manifest_path"])
    results = [r for r in read_jsonl(ROOT / config["pretest_results_path"]) if r.get("status") == "succeeded"]
    expected = {r["pretest_id"] for r in manifest}
    by_id = {r["pretest_id"]: r for r in results}
    if set(by_id) != expected:
        raise ValueError(f"pretest incomplete: expected={len(expected)} succeeded={len(set(by_id)&expected)}")
    rows = [{**item, **by_id[item["pretest_id"]]["scores"]} for item in manifest]
    families = sorted({r["family_id"] for r in rows})
    effects = {}
    for family in families:
        fr = [r for r in rows if r["family_id"] == family]
        lo = [r for r in fr if r["opportunity"] == "low"]
        hi = [r for r in fr if r["opportunity"] == "high"]
        effects[family] = {
            "opportunity_main": mean(r["opportunity_value"] for r in hi) - mean(r["opportunity_value"] for r in lo),
            "danger_cross": mean(r["danger_value"] for r in hi) - mean(r["danger_value"] for r in lo),
        }
    opportunity_main = mean(v["opportunity_main"] for v in effects.values())
    danger_cross_abs = mean(abs(v["danger_cross"]) for v in effects.values())
    correct = sum(v["opportunity_main"] > 0 for v in effects.values())
    t = load_yaml(ROOT / config["thresholds"])["pretest"]
    gates = {
        "opportunity_manipulation": {
            "pass": opportunity_main >= float(t["min_opportunity_main_effect"]),
            "observed": opportunity_main, "threshold": float(t["min_opportunity_main_effect"]),
        },
        "danger_stability": {
            "pass": danger_cross_abs <= float(t["max_opportunity_to_danger_cross_abs"]),
            "observed": danger_cross_abs, "threshold": float(t["max_opportunity_to_danger_cross_abs"]),
        },
        "family_direction": {
            "pass": correct >= int(t["min_families_opportunity_correct_direction"]),
            "correct_families": correct, "threshold": int(t["min_families_opportunity_correct_direction"]),
        },
    }
    return {
        "experiment_id": config["experiment_id"], "phase": config["phase"], "record_count": len(rows),
        "family_count": len(families), "effects": {
            "opportunity_main": opportunity_main, "opportunity_to_danger_cross_abs": danger_cross_abs,
        }, "family_effects": effects, "gates": gates,
        "all_gates_pass": all(g["pass"] for g in gates.values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze PF-EXP-0003 stimulus pretest.")
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
