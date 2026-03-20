# Multimodal Generation Pipelines Phase 3 Retrieval-Grounded Generation MVP

## 1. Purpose

This document implements **Phase 3: Retrieval-grounded generation MVP** from the implementation plan by converting the Phase 2 indexing hand-off into concrete repository contracts. It defines the retrieval and summarization API surface, request and evidence-pack contracts, grounding and citation rules, generation guardrails, and evaluation expectations needed to deliver the first user-facing multimodal generation workflow.

## 2. Phase 3 Objectives

Phase 3 focuses on turning indexed multimodal content into trustworthy, structured outputs that are explicitly grounded in retrieved evidence.

### Primary objectives
- Expose a stable query API for retrieval-backed summarization and question answering over mixed-media assets.
- Define the request contract for user intent, retrieval scope, output schema, and response controls.
- Standardize evidence packaging so prompts receive normalized chunks, captions, table summaries, and figure descriptions with lineage.
- Produce structured grounded summaries with citations, confidence metadata, and schema validation.
- Add basic hallucination and policy checks before returning generated outputs.

## 3. Scope

### In scope
- Query API for grounded summary requests and retrieval inspection.
- Request schema for retrieval options, answer constraints, and desired response format.
- Evidence-pack schema for normalized retrieval results sent to the prompt builder and returned for debugging.
- Prompt-assembly guidance combining intent, retrieved evidence, and output schema requirements.
- Structured generation output conventions using grounded citations and confidence metadata.
- Basic post-generation checks for unsupported claims, schema compliance, and low-evidence responses.

### Out of scope
- Advanced reranking or learning-to-rank training loops.
- Human review tooling and case-management workflows.
- Multi-turn chat memory and agentic planning across repeated requests.
- End-user front-end interfaces for search or summary authoring.
- Production deployment code for model gateways or prompt registries.

## 4. Delivery Artifacts Added in This Phase

Phase 3 is represented in the repository by the following artifacts:

1. `docs/multimodal-generation-pipelines-phase-3-retrieval-grounded-generation.md` — this implementation brief.
2. `docs/api/retrieval-and-generation.openapi.yaml` — API contract for retrieval-backed summary creation, request status, and evidence inspection.
3. `docs/schemas/retrieval-request.schema.json` — schema for grounded generation requests and retrieval controls.
4. `docs/schemas/retrieval-evidence-pack.schema.json` — schema for the normalized evidence package used by the prompt builder and returned for inspection.
5. `docs/schemas/grounded-summary.schema.json` — updated authoritative schema for retrieval-grounded multimodal outputs.

## 5. Phase 3 Architecture Slice

| Component | Responsibility in Phase 3 | Inputs | Outputs |
| --- | --- | --- | --- |
| Query API | Accept end-user summary/query requests and validate scope | Retrieval request payload, tenant context | Accepted summary request |
| Retrieval orchestrator | Execute hybrid retrieval and apply filters/thresholds | Request intent, asset scope, index records | Ranked evidence candidates |
| Evidence pack builder | Normalize retrieved units into prompt-ready evidence | Ranked candidates, CIR lookups | Evidence pack |
| Prompt builder | Compose model instructions, grounding rules, and output schema | User query, evidence pack, schema config | Prompt payload |
| Generation worker | Produce structured grounded output | Prompt payload, model configuration | Grounded summary draft |
| Validation/guardrail stage | Enforce schema, citation, and unsupported-claim checks | Summary draft, evidence pack | Accepted output or flagged response |
| Summary artifact API | Expose status, output payload, and retrieval evidence | Summary request ID | Summary envelope and evidence pack |

## 6. Retrieval and Prompt Assembly Contract

### 6.1 Retrieval request inputs
Every generation request should specify:
- `tenant_id` and caller context for isolation.
- either explicit `asset_ids` or a retrieval filter scope.
- the user `query` or summary objective.
- `task_type` such as `grounded_summary`, `question_answering`, or `risk_brief`.
- the desired output schema version and optional field preferences.
- retrieval controls including `top_k`, modality preferences, and minimum confidence bands.

### 6.2 Evidence-pack normalization rules
The evidence pack should:
- include the original `record_id` and `asset_id` for every retrieved unit,
- preserve the `content_type`, page/region locator, and lineage back to the CIR,
- store a concise `evidence_text` or caption excerpt that can be placed directly into prompts,
- capture retrieval scores and rerank scores separately when both exist,
- keep enough metadata for downstream citation rendering without another lookup in the happy path.

### 6.3 Prompt construction rules
The prompt builder should:
- instruct the model to answer only from retrieved evidence,
- include the exact output schema constraints,
- require citation IDs for each key factual claim,
- preserve the user's framing while preventing unsupported extrapolation,
- fall back to abstention language when retrieved evidence is insufficient.

## 7. Grounding and Citation Requirements

### 7.1 Citation rules
Generated outputs must:
- reference one or more citation IDs for each material claim,
- map citation IDs to asset IDs plus human-readable locators,
- distinguish evidence types such as `chunk`, `table`, `figure`, `caption`, and `page_summary`,
- avoid using citations from filtered-out or policy-blocked evidence,
- support deterministic rendering into downstream reports or UI components.

### 7.2 Unsupported-claim checks
Before returning a response:
- verify all cited IDs exist in the evidence pack,
- reject outputs that mention uncited numeric facts, dates, or named entities when the task requires strict grounding,
- downgrade confidence when evidence coverage is sparse or contradictory,
- return a structured warning when the model abstains or partially answers.

## 8. API Design

The OpenAPI contract in `docs/api/retrieval-and-generation.openapi.yaml` defines the minimal user-facing API surface required for this phase.

### 8.1 `POST /v1/grounded-summaries`
Creates a retrieval-grounded generation request and returns a summary request ID.

### 8.2 `GET /v1/grounded-summaries/{summary_request_id}`
Returns request status, the grounded summary output when available, and validation warnings.

### 8.3 `GET /v1/grounded-summaries/{summary_request_id}/evidence`
Returns the normalized evidence pack used to ground the request for debugging, evaluation, and audit purposes.

## 9. Operational Expectations

### 9.1 Observability
Capture at minimum:
- request volume by `task_type`, tenant, and model version,
- retrieval latency and generation latency,
- evidence count and modality distribution per request,
- schema pass/fail rate,
- abstention rate and unsupported-claim rejection rate,
- average citations per answer and low-evidence warning frequency.

### 9.2 Guardrails
- Enforce tenant isolation before retrieval executes.
- Support policy labels from Phase 2 filtering so unsafe records do not enter prompts.
- Limit evidence-pack size to bounded token budgets.
- Return a structured partial response when retrieval succeeds but generation validation fails.
- Preserve prompt, model, and retrieval config versions in request metadata for replayability.

## 10. Evaluation Expectations

### 10.1 Offline evaluation
For the sample corpus, Phase 3 should measure:
- evidence recall for known-answer prompts,
- citation precision for generated claims,
- summary schema pass rate,
- abstention correctness when evidence is missing,
- qualitative grounding quality across text-only, document-heavy, and image-heavy assets.

### 10.2 Manual review guidance
Reviewers should inspect:
- whether summaries faithfully reflect cited evidence,
- whether key claims can be traced to specific pages, chunks, or captions,
- whether confidence and warnings align with evidence quality,
- whether the model refrains from speculation when retrieval is weak.

## 11. Phase 3 Exit Checklist

Phase 3 should be considered implemented when:
- grounded summary requests can be submitted through the documented API,
- retrieval requests validate against the repository schema and enforce tenant-aware scope,
- evidence packs validate against the repository schema and preserve CIR lineage,
- grounded outputs validate against the repository summary schema,
- generated outputs include citations and confidence metadata,
- validation checks enforce the presence of all Phase 3 contracts.

## 12. Immediate Phase 4 Hand-off

Once Phase 3 is operating, Phase 4 should start with:
1. adding dashboards and alerts for retrieval and generation quality,
2. introducing prompt versioning and fallback model routing controls,
3. routing low-confidence or policy-sensitive outputs into review workflows,
4. expanding audit logging and redaction controls,
5. load-testing retrieval and generation paths under pilot traffic expectations.
