import json
from pathlib import Path

import jsonschema

from src.pilot import ROOT, build_manifest, load_yaml


def test_manifest_is_deterministic_and_bounded():
    config = load_yaml(ROOT / "experiment.yaml")
    first = build_manifest(config)
    second = build_manifest(config)
    assert first == second
    assert len(first) == 24
    assert len({row["run_id"] for row in first}) == 24


def test_full_factorial_has_expected_size():
    config = load_yaml(ROOT / "experiment.yaml")
    config["max_runs"] = None
    assert len(build_manifest(config)) == 8 * 12


def test_schema_accepts_representative_output():
    schema = json.loads((Path(ROOT) / "output.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate({
        "interpretation": {"summary": "A possible opportunity with uncertainty.", "approach_valence": 5, "threat_valence": 3, "regulation": 4},
        "response": {"action": "Ask for details before deciding.", "action_category": "observe", "intensity": 3, "latency": 4},
    }, schema)

