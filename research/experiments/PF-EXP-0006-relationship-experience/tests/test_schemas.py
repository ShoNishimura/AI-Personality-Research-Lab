import json

from src.common import ROOT


def test_schemas_parse():
    for name in ("output.schema.json", "evaluation.schema.json", "pretest.schema.json"):
        data = json.loads((ROOT / name).read_text(encoding="utf-8"))
        assert data["additionalProperties"] is False
