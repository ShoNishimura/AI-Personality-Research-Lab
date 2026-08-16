from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any

from .common import ROOT, design_hashes, load_yaml, read_jsonl
from .pretest import BOUNDARY_PRETEST, REL_PRETEST


def _latest(rows: list[dict[str, Any]], id_key: str) -> dict[str, dict[str, Any]]:
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
    successes = _latest(read_jsonl(ROOT / config["pretest_results_path"]), "pretest_id")

    missing = {str(r["pretest_id"]) for r in manifest} - set(successes)
    if missing:
        raise RuntimeError(f"pretest incomplete: {len(missing)} missing succeeded rows")

    rows = [successes[str(r["pretest_id"])] for r in manifest]
    rel_rows = [r for r in rows if r["pretest_kind"] == REL_PRETEST]
    boundary_rows = [r for r in rows if r["pretest_kind"] == BOUNDARY_PRETEST]
    if len(rel_rows) != 16 or len(boundary_rows) != 8:
        raise RuntimeError(f"unexpected split pretest counts: relationship={len(rel_rows)} boundary={len(boundary_rows)}")

    by_condition = {"REL-T": [], "REL-D": []}
    by_family: dict[str, dict[str, dict[str, Any]]] = {}
    for row in rel_rows:
        rel_id = str(row["rel_id"])
        by_condition[rel_id].append(row)
        by_family.setdefault(str(row["family_id"]), {})[rel_id] = row

    trust_t = _mean([float(r["scores"]["trust_orientation"]) for r in by_condition["REL-T"]])
    trust_d = _mean([float(r["scores"]["trust_orientation"]) for r in by_condition["REL-D"]])
    distrust_t = _mean([float(r["scores"]["distrust_orientation"]) for r in by_condition["REL-T"]])
    distrust_d = _mean([float(r["scores"]["distrust_orientation"]) for r in by_condition["REL-D"]])
    trust_sep = trust_t - trust_d
    distrust_sep = distrust_d - distrust_t

    family_effects: dict[str, dict[str, float | bool]] = {}
    correct_families = 0
    for family_id, pair in sorted(by_family.items()):
        if set(pair) != {"REL-T", "REL-D"}:
            raise RuntimeError(f"{family_id}: incomplete Relationship pair")
        dt = float(pair["REL-T"]["scores"]["trust_orientation"]) - float(pair["REL-D"]["scores"]["trust_orientation"])
        dd = float(pair["REL-D"]["scores"]["distrust_orientation"]) - float(pair["REL-T"]["scores"]["distrust_orientation"])
        ok = dt > 0 and dd > 0
        correct_families += int(ok)
        family_effects[family_id] = {
            "delta_trust_orientation": dt,
            "delta_distrust_orientation": dd,
            "dual_positive": ok,
        }

    directiveness = [float(r["scores"]["current_response_directiveness"]) for r in rel_rows]
    situation_leakage = [float(r["scores"]["current_situation_leakage"]) for r in rel_rows]
    generalized_vb = [float(r["scores"]["generalized_vb_leakage"]) for r in rel_rows]
    closeness = [float(r["scores"]["closeness_affection_leakage"]) for r in rel_rows]
    power = [float(r["scores"]["power_dependency_leakage"]) for r in rel_rows]
    preload = [float(r["scores"]["experience_meaning_preload"]) for r in boundary_rows]

    gates = {
        "P1_trust_separation": (
            trust_sep >= float(thresholds["min_trust_orientation_separation"])
            and distrust_sep >= float(thresholds["min_distrust_orientation_separation"])
            and correct_families >= int(thresholds["min_families_correct_relationship_direction"])
        ),
        "P2_no_current_response_directiveness": (
            _mean(directiveness) <= float(thresholds["max_mean_current_response_directiveness"])
            and max(directiveness) <= float(thresholds["max_single_current_response_directiveness"])
        ),
        "P3_no_current_situation_leakage": (
            _mean(situation_leakage) <= float(thresholds["max_mean_current_situation_leakage"])
            and max(situation_leakage) <= float(thresholds["max_single_current_situation_leakage"])
        ),
        "P4_trust_isolation": (
            _mean(generalized_vb) <= float(thresholds["max_mean_generalized_vb_leakage"])
            and max(generalized_vb) <= float(thresholds["max_single_generalized_vb_leakage"])
            and _mean(closeness) <= float(thresholds["max_mean_closeness_affection_leakage"])
            and max(closeness) <= float(thresholds["max_single_closeness_affection_leakage"])
            and _mean(power) <= float(thresholds["max_mean_power_dependency_leakage"])
            and max(power) <= float(thresholds["max_single_power_dependency_leakage"])
        ),
        "P5_perception_boundary": (
            _mean(preload) <= float(thresholds["max_mean_experience_meaning_preload"])
            and max(preload) <= float(thresholds["max_single_experience_meaning_preload"])
        ),
    }

    boundary_scores = {
        str(r["family_id"]): {"experience_meaning_preload": float(r["scores"]["experience_meaning_preload"])}
        for r in sorted(boundary_rows, key=lambda item: str(item["family_id"]))
    }

    return {
        "experiment_id": config["experiment_id"],
        "phase": config["phase"],
        "pretest_rows": len(rows),
        "relationship_quality_rows": len(rel_rows),
        "perception_boundary_rows": len(boundary_rows),
        "observed": {
            "trust_orientation_mean_REL-T": trust_t,
            "trust_orientation_mean_REL-D": trust_d,
            "trust_orientation_separation": trust_sep,
            "distrust_orientation_mean_REL-T": distrust_t,
            "distrust_orientation_mean_REL-D": distrust_d,
            "distrust_orientation_separation": distrust_sep,
            "families_correct_relationship_direction": correct_families,
            "current_response_directiveness_mean": _mean(directiveness),
            "current_response_directiveness_max": max(directiveness),
            "current_situation_leakage_mean": _mean(situation_leakage),
            "current_situation_leakage_max": max(situation_leakage),
            "generalized_vb_leakage_mean": _mean(generalized_vb),
            "generalized_vb_leakage_max": max(generalized_vb),
            "closeness_affection_leakage_mean": _mean(closeness),
            "closeness_affection_leakage_max": max(closeness),
            "power_dependency_leakage_mean": _mean(power),
            "power_dependency_leakage_max": max(power),
            "experience_meaning_preload_mean": _mean(preload),
            "experience_meaning_preload_max": max(preload),
        },
        "family_effects": family_effects,
        "boundary_scores": boundary_scores,
        "thresholds": thresholds,
        "gates": gates,
        "all_gates_pass": all(gates.values()),
        "design_hashes": design_hashes(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze PF-EXP-0006 split pretest gates.")
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
