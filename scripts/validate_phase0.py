#!/usr/bin/env python3
"""Lightweight repository validation for Phase 0 and Phase 1 artifacts."""

from __future__ import annotations

import json
from pathlib import Path

REQUIRED_FILES = [
    Path("docs/multimodal-generation-pipelines-phase-0-foundation.md"),
    Path("docs/multimodal-generation-pipelines-phase-1-ingestion-extraction.md"),
    Path("docs/api/ingestion-and-processing.openapi.yaml"),
    Path("docs/schemas/cir.schema.json"),
    Path("docs/schemas/grounded-summary.schema.json"),
    Path("docs/schemas/processing-job.schema.json"),
    Path("docs/schemas/extraction-bundle.schema.json"),
    Path("data/sample-corpora/README.md"),
    Path("AGENTS.md"),
]

JSON_FILES = [
    Path("docs/schemas/cir.schema.json"),
    Path("docs/schemas/grounded-summary.schema.json"),
    Path("docs/schemas/processing-job.schema.json"),
    Path("docs/schemas/extraction-bundle.schema.json"),
]

OPENAPI_REQUIRED_SNIPPETS = [
    "openapi: 3.1.0",
    "/v1/assets:ingest:",
    "/v1/jobs/{job_id}:",
    "/v1/jobs/{job_id}:retry:",
    "/v1/assets/{asset_id}/artifacts/extraction:",
]


def main() -> int:
    missing = [str(path) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        print("Missing required files:")
        for path in missing:
            print(f"- {path}")
        return 1

    for schema_path in JSON_FILES:
        with schema_path.open("r", encoding="utf-8") as handle:
            json.load(handle)
        print(f"Validated JSON: {schema_path}")

    openapi_path = Path("docs/api/ingestion-and-processing.openapi.yaml")
    openapi_text = openapi_path.read_text(encoding="utf-8")
    missing_snippets = [snippet for snippet in OPENAPI_REQUIRED_SNIPPETS if snippet not in openapi_text]
    if missing_snippets:
        print(f"OpenAPI contract is missing required snippets in {openapi_path}:")
        for snippet in missing_snippets:
            print(f"- {snippet}")
        return 1

    print(f"Validated OpenAPI contract markers: {openapi_path}")
    print("Phase 0 and Phase 1 validation checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
