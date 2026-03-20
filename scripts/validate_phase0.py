#!/usr/bin/env python3
"""Lightweight repository validation for Phase 0 through Phase 3 artifacts."""

from __future__ import annotations

import json
from pathlib import Path

REQUIRED_FILES = [
    Path("docs/multimodal-generation-pipelines-phase-0-foundation.md"),
    Path("docs/multimodal-generation-pipelines-phase-1-ingestion-extraction.md"),
    Path("docs/multimodal-generation-pipelines-phase-2-cir-indexing.md"),
    Path("docs/multimodal-generation-pipelines-phase-3-retrieval-grounded-generation.md"),
    Path("docs/api/ingestion-and-processing.openapi.yaml"),
    Path("docs/api/cir-and-indexing.openapi.yaml"),
    Path("docs/api/retrieval-and-generation.openapi.yaml"),
    Path("docs/schemas/cir.schema.json"),
    Path("docs/schemas/grounded-summary.schema.json"),
    Path("docs/schemas/processing-job.schema.json"),
    Path("docs/schemas/extraction-bundle.schema.json"),
    Path("docs/schemas/index-record.schema.json"),
    Path("docs/schemas/indexing-run.schema.json"),
    Path("docs/schemas/retrieval-request.schema.json"),
    Path("docs/schemas/retrieval-evidence-pack.schema.json"),
    Path("data/sample-corpora/README.md"),
    Path("AGENTS.md"),
]

JSON_FILES = [
    Path("docs/schemas/cir.schema.json"),
    Path("docs/schemas/grounded-summary.schema.json"),
    Path("docs/schemas/processing-job.schema.json"),
    Path("docs/schemas/extraction-bundle.schema.json"),
    Path("docs/schemas/index-record.schema.json"),
    Path("docs/schemas/indexing-run.schema.json"),
    Path("docs/schemas/retrieval-request.schema.json"),
    Path("docs/schemas/retrieval-evidence-pack.schema.json"),
]

OPENAPI_MARKERS = {
    Path("docs/api/ingestion-and-processing.openapi.yaml"): [
        "openapi: 3.1.0",
        "/v1/assets:ingest:",
        "/v1/jobs/{job_id}:",
        "/v1/jobs/{job_id}:retry:",
        "/v1/assets/{asset_id}/artifacts/extraction:",
    ],
    Path("docs/api/cir-and-indexing.openapi.yaml"): [
        "openapi: 3.1.0",
        "/v1/assets/{asset_id}:materialize-cir:",
        "/v1/assets/{asset_id}/cir:",
        "/v1/indexing-runs:",
        "/v1/indexing-runs/{indexing_run_id}:",
        "/v1/assets/{asset_id}/index-records:",
    ],
    Path("docs/api/retrieval-and-generation.openapi.yaml"): [
        "openapi: 3.1.0",
        "/v1/grounded-summaries:",
        "/v1/grounded-summaries/{summary_request_id}:",
        "/v1/grounded-summaries/{summary_request_id}/evidence:",
    ],
}


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

    for openapi_path, markers in OPENAPI_MARKERS.items():
        openapi_text = openapi_path.read_text(encoding="utf-8")
        missing_markers = [marker for marker in markers if marker not in openapi_text]
        if missing_markers:
            print(f"OpenAPI contract is missing required markers in {openapi_path}:")
            for marker in missing_markers:
                print(f"- {marker}")
            return 1
        print(f"Validated OpenAPI contract markers: {openapi_path}")

    print("Phase 0 through Phase 3 validation checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
