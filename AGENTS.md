# Repository Agent Notes

## Purpose
This repository stores architecture and supporting documentation for multimodal generation pipelines that combine text, image, and document AI workflows.

## Current Status
- Added an architecture document at `docs/multimodal-generation-pipelines-architecture.md`.
- Added an implementation plan at `docs/multimodal-generation-pipelines-implementation-plan.md`.
- Added a Phase 0 foundation brief at `docs/multimodal-generation-pipelines-phase-0-foundation.md` with prioritized MVP workflows, baseline service decisions, repository standards, and an exit checklist.
- Added a Phase 1 ingestion and extraction implementation brief at `docs/multimodal-generation-pipelines-phase-1-ingestion-extraction.md` covering API scope, job lifecycle, extraction outputs, storage conventions, and Phase 2 hand-off expectations.
- Added a Phase 2 CIR and indexing implementation brief at `docs/multimodal-generation-pipelines-phase-2-cir-indexing.md` covering CIR materialization, searchable units, embeddings, indexing runs, and Phase 3 hand-off expectations.
- Added versioned schema contracts under `docs/schemas/` for the canonical intermediate representation, grounded summary outputs, processing jobs, extraction bundles, index records, indexing runs, retrieval requests, and retrieval evidence packs.
- Added OpenAPI contracts at `docs/api/ingestion-and-processing.openapi.yaml`, `docs/api/cir-and-indexing.openapi.yaml`, and `docs/api/retrieval-and-generation.openapi.yaml` for upload, retry, extraction artifacts, CIR materialization, indexing runs, grounded summary creation, and evidence inspection.
- Added a sample corpus inventory at `data/sample-corpora/README.md` to define the MVP evaluation dataset shape and coverage.
- Expanded the lightweight validation script and GitHub Actions workflow to cover Phase 0 through Phase 3 repository checks.
- Added a recruiter-friendly `README.md` for fast repository scanning and portfolio review.
- Added a Phase 3 retrieval-grounded generation brief at `docs/multimodal-generation-pipelines-phase-3-retrieval-grounded-generation.md` covering query APIs, evidence packs, grounded summaries, citations, and guardrails.
- Added a Phase 4 quality, controls, and operations implementation brief at `docs/multimodal-generation-pipelines-phase-4-quality-controls-operations.md` covering dashboards, prompt/model controls, review workflows, audit logging, redaction, and pilot SLO guidance.
- Added versioned operational control schemas under `docs/schemas/` for prompt versions, model routing policies, review queue items, and audit events.
- Added an operations control-plane OpenAPI contract at `docs/api/quality-and-operations.openapi.yaml` for prompt activation, routing policy management, review decisions, and audit-event search.
- Expanded the lightweight validation script and repository overview to cover Phase 0 through Phase 4 repository checks and discovery.
- The repository now includes implementation-ready contracts for ingestion, CIR materialization, indexing, grounded generation, and operational hardening, while still primarily focusing on system design documentation and delivery governance artifacts.

## Change Log
### 2026-03-20
- Added `docs/multimodal-generation-pipelines-phase-4-quality-controls-operations.md` to implement the next roadmap phase with concrete observability, prompt/routing governance, review, and audit-control guidance.
- Added `docs/api/quality-and-operations.openapi.yaml` to define Phase 4 administrative endpoints for prompt versions, model routing policies, review queue operations, and audit-event access.
- Added `docs/schemas/prompt-version.schema.json`, `docs/schemas/model-routing-policy.schema.json`, `docs/schemas/review-queue-item.schema.json`, and `docs/schemas/audit-event.schema.json` to version control-plane and review-workflow contracts.
- Updated `scripts/validate_phase0.py` and `README.md` so repository validation and discovery now cover the new Phase 4 artifacts.

### 2026-03-20
- Added `docs/multimodal-generation-pipelines-phase-3-retrieval-grounded-generation.md` to implement the next roadmap phase with concrete retrieval orchestration, evidence-pack, grounding, and citation guidance.
- Added `docs/api/retrieval-and-generation.openapi.yaml` to define Phase 3 user-facing endpoints for grounded summary creation, status retrieval, and evidence inspection.
- Added `docs/schemas/retrieval-request.schema.json` and `docs/schemas/retrieval-evidence-pack.schema.json` to version grounded-generation request and prompt-evidence interfaces.
- Updated `docs/schemas/grounded-summary.schema.json` to capture Phase 3 status, grounding confidence, evidence stats, and richer citations.
- Updated `scripts/validate_phase0.py`, `.github/workflows/phase0-validation.yml`, and `README.md` so repository validation and discovery now cover the new Phase 3 artifacts.

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
