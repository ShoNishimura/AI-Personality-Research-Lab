from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any

from .common import ROOT, load_yaml, read_jsonl

METRICS = (
    "opportunity_salience",
    "danger_salience",
    "seeking_activation",
    "negative_activation",
)

FLOAT_EPSILON = 1e-12


def _zero_small(value: float) -> float:
    return 0.0 if abs(value) <= FLOAT_EPSILON else value


def _mean(rows: list[dict[str, Any]], key: str) -> float:
    if not rows:
        raise ValueError(f"empty subset for {key}")
    return mean(float(row[key]) for row in rows)


def _cell_summary(rows: list[dict[str, Any]], concurrent_cut: int) -> dict[str, float | int]:
    if not rows:
        raise ValueError("empty cell")
    result: dict[str, float | int] = {"n": len(rows)}
    for metric in METRICS:
        result[metric] = _mean(rows, metric)
    result["joint_salience"] = mean(
        min(float(row["opportunity_salience"]), float(row["danger_salience"])) for row in rows
    )
    result["concurrent_rate"] = mean(
        1.0
        if row["opportunity_salience"] >= concurrent_cut and row["danger_salience"] >= concurrent_cut
        else 0.0
        for row in rows
    )
    return result


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
        rows.append(
            {
                **key,
                **scores[key["blind_id"]],
                "s_high": key["condition_id"] == "T11",
            }
        )
    if len(rows) != 96:
        raise ValueError(f"expected 96 evaluated records; got {len(rows)}")

    families = sorted({row["family_id"] for row in rows})
    if len(families) != 8:
        raise ValueError(f"expected 8 families; got {len(families)}")

    thresholds = load_yaml(ROOT / config["thresholds"])["pilot"]
    concurrent_cut = int(thresholds["concurrent_min_score_each"])

    cells: dict[str, dict[str, float | int]] = {}
    for condition_id in ("T01", "T11"):
        for opportunity in ("low", "high"):
            subset = [
                row
                for row in rows
                if row["condition_id"] == condition_id and row["opportunity"] == opportunity
            ]
            cells[f"{condition_id}_O_{opportunity}"] = _cell_summary(subset, concurrent_cut)

    seeking_main = _mean([row for row in rows if row["s_high"]], "seeking_activation") - _mean(
        [row for row in rows if not row["s_high"]], "seeking_activation"
    )

    t11 = [row for row in rows if row["condition_id"] == "T11"]
    t01 = [row for row in rows if row["condition_id"] == "T01"]

    t11_opp_delta = _mean(
        [row for row in t11 if row["opportunity"] == "high"], "opportunity_salience"
    ) - _mean([row for row in t11 if row["opportunity"] == "low"], "opportunity_salience")
    t01_opp_delta = _mean(
        [row for row in t01 if row["opportunity"] == "high"], "opportunity_salience"
    ) - _mean([row for row in t01 if row["opportunity"] == "low"], "opportunity_salience")
    t11_danger_delta = _mean(
        [row for row in t11 if row["opportunity"] == "high"], "danger_salience"
    ) - _mean([row for row in t11 if row["opportunity"] == "low"], "danger_salience")
    t01_danger_delta = _mean(
        [row for row in t01 if row["opportunity"] == "high"], "danger_salience"
    ) - _mean([row for row in t01 if row["opportunity"] == "low"], "danger_salience")

    primary_interaction = t11_danger_delta - t01_danger_delta
    opportunity_interaction = t11_opp_delta - t01_opp_delta

    family_interactions: dict[str, float] = {}
    family_deltas: dict[str, dict[str, float]] = {}
    for family in families:
        family_rows = [row for row in rows if row["family_id"] == family]
        a = [row for row in family_rows if row["condition_id"] == "T01"]
        b = [row for row in family_rows if row["condition_id"] == "T11"]
        da = _mean([row for row in a if row["opportunity"] == "high"], "danger_salience") - _mean(
            [row for row in a if row["opportunity"] == "low"], "danger_salience"
        )
        db = _mean([row for row in b if row["opportunity"] == "high"], "danger_salience") - _mean(
            [row for row in b if row["opportunity"] == "low"], "danger_salience"
        )
        family_deltas[family] = {
            "t01_danger_delta": da,
            "t11_danger_delta": db,
        }
        family_interactions[family] = _zero_small(db - da)

    positive_count = sum(value > 0 for value in family_interactions.values())
    leave_one_out = {
        omitted: _zero_small(
            mean(value for family, value in family_interactions.items() if family != omitted)
        )
        for omitted in families
    }

    target = cells["T11_O_high"]
    target_opp = float(target["opportunity_salience"])
    target_danger = float(target["danger_salience"])
    concurrent_rate = float(target["concurrent_rate"])

    pretest_path = ROOT / config["pretest_analysis_path"]
    if not pretest_path.exists():
        raise FileNotFoundError("pretest analysis missing")
    pretest = json.loads(pretest_path.read_text(encoding="utf-8"))

    gates = {
        "G1_pretest": {
            "pass": bool(pretest.get("all_gates_pass", False)),
        },
        "G2_seeking_and_opportunity_uptake": {
            "pass": (
                seeking_main >= float(thresholds["min_seeking_main_effect"])
                and t11_opp_delta >= float(thresholds["min_t11_opportunity_uptake"])
            ),
            "seeking_main": seeking_main,
            "t11_opportunity_delta": t11_opp_delta,
            "thresholds": {
                "min_seeking_main_effect": float(thresholds["min_seeking_main_effect"]),
                "min_t11_opportunity_uptake": float(thresholds["min_t11_opportunity_uptake"]),
            },
        },
        "G3_danger_preservation": {
            "pass": (
                t11_danger_delta >= float(thresholds["min_t11_danger_delta"])
                and primary_interaction >= float(thresholds["min_primary_danger_interaction"])
            ),
            "t11_danger_delta": t11_danger_delta,
            "primary_interaction": primary_interaction,
            "thresholds": {
                "min_t11_danger_delta": float(thresholds["min_t11_danger_delta"]),
                "min_primary_danger_interaction": float(thresholds["min_primary_danger_interaction"]),
            },
        },
        "G4_family_generalization": {
            "pass": (
                positive_count >= int(thresholds["min_positive_family_interactions"])
                and min(leave_one_out.values())
                > float(thresholds["min_leave_one_family_out_interaction_exclusive"])
            ),
            "positive_family_count": positive_count,
            "min_leave_one_family_out_interaction": min(leave_one_out.values()),
            "thresholds": {
                "min_positive_family_interactions": int(thresholds["min_positive_family_interactions"]),
                "min_leave_one_family_out_interaction_exclusive": float(
                    thresholds["min_leave_one_family_out_interaction_exclusive"]
                ),
            },
        },
        "G5_concurrent_salience_state": {
            "pass": (
                target_opp >= float(thresholds["min_t11_o_high_opportunity_salience"])
                and target_danger >= float(thresholds["min_t11_o_high_danger_salience"])
                and concurrent_rate >= float(thresholds["min_t11_o_high_concurrent_rate"])
            ),
            "opportunity_salience": target_opp,
            "danger_salience": target_danger,
            "joint_salience": float(target["joint_salience"]),
            "concurrent_rate": concurrent_rate,
            "concurrent_min_score_each": concurrent_cut,
            "thresholds": {
                "min_opportunity_salience": float(thresholds["min_t11_o_high_opportunity_salience"]),
                "min_danger_salience": float(thresholds["min_t11_o_high_danger_salience"]),
                "min_concurrent_rate": float(thresholds["min_t11_o_high_concurrent_rate"]),
            },
        },
    }

    return {
        "experiment_id": config["experiment_id"],
        "phase": config["phase"],
        "record_count": len(rows),
        "family_count": len(families),
        "cell_means": cells,
        "effects": {
            "seeking_main": seeking_main,
            "t01_opportunity_delta": t01_opp_delta,
            "t11_opportunity_delta": t11_opp_delta,
            "opportunity_interaction_exploratory": opportunity_interaction,
            "t01_danger_delta": t01_danger_delta,
            "t11_danger_delta": t11_danger_delta,
            "primary_interaction": primary_interaction,
        },
        "family_deltas": family_deltas,
        "family_interactions": family_interactions,
        "leave_one_family_out": leave_one_out,
        "target_t11_o_high": target,
        "gates": gates,
        "all_gates_pass": all(gate["pass"] for gate in gates.values()),
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
