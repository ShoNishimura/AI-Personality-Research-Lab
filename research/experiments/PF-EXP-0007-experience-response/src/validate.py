from __future__ import annotations

import json

from .common import ROOT, design, experience_ids, load_yaml, stimuli_for_split
from .pilot import build_manifest
from .pretest import EXPERIENCE_PRETEST, SITUATION_PRETEST, build_pretest_manifest


def main() -> int:
    config = load_yaml(ROOT / "experiment.yaml")
    thresholds = load_yaml(ROOT / config["thresholds"])
    for schema_name in (config["output_schema"], config["evaluation_schema"], config["pretest_schema"]):
        json.loads((ROOT / schema_name).read_text(encoding="utf-8"))

    current_design = design()
    if set(current_design["experiences"]) != {"E-B", "E-A"}:
        raise RuntimeError("Experience conditions must be exactly E-B and E-A")
    if experience_ids() != ("E-B", "E-A"):
        raise RuntimeError("unexpected Experience condition order")

    stimuli = stimuli_for_split(config["stimulus_split"])
    if len(stimuli) != 8:
        raise RuntimeError(f"expected 8 pilot stimuli, got {len(stimuli)}")
    if len({s["id"] for s in stimuli}) != 8 or len({s["family_id"] for s in stimuli}) != 8:
        raise RuntimeError("stimulus and family ids must be unique")

    banned = ("警戒する", "身構える", "距離を取りたい", "関わり続けたい", "質問する", "断る")
    for exp_id in experience_ids():
        packet = str(current_design["experiences"][exp_id]["packet"])
        for token in banned:
            if token in packet:
                raise RuntimeError(f"{exp_id}: banned Response-tendency wording found: {token}")

    pretest = build_pretest_manifest(config)
    exp_count = sum(r["pretest_kind"] == EXPERIENCE_PRETEST for r in pretest)
    situation_count = sum(r["pretest_kind"] == SITUATION_PRETEST for r in pretest)
    if (len(pretest), exp_count, situation_count) != (24, 16, 8):
        raise RuntimeError(f"unexpected pretest counts: total={len(pretest)} experience={exp_count} situation={situation_count}")

    main_manifest = build_manifest(config)
    if len(main_manifest) != 48:
        raise RuntimeError(f"expected 48 main generation rows, got {len(main_manifest)}")
    if len({r["run_id"] for r in main_manifest}) != 48:
        raise RuntimeError("main run ids are not unique")

    pre = thresholds["pretest"]
    pilot = thresholds["pilot"]
    assert float(pre["min_benign_meaning_separation"]) == 2.0
    assert float(pre["min_adverse_meaning_separation"]) == 2.0
    assert int(pre["min_families_correct_experience_direction"]) == 7
    assert float(pilot["min_constructive_engagement_effect"]) == 0.75
    assert float(pilot["min_protective_distancing_effect"]) == 0.75
    assert int(pilot["min_families_dual_positive_effect"]) == 6

    print("PF-EXP-0007 static validation: PASS")
    print("families=8 pretest=24 (experience=16 situation=8) main_generation=48 blind_evaluation=48")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
