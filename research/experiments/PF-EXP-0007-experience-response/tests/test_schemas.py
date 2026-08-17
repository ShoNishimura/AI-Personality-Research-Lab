import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_json_schemas_parse():
    for name in ("output.schema.json", "evaluation.schema.json", "pretest.schema.json"):
        assert isinstance(json.loads((ROOT / name).read_text(encoding="utf-8")), dict)
