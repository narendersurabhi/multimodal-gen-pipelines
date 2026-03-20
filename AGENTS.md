# Repository Agent Notes

## Purpose
This repository stores architecture and supporting documentation for multimodal generation pipelines that combine text, image, and document AI workflows.

## Current Status
- Added an architecture document at `docs/multimodal-generation-pipelines-architecture.md`.
- Added an implementation plan at `docs/multimodal-generation-pipelines-implementation-plan.md`.
- Added a Phase 0 foundation brief at `docs/multimodal-generation-pipelines-phase-0-foundation.md` with prioritized MVP workflows, baseline service decisions, repository standards, and an exit checklist.
- Added versioned schema contracts under `docs/schemas/` for the canonical intermediate representation and grounded summary outputs.
- Added a sample corpus inventory at `data/sample-corpora/README.md` to define the MVP evaluation dataset shape and coverage.
- Added a lightweight validation script and GitHub Actions workflow for Phase 0 repository checks.
- Added a recruiter-friendly `README.md` for fast repository scanning and portfolio review.
- The repository currently focuses on system design documentation plus early implementation-governance artifacts rather than executable product code.

## Change Log
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
