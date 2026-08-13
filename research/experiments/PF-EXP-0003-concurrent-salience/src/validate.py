from __future__ import annotations

import json
from collections import Counter
from typing import Any

import jsonschema

from .common import (
    ROOT,
    canonical_json,
    load_yaml,
    read_jsonl,
    sha256_normalized_text_file,
    sha256_text,
)
from .pilot import build_manifest
from .pretest import build_pretest_manifest

EXPECTED_CONDITIONS = {"T01", "T11"}


def _rows_hash(rows: list[dict[str, Any]]) -> str:
    return sha256_text("".join(canonical_json(row) + "\n" for row in rows))


def main() -> int:
    config = load_yaml(ROOT / "experiment.yaml")
    conditions = load_yaml(ROOT / "conditions.yaml")["conditions"]
    stimuli = [
        row
        for row in load_yaml(ROOT / "stimuli.yaml")["stimuli"]
        if row["split"] == config["stimulus_split"]
    ]
    thresholds = load_yaml(ROOT / config["thresholds"])
    status = load_yaml(ROOT / config["status_path"])
    errors: list[str] = []

    if config["experiment_id"] != "PF-EXP-0003":
        errors.append("experiment_id must be PF-EXP-0003")
    if int(config["replicates"]) != 3 or int(config["pretest_replicates"]) != 1:
        errors.append("replicates must be 3 and pretest_replicates 1")
    if {condition["id"] for condition in conditions} != EXPECTED_CONDITIONS:
        errors.append("conditions must be exactly T01 and T11")
    if any(condition["negative_affectivity"] != "high" for condition in conditions):
        errors.append("N must be fixed High")

    if len(stimuli) != 16:
        errors.append(f"expected 16 stimuli; got {len(stimuli)}")
    if len({row["id"] for row in stimuli}) != len(stimuli):
        errors.append("stimulus IDs must be unique")

    families = Counter(row["family_id"] for row in stimuli)
    if len(families) != 8 or any(count != 2 for count in families.values()):
        errors.append("expected 8 families with exactly 2 variants each")
    if any(row["danger"] != "high" for row in stimuli):
        errors.append("Danger must be fixed High")

    for family in sorted(families):
        pair = [row for row in stimuli if row["family_id"] == family]
        if {row["opportunity"] for row in pair} != {"low", "high"}:
            errors.append(f"{family}: Opportunity variants must be low/high")
        if len({row["context_clause"] for row in pair}) != 1:
            errors.append(f"{family}: context_clause differs")
        if len({row["danger_clause"] for row in pair}) != 1:
            errors.append(f"{family}: danger_clause differs")
        for row in pair:
            expected_text = f'{row["context_clause"]} {row["opportunity_clause"]} {row["danger_clause"]}'
            if row["text"] != expected_text:
                errors.append(f'{row["id"]}: text does not match frozen clauses')

    prior_texts: set[str] = set()
    for prior_dir in (
        ROOT.parent / "PF-EXP-0001-temperament-interpretation",
        ROOT.parent / "PF-EXP-0002-opportunity-danger-interaction",
    ):
        path = prior_dir / "stimuli.yaml"
        if path.exists():
            prior_texts.update(row["text"] for row in load_yaml(path)["stimuli"])
    reused = sorted(row["id"] for row in stimuli if row["text"] in prior_texts)
    if reused:
        errors.append(f"stimulus text reused from PF-EXP-0001/0002: {reused}")

    review = load_yaml(ROOT / "reviews/stimulus-review.yaml")
    if review.get("status") != "frozen_before_responses":
        errors.append("stimulus review must be frozen_before_responses")
    if int(review.get("families_reviewed", 0)) != 8:
        errors.append("stimulus review must cover 8 families")
    if int(review.get("stimuli_reviewed", 0)) != 16:
        errors.append("stimulus review must cover 16 stimuli")

    for schema_name in (
        config["output_schema"],
        config["evaluation_schema"],
        config["pretest_schema"],
    ):
        schema = json.loads((ROOT / schema_name).read_text(encoding="utf-8"))
        try:
            jsonschema.Draft202012Validator.check_schema(schema)
        except jsonschema.SchemaError as exc:
            errors.append(f"invalid schema {schema_name}: {exc.message}")

    if set(thresholds) != {"pretest", "pilot"}:
        errors.append("thresholds.yaml must define pretest and pilot sections")
    else:
        pretest_thresholds = thresholds["pretest"]
        pilot_thresholds = thresholds["pilot"]
        expected_thresholds = {
            "pre_min_opp": (pretest_thresholds["min_opportunity_main_effect"], 1.50),
            "pre_max_cross": (pretest_thresholds["max_opportunity_to_danger_cross_abs"], 0.50),
            "pre_family": (pretest_thresholds["min_families_opportunity_correct_direction"], 7),
            "g2_seek": (pilot_thresholds["min_seeking_main_effect"], 0.75),
            "g2_opp": (pilot_thresholds["min_t11_opportunity_uptake"], 0.50),
            "g3_danger": (pilot_thresholds["min_t11_danger_delta"], -0.25),
            "g3_interaction": (pilot_thresholds["min_primary_danger_interaction"], 0.20),
            "g4_family": (pilot_thresholds["min_positive_family_interactions"], 5),
            "g4_loo": (pilot_thresholds["min_leave_one_family_out_interaction_exclusive"], 0.0),
            "g5_opp": (pilot_thresholds["min_t11_o_high_opportunity_salience"], 2.50),
            "g5_danger": (pilot_thresholds["min_t11_o_high_danger_salience"], 2.50),
            "g5_rate": (pilot_thresholds["min_t11_o_high_concurrent_rate"], 0.75),
            "joint_cut": (pilot_thresholds["concurrent_min_score_each"], 2),
        }
        for name, (actual, wanted) in expected_thresholds.items():
            if float(actual) != float(wanted):
                errors.append(f"{name}: expected {wanted}, got {actual}")

    pretest_manifest = build_pretest_manifest(config)
    if len(pretest_manifest) != 16:
        errors.append(f"pretest manifest must contain 16 runs; got {len(pretest_manifest)}")
    if len({row["pretest_id"] for row in pretest_manifest}) != len(pretest_manifest):
        errors.append("pretest IDs must be unique")

    manifest = build_manifest(config)
    if len(manifest) != 96:
        errors.append(f"main manifest must contain 96 runs; got {len(manifest)}")
    if len({row["run_id"] for row in manifest}) != len(manifest):
        errors.append("main run IDs must be unique")

    condition_counts = Counter(row["condition_id"] for row in manifest)
    if any(condition_counts[condition] != 48 for condition in EXPECTED_CONDITIONS):
        errors.append(f"each condition must have 48 runs; got {dict(condition_counts)}")
    stimulus_counts = Counter(row["stimulus_id"] for row in manifest)
    if any(count != 6 for count in stimulus_counts.values()):
        errors.append("each stimulus must have 6 runs")
    pair_counts = Counter((row["condition_id"], row["stimulus_id"]) for row in manifest)
    if any(count != 3 for count in pair_counts.values()):
        errors.append("each condition x stimulus pair must have exactly 3 replicates")

    for path_key, expected_rows in (
        ("pretest_manifest_path", pretest_manifest),
        ("manifest_path", manifest),
    ):
        path = ROOT / config[path_key]
        if path.exists() and read_jsonl(path) != expected_rows:
            errors.append(f"{path_key} does not match deterministic definition")

    frozen_hashes = {
        "pretest_manifest_sha256": _rows_hash(pretest_manifest),
        "manifest_sha256": _rows_hash(manifest),
        "thresholds_sha256": sha256_normalized_text_file(ROOT / config["thresholds"]),
        "stimuli_sha256": sha256_normalized_text_file(ROOT / "stimuli.yaml"),
    }
    for key, observed in frozen_hashes.items():
        if status.get(key) != observed:
            errors.append(f"status {key} mismatch")

    required = [
        "src/pretest.py",
        "src/pretest_analyze.py",
        "src/blind.py",
        "src/evaluate.py",
        "src/analyze.py",
        "tests/test_design.py",
        "tests/test_analysis.py",
        "reviews/stimulus-review.yaml",
    ]
    for rel in required:
        if not (ROOT / rel).exists():
            errors.append(f"missing required file: {rel}")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: PF-EXP-0003 static validation")
    print("  pretest: 16 / generation: 96 / evaluation: 96")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
