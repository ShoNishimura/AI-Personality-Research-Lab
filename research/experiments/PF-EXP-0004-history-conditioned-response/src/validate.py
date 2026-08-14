from __future__ import annotations

import json
from collections import Counter
from typing import Any

import jsonschema

from .common import (
    ROOT,
    design_hashes,
    history_by_id,
    load_yaml,
    render_evaluator_prompts,
    render_generation_prompts,
    render_pretest_prompts,
    stimuli_for_split,
)
from .pilot import build_manifest
from .pretest import build_pretest_manifest

EXPECTED_HISTORY_IDS = {"H+", "H-"}
FORBIDDEN_GENERATION_TERMS = ("Temperament", "Seeking Reactivity", "Negative Affectivity", "T0")
FORBIDDEN_HISTORY_PHRASES = ("今回は", "次も", "べき", "自信を持", "慎重な性格", "臆病", "積極的な性格")


def _check_thresholds(thresholds: dict[str, Any], errors: list[str]) -> None:
    expected = {
        ("pretest", "min_outcome_valence_separation"): 2.00,
        ("pretest", "max_mean_current_response_directiveness"): 0.50,
        ("pretest", "max_single_current_response_directiveness"): 1,
        ("pretest", "max_mean_trait_labeling"): 0.50,
        ("pretest", "max_single_trait_labeling"): 1,
        ("pretest", "min_families_correct_valence_direction"): 7,
        ("pilot", "min_primary_approach_effect"): 0.75,
        ("pilot", "min_families_positive_approach_effect"): 6,
        ("pilot", "min_leave_one_family_out_approach_effect_exclusive"): 0.0,
    }
    for (section, key), wanted in expected.items():
        actual = thresholds.get(section, {}).get(key)
        if actual is None or float(actual) != float(wanted):
            errors.append(f"threshold {section}.{key}: expected {wanted}, got {actual}")


def main() -> int:
    config = load_yaml(ROOT / "experiment.yaml")
    stimuli = stimuli_for_split(config["stimulus_split"])
    thresholds = load_yaml(ROOT / config["thresholds"])
    errors: list[str] = []

    if config["experiment_id"] != "PF-EXP-0004":
        errors.append("experiment_id must be PF-EXP-0004")
    if config["canonical_model"] != "APRL Personality Formation Model v1.1":
        errors.append("canonical model must be v1.1")
    if int(config["replicates"]) != 3 or int(config["pretest_replicates"]) != 1:
        errors.append("replicates must be 3 and pretest_replicates 1")
    if not config.get("require_pretest_pass", False):
        errors.append("require_pretest_pass must be true")
    if len(stimuli) != 8:
        errors.append(f"expected 8 scenario families; got {len(stimuli)}")
    if len({row["id"] for row in stimuli}) != len(stimuli):
        errors.append("stimulus IDs must be unique")

    for stimulus in stimuli:
        family = stimulus["family_id"]
        if stimulus["id"] != family:
            errors.append(f"{family}: stimulus id must equal family id")
        if stimulus["relationship"] != "none / neutral":
            errors.append(f"{family}: Relationship must be none / neutral")
        histories = stimulus["histories"]
        if {row["id"] for row in histories} != EXPECTED_HISTORY_IDS:
            errors.append(f"{family}: histories must be exactly H+ and H-")
            continue
        plus = history_by_id(stimulus, "H+")
        minus = history_by_id(stimulus, "H-")
        if plus["valence"] != "favorable" or minus["valence"] != "adverse":
            errors.append(f"{family}: history valence metadata mismatch")
        if len(plus["episodes"]) != 3 or len(minus["episodes"]) != 3:
            errors.append(f"{family}: each history must contain exactly 3 episodes")
        plus_responses = [row["response"] for row in plus["episodes"]]
        minus_responses = [row["response"] for row in minus["episodes"]]
        if plus_responses != minus_responses:
            errors.append(f"{family}: past Response wording must be identical across H+ / H-")
        plus_outcomes = [row["outcome"] for row in plus["episodes"]]
        minus_outcomes = [row["outcome"] for row in minus["episodes"]]
        if plus_outcomes == minus_outcomes:
            errors.append(f"{family}: outcomes must differ across H+ / H-")
        for history in histories:
            for episode in history["episodes"]:
                text = f"{episode['response']} {episode['outcome']}"
                for phrase in FORBIDDEN_HISTORY_PHRASES:
                    if phrase in text:
                        errors.append(f"{family}/{history['id']}: forbidden directive/trait phrase {phrase!r}")

        system_plus, user_plus = render_generation_prompts(stimulus, "H+")
        system_minus, user_minus = render_generation_prompts(stimulus, "H-")
        for term in FORBIDDEN_GENERATION_TERMS:
            if term in system_plus or term in user_plus or term in system_minus or term in user_minus:
                errors.append(f"{family}: generation prompt contains forbidden term {term}")
        if "H+" in user_plus or "H-" in user_plus or "H+" in user_minus or "H-" in user_minus:
            errors.append(f"{family}: condition label leaked into generation prompt")

        _, pre_plus = render_pretest_prompts(stimulus, "H+")
        _, pre_minus = render_pretest_prompts(stimulus, "H-")
        if "H+" in pre_plus or "H-" in pre_plus or "H+" in pre_minus or "H-" in pre_minus:
            errors.append(f"{family}: condition label leaked into pretest prompt")

    for schema_name in (config["output_schema"], config["evaluation_schema"], config["pretest_schema"]):
        schema = json.loads((ROOT / schema_name).read_text(encoding="utf-8"))
        try:
            jsonschema.Draft202012Validator.check_schema(schema)
        except jsonschema.SchemaError as exc:
            errors.append(f"invalid schema {schema_name}: {exc.message}")

    _check_thresholds(thresholds, errors)

    pretest_manifest = build_pretest_manifest(config)
    manifest = build_manifest(config)
    if len(pretest_manifest) != 16:
        errors.append(f"pretest manifest must contain 16 runs; got {len(pretest_manifest)}")
    if len(manifest) != 48:
        errors.append(f"main manifest must contain 48 runs; got {len(manifest)}")
    if len({row["pretest_id"] for row in pretest_manifest}) != len(pretest_manifest):
        errors.append("pretest IDs must be unique")
    if len({row["run_id"] for row in manifest}) != len(manifest):
        errors.append("main run IDs must be unique")

    family_counts = Counter(row["family_id"] for row in manifest)
    if any(count != 6 for count in family_counts.values()) or len(family_counts) != 8:
        errors.append(f"each family must have 6 main runs; got {dict(family_counts)}")
    cell_counts = Counter((row["family_id"], row["history_id"]) for row in manifest)
    if any(count != 3 for count in cell_counts.values()):
        errors.append("each family x history cell must contain exactly 3 replicates")

    review = load_yaml(ROOT / "reviews/stimulus-review.yaml")
    if review.get("status") != "frozen_before_responses":
        errors.append("stimulus review must be frozen_before_responses")
    if int(review.get("families_reviewed", 0)) != 8 or int(review.get("history_stimuli_reviewed", 0)) != 16:
        errors.append("stimulus review must cover 8 families / 16 histories")

    sample_blind = {
        "current_experience": stimuli[0]["current_experience"],
        "perception": stimuli[0]["perception"],
        "response": {"action": "限定範囲で試す。", "intensity": 2, "latency": 1},
    }
    _, evaluator_user = render_evaluator_prompts(sample_blind)
    if "Past History" in evaluator_user or "H+" in evaluator_user or "H-" in evaluator_user:
        errors.append("evaluator prompt leaks History information")

    required = [
        "src/common.py",
        "src/pretest.py",
        "src/pretest_analyze.py",
        "src/pilot.py",
        "src/blind.py",
        "src/evaluate.py",
        "src/analyze.py",
        "tests/test_design.py",
        "tests/test_analysis.py",
        "tests/test_prompts.py",
        "tests/test_schemas.py",
        "reviews/stimulus-review.yaml",
    ]
    for rel in required:
        if not (ROOT / rel).exists():
            errors.append(f"missing required file: {rel}")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("PASS: PF-EXP-0004 static validation")
    print("  pretest: 16 / generation: 48 / evaluation: 48")
    print(json.dumps({"design_hashes": design_hashes()}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
