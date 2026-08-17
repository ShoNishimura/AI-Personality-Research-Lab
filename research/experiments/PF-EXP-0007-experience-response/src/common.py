from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
from datetime import UTC, datetime
from importlib import metadata as importlib_metadata
from pathlib import Path
from typing import Any

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
DESIGN_FILES = (
    "experiment.yaml",
    "stimuli.yaml",
    "thresholds.yaml",
    "output.schema.json",
    "evaluation.schema.json",
    "pretest.schema.json",
    "pyproject.toml",
    "prompts/system.md",
    "prompts/task.md",
    "prompts/evaluator-system.md",
    "prompts/evaluator-task.md",
    "prompts/pretest-system.md",
    "prompts/pretest-task.md",
    "src/__init__.py",
    "src/common.py",
    "src/pretest.py",
    "src/pretest_analyze.py",
    "src/pilot.py",
    "src/blind.py",
    "src/evaluate.py",
    "src/analyze.py",
    "src/validate.py",
)


class ResponseOutputError(ValueError):
    def __init__(self, message: str, *, error_type: str, metadata: dict[str, Any]):
        super().__init__(message)
        self.error_type = error_type
        self.metadata = metadata


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"expected mapping in {path}")
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_normalized_text_file(path: Path) -> str:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return sha256_text(text)


def design_hashes() -> dict[str, str]:
    return {rel: sha256_normalized_text_file(ROOT / rel) for rel in DESIGN_FILES}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]], *, refuse_change: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    proposed = "".join(canonical_json(row) + "\n" for row in rows)
    if path.exists() and refuse_change:
        if path.read_text(encoding="utf-8") != proposed:
            raise FileExistsError(f"refusing to overwrite a different frozen file: {path}")
        return
    path.write_text(proposed, encoding="utf-8", newline="\n")


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(canonical_json(row) + "\n")
        handle.flush()


def completed_ids(path: Path, id_key: str) -> set[str]:
    return {str(r[id_key]) for r in read_jsonl(path) if r.get("status") == "succeeded" and id_key in r}


def usage_dict(response: Any) -> dict[str, Any]:
    usage = getattr(response, "usage", None)
    if usage is None:
        return {}
    return usage.model_dump(mode="json") if hasattr(usage, "model_dump") else dict(usage)


def response_metadata(response: Any) -> dict[str, Any]:
    incomplete = getattr(response, "incomplete_details", None)
    return {
        "response_status": getattr(response, "status", None),
        "incomplete_reason": getattr(incomplete, "reason", None) if incomplete else None,
        "model_returned": getattr(response, "model", None),
        "response_id": getattr(response, "id", None),
        "x_request_id": getattr(response, "_request_id", None),
        "http_status": 200,
        "usage": usage_dict(response),
    }


def parse_structured_response(response: Any, schema: dict[str, Any]) -> dict[str, Any]:
    metadata = response_metadata(response)
    raw = getattr(response, "output_text", "") or ""
    metadata["output_text_length"] = len(raw)
    if metadata["response_status"] != "completed":
        raise ResponseOutputError("response not completed", error_type="IncompleteResponse", metadata=metadata)
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ResponseOutputError(str(exc), error_type="JSONDecodeError", metadata=metadata) from exc
    try:
        jsonschema.validate(parsed, schema)
    except jsonschema.ValidationError as exc:
        raise ResponseOutputError(exc.message, error_type="SchemaValidationError", metadata=metadata) from exc
    return parsed


def create_openai_client() -> Any:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"], base_url="https://api.openai.com/v1")
    client.organization = None
    client.project = None
    return client


def design() -> dict[str, Any]:
    return load_yaml(ROOT / "stimuli.yaml")


def stimuli_for_split(split: str) -> list[dict[str, Any]]:
    return [row for row in design()["stimuli"] if row["split"] == split]


def experience_by_id(exp_id: str) -> dict[str, Any]:
    entries = design()["experiences"]
    if exp_id not in entries:
        raise ValueError(f"unknown Experience condition: {exp_id}")
    return {"id": exp_id, **entries[exp_id]}


def experience_ids() -> tuple[str, str]:
    return ("E-B", "E-A")


def render_generation_prompts(stimulus: dict[str, Any], exp_id: str) -> tuple[str, str]:
    system = (ROOT / "prompts/system.md").read_text(encoding="utf-8")
    user = (ROOT / "prompts/task.md").read_text(encoding="utf-8").format(
        situation=stimulus["situation"],
        experience=experience_by_id(exp_id)["packet"],
    )
    return system, user


def render_evaluator_prompts(row: dict[str, Any]) -> tuple[str, str]:
    system = (ROOT / "prompts/evaluator-system.md").read_text(encoding="utf-8")
    user = (ROOT / "prompts/evaluator-task.md").read_text(encoding="utf-8").format(
        situation=row["situation"], action=row["action"]
    )
    return system, user


def runtime_environment() -> dict[str, Any]:
    versions: dict[str, str | None] = {}
    for package in ("openai", "jsonschema", "PyYAML"):
        try:
            versions[package] = importlib_metadata.version(package)
        except importlib_metadata.PackageNotFoundError:
            versions[package] = None
    return {
        "python": sys.version,
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "packages": versions,
        "design_hashes": design_hashes(),
    }


def write_runtime_environment(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(runtime_environment(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def assert_pretest_execution_design(config: dict[str, Any]) -> None:
    path = ROOT / config["pretest_environment_path"]
    if not path.exists():
        raise RuntimeError("pretest environment snapshot not found; rerun pretest before analysis")
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    expected = snapshot.get("design_hashes")
    current = design_hashes()
    if expected != current:
        raise RuntimeError("design hashes changed after pretest execution; refusing pretest analysis")


def assert_frozen_design(config: dict[str, Any]) -> None:
    path = ROOT / config["pretest_analysis_path"]
    if not path.exists():
        raise RuntimeError("pretest analysis not found; run pretest and pretest_analyze first")
    result = json.loads(path.read_text(encoding="utf-8"))
    if config.get("require_pretest_pass", False) and not result.get("all_gates_pass"):
        raise RuntimeError("pretest did not pass; downstream execution is prohibited")
    expected = result.get("design_hashes")
    current = design_hashes()
    if expected != current:
        raise RuntimeError("design hashes changed after pretest; refusing downstream execution")


def make_api_failure(exc: Exception, row: dict[str, Any], config: dict[str, Any], attempt: int) -> dict[str, Any]:
    failure: dict[str, Any] = {
        **row,
        "experiment_phase": config["phase"],
        "status": "failed",
        "attempt": attempt,
        "failed_at": datetime.now(UTC).isoformat(),
        "error_type": exc.error_type if isinstance(exc, ResponseOutputError) else type(exc).__name__,
        "error": str(exc),
    }
    if isinstance(exc, ResponseOutputError):
        failure.update(exc.metadata)
    try:
        from openai import APIStatusError
        if isinstance(exc, APIStatusError):
            body = exc.body if isinstance(exc.body, dict) else {}
            detail = body.get("error", body) if isinstance(body, dict) else {}
            failure.update({
                "http_status": exc.status_code,
                "api_error_type": detail.get("type") if isinstance(detail, dict) else None,
                "api_error_code": detail.get("code") if isinstance(detail, dict) else None,
                "x_request_id": exc.response.headers.get("x-request-id") if exc.response is not None else None,
            })
    except ImportError:
        pass
    return failure
