from __future__ import annotations

import json
from pathlib import Path

from src import analyze, pretest_analyze
from src.blind import build_blind_files
from src.common import ROOT, load_yaml, write_jsonl
from src.pilot import build_manifest
from src.pretest import build_pretest_manifest
from src.validate import validate_static


def test_static_validation_passes():
    config = load_yaml(ROOT / "experiment.yaml")
    assert validate_static(config) == []


def test_manifests_are_balanced():
    config = load_yaml(ROOT / "experiment.yaml")
    pretest = build_pretest_manifest(config)
    main = build_manifest(config)
    assert len(pretest) == 24
    assert len({row["pretest_id"] for row in pretest}) == 24
    assert len(main) == 192
    assert len({row["run_id"] for row in main}) == 192

    conditions = {cid: 0 for cid in ("T00", "T01", "T10", "T11")}
    stimuli = {}
    for row in main:
        conditions[row["condition_id"]] += 1
        stimuli[row["stimulus_id"]] = stimuli.get(row["stimulus_id"], 0) + 1
    assert set(conditions.values()) == {48}
    assert set(stimuli.values()) == {8}


def test_generation_schema_contains_only_interpretation():
    schema = json.loads((ROOT / "output.schema.json").read_text(encoding="utf-8"))
    assert set(schema["properties"]) == {"interpretation"}
    assert schema["required"] == ["interpretation"]
    assert schema["additionalProperties"] is False


def test_evaluation_schema_contains_four_axes():
    schema = json.loads((ROOT / "evaluation.schema.json").read_text(encoding="utf-8"))
    assert set(schema["properties"]) == {
        "opportunity_salience",
        "danger_salience",
        "seeking_activation",
        "negative_activation",
    }


def test_blind_export_hides_design_metadata(tmp_path, monkeypatch):
    config = load_yaml(ROOT / "experiment.yaml").copy()
    manifest = build_manifest(config)
    results = [
        {**row, "status": "succeeded", "parsed_output": {"interpretation": "example"}}
        for row in manifest
    ]

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
    assert len(blind_rows) == 192
    assert set(blind_rows[0]) == {"blind_id", "interpretation"}
    assert "condition_id" in key_rows[0]
    assert "opportunity" in key_rows[0]
    assert "danger" in key_rows[0]


def test_pretest_analysis_on_clear_minimal_pairs(tmp_path, monkeypatch):
    config = load_yaml(ROOT / "experiment.yaml").copy()
    manifest = build_pretest_manifest(config)
    results = []
    for row in manifest:
        results.append(
            {
                **row,
                "status": "succeeded",
                "scores": {
                    "opportunity_value": 3 if row["opportunity"] == "high" else 1,
                    "danger_value": 3 if row["danger"] == "high" else 1,
                },
            }
        )

    manifest_path = tmp_path / "pre-manifest.jsonl"
    results_path = tmp_path / "pre-results.jsonl"
    thresholds_path = ROOT / "thresholds.yaml"
    write_jsonl(manifest_path, manifest)
    write_jsonl(results_path, results)
    config.update(
        {
            "pretest_manifest_path": str(manifest_path),
            "pretest_results_path": str(results_path),
            "thresholds": str(thresholds_path),
        }
    )
    monkeypatch.setattr(pretest_analyze, "ROOT", Path("/"))
    result = pretest_analyze.analyze(config)
    assert result["all_gates_pass"] is True
    assert result["effects"]["opportunity_main"] == 2
    assert result["effects"]["danger_main"] == 2


def test_main_analysis_detects_target_interaction(tmp_path, monkeypatch):
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
                    key: row[key]
                    for key in (
                        "run_id",
                        "condition_id",
                        "stimulus_id",
                        "family_id",
                        "opportunity",
                        "danger",
                        "replicate_id",
                    )
                },
            }
        )
        s_high = row["condition_id"][1] == "1"
        n_high = row["condition_id"][2] == "1"
        opp_high = row["opportunity"] == "high"
        danger_high = row["danger"] == "high"

        opportunity_salience = 3 if opp_high else 1
        danger_salience = 3 if danger_high else 0
        seeking_activation = (3 if s_high else 1) if opp_high else 0
        negative_activation = (3 if n_high else 1) if danger_high else 0

        if danger_high and n_high and s_high and opp_high:
            danger_salience = 2

        eval_rows.append(
            {
                "blind_id": blind_id,
                "status": "succeeded",
                "scores": {
                    "opportunity_salience": opportunity_salience,
                    "danger_salience": danger_salience,
                    "seeking_activation": seeking_activation,
                    "negative_activation": negative_activation,
                },
            }
        )

    key_path = tmp_path / "key.jsonl"
    eval_path = tmp_path / "eval.jsonl"
    pretest_path = tmp_path / "pretest.json"
    thresholds_path = ROOT / "thresholds.yaml"
    write_jsonl(key_path, key_rows)
    write_jsonl(eval_path, eval_rows)
    pretest_path.write_text('{"all_gates_pass": true}\n', encoding="utf-8")
    config.update(
        {
            "blind_key_path": str(key_path),
            "evaluation_results_path": str(eval_path),
            "pretest_analysis_path": str(pretest_path),
            "thresholds": str(thresholds_path),
        }
    )
    monkeypatch.setattr(analyze, "ROOT", Path("/"))
    result = analyze.analyze(config)
    assert result["all_gates_pass"] is True
    assert result["effects"]["primary_interaction"] == -1
    assert all(value == -1 for value in result["family_interactions"].values())
