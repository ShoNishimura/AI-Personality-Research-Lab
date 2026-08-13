from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any

from .common import ROOT, load_yaml, read_jsonl


def _mean(rows: list[dict[str, Any]], key: str) -> float:
    if not rows:
        raise ValueError(f"cannot calculate mean for empty subset: {key}")
    return mean(float(row[key]) for row in rows)


def _condition_flags(condition_id: str) -> tuple[bool, bool]:
    if condition_id not in {"T00", "T01", "T10", "T11"}:
        raise ValueError(f"unexpected condition_id: {condition_id}")
    return condition_id[1] == "1", condition_id[2] == "1"


def analyze(config: dict[str, Any]) -> dict[str, Any]:
    key_rows = read_jsonl(ROOT / config["blind_key_path"])
    eval_rows = [
        row
        for row in read_jsonl(ROOT / config["evaluation_results_path"])
        if row.get("status") == "succeeded"
    ]
    scores = {row["blind_id"]: row["scores"] for row in eval_rows}
    if len(scores) != len(key_rows):
        raise ValueError(f"evaluation incomplete: key={len(key_rows)} succeeded={len(scores)}")

    rows: list[dict[str, Any]] = []
    for key in key_rows:
        if key["blind_id"] not in scores:
            raise ValueError(f"missing evaluation for blind_id={key['blind_id']}")
        score = scores[key["blind_id"]]
        s_high, n_high = _condition_flags(key["condition_id"])
        rows.append(
            {
                **key,
                "s_high": s_high,
                "n_high": n_high,
                "opportunity_salience": score["opportunity_salience"],
                "danger_salience": score["danger_salience"],
                "seeking_activation": score["seeking_activation"],
                "negative_activation": score["negative_activation"],
            }
        )

    if len(rows) != 192:
        raise ValueError(f"expected 192 evaluated records; got {len(rows)}")

    # Temperament replication in relevant stimulus contexts.
    o_high = [row for row in rows if row["opportunity"] == "high"]
    d_high = [row for row in rows if row["danger"] == "high"]
    seeking_main = _mean([r for r in o_high if r["s_high"]], "seeking_activation") - _mean(
        [r for r in o_high if not r["s_high"]], "seeking_activation"
    )
    negative_main = _mean([r for r in d_high if r["n_high"]], "negative_activation") - _mean(
        [r for r in d_high if not r["n_high"]], "negative_activation"
    )

    # Primary target: at N High and Danger High, does raising Opportunity attenuate
    # Danger Salience more when S is High (T11) than when S is Low (T01)?
    families = sorted({row["family_id"] for row in rows})
    family_interactions: dict[str, float] = {}
    family_deltas: dict[str, dict[str, float]] = {}
    for family in families:
        fr = [
            r for r in rows
            if r["family_id"] == family and r["danger"] == "high" and r["n_high"]
        ]
        t01 = [r for r in fr if r["condition_id"] == "T01"]
        t11 = [r for r in fr if r["condition_id"] == "T11"]

        t01_delta = _mean(
            [r for r in t01 if r["opportunity"] == "high"], "danger_salience"
        ) - _mean(
            [r for r in t01 if r["opportunity"] == "low"], "danger_salience"
        )
        t11_delta = _mean(
            [r for r in t11 if r["opportunity"] == "high"], "danger_salience"
        ) - _mean(
            [r for r in t11 if r["opportunity"] == "low"], "danger_salience"
        )
        interaction = t11_delta - t01_delta
        family_deltas[family] = {
            "t01_opportunity_effect_on_danger": t01_delta,
            "t11_opportunity_effect_on_danger": t11_delta,
        }
        family_interactions[family] = interaction

    primary_interaction = mean(family_interactions.values())
    negative_family_count = sum(value < 0 for value in family_interactions.values())

    leave_one_out: dict[str, float] = {}
    for omitted in families:
        remaining = [
            value for family, value in family_interactions.items() if family != omitted
        ]
        leave_one_out[omitted] = mean(remaining)

    # Reciprocal exploratory interaction:
    # at S High and Opportunity High, does raising Danger attenuate Opportunity Salience
    # more when N is High (T11) than when N is Low (T10)?
    reciprocal_family_interactions: dict[str, float] = {}
    for family in families:
        fr = [
            r for r in rows
            if r["family_id"] == family and r["opportunity"] == "high" and r["s_high"]
        ]
        t10 = [r for r in fr if r["condition_id"] == "T10"]
        t11 = [r for r in fr if r["condition_id"] == "T11"]
        t10_delta = _mean(
            [r for r in t10 if r["danger"] == "high"], "opportunity_salience"
        ) - _mean(
            [r for r in t10 if r["danger"] == "low"], "opportunity_salience"
        )
        t11_delta = _mean(
            [r for r in t11 if r["danger"] == "high"], "opportunity_salience"
        ) - _mean(
            [r for r in t11 if r["danger"] == "low"], "opportunity_salience"
        )
        reciprocal_family_interactions[family] = t11_delta - t10_delta

    reciprocal_interaction = mean(reciprocal_family_interactions.values())

    pretest_path = ROOT / config["pretest_analysis_path"]
    if not pretest_path.exists():
        raise FileNotFoundError("pretest analysis missing")
    pretest = json.loads(pretest_path.read_text(encoding="utf-8"))

    thresholds = load_yaml(ROOT / config["thresholds"])["pilot"]
    gates = {
        "G1_pretest": {
            "pass": bool(pretest.get("all_gates_pass", False)),
        },
        "G2_temperament_replication": {
            "pass": (
                seeking_main >= float(thresholds["min_seeking_main_effect"])
                and negative_main >= float(thresholds["min_negative_main_effect"])
            ),
            "seeking_main": seeking_main,
            "negative_main": negative_main,
            "thresholds": {
                "min_seeking_main_effect": float(thresholds["min_seeking_main_effect"]),
                "min_negative_main_effect": float(thresholds["min_negative_main_effect"]),
            },
        },
        "G3_target_interaction": {
            "pass": (
                primary_interaction <= float(thresholds["max_primary_interaction"])
                and negative_family_count >= int(thresholds["min_negative_family_interactions"])
            ),
            "observed": primary_interaction,
            "negative_family_count": negative_family_count,
            "thresholds": {
                "max_primary_interaction": float(thresholds["max_primary_interaction"]),
                "min_negative_family_interactions": int(thresholds["min_negative_family_interactions"]),
            },
        },
        "G4_generalization": {
            "pass": max(leave_one_out.values())
            <= float(thresholds["max_leave_one_family_out_interaction"]),
            "max_leave_one_family_out_interaction": max(leave_one_out.values()),
            "threshold": float(thresholds["max_leave_one_family_out_interaction"]),
        },
    }

    return {
        "experiment_id": config["experiment_id"],
        "phase": config["phase"],
        "record_count": len(rows),
        "family_count": len(families),
        "effects": {
            "seeking_main": seeking_main,
            "negative_main": negative_main,
            "primary_interaction": primary_interaction,
            "reciprocal_interaction_exploratory": reciprocal_interaction,
        },
        "family_deltas": family_deltas,
        "family_interactions": family_interactions,
        "leave_one_family_out": leave_one_out,
        "reciprocal_family_interactions_exploratory": reciprocal_family_interactions,
        "gates": gates,
        "all_gates_pass": all(gate["pass"] for gate in gates.values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze PF-EXP-0002 interaction pilot.")
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
