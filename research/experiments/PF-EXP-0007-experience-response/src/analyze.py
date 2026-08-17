from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any

from .common import ROOT, assert_frozen_design, experience_by_id, load_yaml, read_jsonl


def _latest(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        if row.get("status") == "succeeded" and key in row:
            out[str(row[key])] = row
    return out


def _mean(values: list[float]) -> float:
    if not values:
        raise ValueError("cannot compute mean of empty values")
    return statistics.fmean(values)


def _bigrams(text: str) -> set[str]:
    normalized = "".join(ch for ch in text if not ch.isspace())
    return {normalized[i:i + 2] for i in range(max(0, len(normalized) - 1))}


def _overlap(a: str, b: str) -> float:
    aa, bb = _bigrams(a), _bigrams(b)
    if not aa or not bb:
        return 0.0
    return len(aa & bb) / len(aa | bb)


def _validate_layout(rows: list[dict[str, Any]]) -> None:
    if len(rows) != 48:
        raise RuntimeError(f"expected 48 analyzed rows, got {len(rows)}")

    condition_counts = {
        "E-B": sum(r["exp_id"] == "E-B" for r in rows),
        "E-A": sum(r["exp_id"] == "E-A" for r in rows),
    }
    if condition_counts != {"E-B": 24, "E-A": 24}:
        raise RuntimeError(f"unexpected Experience condition counts: {condition_counts}")

    family_ids = sorted({str(r["family_id"]) for r in rows})
    if len(family_ids) != 8:
        raise RuntimeError(f"expected 8 families, got {len(family_ids)}")

    for family_id in family_ids:
        family = [r for r in rows if str(r["family_id"]) == family_id]
        counts = {
            "E-B": sum(r["exp_id"] == "E-B" for r in family),
            "E-A": sum(r["exp_id"] == "E-A" for r in family),
        }
        if len(family) != 6 or counts != {"E-B": 3, "E-A": 3}:
            raise RuntimeError(f"{family_id}: unexpected cell layout total={len(family)} counts={counts}")


def analyze(config_path: Path) -> dict[str, Any]:
    config = load_yaml(config_path)
    assert_frozen_design(config)
    thresholds = load_yaml(ROOT / config["thresholds"])["pilot"]

    blind_key_rows = read_jsonl(ROOT / config["blind_key_path"])
    if len(blind_key_rows) != 48 or len({str(r["evaluation_id"]) for r in blind_key_rows}) != 48:
        raise RuntimeError("blind key must contain exactly 48 unique evaluation rows")
    blind_key = {str(r["evaluation_id"]): r for r in blind_key_rows}

    eval_success = _latest(read_jsonl(ROOT / config["evaluation_results_path"]), "evaluation_id")
    generation_success = _latest(read_jsonl(ROOT / config["results_path"]), "run_id")

    missing = set(blind_key) - set(eval_success)
    if missing:
        raise RuntimeError(f"blind evaluation incomplete: {len(missing)} missing succeeded rows")

    rows: list[dict[str, Any]] = []
    for evaluation_id, key in blind_key.items():
        run_id = str(key["run_id"])
        if run_id not in generation_success:
            raise RuntimeError(f"generation result missing for run_id={run_id}")
        scores = eval_success[evaluation_id]["scores"]
        parsed = generation_success[run_id]["parsed_output"]
        action = str(parsed["action"])
        exp_id = str(key["exp_id"])
        rows.append({
            **key,
            **scores,
            "action": action,
            "intensity": float(parsed["intensity"]),
            "latency": float(parsed["latency"]),
            "experience_action_lexical_repetition": _overlap(action, experience_by_id(exp_id)["packet"]),
        })

    _validate_layout(rows)

    by_condition = {
        "E-B": [r for r in rows if r["exp_id"] == "E-B"],
        "E-A": [r for r in rows if r["exp_id"] == "E-A"],
    }

    constructive_b = _mean([float(r["constructive_engagement"]) for r in by_condition["E-B"]])
    constructive_a = _mean([float(r["constructive_engagement"]) for r in by_condition["E-A"]])
    protective_b = _mean([float(r["protective_distancing"]) for r in by_condition["E-B"]])
    protective_a = _mean([float(r["protective_distancing"]) for r in by_condition["E-A"]])
    delta_c = constructive_b - constructive_a
    delta_p = protective_a - protective_b

    family_ids = sorted({str(r["family_id"]) for r in rows})
    family_effects: dict[str, dict[str, float | bool]] = {}
    dual_positive_count = 0
    for family_id in family_ids:
        family = [r for r in rows if r["family_id"] == family_id]
        benign = [r for r in family if r["exp_id"] == "E-B"]
        adverse = [r for r in family if r["exp_id"] == "E-A"]
        dc = _mean([float(r["constructive_engagement"]) for r in benign]) - _mean([float(r["constructive_engagement"]) for r in adverse])
        dp = _mean([float(r["protective_distancing"]) for r in adverse]) - _mean([float(r["protective_distancing"]) for r in benign])
        dual = dc > 0 and dp > 0
        dual_positive_count += int(dual)
        family_effects[family_id] = {
            "delta_constructive_engagement": dc,
            "delta_protective_distancing": dp,
            "dual_positive": dual,
        }

    leave_one_family_out: dict[str, dict[str, float]] = {}
    for omitted in family_ids:
        subset = [r for r in rows if r["family_id"] != omitted]
        benign = [r for r in subset if r["exp_id"] == "E-B"]
        adverse = [r for r in subset if r["exp_id"] == "E-A"]
        dc = _mean([float(r["constructive_engagement"]) for r in benign]) - _mean([float(r["constructive_engagement"]) for r in adverse])
        dp = _mean([float(r["protective_distancing"]) for r in adverse]) - _mean([float(r["protective_distancing"]) for r in benign])
        leave_one_family_out[omitted] = {
            "delta_constructive_engagement": dc,
            "delta_protective_distancing": dp,
        }

    validity = [float(r["action_validity_failure"]) for r in rows]
    invention = [float(r["external_fact_invention"]) for r in rows]
    min_loo_c = min(v["delta_constructive_engagement"] for v in leave_one_family_out.values())
    min_loo_p = min(v["delta_protective_distancing"] for v in leave_one_family_out.values())

    gates = {
        "G1_constructive_engagement_effect": delta_c >= float(thresholds["min_constructive_engagement_effect"]),
        "G2_protective_distancing_effect": delta_p >= float(thresholds["min_protective_distancing_effect"]),
        "G3_family_generalization": dual_positive_count >= int(thresholds["min_families_dual_positive_effect"]),
        "G4_leave_one_family_out_robustness": (
            min_loo_c > float(thresholds["min_leave_one_family_out_constructive_effect_exclusive"])
            and min_loo_p > float(thresholds["min_leave_one_family_out_protective_effect_exclusive"])
        ),
        "G5_response_boundary_quality": (
            _mean(validity) <= float(thresholds["max_mean_action_validity_failure"])
            and max(validity) <= float(thresholds["max_single_action_validity_failure"])
            and _mean(invention) <= float(thresholds["max_mean_external_fact_invention"])
            and max(invention) <= float(thresholds["max_single_external_fact_invention"])
        ),
    }

    coactivation = [
        1 for r in rows
        if float(r["constructive_engagement"]) >= 2 and float(r["protective_distancing"]) >= 2
    ]

    return {
        "experiment_id": config["experiment_id"],
        "phase": config["phase"],
        "n_evaluated": len(rows),
        "observed": {
            "constructive_mean_E-B": constructive_b,
            "constructive_mean_E-A": constructive_a,
            "delta_constructive_engagement": delta_c,
            "protective_mean_E-B": protective_b,
            "protective_mean_E-A": protective_a,
            "delta_protective_distancing": delta_p,
            "families_dual_positive_effect": dual_positive_count,
            "min_leave_one_family_out_constructive_effect": min_loo_c,
            "min_leave_one_family_out_protective_effect": min_loo_p,
            "action_validity_failure_mean": _mean(validity),
            "action_validity_failure_max": max(validity),
            "external_fact_invention_mean": _mean(invention),
            "external_fact_invention_max": max(invention),
        },
        "family_effects": family_effects,
        "leave_one_family_out": leave_one_family_out,
        "secondary": {
            "intensity_mean_E-B": _mean([float(r["intensity"]) for r in by_condition["E-B"]]),
            "intensity_mean_E-A": _mean([float(r["intensity"]) for r in by_condition["E-A"]]),
            "latency_mean_E-B": _mean([float(r["latency"]) for r in by_condition["E-B"]]),
            "latency_mean_E-A": _mean([float(r["latency"]) for r in by_condition["E-A"]]),
            "action_axis_coactivation_rate": len(coactivation) / len(rows),
            "experience_action_lexical_repetition_mean": _mean([float(r["experience_action_lexical_repetition"]) for r in rows]),
        },
        "thresholds": thresholds,
        "gates": gates,
        "all_gates_pass": all(gates.values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze PF-EXP-0007 confirmatory gates.")
    parser.add_argument("--config", type=Path, default=ROOT / "experiment.yaml")
    args = parser.parse_args()
    config_path = args.config.resolve()
    result = analyze(config_path)
    config = load_yaml(config_path)
    output_path = ROOT / config["analysis_path"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["all_gates_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
