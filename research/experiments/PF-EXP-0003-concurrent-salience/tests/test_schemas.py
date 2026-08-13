import json

from src.common import ROOT


def test_all_schemas_are_strict_objects():
    for name in ("output.schema.json", "evaluation.schema.json", "pretest.schema.json"):
        schema = json.loads((ROOT / name).read_text(encoding="utf-8"))
        assert schema["type"] == "object"
        assert schema["additionalProperties"] is False
