import json

import jsonschema

from src.common import ROOT


def test_schemas_are_valid_draft_2020_12() -> None:
    for name in ("output.schema.json", "evaluation.schema.json", "pretest.schema.json"):
        schema = json.loads((ROOT / name).read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
