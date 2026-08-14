from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any

from .common import ROOT, design_hashes, load_yaml, read_jsonl

SECONDARY_METRICS = (
    "caution_information_seeking",
    "response_intensity",
    "response_latency",
)
FLOAT_EPSILON = 1e-12


def _zero_small(value: float) -> float:
    return 0.0 if abs(value) <= FLOAT_EPSILON else value


def _mean(rows: list[dict[str, Any]], key: str) -> float:
    if not rows:
        raise ValueError(f"empty subset for {key}")
    return mean(float(row[key]) for row in rows)


def analyze_rows(rows: list[dict[str, Any]], thresholds: dict[str, Any]) -> dict[str, Any]:
    if len(rows) != 48:
        raise ValueError(f"expected 48 evaluated records; got {len(rows)}")
    families = sorted({row["family_id"] for row in rows})
    if len(families) != 8:
        raise ValueError(f"expected 8 families; got {len(families)}")

    plus = [row for row in rows if row["history_id"] == "H+"]
    minus = [row for row in rows if row["history_id"] == "H-"]
    if len(plus) != 24 or len(minus) != 24:
        raise ValueError(f"expected 24 H+ and 24 H-; got H+={len(plus)} H-={len(minus)}")

    primary_effect = _zero_small(_mean(plus, "approach_commitment") - _mean(minus, "approach_commitment"))

    family_effects: dict[str, float] = {}
    family_means: dict[str, dict[str, float]] = {}
    for family in families:
        family_rows = [row for row in rows if row["family_id"] == family]
        fp = [row for row in family_rows if row["history_id"] == "H+"]
        fm = [row for row in family_rows if row["history_id"] == "H-"]
        if len(fp) != 3 or len(fm) != 3:
            raise ValueError(f"{family}: expected 3 H+ and 3 H- records")
        plus_mean = _mean(fp, "approach_commitment")
        minus_mean = _mean(fm, "approach_commitment")
        family_means[family] = {"H+": plus_mean, "H-": minus_mean}
        family_effects[family] = _zero_small(plus_mean - minus_mean)

    positive_count = sum(value > 0 for value in family_effects.values())
    leave_one_out: dict[str, float] = {}
    for omitted in families:
        subset = [row for row in rows if row["family_id"] != omitted]
        sp = [row for row in subset if row["history_id"] == "H+"]
        sm = [row for row in subset if row["history_id"] == "H-"]
        leave_one_out[omitted] = _zero_small(_mean(sp, "approach_commitment") - _mean(sm, "approach_commitment"))

    secondary = {
        metric: _zero_small(_mean(plus, metric) - _mean(minus, metric)) for metric in SECONDARY_METRICS
    }
    action_category_counts = {
        "H+": dict(Counter(row["action_category"] for row in plus)),
        "H-": dict(Counter(row["action_category"] for row in minus)),
    }

    gates = {
        "G1_primary_history_effect": {
            "pass": primary_effect >= float(thresholds["min_primary_approach_effect"]),
            "observed": primary_effect,
            "threshold": float(thresholds["min_primary_approach_effect"]),
        },
        "G2_family_generalization": {
            "pass": positive_count >= int(thresholds["min_families_positive_approach_effect"]),
            "positive_family_count": positive_count,
            "threshold": int(thresholds["min_families_positive_approach_effect"]),
        },
        "G3_leave_one_family_out_robustness": {
            "pass": min(leave_one_out.values())
            > float(thresholds["min_leave_one_family_out_approach_effect_exclusive"]),
            "minimum_leave_one_out": min(leave_one_out.values()),
            "exclusive_threshold": float(thresholds["min_leave_one_family_out_approach_effect_exclusive"]),
        },
    }

    return {
        "record_count": len(rows),
        "family_count": len(families),
        "approach_means": {
            "H+": _mean(plus, "approach_commitment"),
            "H-": _mean(minus, "approach_commitment"),
        },
        "primary_approach_effect": primary_effect,
        "family_approach_means": family_means,
        "family_approach_effects": family_effects,
        "positive_family_count": positive_count,
        "leave_one_family_out": leave_one_out,
        "secondary_effects_Hplus_minus_Hminus": secondary,
        "action_category_counts": action_category_counts,
        "gates": gates,
        "all_gates_pass": all(gate["pass"] for gate in gates.values()),
    }


def analyze(config: dict[str, Any]) -> dict[str, Any]:
    key_rows = read_jsonl(ROOT / config["blind_key_path"])
    eval_rows = [
        row for row in read_jsonl(ROOT / config["evaluation_results_path"]) if row.get("status") == "succeeded"
    ]
    scores = {row["blind_id"]: row["scores"] for row in eval_rows}
    if len(key_rows) != 48 or len(scores) != len(key_rows):
        raise ValueError(f"evaluation incomplete: key={len(key_rows)} succeeded={len(scores)}")

    rows: list[dict[str, Any]] = []
    for key in key_rows:
        if key["blind_id"] not in scores:
            raise ValueError(f"missing evaluation for blind_id={key['blind_id']}")
        rows.append({**key, **scores[key["blind_id"]]})

    pretest_path = ROOT / config["pretest_analysis_path"]
    if not pretest_path.exists():
        raise FileNotFoundError("pretest analysis missing")
    pretest = json.loads(pretest_path.read_text(encoding="utf-8"))
    if not pretest.get("all_gates_pass", False):
        raise ValueError("pretest gates are not all PASS")
    if pretest.get("design_hashes") != design_hashes():
        raise ValueError("design files differ from the successful pretest freeze")

    thresholds = load_yaml(ROOT / config["thresholds"])["pilot"]
    result = analyze_rows(rows, thresholds)
    return {
        "experiment_id": config["experiment_id"],
        "phase": config["phase"],
        **result,
        "pretest_all_gates_pass": True,
        "design_hashes": design_hashes(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze PF-EXP-0004 History-conditioned Response pilot.")
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
