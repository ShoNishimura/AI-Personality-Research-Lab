from src.common import DESIGN_FILES, ROOT, design, experience_by_id, load_yaml, stimuli_for_split
from src.pilot import build_manifest
from src.pretest import EXPERIENCE_PRETEST, SITUATION_PRETEST, build_pretest_manifest


def test_design_counts_and_conditions():
    config = load_yaml(ROOT / "experiment.yaml")
    stimuli = stimuli_for_split(config["stimulus_split"])
    assert len(stimuli) == 8
    assert len({s["family_id"] for s in stimuli}) == 8
    assert set(design()["experiences"]) == {"E-B", "E-A"}


def test_experience_packets_do_not_preload_response_tendency():
    banned = ("警戒する", "身構える", "距離を取りたい", "関わり続けたい", "質問する", "断る")
    for exp_id in ("E-B", "E-A"):
        packet = experience_by_id(exp_id)["packet"]
        assert not any(token in packet for token in banned)


def test_pretest_manifest_split_and_uniqueness():
    config = load_yaml(ROOT / "experiment.yaml")
    rows = build_pretest_manifest(config)
    assert len(rows) == 24
    assert sum(r["pretest_kind"] == EXPERIENCE_PRETEST for r in rows) == 16
    assert sum(r["pretest_kind"] == SITUATION_PRETEST for r in rows) == 8
    assert len({r["pretest_id"] for r in rows}) == 24


def test_main_manifest_count_pairing_and_uniqueness():
    config = load_yaml(ROOT / "experiment.yaml")
    rows = build_manifest(config)
    assert len(rows) == 48
    assert len({r["run_id"] for r in rows}) == 48
    pairs = {(r["family_id"], r["replicate_id"]): set() for r in rows}
    for row in rows:
        pairs[(row["family_id"], row["replicate_id"])].add(row["exp_id"])
    assert all(value == {"E-B", "E-A"} for value in pairs.values())


def test_planned_thresholds_are_frozen():
    config = load_yaml(ROOT / "experiment.yaml")
    thresholds = load_yaml(ROOT / config["thresholds"])
    assert thresholds["pretest"]["min_benign_meaning_separation"] == 2.0
    assert thresholds["pretest"]["min_adverse_meaning_separation"] == 2.0
    assert thresholds["pretest"]["min_families_correct_experience_direction"] == 7
    assert thresholds["pilot"]["min_constructive_engagement_effect"] == 0.75
    assert thresholds["pilot"]["min_protective_distancing_effect"] == 0.75
    assert thresholds["pilot"]["min_families_dual_positive_effect"] == 6


def test_freeze_covers_runtime_code_and_environment_snapshots_are_separate():
    config = load_yaml(ROOT / "experiment.yaml")
    required = {
        "src/common.py",
        "src/pretest.py",
        "src/pretest_analyze.py",
        "src/pilot.py",
        "src/blind.py",
        "src/evaluate.py",
        "src/analyze.py",
        "src/validate.py",
    }
    assert required.issubset(set(DESIGN_FILES))
    assert config["pretest_environment_path"] != config["main_environment_path"]
