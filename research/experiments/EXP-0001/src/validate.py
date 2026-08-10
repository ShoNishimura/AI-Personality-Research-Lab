from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]


def validate(path: Path) -> int:
    schema = json.loads((ROOT / "output.schema.json").read_text(encoding="utf-8"))
    counts: Counter[str] = Counter()
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            record = json.loads(line)
            counts[record.get("status", "unknown")] += 1
            if record.get("status") == "succeeded":
                try:
                    jsonschema.validate(record["parsed_output"], schema)
                except jsonschema.ValidationError as exc:
                    raise SystemExit(f"line {line_number}: {exc.message}") from exc
    print(json.dumps(counts, sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate EXP-0001 JSONL results.")
    parser.add_argument("path", type=Path, nargs="?", default=ROOT / "runs/pilot/results.jsonl")
    return validate(parser.parse_args().path)


if __name__ == "__main__":
    raise SystemExit(main())

