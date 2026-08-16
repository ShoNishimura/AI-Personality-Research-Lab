from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any

from .common import ROOT, load_yaml, read_jsonl, relationship_by_id


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
    return {normalized[i : i + 2] for i in range(max(0, len(normalized) - 1))}


def _overlap(a: str, b: str) -> float:
    aa, bb = _bigrams(a), _bigrams(b)
    if not aa or not bb:
        return 0.0
    return len(aa & bb) / len(aa | bb)


def analyze(config_path: Path) -> dict[str, Any]:
    config = load_yaml(config_path)
    thresholds = load_yaml(ROOT / config["thresholds"])["pilot"]
    blind_key = {str(r["evaluation_id"]): r for r in read_jsonl(ROOT / config["blind_key_path"])}
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
        experience = str(generation_success[run_id]["parsed_output"]["experience"])
        rel_id = str(key["rel_id"])
        rows.append({
            **key,
            **scores,
            "experience": experience,
            "relationship_lexical_repetition": _overlap(experience, relationship_by_id(rel_id)["packet"]),
        })

    by_condition = {
        "REL-T": [r for r in rows if r["rel_id"] == "REL-T"],
        "REL-D": [r for r in rows if r["rel_id"] == "REL-D"],
    }

    benign_t = _mean([float(r["benign_good_faith_meaning"]) for r in by_condition["REL-T"]])
    benign_d = _mean([float(r["benign_good_faith_meaning"]) for r in by_condition["REL-D"]])
    suspicious_t = _mean([float(r["suspicious_adverse_intent_meaning"]) for r in by_condition["REL-T"]])
    suspicious_d = _mean([float(r["suspicious_adverse_intent_meaning"]) for r in by_condition["REL-D"]])
    delta_b = benign_t - benign_d
    delta_s = suspicious_d - suspicious_t

    family_ids = sorted({str(r["family_id"]) for r in rows})
    family_effects: dict[str, dict[str, float | bool]] = {}
    dual_positive_count = 0
    for family_id in family_ids:
        family = [r for r in rows if r["family_id"] == family_id]
        trust = [r for r in family if r["rel_id"] == "REL-T"]
        distrust = [r for r in family if r["rel_id"] == "REL-D"]
        db = _mean([float(r["benign_good_faith_meaning"]) for r in trust]) - _mean([float(r["benign_good_faith_meaning"]) for r in distrust])
        ds = _mean([float(r["suspicious_adverse_intent_meaning"]) for r in distrust]) - _mean([float(r["suspicious_adverse_intent_meaning"]) for r in trust])
        dual = db > 0 and ds > 0
        dual_positive_count += int(dual)
        family_effects[family_id] = {
            "delta_benign_good_faith": db,
            "delta_suspicious_adverse_intent": ds,
            "dual_positive": dual,
        }

    leave_one_family_out: dict[str, dict[str, float]] = {}
    for omitted in family_ids:
        subset = [r for r in rows if r["family_id"] != omitted]
        trust = [r for r in subset if r["rel_id"] == "REL-T"]
        distrust = [r for r in subset if r["rel_id"] == "REL-D"]
        db = _mean([float(r["benign_good_faith_meaning"]) for r in trust]) - _mean([float(r["benign_good_faith_meaning"]) for r in distrust])
        ds = _mean([float(r["suspicious_adverse_intent_meaning"]) for r in distrust]) - _mean([float(r["suspicious_adverse_intent_meaning"]) for r in trust])
        leave_one_family_out[omitted] = {
            "delta_benign_good_faith": db,
            "delta_suspicious_adverse_intent": ds,
        }

    leakage = [float(r["response_leakage"]) for r in rows]
    min_loo_b = min(v["delta_benign_good_faith"] for v in leave_one_family_out.values())
    min_loo_s = min(v["delta_suspicious_adverse_intent"] for v in leave_one_family_out.values())

    gates = {
        "G1_benign_good_faith_meaning_effect": delta_b >= float(thresholds["min_benign_good_faith_meaning_effect"]),
        "G2_suspicious_adverse_intent_meaning_effect": delta_s >= float(thresholds["min_suspicious_adverse_intent_meaning_effect"]),
        "G3_family_generalization": dual_positive_count >= int(thresholds["min_families_dual_positive_effect"]),
        "G4_leave_one_family_out_robustness": (
            min_loo_b > float(thresholds["min_leave_one_family_out_benign_effect_exclusive"])
            and min_loo_s > float(thresholds["min_leave_one_family_out_suspicious_effect_exclusive"])
        ),
        "G5_experience_boundary_quality": (
            _mean(leakage) <= float(thresholds["max_mean_response_leakage"])
            and max(leakage) <= float(thresholds["max_single_response_leakage"])
        ),
    }

    coactivation = [
        1 for r in rows
        if float(r["benign_good_faith_meaning"]) >= 2 and float(r["suspicious_adverse_intent_meaning"]) >= 2
    ]

    return {
        "experiment_id": config["experiment_id"],
        "phase": config["phase"],
        "n_evaluated": len(rows),
        "observed": {
            "benign_mean_REL-T": benign_t,
            "benign_mean_REL-D": benign_d,
            "delta_benign_good_faith": delta_b,
            "suspicious_mean_REL-T": suspicious_t,
            "suspicious_mean_REL-D": suspicious_d,
            "delta_suspicious_adverse_intent": delta_s,
            "families_dual_positive_effect": dual_positive_count,
            "min_leave_one_family_out_benign_effect": min_loo_b,
            "min_leave_one_family_out_suspicious_effect": min_loo_s,
            "response_leakage_mean": _mean(leakage),
            "response_leakage_max": max(leakage),
        },
        "family_effects": family_effects,
        "leave_one_family_out": leave_one_family_out,
        "secondary": {
            "experience_valence_mean_REL-T": _mean([float(r["experience_valence"]) for r in by_condition["REL-T"]]),
            "experience_valence_mean_REL-D": _mean([float(r["experience_valence"]) for r in by_condition["REL-D"]]),
            "experience_arousal_mean_REL-T": _mean([float(r["experience_arousal"]) for r in by_condition["REL-T"]]),
            "experience_arousal_mean_REL-D": _mean([float(r["experience_arousal"]) for r in by_condition["REL-D"]]),
            "dual_meaning_coactivation_rate": len(coactivation) / len(rows),
            "relationship_lexical_repetition_mean": _mean([float(r["relationship_lexical_repetition"]) for r in rows]),
        },
        "thresholds": thresholds,
        "gates": gates,
        "all_gates_pass": all(gates.values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze PF-EXP-0006 confirmatory gates.")
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
