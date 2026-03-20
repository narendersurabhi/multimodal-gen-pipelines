#!/usr/bin/env python3
"""Lightweight repository validation for Phase 0 artifacts."""

from __future__ import annotations

import json
from pathlib import Path

REQUIRED_FILES = [
    Path("docs/multimodal-generation-pipelines-phase-0-foundation.md"),
    Path("docs/schemas/cir.schema.json"),
    Path("docs/schemas/grounded-summary.schema.json"),
    Path("data/sample-corpora/README.md"),
    Path("AGENTS.md"),
]


def main() -> int:
    missing = [str(path) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        print("Missing required files:")
        for path in missing:
            print(f"- {path}")
        return 1

    for schema_path in [Path("docs/schemas/cir.schema.json"), Path("docs/schemas/grounded-summary.schema.json")]:
        with schema_path.open("r", encoding="utf-8") as handle:
            json.load(handle)
        print(f"Validated JSON: {schema_path}")

    print("Phase 0 validation checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
