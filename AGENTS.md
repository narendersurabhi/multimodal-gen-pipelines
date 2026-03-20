# Repository Agent Notes

## Purpose
This repository stores architecture and supporting documentation for multimodal generation pipelines that combine text, image, and document AI workflows.

## Current Status
- Added an architecture document at `docs/multimodal-generation-pipelines-architecture.md`.
- Added an implementation plan at `docs/multimodal-generation-pipelines-implementation-plan.md`.
- Added a Phase 0 foundation brief at `docs/multimodal-generation-pipelines-phase-0-foundation.md` with prioritized MVP workflows, baseline service decisions, repository standards, and an exit checklist.
- Added a Phase 1 ingestion and extraction implementation brief at `docs/multimodal-generation-pipelines-phase-1-ingestion-extraction.md` covering API scope, job lifecycle, extraction outputs, storage conventions, and Phase 2 hand-off expectations.
- Added a Phase 2 CIR and indexing implementation brief at `docs/multimodal-generation-pipelines-phase-2-cir-indexing.md` covering CIR materialization, searchable units, embeddings, indexing runs, and Phase 3 hand-off expectations.
- Added versioned schema contracts under `docs/schemas/` for the canonical intermediate representation, grounded summary outputs, processing jobs, extraction bundles, index records, and indexing runs.
- Added OpenAPI contracts at `docs/api/ingestion-and-processing.openapi.yaml` and `docs/api/cir-and-indexing.openapi.yaml` for upload, retry, extraction artifacts, CIR materialization, indexing runs, and indexed record inspection.
- Added a sample corpus inventory at `data/sample-corpora/README.md` to define the MVP evaluation dataset shape and coverage.
- Expanded the lightweight validation script and GitHub Actions workflow to cover Phase 0, Phase 1, and Phase 2 repository checks.
- Added a recruiter-friendly `README.md` for fast repository scanning and portfolio review.
- The repository now includes implementation-ready contracts for ingestion, CIR materialization, and indexing, while still primarily focusing on system design documentation and delivery governance artifacts.

## Change Log
### 2026-03-20
- Added `docs/multimodal-generation-pipelines-phase-2-cir-indexing.md` to implement the next roadmap phase with concrete CIR mapping, searchable-unit, embedding, and re-index guidance.
- Added `docs/api/cir-and-indexing.openapi.yaml` to define Phase 2 administrative endpoints for CIR materialization, indexing runs, status, and indexed record inspection.
- Added `docs/schemas/index-record.schema.json` and `docs/schemas/indexing-run.schema.json` to version searchable retrieval records and indexing/backfill job interfaces.
- Updated `docs/schemas/cir.schema.json` to finalize the CIR as a Phase 2 system-of-record contract with lineage and artifact references.
- Updated `scripts/validate_phase0.py` and `README.md` so repository validation and discovery now cover the new Phase 2 artifacts.

### 2026-03-20
- Added `docs/multimodal-generation-pipelines-phase-1-ingestion-extraction.md` to implement the next roadmap phase with concrete ingestion, processing, storage, and observability guidance.
- Added `docs/api/ingestion-and-processing.openapi.yaml` to define the MVP ingestion API, job status, retry, and extraction artifact contracts.
- Added `docs/schemas/processing-job.schema.json` and `docs/schemas/extraction-bundle.schema.json` to version the asynchronous job record and pre-CIR extraction bundle interfaces.
- Updated `scripts/validate_phase0.py` and `.github/workflows/phase0-validation.yml` so repository validation now enforces the new Phase 1 artifacts as well.
- Updated `README.md` so the new Phase 1 implementation assets are discoverable from the repository overview.

### 2026-03-20
- Added `docs/multimodal-generation-pipelines-phase-0-foundation.md` to operationalize Phase 0 with concrete MVP workflows, success metrics, service boundaries, managed-service decisions, repository standards, and a hand-off checklist.
- Added `docs/schemas/cir.schema.json` and `docs/schemas/grounded-summary.schema.json` to version the initial CIR and grounded summary contracts for downstream implementation.
- Added `data/sample-corpora/README.md` to define the initial sample dataset mix, metadata expectations, and evaluation prompt coverage.
- Added `scripts/validate_phase0.py` and `.github/workflows/phase0-validation.yml` for lightweight JSON and artifact presence checks.
- Updated `README.md` so the new Phase 0 artifacts are discoverable from the repository overview.

### 2026-03-20
- Created `README.md` with a recruiter-friendly overview covering project value, architecture highlights, implementation highlights, demonstrated skills, and a recommended reading order.
- Created `docs/multimodal-generation-pipelines-implementation-plan.md` with phased delivery guidance covering MVP scope, workstreams, roadmap phases, milestones, team responsibilities, risks, and success metrics.
- Created `docs/multimodal-generation-pipelines-architecture.md` with a reference architecture covering ingestion, preprocessing, document AI, vision processing, canonical intermediate representation, embeddings, retrieval, orchestration, model serving, validation, deployment, security, and tradeoff analysis.
- Initialized this root `AGENTS.md` file to track repository changes and provide future agents with project context.

## Guidance For Future Agents
- Read this file before making changes.
- Keep the **Current Status** and **Change Log** sections up to date whenever you modify the repository.
- Prefer adding new architecture or design artifacts under `docs/` unless the user requests a different structure.
