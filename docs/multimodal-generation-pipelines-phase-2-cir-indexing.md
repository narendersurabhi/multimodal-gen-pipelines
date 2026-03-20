# Multimodal Generation Pipelines Phase 2 CIR and Indexing

## 1. Purpose

This document implements **Phase 2: CIR and indexing** from the implementation plan by turning the Phase 1 extraction hand-off into concrete repository contracts. It defines the finalized canonical intermediate representation (CIR), the indexing record model, embedding and filter conventions, and the operational workflow for initial indexing, re-indexing, and backfills.

## 2. Phase 2 Objectives

Phase 2 focuses on making multimodal extraction outputs durable, standardized, and searchable so downstream retrieval and generation stages can rely on a stable data layer.

### Primary objectives
- Finalize the CIR schema used as the system-of-record representation for normalized multimodal content.
- Map Phase 1 extraction bundles into CIR documents with explicit lineage to source artifacts.
- Define the searchable unit contract used by the vector index and metadata filters.
- Standardize embedding generation, indexing runs, and re-index/backfill workflows.
- Capture enough observability and quality metadata to support retrieval tuning in Phase 3.

## 3. Scope

### In scope
- CIR materialization from successful Phase 1 extraction bundles.
- Storage conventions for CIR documents and searchable index records.
- Embedding generation for text chunks, table summaries, and image captions.
- Metadata filter definitions for tenant isolation, source modality, language, and confidence thresholds.
- Indexing run lifecycle for initial ingestion, backfill, and schema/model migrations.
- Administrative API contracts for CIR creation, indexing runs, and indexed record retrieval.

### Out of scope
- End-user query and grounded answer generation APIs.
- Prompt templates, retrieval ranking logic, and reranking policies.
- Human review workflows for generated outputs.
- Production infrastructure code for vector databases or metadata stores.

## 4. Delivery Artifacts Added in This Phase

Phase 2 is represented in the repository by the following artifacts:

1. `docs/multimodal-generation-pipelines-phase-2-cir-indexing.md` — this implementation brief.
2. `docs/api/cir-and-indexing.openapi.yaml` — administrative API contract for CIR materialization, indexing runs, status, and indexed record inspection.
3. `docs/schemas/cir.schema.json` — finalized CIR schema version for normalized multimodal content.
4. `docs/schemas/index-record.schema.json` — schema for vector-searchable units derived from CIR content.
5. `docs/schemas/indexing-run.schema.json` — schema for backfill, re-index, and migration runs.

## 5. Phase 2 Architecture Slice

| Component | Responsibility in Phase 2 | Inputs | Outputs |
| --- | --- | --- | --- |
| CIR mapper | Convert extraction bundle content into normalized CIR entities | Extraction bundle, job metadata, storage URIs | CIR document |
| CIR store | Persist canonical records and support version-aware reads | CIR documents | Durable CIR URIs and metadata |
| Embedding worker | Generate vectors for searchable units | CIR chunks, captions, table summaries | Embedding references and metrics |
| Index publisher | Write searchable units into the vector index and metadata index | Index records, embedding references | Search-ready vector records |
| Indexing run orchestrator | Manage initial indexing, backfills, and re-index jobs | Asset IDs, filters, job configuration | Indexing run state and counters |
| Admin artifact API | Expose CIR records and index status for debugging and operations | Asset ID, run ID | CIR payloads, indexing run payloads, indexed records |

## 6. CIR Finalization Rules

The Phase 1 extraction bundle is intentionally verbose and provider-oriented. Phase 2 turns it into a stable system-of-record contract with the following normalization rules.

### 6.1 Mapping rules
- Preserve the original `asset_id`, `tenant_id`, MIME metadata, and checksum from ingestion.
- Map OCR/layout text and inline source text into `content.chunks` with page spans and source references.
- Convert table detections into structured `content.tables` entries plus optional table summary text for search.
- Convert figure regions and image assets into `content.figures` with optional linked captions.
- Normalize all captioning outputs into `content.captions` so image evidence can participate in retrieval.
- Record derivation links back to the extraction bundle, raw asset, and all derived artifacts.

### 6.2 CIR contract expectations
Every CIR document should:
- validate against `docs/schemas/cir.schema.json`,
- be immutable once written for a given version,
- include provenance for every searchable unit,
- identify the exact extraction bundle version used to create it,
- support downstream re-indexing without re-running extraction unless the source artifacts change.

## 7. Searchable Unit and Indexing Model

Search is performed over normalized **index records** rather than directly over the whole CIR document.

### 7.1 Searchable unit types
- `text_chunk`
- `caption`
- `table_summary`
- `figure_description`
- `page_summary`

### 7.2 Required filter dimensions
Each index record must include filterable metadata for:
- `tenant_id`
- `asset_id`
- `source_type`
- `content_type`
- `language`
- `document_type`
- `ingested_at`
- `confidence_band`
- `safety_labels`
- `schema_version`

### 7.3 Index write requirements
- Store one vector per searchable unit.
- Maintain a deterministic `record_id` so re-index operations can upsert cleanly.
- Keep the plain-text retrieval payload small enough for fast recall, while linking back to richer CIR artifacts.
- Persist keyword terms and metadata alongside vectors to support hybrid retrieval in Phase 3.

## 8. Embedding Strategy

### 8.1 MVP embedding targets
The initial indexing pass should generate embeddings for:
- normalized text chunks,
- captions derived from images or figures,
- concise table summaries generated from extracted table structure,
- optional page summaries for long documents with sparse caption coverage.

### 8.2 Provider abstraction
Embedding generation should be treated as a replaceable dependency. The indexing run metadata should record:
- embedding provider name,
- model/version,
- vector dimensionality,
- truncation strategy,
- token counts or character counts per indexed unit,
- fallback behavior when a unit cannot be embedded.

### 8.3 Failure handling
- Units that fail embedding generation should be marked with explicit failure codes.
- CIR materialization should still succeed if a subset of embeddings fail.
- The indexing run should expose success/failure counters at the unit and asset levels.
- Re-index operations should support targeting only failed or stale units.

## 9. Storage Conventions

### 9.1 Object storage prefixes
- `canonical/{tenant_id}/{asset_id}/cir/v1.1.0.json`
- `canonical/{tenant_id}/{asset_id}/index-records/{record_id}.json`
- `canonical/{tenant_id}/{asset_id}/embeddings/{record_id}.json`
- `operations/indexing-runs/{indexing_run_id}.json`

### 9.2 Metadata store keys
The metadata store should add the following Phase 2 fields:
- `cir_version`
- `cir_uri`
- `cir_materialized_at`
- `indexing_status`
- `last_indexed_at`
- `active_embedding_model`
- `active_index_namespace`
- `searchable_record_count`

## 10. Administrative API Design

The OpenAPI contract in `docs/api/cir-and-indexing.openapi.yaml` defines the minimal administrative surface required for this phase.

### 10.1 `POST /v1/assets/{asset_id}:materialize-cir`
Creates or re-creates a CIR document from the latest successful extraction bundle.

### 10.2 `GET /v1/assets/{asset_id}/cir`
Returns the current CIR document and artifact metadata for inspection and downstream service integration.

### 10.3 `POST /v1/indexing-runs`
Starts an indexing run for a specific asset set, tenant scope, or backfill filter.

### 10.4 `GET /v1/indexing-runs/{indexing_run_id}`
Returns the indexing run state, counters, model configuration, and failure summary.

### 10.5 `GET /v1/assets/{asset_id}/index-records`
Lists the normalized indexed records derived from the CIR for debugging and retrieval inspection.

## 11. Operational Expectations

### 11.1 Observability
Capture the following metrics for every indexing run:
- CIR materialization success rate,
- embedding latency per content type,
- indexing throughput by asset and searchable unit,
- percentage of units skipped for low confidence or policy reasons,
- total searchable record count by tenant and modality,
- stale-record count after schema or model updates.

### 11.2 Quality controls
- Do not publish index records with missing lineage back to the CIR.
- Reject records whose filter metadata is incomplete for tenant isolation.
- Bucket confidence into `high`, `medium`, or `low` bands for retrieval gating.
- Preserve the previous active index namespace until a backfill or migration completes.

## 12. Phase 2 Exit Checklist

Phase 2 should be considered implemented when:
- every successful Phase 1 asset can be materialized into a valid CIR document,
- index records validate against the repository schema and include deterministic IDs,
- embedding metadata is captured for every searchable unit or explicit failure state,
- indexing runs support initial indexing, backfill, and re-index modes,
- searchable records can be enumerated per asset for operational inspection,
- repository validation checks enforce the presence of all Phase 2 contracts.

## 13. Immediate Phase 3 Hand-off

Once Phase 2 is operating, Phase 3 should start with:
1. building the query and retrieval API over the indexed records,
2. adding hybrid search, reranking, and retrieval quality evaluation,
3. assembling prompts from retrieved multimodal evidence,
4. generating grounded summaries and structured outputs with citations,
5. monitoring retrieval hit quality before broadening generation use cases.
