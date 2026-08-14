from __future__ import annotations

import argparse
import json
from pathlib import Path

import jsonschema

from .common import ROOT, design, design_hashes, load_yaml, render_generation_prompts, stimuli_for_split, vb_ids
from .pretest import BOUNDARY_PRETEST, VB_PRETEST, build_pretest_manifest, render_pretest_prompts


def validate_design(config_path: Path) -> list[str]:
    errors: list[str] = []
    config = load_yaml(config_path)
    data = design()

    if config.get("experiment_id") != "PF-EXP-0005":
        errors.append("experiment_id must be PF-EXP-0005")
    if config.get("phase") != "pilot-002":
        errors.append("phase must be pilot-002")
    if config.get("canonical_model") != "APRL Personality Formation Model v1.2":
        errors.append("canonical_model must be v1.2")
    if int(config.get("replicates", 0)) != 3:
        errors.append("replicates must remain frozen at 3")
    if int(config.get("pretest_replicates", 0)) != 1:
        errors.append("pretest_replicates must remain frozen at 1")
    if not bool(config.get("require_pretest_pass", False)):
        errors.append("require_pretest_pass must be true")

    vbs = data.get("values_beliefs")
    if not isinstance(vbs, dict) or set(vbs) != set(vb_ids()):
        errors.append("values_beliefs must contain exactly VB-L and VB-E")
    else:
        packets = [str(vbs[v]["packet"]).strip() for v in vb_ids()]
        if not all(packets):
            errors.append("Values & Beliefs packets must be non-empty")
        forbidden = ("今回は", "この状況", "べき", "しなければ", "反論", "修正する", "行動")
        for vb_id in vb_ids():
            packet = str(vbs[vb_id]["packet"])
            hits = [word for word in forbidden if word in packet]
            if hits:
                errors.append(f"{vb_id}: possible current-response directiveness: {hits}")

    stimuli = stimuli_for_split(str(config.get("stimulus_split", "pilot")))
    if len(stimuli) != 8:
        errors.append(f"expected 8 pilot families, got {len(stimuli)}")
    family_ids = [row.get("family_id") for row in stimuli]
    if len(set(family_ids)) != len(family_ids):
        errors.append("family_id values must be unique")
    stimulus_ids = [row.get("id") for row in stimuli]
    if len(set(stimulus_ids)) != len(stimulus_ids):
        errors.append("stimulus ids must be unique")
    for row in stimuli:
        for key in ("id", "family_id", "situation", "perception", "relationship"):
            if not str(row.get(key, "")).strip():
                errors.append(f"{row.get('id', '?')}: missing {key}")
        if row.get("relationship") != "none / neutral":
            errors.append(f"{row.get('id')}: relationship must be none / neutral")
        if any(word in str(row.get("situation", "")) for word in ("感じ", "考え", "価値")):
            errors.append(f"{row.get('id')}: Situation may contain internal-state wording")
        if any(word in str(row.get("perception", "")) for word in ("成長", "改善点", "能力評価", "立場を脅", "学習機会")):
            errors.append(f"{row.get('id')}: Perception may preload Experience-level meaning")
        for vb_id in vb_ids():
            render_generation_prompts(row, vb_id)
            render_pretest_prompts(row, VB_PRETEST, vb_id)
        render_pretest_prompts(row, BOUNDARY_PRETEST)

    thresholds = load_yaml(ROOT / config["thresholds"])
    expected_pretest = {
        "min_learning_orientation_separation": 2.00,
        "min_evaluation_protection_orientation_separation": 2.00,
        "min_families_correct_vb_direction": 7,
        "max_mean_current_response_directiveness": 0.50,
        "max_single_current_response_directiveness": 1,
        "max_mean_current_situation_leakage": 0.50,
        "max_single_current_situation_leakage": 1,
        "max_mean_experience_meaning_preload": 0.50,
        "max_single_experience_meaning_preload": 1,
        "max_mean_relationship_salience": 0.50,
        "max_single_relationship_salience": 1,
    }
    expected_pilot = {
        "min_learning_meaning_effect": 0.75,
        "min_evaluation_threat_meaning_effect": 0.75,
        "min_families_dual_positive_effect": 6,
        "min_leave_one_family_out_learning_effect_exclusive": 0.0,
        "min_leave_one_family_out_evaluation_effect_exclusive": 0.0,
        "max_mean_response_leakage": 0.50,
        "max_single_response_leakage": 1,
    }
    if thresholds.get("pretest") != expected_pretest:
        errors.append("pretest thresholds differ from frozen plan")
    if thresholds.get("pilot") != expected_pilot:
        errors.append("pilot thresholds differ from frozen plan")

    for schema_key in ("output_schema", "evaluation_schema", "pretest_schema"):
        path = ROOT / config[schema_key]
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
            jsonschema.Draft202012Validator.check_schema(schema)
        except Exception as exc:
            errors.append(f"{path.name}: invalid schema: {exc}")

    manifest = build_pretest_manifest(config)
    kinds = [row["pretest_kind"] for row in manifest]
    if len(manifest) != 24 or kinds.count(VB_PRETEST) != 16 or kinds.count(BOUNDARY_PRETEST) != 8:
        errors.append("pilot-002 pretest manifest must contain 16 VB-quality + 8 boundary rows")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Static validation for PF-EXP-0005.")
    parser.add_argument("--config", type=Path, default=ROOT / "experiment.yaml")
    args = parser.parse_args()
    errors = validate_design(args.config.resolve())
    if errors:
        print("STATIC VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    config = load_yaml(args.config.resolve())
    families = len(stimuli_for_split(config["stimulus_split"]))
    pretest_count = len(build_pretest_manifest(config))
    print("STATIC VALIDATION: PASS")
    print(f"families={families}")
    print(f"pretest_manifest={pretest_count} (vb_quality=16, perception_boundary=8)")
    print(f"main_manifest={families * len(vb_ids()) * int(config['replicates'])}")
    print(f"blind_evaluation={families * len(vb_ids()) * int(config['replicates'])}")
    print("design hashes:")
    for path, digest in design_hashes().items():
        print(f"  {path}: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
