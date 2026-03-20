# Multimodal Generation Pipelines Phase 0 Foundation

## 1. Purpose

This document turns **Phase 0: Discovery and foundation** from the implementation plan into concrete repository artifacts. It defines the first business workflows, sample datasets, initial contracts, baseline service choices, and repository standards needed to begin implementation with a clear MVP boundary.

## 2. Priority MVP Workflows

Phase 0 narrows the initial scope to three workflows that exercise all major modalities while remaining deliverable in an MVP.

### Workflow 1: Analyst-ready document summary
**Input**
- PDF reports
- scanned PDF pages
- embedded screenshots and charts

**System behavior**
- Extract text, layout, tables, and figures from the document.
- Caption image-heavy regions and screenshots.
- Retrieve the most relevant sections for the user's task.
- Generate a grounded executive summary with citations and structured risk/action-item fields.

**Primary value**
- Reduces manual review time for operations, risk, and research teams.

**Success metrics**
- Time to first usable summary under 5 minutes for a 25-page document.
- At least 90% JSON schema validity for the summary output.
- Human review acceptance at or above 80% on the initial evaluation set.

### Workflow 2: Multimodal asset extraction to canonical records
**Input**
- standalone images
- scanned forms
- short text context provided by a user or upstream system

**System behavior**
- Normalize the assets.
- Run OCR and captioning.
- Convert extraction results into a versioned CIR document.
- Persist the CIR record together with provenance, quality scores, and storage references.

**Primary value**
- Creates reusable structured records for retrieval, downstream analytics, and later generation steps.

**Success metrics**
- 99% CIR schema validation on processed sample assets.
- Provenance captured for every chunk, table, and caption.
- Extraction job status observable end to end.

### Workflow 3: Cross-modal retrieval-backed question answering
**Input**
- text question from a user
- previously ingested documents and images

**System behavior**
- Retrieve text chunks, table fragments, and image captions from the indexed corpus.
- Assemble evidence with metadata filters.
- Return a grounded answer with citations and confidence metadata.

**Primary value**
- Demonstrates retrieval quality before more advanced generation workflows are added.

**Success metrics**
- Evidence attached to every answer.
- Median retrieval latency under 2 seconds for the MVP corpus.
- Top-k relevance judged acceptable in at least 75% of evaluation prompts.

## 3. Baseline Service Boundaries

The initial delivery should use clear service boundaries that can later be split or scaled independently.

| Service | Initial responsibility | Notes |
| --- | --- | --- |
| Ingestion API | Accept uploads, assign IDs, validate input, persist metadata | Synchronous request entry point |
| Processing worker | Preprocess assets and trigger modality-specific extraction | Async, queue-driven |
| Document AI adapter | OCR, layout, tables, and page-level figures | Provider-abstracted interface |
| Vision adapter | Image normalization, captioning, and safety labels | Provider-abstracted interface |
| CIR mapper | Transform extraction outputs into the canonical schema | Versioned contract boundary |
| Indexing service | Generate embeddings and publish searchable records | Supports re-index and backfill |
| Retrieval API | Hybrid retrieval and metadata filtering | Shared by QA and summarization |
| Generation orchestrator | Build prompts, invoke model tiers, validate structured output | Adds citations and confidence fields |

## 4. Initial Managed Service Decisions

These choices are intended to accelerate the MVP while keeping the architecture provider-neutral.

### 4.1 Cloud and runtime
- **Primary cloud**: AWS
- **Core compute approach**: managed container runtime for APIs and workers
- **Async orchestration**: queue plus workflow/state-machine pattern for long-running extraction and generation jobs

### 4.2 Storage
- **Raw and derived asset storage**: S3-style object storage
- **Metadata and lineage store**: DynamoDB-style key-value/document store for request and asset tracking
- **Search index**: vector database with metadata filtering and hybrid retrieval support

### 4.3 Model categories
- **OCR/layout baseline**: managed document AI provider with page, table, and layout extraction
- **Captioning baseline**: hosted vision-language model capable of concise image descriptions
- **Embedding baseline**: text embedding model shared across chunks and captions for the MVP
- **Summarization baseline**: instruction-following LLM with structured JSON output support

### 4.4 Decision criteria
- Minimal operational burden during MVP.
- Strong API support for asynchronous document workloads.
- Schema-constrained generation support.
- Exportable metadata and confidence signals.
- Ability to swap providers behind adapters in later phases.

## 5. Phase 0 Data Contracts

Phase 0 establishes two foundational contracts in this repository:

1. `docs/schemas/cir.schema.json` for the canonical intermediate representation.
2. `docs/schemas/grounded-summary.schema.json` for retrieval-grounded summary output.

These contracts should be treated as versioned platform interfaces. Extraction, retrieval, generation, and evaluation changes should align to them unless a new schema version is explicitly introduced.

## 6. Sample Dataset Definition

The MVP evaluation corpus is intentionally small but modality-diverse.

### 6.1 Corpus composition
- 5 text-first reports or briefs
- 5 scanned PDF documents with OCR challenges
- 5 image-heavy documents containing charts, screenshots, or diagrams
- 10 standalone images with short human-authored reference descriptions
- 15 retrieval/evaluation prompts spanning summarization, extraction, and grounded QA

### 6.2 Dataset requirements
- Include representative noisy scans and clean digital PDFs.
- Include examples with tables, figures, and mixed page layouts.
- Record licensing, provenance, and redaction status for every item.
- Store a gold reference summary or answer for evaluation prompts where possible.

### 6.3 Repository artifact
The concrete dataset inventory for Phase 0 lives in `data/sample-corpora/README.md` and should be updated whenever seed assets or evaluation prompts change.

## 7. Repository Standards and CI Checks

### 7.1 Repository standards
- Keep architecture, implementation, and planning artifacts under `docs/` unless implementation code requires another location.
- Version schemas in-place and document breaking changes in `AGENTS.md`.
- Keep sample datasets documented with provenance and evaluation intent.
- Prefer small validation scripts that run without external dependencies.

### 7.2 Initial CI checks
Phase 0 adds lightweight validation focused on documentation-first assets.
- Validate JSON schemas parse correctly.
- Verify required Phase 0 artifacts are present.
- Fail fast when repository contracts are accidentally removed.

## 8. Phase 0 Exit Checklist

The repository should consider Phase 0 complete when all items below are true:
- MVP workflows are documented and approved.
- Sample dataset inventory exists and includes evaluation intent.
- CIR and grounded summary schemas are defined.
- Baseline service boundaries and managed-service choices are documented.
- CI validates the repository's documentation-first contracts.

## 9. Immediate Phase 1 Hand-off

Once Phase 0 is approved, implementation should begin with:
1. Upload and job submission API design.
2. Object storage and metadata model setup.
3. OCR/layout and image captioning adapters.
4. CIR serialization from extraction outputs.
5. Initial indexing pipeline for chunks and captions.
