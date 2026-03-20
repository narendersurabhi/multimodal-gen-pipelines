# Multimodal Generation Pipelines Phase 1 Ingestion and Extraction MVP

## 1. Purpose

This document implements **Phase 1: Ingestion and extraction MVP** from the implementation plan by converting the Phase 0 hand-off into concrete repository contracts. It defines the ingestion surface, job lifecycle, extraction bundle shape, storage conventions, and observability expectations required to begin building the first runnable services.

## 2. Phase 1 Objectives

Phase 1 focuses on proving that the platform can reliably accept multimodal assets and convert them into normalized extraction outputs suitable for CIR mapping in Phase 2.

### Primary objectives
- Accept text, image, and document uploads through a stable API contract.
- Persist raw assets and derived artifacts with consistent metadata and provenance.
- Run asynchronous preprocessing and extraction jobs with observable state transitions.
- Normalize document AI, OCR, and image-caption outputs into a versioned extraction bundle.
- Provide retryable failure handling and enough metadata to support later CIR mapping and indexing.

## 3. Scope

### In scope
- Upload contract for text snippets, PDFs, image files, and externally referenced assets.
- Asset metadata capture, validation, and checksum recording.
- Processing job creation and status tracking.
- Page rasterization, OCR/layout extraction, image normalization, caption generation, and text chunking.
- Versioned extraction bundle schema for pre-CIR outputs.
- Operational metadata for retries, confidence, latency, and provenance.

### Out of scope
- Embedding generation and vector indexing.
- CIR persistence beyond defining extraction-to-CIR mapping expectations.
- End-user search and grounded generation APIs.
- Production IAM policy documents or infrastructure-as-code stacks.

## 4. Delivery Artifacts Added in This Phase

Phase 1 is represented in the repository by the following artifacts:

1. `docs/api/ingestion-and-processing.openapi.yaml` — API contract for upload, job submission, job status, and artifact retrieval.
2. `docs/schemas/processing-job.schema.json` — schema for asynchronous processing job records.
3. `docs/schemas/extraction-bundle.schema.json` — schema for normalized extraction outputs before CIR mapping.
4. `docs/multimodal-generation-pipelines-phase-1-ingestion-extraction.md` — this implementation brief.

## 5. Service Design for the MVP Slice

| Service | Responsibility in Phase 1 | Inputs | Outputs |
| --- | --- | --- | --- |
| Ingestion API | Validate requests, assign asset/job IDs, persist request metadata | Uploads, metadata, external asset references | Accepted asset record, processing job record |
| Asset storage layer | Store raw files, normalized derivatives, and manifest metadata | Binary payloads, rendered pages, JSON manifests | Durable storage URIs |
| Processing orchestrator | Dispatch preprocessing and modality-specific tasks | Job records, asset references | Worker task state updates |
| Document extraction worker | OCR, layout parsing, page rendering, table/figure region extraction | PDFs, scans, rasterized pages | Document extraction fragments |
| Vision extraction worker | Image normalization, captioning, visible text extraction | Images, screenshots, rendered pages | Captions, tags, OCR text |
| Text normalization worker | Language detection, chunking, cleanup | Raw text, OCR text | Text chunks with provenance |
| Artifact API | Return job state and extraction bundle payloads | Job ID, asset ID | Job metadata and extraction bundle |

## 6. API Design

The OpenAPI contract in `docs/api/ingestion-and-processing.openapi.yaml` defines four initial endpoints.

### 6.1 `POST /v1/assets:ingest`
Creates an asset and an associated processing job.

**Supported asset modes**
- Inline text payload
- Multipart/binary upload for PDF and image assets
- External URI reference for staged ingestion

**Required behaviors**
- Enforce MIME allow-list.
- Capture `source_type`, `tenant_id`, and user-supplied metadata.
- Generate `asset_id`, `job_id`, and checksum fields.
- Return `202 Accepted` with links to the job status resource.

### 6.2 `GET /v1/jobs/{job_id}`
Returns the current processing job record, including lifecycle state, stage timings, retry counts, and failure summaries.

### 6.3 `POST /v1/jobs/{job_id}:retry`
Requeues jobs that ended in `failed` or `partial_success`, preserving an audit trail of the previous attempt.

### 6.4 `GET /v1/assets/{asset_id}/artifacts/extraction`
Returns the normalized extraction bundle for a successfully processed asset.

## 7. Processing Job Lifecycle

The processing job schema standardizes the asynchronous execution model.

### 7.1 States
- `queued`
- `running`
- `succeeded`
- `partial_success`
- `failed`
- `cancelled`

### 7.2 Stage progression
1. `ingestion_validation`
2. `normalization`
3. `document_extraction`
4. `vision_extraction`
5. `text_chunking`
6. `artifact_persistence`

Each stage captures:
- start and finish timestamps
- provider or subsystem used
- latency in milliseconds
- warnings and error codes
- retry eligibility

## 8. Extraction Bundle Contract

The extraction bundle is the Phase 1 hand-off object for Phase 2 CIR mapping.

### 8.1 Required sections
- **Asset metadata**: identifiers, MIME type, size, checksum, source channel, and storage URIs.
- **Document structure**: page manifests, OCR spans, layout blocks, detected tables, and figure regions.
- **Vision outputs**: captions, tags, visible text, and safety annotations.
- **Text chunks**: normalized chunks with offsets, language, and provenance.
- **Quality signals**: provider confidence, extraction warnings, and stage-level status.

### 8.2 Phase 2 mapping guidance
The bundle is intentionally richer than the CIR so Phase 2 can:
- collapse modality-specific details into the canonical schema,
- preserve lineage for every chunk and caption,
- backfill improved providers without re-uploading raw assets.

## 9. Storage and Naming Conventions

### 9.1 Object storage prefixes
- `raw/{tenant_id}/{asset_id}/source`
- `derived/{tenant_id}/{asset_id}/pages/{page_number}.png`
- `derived/{tenant_id}/{asset_id}/ocr/{provider}.json`
- `derived/{tenant_id}/{asset_id}/captions/{provider}.json`
- `derived/{tenant_id}/{asset_id}/extraction-bundle/v1.json`

### 9.2 Metadata keys
The metadata store should track at minimum:
- `tenant_id`
- `asset_id`
- `job_id`
- `source_type`
- `mime_type`
- `sha256`
- `ingested_at`
- `processing_state`
- `latest_attempt`
- `artifact_versions`

## 10. Operational Expectations

### 10.1 Observability
Capture the following per job:
- total end-to-end latency
- per-stage latency
- worker/provider used
- number of retries
- warning and error code counts
- extraction confidence distributions

### 10.2 Failure handling
- Validation failures should be terminal and user-correctable.
- Provider timeouts should be retryable.
- Partial results may be returned when OCR or captioning succeeds for only part of the asset.
- Jobs must preserve the last good artifact URIs even if a later retry fails.

## 11. Phase 1 Exit Checklist

Phase 1 should be considered implemented when:
- uploads create asset and processing job records through the documented API,
- multimodal assets produce extraction bundles that validate against the repository schema,
- job lifecycle states are persisted and queryable,
- failures are retryable with audit history,
- derived artifacts follow the documented storage layout,
- the repository validation checks enforce the presence of all Phase 1 contracts.

## 12. Immediate Phase 2 Hand-off

Once Phase 1 is operating, Phase 2 should start with:
1. mapping extraction bundle sections into the CIR,
2. persisting CIR documents alongside asset metadata,
3. generating embeddings for text chunks and captions,
4. indexing searchable units with metadata filters,
5. backfilling existing Phase 1 assets into the new indexing pipeline.
