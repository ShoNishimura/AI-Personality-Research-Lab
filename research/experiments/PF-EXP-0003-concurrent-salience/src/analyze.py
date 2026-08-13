from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any

from .common import ROOT, load_yaml, read_jsonl


def _mean(rows: list[dict[str, Any]], key: str) -> float:
    if not rows:
        raise ValueError(f"empty subset for {key}")
    return mean(float(r[key]) for r in rows)


def analyze(config: dict[str, Any]) -> dict[str, Any]:
    key_rows = read_jsonl(ROOT / config["blind_key_path"])
    eval_rows = [r for r in read_jsonl(ROOT / config["evaluation_results_path"]) if r.get("status") == "succeeded"]
    scores = {r["blind_id"]: r["scores"] for r in eval_rows}
    if len(scores) != len(key_rows):
        raise ValueError(f"evaluation incomplete: key={len(key_rows)} succeeded={len(scores)}")
    rows = []
    for key in key_rows:
        score = scores[key["blind_id"]]
        rows.append({**key, **score, "s_high": key["condition_id"] == "T11"})
    if len(rows) != 96:
        raise ValueError(f"expected 96 evaluated records; got {len(rows)}")
    families = sorted({r["family_id"] for r in rows})
    seeking_main = _mean([r for r in rows if r["s_high"]], "seeking_activation") - _mean(
        [r for r in rows if not r["s_high"]], "seeking_activation"
    )
    t11 = [r for r in rows if r["condition_id"] == "T11"]
    t01 = [r for r in rows if r["condition_id"] == "T01"]
    t11_opp_delta = _mean([r for r in t11 if r["opportunity"] == "high"], "opportunity_salience") - _mean(
        [r for r in t11 if r["opportunity"] == "low"], "opportunity_salience"
    )
    t11_danger_delta = _mean([r for r in t11 if r["opportunity"] == "high"], "danger_salience") - _mean(
        [r for r in t11 if r["opportunity"] == "low"], "danger_salience"
    )
    t01_danger_delta = _mean([r for r in t01 if r["opportunity"] == "high"], "danger_salience") - _mean(
        [r for r in t01 if r["opportunity"] == "low"], "danger_salience"
    )
    primary = t11_danger_delta - t01_danger_delta
    family_interactions = {}
    family_deltas = {}
    for family in families:
        fr = [r for r in rows if r["family_id"] == family]
        a = [r for r in fr if r["condition_id"] == "T01"]
        b = [r for r in fr if r["condition_id"] == "T11"]
        da = _mean([r for r in a if r["opportunity"] == "high"], "danger_salience") - _mean(
            [r for r in a if r["opportunity"] == "low"], "danger_salience"
        )
        db = _mean([r for r in b if r["opportunity"] == "high"], "danger_salience") - _mean(
            [r for r in b if r["opportunity"] == "low"], "danger_salience"
        )
        family_deltas[family] = {"t01_danger_delta": da, "t11_danger_delta": db}
        family_interactions[family] = db - da
    positive_count = sum(v > 0 for v in family_interactions.values())
    leave_one_out = {
        omitted: mean(v for f, v in family_interactions.items() if f != omitted) for omitted in families
    }
    target = [r for r in t11 if r["opportunity"] == "high"]
    target_opp = _mean(target, "opportunity_salience")
    target_danger = _mean(target, "danger_salience")
    joint_salience = _mean(
        [{"joint": min(r["opportunity_salience"], r["danger_salience"])} for r in target], "joint"
    )
    concurrent_rate = mean(
        1.0 if r["opportunity_salience"] >= 2 and r["danger_salience"] >= 2 else 0.0 for r in target
    )
    pretest = json.loads((ROOT / config["pretest_analysis_path"]).read_text(encoding="utf-8"))
    t = load_yaml(ROOT / config["thresholds"])["pilot"]
    gates = {
        "G1_pretest": {"pass": bool(pretest.get("all_gates_pass", False))},
        "G2_seeking_and_opportunity_uptake": {
            "pass": seeking_main >= float(t["min_seeking_main_effect"])
            and t11_opp_delta >= float(t["min_t11_opportunity_uptake"]),
            "seeking_main": seeking_main, "t11_opportunity_delta": t11_opp_delta,
        },
        "G3_danger_preservation": {
            "pass": t11_danger_delta >= float(t["min_t11_danger_delta"])
            and primary >= float(t["min_primary_danger_interaction"]),
            "t11_danger_delta": t11_danger_delta, "primary_interaction": primary,
        },
        "G4_family_generalization": {
            "pass": positive_count >= int(t["min_positive_family_interactions"])
            and min(leave_one_out.values()) > float(t["min_leave_one_family_out_interaction_exclusive"]),
            "positive_family_count": positive_count,
            "min_leave_one_family_out_interaction": min(leave_one_out.values()),
        },
        "G5_concurrent_salience_state": {
            "pass": target_opp >= float(t["min_t11_o_high_opportunity_salience"])
            and target_danger >= float(t["min_t11_o_high_danger_salience"])
            and concurrent_rate >= float(t["min_t11_o_high_concurrent_rate"]),
            "opportunity_salience": target_opp, "danger_salience": target_danger,
            "joint_salience": joint_salience, "concurrent_rate": concurrent_rate,
        },
    }
    return {
        "experiment_id": config["experiment_id"], "phase": config["phase"], "record_count": len(rows),
        "family_count": len(families), "effects": {
            "seeking_main": seeking_main, "t11_opportunity_delta": t11_opp_delta,
            "t01_danger_delta": t01_danger_delta, "t11_danger_delta": t11_danger_delta,
            "primary_interaction": primary,
        },
        "family_deltas": family_deltas, "family_interactions": family_interactions,
        "leave_one_family_out": leave_one_out,
        "target_t11_o_high": {
            "opportunity_salience": target_opp, "danger_salience": target_danger,
            "joint_salience": joint_salience, "concurrent_rate": concurrent_rate,
        },
        "gates": gates, "all_gates_pass": all(g["pass"] for g in gates.values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze PF-EXP-0003 concurrent-salience pilot.")
    parser.add_argument("--config", type=Path, default=ROOT / "experiment.yaml")
    args = parser.parse_args()
    config = load_yaml(args.config.resolve())
    result = analyze(config)
    path = ROOT / config["analysis_path"]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["all_gates_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
