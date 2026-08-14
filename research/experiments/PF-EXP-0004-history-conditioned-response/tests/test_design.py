from collections import Counter

from src.common import history_by_id, load_yaml, stimuli_for_split
from src.pilot import build_manifest
from src.pretest import build_pretest_manifest


def test_manifest_shape_and_history_pairing() -> None:
    config = load_yaml(__import__("src.common", fromlist=["ROOT"]).ROOT / "experiment.yaml")
    stimuli = stimuli_for_split(config["stimulus_split"])
    assert len(stimuli) == 8
    for stimulus in stimuli:
        plus = history_by_id(stimulus, "H+")
        minus = history_by_id(stimulus, "H-")
        assert [episode["response"] for episode in plus["episodes"]] == [
            episode["response"] for episode in minus["episodes"]
        ]
        assert [episode["outcome"] for episode in plus["episodes"]] != [
            episode["outcome"] for episode in minus["episodes"]
        ]

    pretest = build_pretest_manifest(config)
    main = build_manifest(config)
    assert len(pretest) == 16
    assert len(main) == 48
    assert len({row["pretest_id"] for row in pretest}) == 16
    assert len({row["run_id"] for row in main}) == 48
    assert set(Counter((row["family_id"], row["history_id"]) for row in main).values()) == {3}
