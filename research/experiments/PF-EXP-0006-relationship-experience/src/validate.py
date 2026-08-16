from __future__ import annotations

import json

from .common import ROOT, design_hashes, load_yaml, relationship_ids, stimuli_for_split
from .pilot import build_manifest
from .pretest import BOUNDARY_PRETEST, REL_PRETEST, build_pretest_manifest


def main() -> int:
    config = load_yaml(ROOT / "experiment.yaml")
    stimuli = stimuli_for_split(config["stimulus_split"])
    errors: list[str] = []

    if config["experiment_id"] != "PF-EXP-0006":
        errors.append("experiment_id must be PF-EXP-0006")
    if config["phase"] != "pilot-001":
        errors.append("phase must be pilot-001")
    if len(stimuli) != 8:
        errors.append(f"expected 8 stimuli, got {len(stimuli)}")
    if len({s["family_id"] for s in stimuli}) != 8:
        errors.append("family_id must be unique across 8 stimuli")
    if set(relationship_ids()) != {"REL-T", "REL-D"}:
        errors.append("relationship conditions must be REL-T / REL-D")

    for stimulus in stimuli:
        if not stimulus.get("situation") or not stimulus.get("perception"):
            errors.append(f"{stimulus.get('id')}: missing situation/perception")

    pretest = build_pretest_manifest(config)
    relationship_count = sum(r["pretest_kind"] == REL_PRETEST for r in pretest)
    boundary_count = sum(r["pretest_kind"] == BOUNDARY_PRETEST for r in pretest)
    main_manifest = build_manifest(config)

    if (len(pretest), relationship_count, boundary_count) != (24, 16, 8):
        errors.append(
            f"pretest counts wrong: total={len(pretest)} relationship={relationship_count} boundary={boundary_count}"
        )
    if len(main_manifest) != 48:
        errors.append(f"main count wrong: {len(main_manifest)}")

    for schema_name in ("output.schema.json", "evaluation.schema.json", "pretest.schema.json"):
        json.loads((ROOT / schema_name).read_text(encoding="utf-8"))

    print(json.dumps({
        "experiment_id": config["experiment_id"],
        "phase": config["phase"],
        "families": len(stimuli),
        "pretest_total": len(pretest),
        "pretest_relationship": relationship_count,
        "pretest_boundary": boundary_count,
        "main_generation": len(main_manifest),
        "blind_evaluation": len(main_manifest),
        "design_hashes": design_hashes(),
        "errors": errors,
    }, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
