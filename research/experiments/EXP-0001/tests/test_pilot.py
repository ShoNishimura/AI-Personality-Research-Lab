import json
from pathlib import Path

import jsonschema
from openai import Omit

from src.blind import build_blind_files
from src.pilot import ROOT, build_manifest, create_openai_client, load_yaml, write_jsonl
from src.validate import validate


def test_manifest_is_deterministic_and_balanced():
    config = load_yaml(ROOT / "experiment.yaml")
    first = build_manifest(config)
    second = build_manifest(config)
    assert first == second
    assert len(first) == 96
    assert len({row["run_id"] for row in first}) == 96
    assert {sum(row["condition_id"][axis] == "1" for row in first) for axis in (1, 2, 3)} == {48}
    assert {sum(row["stimulus_id"] == stimulus_id for row in first) for stimulus_id in {r["stimulus_id"] for r in first}} == {8}


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


def test_manifest_refuses_different_overwrite(tmp_path):
    path = tmp_path / "manifest.jsonl"
    write_jsonl(path, [{"run_id": "one"}])
    with __import__("pytest").raises(FileExistsError):
        write_jsonl(path, [{"run_id": "two"}])


def test_validate_rejects_mojibake(tmp_path):
    record = {
        "status": "succeeded",
        "parsed_output": {
            "interpretation": {"summary": "member窶冱 response", "approach_valence": 4, "threat_valence": 4, "regulation": 4},
            "response": {"action": "Wait.", "action_category": "defer", "intensity": 3, "latency": 4},
        },
    }
    path = tmp_path / "results.jsonl"
    path.write_text(json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8")
    with __import__("pytest").raises(SystemExit, match="mojibake"):
        validate(path)


def test_blind_export_omits_condition_and_hypothesis(tmp_path):
    result = {
        "run_id": "abc", "condition_id": "T111", "stimulus_id": "DEV-RN-01", "status": "succeeded",
        "parsed_output": {"interpretation": {"summary": "An opportunity."}, "response": {"action": "Ask."}},
    }
    path = tmp_path / "results.jsonl"
    path.write_text(json.dumps(result) + "\n", encoding="utf-8")
    evaluations, key = build_blind_files(path, 1, "private")
    assert set(evaluations[0]) == {"blind_id", "experience", "interpretation", "action", "ratings"}
    assert key[0]["condition_id"] == "T111"


def test_client_uses_canonical_endpoint_and_explicit_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "diagnostic-test-key")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://example.invalid/stale-route")
    monkeypatch.setenv("OPENAI_ORG_ID", "org_stale")
    monkeypatch.setenv("OPENAI_PROJECT_ID", "proj_stale")

    client = create_openai_client()

    assert str(client.base_url) == "https://api.openai.com/v1/"
    assert client.api_key == "diagnostic-test-key"
    assert client.auth_headers == {"Authorization": "Bearer diagnostic-test-key"}
    assert client.organization is None
    assert client.project is None
    assert isinstance(client.default_headers["OpenAI-Organization"], Omit)
    assert isinstance(client.default_headers["OpenAI-Project"], Omit)
