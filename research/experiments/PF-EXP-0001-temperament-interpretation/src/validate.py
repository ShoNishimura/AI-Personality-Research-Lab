from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

import jsonschema

from .common import ROOT, canonical_json, load_yaml, read_jsonl, sha256_normalized_text_file, sha256_text
from .pilot import build_manifest

EXPECTED_CLASSES = {"seeking-target", "negative-target", "conflict", "neutral"}
EXPECTED_CONDITIONS = {"T00", "T01", "T10", "T11"}


def validate_static(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    conditions = load_yaml(ROOT / "conditions.yaml")["conditions"]
    condition_ids = {row["id"] for row in conditions}
    if condition_ids != EXPECTED_CONDITIONS:
        errors.append(f"conditions must be {sorted(EXPECTED_CONDITIONS)}; got {sorted(condition_ids)}")

    stimuli = [
        row
        for row in load_yaml(ROOT / "stimuli.yaml")["stimuli"]
        if row["split"] == config["stimulus_split"]
    ]
    if len(stimuli) != 12:
        errors.append(f"pilot must contain 12 stimuli; got {len(stimuli)}")
    class_counts = Counter(row["class"] for row in stimuli)
    if set(class_counts) != EXPECTED_CLASSES or any(class_counts[c] != 3 for c in EXPECTED_CLASSES):
        errors.append(f"each stimulus class must contain 3 items; got {dict(class_counts)}")
    if len({row["id"] for row in stimuli}) != len(stimuli):
        errors.append("stimulus IDs must be unique")

    review = load_yaml(ROOT / "reviews/stimulus-review.yaml")
    criteria = review["criteria"]
    minimum_total = int(review["minimum_total"])
    reviewed_ids = set(review["reviews"])
    stimulus_ids = {row["id"] for row in stimuli}
    if reviewed_ids != stimulus_ids:
        errors.append("stimulus review IDs do not exactly match pilot stimulus IDs")
    for stimulus_id, scores in review["reviews"].items():
        if set(scores) != set(criteria):
            errors.append(f"{stimulus_id}: review criteria mismatch")
            continue
        values = [int(scores[name]) for name in criteria]
        if sum(values) < minimum_total:
            errors.append(f"{stimulus_id}: review total below {minimum_total}")
        if review.get("no_zero_allowed") and any(value == 0 for value in values):
            errors.append(f"{stimulus_id}: review contains zero")

    for schema_name in (config["output_schema"], config["evaluation_schema"]):
        schema = json.loads((ROOT / schema_name).read_text(encoding="utf-8"))
        try:
            jsonschema.Draft202012Validator.check_schema(schema)
        except jsonschema.SchemaError as exc:
            errors.append(f"invalid schema {schema_name}: {exc.message}")

    thresholds = load_yaml(ROOT / config["thresholds"])["gates"]
    expected_gates = {
        "G1_seeking_main_effect",
        "G2_negative_main_effect",
        "G3_discriminant_validity",
        "G4_conflict_coactivation",
        "G5_neutrality",
    }
    if set(thresholds) != expected_gates:
        errors.append("thresholds.yaml must define exactly G1-G5")

    manifest = build_manifest(config)
    if len(manifest) != 96:
        errors.append(f"manifest must contain 96 runs; got {len(manifest)}")
    if len({row["run_id"] for row in manifest}) != len(manifest):
        errors.append("manifest run IDs must be unique")
    condition_counts = Counter(row["condition_id"] for row in manifest)
    if any(condition_counts[c] != 24 for c in EXPECTED_CONDITIONS):
        errors.append(f"each condition must have 24 runs; got {dict(condition_counts)}")
    stimulus_counts = Counter(row["stimulus_id"] for row in manifest)
    if any(count != 8 for count in stimulus_counts.values()):
        errors.append("each stimulus must have 8 runs")
    pair_counts = Counter((row["condition_id"], row["stimulus_id"]) for row in manifest)
    if any(count != 2 for count in pair_counts.values()):
        errors.append("each condition × stimulus pair must have exactly 2 replicates")

    frozen_manifest_path = ROOT / config["manifest_path"]
    if frozen_manifest_path.exists():
        frozen = read_jsonl(frozen_manifest_path)
        if frozen != manifest:
            errors.append("generated manifest does not match current prompts/stimuli/config")

    status_path = ROOT / "runs/pilot-001/status.yaml"
    if status_path.exists():
        status = load_yaml(status_path)
        proposed_manifest = "".join(canonical_json(row) + "\n" for row in manifest)
        if status.get("manifest_sha256") != sha256_text(proposed_manifest):
            errors.append("status manifest_sha256 does not match deterministic manifest definition")
        if status.get("thresholds_sha256") != sha256_normalized_text_file(ROOT / config["thresholds"]):
            errors.append("status thresholds_sha256 does not match thresholds.yaml")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate PF-EXP-0001 frozen pilot design.")
    parser.add_argument("--config", type=Path, default=ROOT / "experiment.yaml")
    args = parser.parse_args()
    config = load_yaml(args.config.resolve())
    errors = validate_static(config)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: PF-EXP-0001 static validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
