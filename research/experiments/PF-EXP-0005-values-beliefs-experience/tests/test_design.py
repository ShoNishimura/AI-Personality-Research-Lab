from pathlib import Path

from src.common import ROOT, design_hashes, load_yaml, render_generation_prompts, stimuli_for_split, vb_ids
from src.pilot import build_manifest
from src.pretest import BOUNDARY_PRETEST, VB_PRETEST, build_pretest_manifest, render_pretest_prompts
from src.validate import validate_design


def test_static_validation_passes() -> None:
    assert validate_design(ROOT / "experiment.yaml") == []


def test_manifest_counts_are_frozen() -> None:
    config = load_yaml(ROOT / "experiment.yaml")
    pretest = build_pretest_manifest(config)
    main = build_manifest(config)
    assert len(pretest) == 24
    assert sum(row["pretest_kind"] == VB_PRETEST for row in pretest) == 16
    assert sum(row["pretest_kind"] == BOUNDARY_PRETEST for row in pretest) == 8
    assert len(main) == 48
    assert len({row["pretest_id"] for row in pretest}) == 24
    assert len({row["run_id"] for row in main}) == 48


def test_eight_independent_families_and_neutral_relationship() -> None:
    config = load_yaml(ROOT / "experiment.yaml")
    stimuli = stimuli_for_split(config["stimulus_split"])
    assert len(stimuli) == 8
    assert len({row["family_id"] for row in stimuli}) == 8
    assert all(row["relationship"] == "none / neutral" for row in stimuli)


def test_generation_prompt_holds_situation_and_perception_fixed_within_family() -> None:
    config = load_yaml(ROOT / "experiment.yaml")
    for stimulus in stimuli_for_split(config["stimulus_split"]):
        _, task_l = render_generation_prompts(stimulus, "VB-L")
        _, task_e = render_generation_prompts(stimulus, "VB-E")
        assert stimulus["situation"] in task_l and stimulus["situation"] in task_e
        assert stimulus["perception"] in task_l and stimulus["perception"] in task_e
        assert "VB-L" not in task_l
        assert "VB-E" not in task_e


def test_boundary_pretest_does_not_show_values_beliefs() -> None:
    config = load_yaml(ROOT / "experiment.yaml")
    for stimulus in stimuli_for_split(config["stimulus_split"]):
        _, task = render_pretest_prompts(stimulus, BOUNDARY_PRETEST)
        assert stimulus["perception"] in task
        assert "[not shown in PERCEPTION_BOUNDARY mode]" in task
        for vb_id in vb_ids():
            assert vb_id not in task


def test_vb_pretest_does_not_show_perception() -> None:
    config = load_yaml(ROOT / "experiment.yaml")
    for stimulus in stimuli_for_split(config["stimulus_split"]):
        for vb_id in vb_ids():
            _, task = render_pretest_prompts(stimulus, VB_PRETEST, vb_id)
            assert stimulus["perception"] not in task
            assert "[not shown in VB_QUALITY mode]" in task


def test_design_hashes_cover_all_frozen_files() -> None:
    hashes = design_hashes()
    assert len(hashes) == 12
    assert all(len(value) == 64 for value in hashes.values())
