from __future__ import annotations

import json
from pathlib import Path

import pytest

from src import analyze
from src.blind import build_blind_files
from src.common import ROOT, load_yaml, sha256_normalized_text_file, write_jsonl
from src.pilot import build_manifest, create_openai_client
from src.validate import validate_static


def test_static_validation_passes():
    config = load_yaml(ROOT / "experiment.yaml")
    assert validate_static(config) == []


def test_manifest_is_balanced_and_stable():
    config = load_yaml(ROOT / "experiment.yaml")
    first = build_manifest(config)
    second = build_manifest(config)
    assert first == second
    assert len(first) == 96
    assert len({row["run_id"] for row in first}) == 96


def test_generation_schema_contains_only_interpretation():
    schema = json.loads((ROOT / "output.schema.json").read_text(encoding="utf-8"))
    assert set(schema["properties"]) == {"interpretation"}
    assert schema["required"] == ["interpretation"]
    assert schema["additionalProperties"] is False


def test_threshold_hash_is_platform_newline_independent(tmp_path):
    lf_path = tmp_path / "lf.yaml"
    crlf_path = tmp_path / "crlf.yaml"
    content = "gates:\n  G1:\n    threshold: 0.75\n"
    lf_path.write_bytes(content.encode("utf-8"))
    crlf_path.write_bytes(content.replace("\n", "\r\n").encode("utf-8"))
    assert sha256_normalized_text_file(lf_path) == sha256_normalized_text_file(crlf_path)


def test_client_ignores_stale_sdk_routing(monkeypatch):
    openai = pytest.importorskip("openai")
    if not hasattr(openai, "OpenAI"):
        pytest.skip("OpenAI SDK not installed in this local validation environment")
    monkeypatch.setenv("OPENAI_API_KEY", "diagnostic-test-key")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://example.invalid/stale-route")
    monkeypatch.setenv("OPENAI_ORG_ID", "org_stale")
    monkeypatch.setenv("OPENAI_PROJECT_ID", "proj_stale")
    client = create_openai_client()
    assert str(client.base_url) == "https://api.openai.com/v1/"
    assert client.api_key == "diagnostic-test-key"
    assert client.organization is None
    assert client.project is None


def test_blind_export_hides_condition_stimulus_and_hypothesis(tmp_path, monkeypatch):
    config = load_yaml(ROOT / "experiment.yaml").copy()
    manifest = build_manifest(config)
    results = [{**row, "status": "succeeded", "parsed_output": {"interpretation": "example"}} for row in manifest]

    results_path = tmp_path / "results.jsonl"
    manifest_path = tmp_path / "manifest.jsonl"
    blind_path = tmp_path / "blind.jsonl"
    key_path = tmp_path / "key.jsonl"
    write_jsonl(results_path, results)
    write_jsonl(manifest_path, manifest)
    config.update(
        {
            "results_path": str(results_path),
            "manifest_path": str(manifest_path),
            "blind_set_path": str(blind_path),
            "blind_key_path": str(key_path),
        }
    )
    monkeypatch.setattr("src.blind.ROOT", Path("/"))
    blind_rows, key_rows = build_blind_files(config)
    assert len(blind_rows) == 96
    assert set(blind_rows[0]) == {"blind_id", "interpretation"}
    assert "condition_id" in key_rows[0]
    assert "stimulus_id" in key_rows[0]
    assert "stimulus_class" in key_rows[0]


def test_gate_analysis_on_clear_synthetic_pattern(tmp_path, monkeypatch):
    config = load_yaml(ROOT / "experiment.yaml").copy()
    manifest = build_manifest(config)
    key_rows = []
    eval_rows = []
    for i, row in enumerate(manifest):
        blind_id = f"b{i:03d}"
        key_rows.append(
            {
                "blind_id": blind_id,
                **{
                    k: row[k]
                    for k in ("run_id", "condition_id", "stimulus_id", "stimulus_class", "replicate_id")
                },
            }
        )
        s_high = row["condition_id"][1] == "1"
        n_high = row["condition_id"][2] == "1"
        if row["stimulus_class"] == "seeking-target":
            seek, neg = (3 if s_high else 1), 1
        elif row["stimulus_class"] == "negative-target":
            seek, neg = 1, (3 if n_high else 1)
        elif row["stimulus_class"] == "conflict":
            seek, neg = (3 if s_high else 1), (3 if n_high else 1)
        else:
            seek, neg = 1, 1
        eval_rows.append(
            {
                "blind_id": blind_id,
                "status": "succeeded",
                "scores": {"seeking_activation": seek, "negative_activation": neg},
            }
        )

    key_path = tmp_path / "key.jsonl"
    eval_path = tmp_path / "eval.jsonl"
    thresholds_path = ROOT / "thresholds.yaml"
    write_jsonl(key_path, key_rows)
    write_jsonl(eval_path, eval_rows)
    config.update(
        {
            "blind_key_path": str(key_path),
            "evaluation_results_path": str(eval_path),
            "thresholds": str(thresholds_path),
        }
    )
    monkeypatch.setattr(analyze, "ROOT", Path("/"))
    result = analyze.analyze(config)
    assert result["all_gates_pass"] is True
