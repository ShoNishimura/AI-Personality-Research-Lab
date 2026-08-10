from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]

AXIS_TEXT = {
    "surgency": {
        "high": "Novelty, possible reward, and opportunities for engagement readily attract attention and energize approach.",
        "low": "Novelty and possible reward exert a quieter pull, so engagement is less readily energized without situational reasons.",
    },
    "negative_affectivity": {
        "high": "Possible threat, rejection, loss, and failure readily attract attention and carry emotional weight.",
        "low": "Possible threat, rejection, loss, and failure exert a quieter pull unless the situation supplies strong evidence.",
    },
    "effortful_control": {
        "high": "Attention is readily maintained or shifted, and an initially dominant response is readily paused and adjusted.",
        "low": "Attention and an initially dominant response are less readily paused, shifted, or deliberately adjusted.",
    },
}


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def render_prompts(condition: dict[str, str], stimulus: dict[str, str]) -> tuple[str, str]:
    system = (ROOT / "prompts/system.md").read_text(encoding="utf-8")
    temperament = (ROOT / "prompts/temperament.md").read_text(encoding="utf-8").format(
        **condition,
        surgency_text=AXIS_TEXT["surgency"][condition["surgency"]],
        negative_affectivity_text=AXIS_TEXT["negative_affectivity"][condition["negative_affectivity"]],
        effortful_control_text=AXIS_TEXT["effortful_control"][condition["effortful_control"]],
    )
    task = (ROOT / "prompts/task.md").read_text(encoding="utf-8").format(stimulus=stimulus["text"])
    return system, temperament + "\n\n" + task


def build_manifest(config: dict[str, Any]) -> list[dict[str, Any]]:
    conditions = load_yaml(ROOT / "conditions.yaml")["conditions"]
    stimuli = [
        item for item in load_yaml(ROOT / "stimuli.yaml")["stimuli"]
        if item["split"] == config["stimulus_split"]
    ]
    rows: list[dict[str, Any]] = []
    for replicate in range(1, int(config["replicates"]) + 1):
        for condition in conditions:
            for stimulus in stimuli:
                system, user = render_prompts(condition, stimulus)
                identity = {
                    "condition_id": condition["id"],
                    "stimulus_id": stimulus["id"],
                    "replicate_id": f"R{replicate:03d}",
                }
                rows.append({
                    "run_id": sha256_text(canonical_json(identity))[:16],
                    **identity,
                    "event_type": stimulus["event_type"],
                    "prompt_sha256": sha256_text(system + "\n" + user),
                    "stimulus_sha256": sha256_text(stimulus["text"]),
                })
    random.Random(int(config["randomization_seed"])).shuffle(rows)
    max_runs = config.get("max_runs")
    return rows[: int(max_runs)] if max_runs is not None else rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(canonical_json(row) + "\n")


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(canonical_json(row) + "\n")
        handle.flush()


def completed_run_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    completed = set()
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            if record.get("status") == "succeeded":
                completed.add(record["run_id"])
    return completed


def usage_dict(response: Any) -> dict[str, Any]:
    usage = getattr(response, "usage", None)
    if usage is None:
        return {}
    return usage.model_dump(mode="json") if hasattr(usage, "model_dump") else dict(usage)


def execute_run(client: Any, config: dict[str, Any], row: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    conditions = {item["id"]: item for item in load_yaml(ROOT / "conditions.yaml")["conditions"]}
    stimuli = {item["id"]: item for item in load_yaml(ROOT / "stimuli.yaml")["stimuli"]}
    system, user = render_prompts(conditions[row["condition_id"]], stimuli[row["stimulus_id"]])
    started = datetime.now(UTC).isoformat()
    response = client.responses.create(
        model=config["model"],
        instructions=system,
        input=user,
        max_output_tokens=int(config["max_output_tokens"]),
        store=False,
        text={"format": {"type": "json_schema", "name": "aprl_exp_0001_output", "strict": True, "schema": schema}},
    )
    raw_text = response.output_text
    parsed = json.loads(raw_text)
    jsonschema.validate(parsed, schema)
    return {
        **row,
        "status": "succeeded",
        "started_at": started,
        "completed_at": datetime.now(UTC).isoformat(),
        "model_requested": config["model"],
        "model_returned": getattr(response, "model", None),
        "response_id": getattr(response, "id", None),
        "store": False,
        "raw_output": raw_text,
        "parsed_output": parsed,
        "usage": usage_dict(response),
    }


def run(config_path: Path, dry_run: bool) -> int:
    config = load_yaml(config_path)
    manifest = build_manifest(config)
    manifest_path = ROOT / config["manifest_path"]
    results_path = ROOT / config["results_path"]
    write_jsonl(manifest_path, manifest)
    print(f"manifest: {manifest_path} ({len(manifest)} runs)")
    if dry_run:
        print("dry-run: no API requests sent")
        return 0

    from openai import OpenAI, OpenAIError

    schema = json.loads((ROOT / config["output_schema"]).read_text(encoding="utf-8"))
    client = OpenAI()
    technical_errors = (OpenAIError, json.JSONDecodeError, jsonschema.ValidationError, ValueError)
    completed = completed_run_ids(results_path)
    failures = 0
    for index, row in enumerate(manifest, start=1):
        if row["run_id"] in completed:
            print(f"[{index}/{len(manifest)}] skip {row['run_id']}")
            continue
        for attempt in range(int(config["max_retries"]) + 1):
            try:
                record = execute_run(client, config, row, schema)
                record["attempt"] = attempt + 1
                append_jsonl(results_path, record)
                print(f"[{index}/{len(manifest)}] ok {row['run_id']}")
                break
            except technical_errors as exc:  # preserve every technical failure before retrying
                append_jsonl(results_path, {
                    **row,
                    "status": "failed",
                    "attempt": attempt + 1,
                    "failed_at": datetime.now(UTC).isoformat(),
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                })
                if attempt >= int(config["max_retries"]):
                    failures += 1
                    print(f"[{index}/{len(manifest)}] failed {row['run_id']}: {type(exc).__name__}", file=sys.stderr)
                else:
                    time.sleep(1)
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the EXP-0001 pilot.")
    parser.add_argument("--config", type=Path, default=ROOT / "experiment.yaml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.config.resolve(), args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
