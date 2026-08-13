from src.common import ROOT, load_yaml
from src.pilot import build_manifest
from src.pretest import build_pretest_manifest


def test_main_manifest_has_96_unique_runs():
    rows = build_manifest(load_yaml(ROOT / "experiment.yaml"))
    assert len(rows) == 96
    assert len({r["run_id"] for r in rows}) == 96


def test_pretest_manifest_has_16_unique_runs():
    rows = build_pretest_manifest(load_yaml(ROOT / "experiment.yaml"))
    assert len(rows) == 16
    assert len({r["pretest_id"] for r in rows}) == 16


def test_design_uses_only_t01_t11_and_high_danger():
    conditions = load_yaml(ROOT / "conditions.yaml")["conditions"]
    stimuli = load_yaml(ROOT / "stimuli.yaml")["stimuli"]
    assert {c["id"] for c in conditions} == {"T01", "T11"}
    assert {s["danger"] for s in stimuli} == {"high"}


def test_family_context_and_danger_are_identical():
    stimuli = load_yaml(ROOT / "stimuli.yaml")["stimuli"]
    for family in sorted({s["family_id"] for s in stimuli}):
        pair = [s for s in stimuli if s["family_id"] == family]
        assert len({s["context_clause"] for s in pair}) == 1
        assert len({s["danger_clause"] for s in pair}) == 1
