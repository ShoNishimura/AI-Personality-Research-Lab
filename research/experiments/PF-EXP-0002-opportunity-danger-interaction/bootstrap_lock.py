from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "PF-EXP-0001-temperament-interpretation" / "uv.lock"
TARGET = ROOT / "uv.lock"

OLD = 'name = "aprl-exp-0001"'
NEW = 'name = "aprl-exp-0002"'


def main() -> int:
    if not SOURCE.exists():
        raise FileNotFoundError(f"source lockfile not found: {SOURCE}")
    content = SOURCE.read_text(encoding="utf-8")
    count = content.count(OLD)
    if count != 1:
        raise ValueError(f"expected exactly one {OLD!r} in source lockfile; got {count}")
    TARGET.write_text(content.replace(OLD, NEW), encoding="utf-8", newline="\n")
    print(f"bootstrapped: {TARGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
