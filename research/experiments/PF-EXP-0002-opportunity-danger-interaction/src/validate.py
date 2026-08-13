from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
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

EXPECTED_CONDITIONS = {"T00", "T01", "T10", "T11"}
EXPECTED_OD = {("low", "low"), ("low", "high"), ("high", "low"), ("high", "high")}


def _rows_hash(rows: list[dict[str, Any]]) -> str:
    return sha256_text("".join(canonical_json(row) + "\n" for row in rows))


def validate_static(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    conditions = load_yaml(ROOT / "conditions.yaml")["conditions"]
    if {row["id"] for row in conditions} != EXPECTED_CONDITIONS:
        errors.append("conditions must define exactly T00/T01/T10/T11")

    stimuli = [
        row
        for row in load_yaml(ROOT / "stimuli.yaml")["stimuli"]
        if row["split"] == config["stimulus_split"]
    ]
    if len(stimuli) != 24:
        errors.append(f"pilot must contain 24 stimuli; got {len(stimuli)}")
    if len({row["id"] for row in stimuli}) != len(stimuli):
        errors.append("stimulus IDs must be unique")

    by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in stimuli:
        by_family[row["family_id"]].append(row)
    if len(by_family) != 6:
        errors.append(f"pilot must contain 6 scenario families; got {len(by_family)}")
    for family, rows in by_family.items():
        od = {(row["opportunity"], row["danger"]) for row in rows}
        if len(rows) != 4 or od != EXPECTED_OD:
            errors.append(f"{family}: must contain exactly one O/D 2x2 set")

    banned_subjective_terms = ("魅力的", "怖い", "危険だ", "興味深い")
    for row in stimuli:
        for term in banned_subjective_terms:
            if term in row["text"]:
                errors.append(f"{row['id']}: contains subjective cue {term}")

    review = load_yaml(ROOT / "reviews/stimulus-review.yaml")
    reviewed_ids = set(review["reviews"])
    stimulus_ids = {row["id"] for row in stimuli}
    if reviewed_ids != stimulus_ids:
        errors.append("stimulus review IDs do not exactly match pilot stimulus IDs")
    criteria = review["criteria"]
    minimum_total = int(review["minimum_total"])
    for stimulus_id, scores in review["reviews"].items():
        if set(scores) != set(criteria):
            errors.append(f"{stimulus_id}: review criteria mismatch")
            continue
        values = [int(scores[name]) for name in criteria]
        if sum(values) < minimum_total:
            errors.append(f"{stimulus_id}: review total below {minimum_total}")
        if review.get("no_zero_allowed") and any(value == 0 for value in values):
            errors.append(f"{stimulus_id}: review contains zero")

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

    thresholds = load_yaml(ROOT / config["thresholds"])
    if set(thresholds) != {"pretest", "pilot"}:
        errors.append("thresholds.yaml must define pretest and pilot sections")

    pretest_manifest = build_pretest_manifest(config)
    if len(pretest_manifest) != 24:
        errors.append(f"pretest manifest must contain 24 runs; got {len(pretest_manifest)}")
    if len({row["pretest_id"] for row in pretest_manifest}) != len(pretest_manifest):
        errors.append("pretest IDs must be unique")

    manifest = build_manifest(config)
    if len(manifest) != 192:
        errors.append(f"main manifest must contain 192 runs; got {len(manifest)}")
    if len({row["run_id"] for row in manifest}) != len(manifest):
        errors.append("main run IDs must be unique")

    condition_counts = Counter(row["condition_id"] for row in manifest)
    if any(condition_counts[c] != 48 for c in EXPECTED_CONDITIONS):
        errors.append(f"each temperament condition must have 48 runs; got {dict(condition_counts)}")
    stimulus_counts = Counter(row["stimulus_id"] for row in manifest)
    if any(count != 8 for count in stimulus_counts.values()):
        errors.append("each stimulus must have 8 runs")
    pair_counts = Counter((row["condition_id"], row["stimulus_id"]) for row in manifest)
    if any(count != 2 for count in pair_counts.values()):
        errors.append("each condition x stimulus pair must have exactly 2 replicates")

    for path_key, expected_rows in (
        ("pretest_manifest_path", pretest_manifest),
        ("manifest_path", manifest),
    ):
        path = ROOT / config[path_key]
        if path.exists() and read_jsonl(path) != expected_rows:
            errors.append(f"{path_key} does not match deterministic definition")

    status_path = ROOT / config["status_path"]
    if status_path.exists():
        status = load_yaml(status_path)
        if status.get("pretest_manifest_sha256") != _rows_hash(pretest_manifest):
            errors.append("status pretest_manifest_sha256 mismatch")
        if status.get("manifest_sha256") != _rows_hash(manifest):
            errors.append("status manifest_sha256 mismatch")
        if status.get("thresholds_sha256") != sha256_normalized_text_file(ROOT / config["thresholds"]):
            errors.append("status thresholds_sha256 mismatch")
        if status.get("stimuli_sha256") != sha256_normalized_text_file(ROOT / "stimuli.yaml"):
            errors.append("status stimuli_sha256 mismatch")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate PF-EXP-0002 frozen pilot design.")
    parser.add_argument("--config", type=Path, default=ROOT / "experiment.yaml")
    args = parser.parse_args()
    config = load_yaml(args.config.resolve())
    errors = validate_static(config)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: PF-EXP-0002 static validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
