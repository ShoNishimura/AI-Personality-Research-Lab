from src.common import ROOT, load_yaml, relationship_by_id, relationship_ids, render_generation_prompts, stimuli_for_split
from src.pilot import build_manifest
from src.pretest import BOUNDARY_PRETEST, REL_PRETEST, build_pretest_manifest, render_pretest_prompts


def config():
    return load_yaml(ROOT / "experiment.yaml")


def test_counts():
    c = config()
    assert len(stimuli_for_split(c["stimulus_split"])) == 8
    assert len(build_manifest(c)) == 48
    pretest = build_pretest_manifest(c)
    assert len(pretest) == 24
    assert sum(r["pretest_kind"] == REL_PRETEST for r in pretest) == 16
    assert sum(r["pretest_kind"] == BOUNDARY_PRETEST for r in pretest) == 8


def test_relationship_ids_and_packets():
    assert relationship_ids() == ("REL-T", "REL-D")
    assert "信頼性を高く" in relationship_by_id("REL-T")["packet"]
    assert "信頼性を低く" in relationship_by_id("REL-D")["packet"]


def test_generation_pair_differs_only_relationship_input():
    stimulus = stimuli_for_split("pilot")[0]
    system_t, user_t = render_generation_prompts(stimulus, "REL-T")
    system_d, user_d = render_generation_prompts(stimulus, "REL-D")
    assert system_t == system_d
    assert stimulus["situation"] in user_t and stimulus["situation"] in user_d
    assert stimulus["perception"] in user_t and stimulus["perception"] in user_d
    assert user_t != user_d


def test_boundary_pretest_hides_relationship():
    stimulus = stimuli_for_split("pilot")[0]
    _, user = render_pretest_prompts(stimulus, BOUNDARY_PRETEST)
    assert "[not shown in PERCEPTION_BOUNDARY mode]" in user
    assert relationship_by_id("REL-T")["packet"] not in user
    assert relationship_by_id("REL-D")["packet"] not in user


def test_relationship_pretest_hides_perception():
    stimulus = stimuli_for_split("pilot")[0]
    _, user = render_pretest_prompts(stimulus, REL_PRETEST, "REL-T")
    assert "[not shown in RELATIONSHIP_QUALITY mode]" in user
    assert stimulus["perception"] not in user
