from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any

from .common import ROOT, load_yaml, read_jsonl, values_beliefs_by_id


def _latest_success(rows: list[dict[str, Any]], id_key: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        if row.get("status") == "succeeded" and id_key in row:
            out[str(row[id_key])] = row
    return out


def _mean(values: list[float]) -> float:
    if not values:
        raise ValueError("cannot compute mean of empty values")
    return statistics.fmean(values)


def _bigrams(text: str) -> set[str]:
    normalized = "".join(ch for ch in text if not ch.isspace())
    return {normalized[i : i + 2] for i in range(max(0, len(normalized) - 1))}


def _lexical_overlap(a: str, b: str) -> float:
    aa, bb = _bigrams(a), _bigrams(b)
    if not aa or not bb:
        return 0.0
    return len(aa & bb) / len(aa | bb)


def analyze(config_path: Path) -> dict[str, Any]:
    config = load_yaml(config_path)
    thresholds = load_yaml(ROOT / config["thresholds"])["pilot"]

    blind_key = {str(r["evaluation_id"]): r for r in read_jsonl(ROOT / config["blind_key_path"])}
    eval_success = _latest_success(read_jsonl(ROOT / config["evaluation_results_path"]), "evaluation_id")
    generation_success = _latest_success(read_jsonl(ROOT / config["results_path"]), "run_id")

    expected_eval_ids = set(blind_key)
    missing_eval = expected_eval_ids - set(eval_success)
    if missing_eval:
        raise RuntimeError(f"blind evaluation incomplete: {len(missing_eval)} missing succeeded rows")

    rows: list[dict[str, Any]] = []
    for evaluation_id, key in blind_key.items():
        run_id = str(key["run_id"])
        if run_id not in generation_success:
            raise RuntimeError(f"generation result missing for run_id={run_id}")
        generation = generation_success[run_id]
        scores = eval_success[evaluation_id]["scores"]
        vb_id = str(key["vb_id"])
        experience = str(generation["parsed_output"]["experience"])
        rows.append(
            {
                **key,
                **scores,
                "experience": experience,
                "vb_lexical_repetition": _lexical_overlap(experience, values_beliefs_by_id(vb_id)["packet"]),
            }
        )

    by_condition = {
        "VB-L": [r for r in rows if r["vb_id"] == "VB-L"],
        "VB-E": [r for r in rows if r["vb_id"] == "VB-E"],
    }

    learning_l = _mean([float(r["learning_improvement_meaning"]) for r in by_condition["VB-L"]])
    learning_e = _mean([float(r["learning_improvement_meaning"]) for r in by_condition["VB-E"]])
    eval_l = _mean([float(r["evaluation_threat_meaning"]) for r in by_condition["VB-L"]])
    eval_e = _mean([float(r["evaluation_threat_meaning"]) for r in by_condition["VB-E"]])
    delta_l = learning_l - learning_e
    delta_e = eval_e - eval_l

    family_ids = sorted({str(r["family_id"]) for r in rows})
    family_effects: dict[str, dict[str, float | bool]] = {}
    dual_positive_count = 0
    for family_id in family_ids:
        family = [r for r in rows if r["family_id"] == family_id]
        l_rows = [r for r in family if r["vb_id"] == "VB-L"]
        e_rows = [r for r in family if r["vb_id"] == "VB-E"]
        dl = _mean([float(r["learning_improvement_meaning"]) for r in l_rows]) - _mean(
            [float(r["learning_improvement_meaning"]) for r in e_rows]
        )
        de = _mean([float(r["evaluation_threat_meaning"]) for r in e_rows]) - _mean(
            [float(r["evaluation_threat_meaning"]) for r in l_rows]
        )
        dual = dl > 0 and de > 0
        dual_positive_count += int(dual)
        family_effects[family_id] = {
            "delta_learning_meaning": dl,
            "delta_evaluation_threat": de,
            "dual_positive": dual,
        }

    loo: dict[str, dict[str, float]] = {}
    for omitted in family_ids:
        subset = [r for r in rows if r["family_id"] != omitted]
        l_rows = [r for r in subset if r["vb_id"] == "VB-L"]
        e_rows = [r for r in subset if r["vb_id"] == "VB-E"]
        loo_dl = _mean([float(r["learning_improvement_meaning"]) for r in l_rows]) - _mean(
            [float(r["learning_improvement_meaning"]) for r in e_rows]
        )
        loo_de = _mean([float(r["evaluation_threat_meaning"]) for r in e_rows]) - _mean(
            [float(r["evaluation_threat_meaning"]) for r in l_rows]
        )
        loo[omitted] = {"delta_learning_meaning": loo_dl, "delta_evaluation_threat": loo_de}

    leakage = [float(r["response_leakage"]) for r in rows]
    min_loo_l = min(v["delta_learning_meaning"] for v in loo.values())
    min_loo_e = min(v["delta_evaluation_threat"] for v in loo.values())

    gates = {
        "G1_learning_meaning_effect": delta_l >= float(thresholds["min_learning_meaning_effect"]),
        "G2_evaluation_threat_meaning_effect": delta_e >= float(thresholds["min_evaluation_threat_meaning_effect"]),
        "G3_family_generalization": dual_positive_count >= int(thresholds["min_families_dual_positive_effect"]),
        "G4_leave_one_family_out_robustness": (
            min_loo_l > float(thresholds["min_leave_one_family_out_learning_effect_exclusive"])
            and min_loo_e > float(thresholds["min_leave_one_family_out_evaluation_effect_exclusive"])
        ),
        "G5_experience_boundary_quality": (
            _mean(leakage) <= float(thresholds["max_mean_response_leakage"])
            and max(leakage) <= float(thresholds["max_single_response_leakage"])
        ),
    }

    coactivation = [
        1
        for r in rows
        if float(r["learning_improvement_meaning"]) >= 2 and float(r["evaluation_threat_meaning"]) >= 2
    ]
    result = {
        "experiment_id": config["experiment_id"],
        "phase": config["phase"],
        "n_evaluated": len(rows),
        "observed": {
            "learning_mean_VB-L": learning_l,
            "learning_mean_VB-E": learning_e,
            "delta_learning_meaning": delta_l,
            "evaluation_threat_mean_VB-L": eval_l,
            "evaluation_threat_mean_VB-E": eval_e,
            "delta_evaluation_threat": delta_e,
            "families_dual_positive_effect": dual_positive_count,
            "min_leave_one_family_out_learning_effect": min_loo_l,
            "min_leave_one_family_out_evaluation_effect": min_loo_e,
            "response_leakage_mean": _mean(leakage),
            "response_leakage_max": max(leakage),
        },
        "family_effects": family_effects,
        "leave_one_family_out": loo,
        "secondary": {
            "experience_valence_mean_VB-L": _mean([float(r["experience_valence"]) for r in by_condition["VB-L"]]),
            "experience_valence_mean_VB-E": _mean([float(r["experience_valence"]) for r in by_condition["VB-E"]]),
            "experience_arousal_mean_VB-L": _mean([float(r["experience_arousal"]) for r in by_condition["VB-L"]]),
            "experience_arousal_mean_VB-E": _mean([float(r["experience_arousal"]) for r in by_condition["VB-E"]]),
            "dual_meaning_coactivation_rate": len(coactivation) / len(rows),
            "vb_lexical_repetition_mean": _mean([float(r["vb_lexical_repetition"]) for r in rows]),
        },
        "thresholds": thresholds,
        "gates": gates,
        "all_gates_pass": all(gates.values()),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze PF-EXP-0005 confirmatory gates.")
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
