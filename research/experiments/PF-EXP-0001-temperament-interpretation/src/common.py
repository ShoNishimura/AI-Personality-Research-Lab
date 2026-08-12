from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]

AXIS_TEXT = {
    "seeking": {
        "high": "比較的活性化しやすい。",
        "low": "比較的活性化しにくい。",
    },
    "negative_affectivity": {
        "high": "比較的活性化しやすい。",
        "low": "比較的活性化しにくい。",
    },
}


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]], *, refuse_change: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    proposed = "".join(canonical_json(row) + "\n" for row in rows)
    if path.exists() and refuse_change:
        existing = path.read_text(encoding="utf-8")
        if existing != proposed:
            raise FileExistsError(f"refusing to overwrite a different frozen file: {path}")
        return
    path.write_text(proposed, encoding="utf-8", newline="\n")


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(canonical_json(row) + "\n")
        handle.flush()


def completed_ids(path: Path, id_key: str) -> set[str]:
    return {
        str(row[id_key])
        for row in read_jsonl(path)
        if row.get("status") == "succeeded" and id_key in row
    }


def render_generation_prompts(condition: dict[str, str], stimulus: dict[str, str]) -> tuple[str, str]:
    system = (ROOT / "prompts/system.md").read_text(encoding="utf-8")
    temperament = (ROOT / "prompts/temperament.md").read_text(encoding="utf-8").format(
        seeking_text=AXIS_TEXT["seeking"][condition["seeking"]],
        negative_text=AXIS_TEXT["negative_affectivity"][condition["negative_affectivity"]],
    )
    task = (ROOT / "prompts/task.md").read_text(encoding="utf-8").format(stimulus=stimulus["text"])
    return system, temperament + "\n\n" + task


def render_evaluator_prompts(interpretation: str) -> tuple[str, str]:
    system = (ROOT / "prompts/evaluator-system.md").read_text(encoding="utf-8")
    task = (ROOT / "prompts/evaluator-task.md").read_text(encoding="utf-8").format(
        interpretation=interpretation
    )
    return system, task
