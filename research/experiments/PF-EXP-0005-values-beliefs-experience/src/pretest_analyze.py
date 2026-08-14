from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any

from .common import ROOT, design_hashes, load_yaml, read_jsonl


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


def analyze(config_path: Path) -> dict[str, Any]:
    config = load_yaml(config_path)
    thresholds = load_yaml(ROOT / config["thresholds"])["pretest"]
    manifest = read_jsonl(ROOT / config["pretest_manifest_path"])
    successes = _latest_success(read_jsonl(ROOT / config["pretest_results_path"]), "pretest_id")

    expected_ids = {str(row["pretest_id"]) for row in manifest}
    missing = sorted(expected_ids - set(successes))
    if missing:
        raise RuntimeError(f"pretest incomplete: {len(missing)} missing succeeded rows")

    rows = [successes[str(row["pretest_id"])] for row in manifest]
    by_condition: dict[str, list[dict[str, Any]]] = {"VB-L": [], "VB-E": []}
    by_family: dict[str, dict[str, dict[str, Any]]] = {}
    for row in rows:
        vb_id = str(row["vb_id"])
        by_condition[vb_id].append(row)
        by_family.setdefault(str(row["family_id"]), {})[vb_id] = row

    learning_l = _mean([float(r["scores"]["learning_orientation"]) for r in by_condition["VB-L"]])
    learning_e = _mean([float(r["scores"]["learning_orientation"]) for r in by_condition["VB-E"]])
    eval_l = _mean([float(r["scores"]["evaluation_protection_orientation"]) for r in by_condition["VB-L"]])
    eval_e = _mean([float(r["scores"]["evaluation_protection_orientation"]) for r in by_condition["VB-E"]])
    learning_sep = learning_l - learning_e
    evaluation_sep = eval_e - eval_l

    family_effects: dict[str, dict[str, float | bool]] = {}
    correct_families = 0
    for family_id, pair in sorted(by_family.items()):
        if set(pair) != {"VB-L", "VB-E"}:
            raise RuntimeError(f"{family_id}: incomplete VB pair")
        dl = float(pair["VB-L"]["scores"]["learning_orientation"]) - float(pair["VB-E"]["scores"]["learning_orientation"])
        de = float(pair["VB-E"]["scores"]["evaluation_protection_orientation"]) - float(pair["VB-L"]["scores"]["evaluation_protection_orientation"])
        ok = dl > 0 and de > 0
        correct_families += int(ok)
        family_effects[family_id] = {"delta_learning_orientation": dl, "delta_evaluation_protection": de, "dual_positive": ok}

    def score_values(name: str) -> list[float]:
        return [float(r["scores"][name]) for r in rows]

    directiveness = score_values("current_response_directiveness")
    situation_leakage = score_values("current_situation_leakage")
    meaning_preload = score_values("experience_meaning_preload")
    relationship = score_values("relationship_salience")

    gates = {
        "P1_vb_separation": (
            learning_sep >= float(thresholds["min_learning_orientation_separation"])
            and evaluation_sep >= float(thresholds["min_evaluation_protection_orientation_separation"])
            and correct_families >= int(thresholds["min_families_correct_vb_direction"])
        ),
        "P2_no_current_response_directiveness": (
            _mean(directiveness) <= float(thresholds["max_mean_current_response_directiveness"])
            and max(directiveness) <= float(thresholds["max_single_current_response_directiveness"])
        ),
        "P3_no_current_situation_leakage": (
            _mean(situation_leakage) <= float(thresholds["max_mean_current_situation_leakage"])
            and max(situation_leakage) <= float(thresholds["max_single_current_situation_leakage"])
        ),
        "P4_perception_boundary": (
            _mean(meaning_preload) <= float(thresholds["max_mean_experience_meaning_preload"])
            and max(meaning_preload) <= float(thresholds["max_single_experience_meaning_preload"])
        ),
        "P5_relationship_neutrality": (
            _mean(relationship) <= float(thresholds["max_mean_relationship_salience"])
            and max(relationship) <= float(thresholds["max_single_relationship_salience"])
        ),
    }

    return {
        "experiment_id": config["experiment_id"],
        "phase": config["phase"],
        "pretest_rows": len(rows),
        "observed": {
            "learning_orientation_mean_VB-L": learning_l,
            "learning_orientation_mean_VB-E": learning_e,
            "learning_orientation_separation": learning_sep,
            "evaluation_protection_mean_VB-L": eval_l,
            "evaluation_protection_mean_VB-E": eval_e,
            "evaluation_protection_orientation_separation": evaluation_sep,
            "families_correct_vb_direction": correct_families,
            "current_response_directiveness_mean": _mean(directiveness),
            "current_response_directiveness_max": max(directiveness),
            "current_situation_leakage_mean": _mean(situation_leakage),
            "current_situation_leakage_max": max(situation_leakage),
            "experience_meaning_preload_mean": _mean(meaning_preload),
            "experience_meaning_preload_max": max(meaning_preload),
            "relationship_salience_mean": _mean(relationship),
            "relationship_salience_max": max(relationship),
        },
        "family_effects": family_effects,
        "thresholds": thresholds,
        "gates": gates,
        "all_gates_pass": all(gates.values()),
        "design_hashes": design_hashes(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze PF-EXP-0005 pretest gates.")
    parser.add_argument("--config", type=Path, default=ROOT / "experiment.yaml")
    args = parser.parse_args()
    config_path = args.config.resolve()
    result = analyze(config_path)
    config = load_yaml(config_path)
    output_path = ROOT / config["pretest_analysis_path"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["all_gates_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
