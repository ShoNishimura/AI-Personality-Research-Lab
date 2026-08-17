from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any

from .common import ROOT, design_hashes, load_yaml, read_jsonl
from .pretest import EXPERIENCE_PRETEST, SITUATION_PRETEST


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
    exp_rows = [r for r in rows if r["pretest_kind"] == EXPERIENCE_PRETEST]
    situation_rows = [r for r in rows if r["pretest_kind"] == SITUATION_PRETEST]
    if len(exp_rows) != 16 or len(situation_rows) != 8:
        raise RuntimeError(f"unexpected split pretest counts: experience={len(exp_rows)} situation={len(situation_rows)}")

    by_condition = {"E-B": [], "E-A": []}
    by_family: dict[str, dict[str, dict[str, Any]]] = {}
    for row in exp_rows:
        exp_id = str(row["exp_id"])
        by_condition[exp_id].append(row)
        by_family.setdefault(str(row["family_id"]), {})[exp_id] = row

    benign_b = _mean([float(r["scores"]["benign_meaning"]) for r in by_condition["E-B"]])
    benign_a = _mean([float(r["scores"]["benign_meaning"]) for r in by_condition["E-A"]])
    adverse_b = _mean([float(r["scores"]["adverse_meaning"]) for r in by_condition["E-B"]])
    adverse_a = _mean([float(r["scores"]["adverse_meaning"]) for r in by_condition["E-A"]])
    benign_sep = benign_b - benign_a
    adverse_sep = adverse_a - adverse_b

    family_effects: dict[str, dict[str, float | bool]] = {}
    correct_families = 0
    for family_id, pair in sorted(by_family.items()):
        if set(pair) != {"E-B", "E-A"}:
            raise RuntimeError(f"{family_id}: incomplete Experience pair")
        db = float(pair["E-B"]["scores"]["benign_meaning"]) - float(pair["E-A"]["scores"]["benign_meaning"])
        da = float(pair["E-A"]["scores"]["adverse_meaning"]) - float(pair["E-B"]["scores"]["adverse_meaning"])
        ok = db > 0 and da > 0
        correct_families += int(ok)
        family_effects[family_id] = {
            "delta_benign_meaning": db,
            "delta_adverse_meaning": da,
            "dual_positive": ok,
        }

    tendency = [float(r["scores"]["response_tendency_preload"]) for r in exp_rows]
    external = [float(r["scores"]["external_fact_leakage"]) for r in exp_rows]
    vb = [float(r["scores"]["values_beliefs_preload"]) for r in exp_rows]
    rel = [float(r["scores"]["relationship_preload"]) for r in exp_rows]
    temperament = [float(r["scores"]["temperament_preload"]) for r in exp_rows]
    constraint = [float(r["scores"]["response_direction_constraint"]) for r in situation_rows]

    gates = {
        "P1_experience_separation": (
            benign_sep >= float(thresholds["min_benign_meaning_separation"])
            and adverse_sep >= float(thresholds["min_adverse_meaning_separation"])
            and correct_families >= int(thresholds["min_families_correct_experience_direction"])
        ),
        "P2_no_response_tendency_preload": (
            _mean(tendency) <= float(thresholds["max_mean_response_tendency_preload"])
            and max(tendency) <= float(thresholds["max_single_response_tendency_preload"])
        ),
        "P3_no_external_fact_leakage": (
            _mean(external) <= float(thresholds["max_mean_external_fact_leakage"])
            and max(external) <= float(thresholds["max_single_external_fact_leakage"])
        ),
        "P4_upstream_state_isolation": (
            _mean(vb) <= float(thresholds["max_mean_values_beliefs_preload"])
            and max(vb) <= float(thresholds["max_single_values_beliefs_preload"])
            and _mean(rel) <= float(thresholds["max_mean_relationship_preload"])
            and max(rel) <= float(thresholds["max_single_relationship_preload"])
            and _mean(temperament) <= float(thresholds["max_mean_temperament_preload"])
            and max(temperament) <= float(thresholds["max_single_temperament_preload"])
        ),
        "P5_situation_affordance_boundary": (
            _mean(constraint) <= float(thresholds["max_mean_response_direction_constraint"])
            and max(constraint) <= float(thresholds["max_single_response_direction_constraint"])
        ),
    }

    boundary_scores = {
        str(r["family_id"]): {"response_direction_constraint": float(r["scores"]["response_direction_constraint"])}
        for r in sorted(situation_rows, key=lambda item: str(item["family_id"]))
    }

    return {
        "experiment_id": config["experiment_id"],
        "phase": config["phase"],
        "pretest_rows": len(rows),
        "experience_quality_rows": len(exp_rows),
        "situation_affordance_rows": len(situation_rows),
        "observed": {
            "benign_meaning_mean_E-B": benign_b,
            "benign_meaning_mean_E-A": benign_a,
            "benign_meaning_separation": benign_sep,
            "adverse_meaning_mean_E-B": adverse_b,
            "adverse_meaning_mean_E-A": adverse_a,
            "adverse_meaning_separation": adverse_sep,
            "families_correct_experience_direction": correct_families,
            "response_tendency_preload_mean": _mean(tendency),
            "response_tendency_preload_max": max(tendency),
            "external_fact_leakage_mean": _mean(external),
            "external_fact_leakage_max": max(external),
            "values_beliefs_preload_mean": _mean(vb),
            "values_beliefs_preload_max": max(vb),
            "relationship_preload_mean": _mean(rel),
            "relationship_preload_max": max(rel),
            "temperament_preload_mean": _mean(temperament),
            "temperament_preload_max": max(temperament),
            "response_direction_constraint_mean": _mean(constraint),
            "response_direction_constraint_max": max(constraint),
        },
        "family_effects": family_effects,
        "boundary_scores": boundary_scores,
        "thresholds": thresholds,
        "gates": gates,
        "all_gates_pass": all(gates.values()),
        "design_hashes": design_hashes(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze PF-EXP-0007 split pretest gates.")
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
