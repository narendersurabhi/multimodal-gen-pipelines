# Phase 0 Sample Corpora Inventory

This inventory defines the **seed evaluation corpus** for the multimodal generation MVP. The repository does not store production data; instead, this file tracks the shape, provenance, and evaluation intent of the sample assets that should be assembled for Phase 0.

## 1. Dataset Goals

The sample corpus should be sufficient to validate:
- ingestion of text, documents, and images
- OCR and layout extraction quality
- caption quality on screenshots, charts, and diagrams
- CIR schema completeness
- retrieval quality for grounded summarization and QA

## 2. Target Asset Mix

| Asset group | Count | Purpose | Notes |
| --- | --- | --- | --- |
| Text-first reports | 5 | Baseline chunking, retrieval, and summarization | Clean digital text, minimal OCR needs |
| Scanned PDFs | 5 | OCR robustness and layout fidelity | Include skew, low contrast, and mixed scan quality |
| Image-heavy documents | 5 | Figure/table/caption workflows | Use charts, screenshots, diagrams, and callouts |
| Standalone images | 10 | Image captioning and image-linked retrieval | Include screenshots, product/scene images, and diagrams |
| Evaluation prompt set | 15 | Summarization, extraction, and grounded QA | Maintain gold references where possible |

## 3. Metadata To Track For Each Asset

Record the following fields in the private source-of-truth dataset sheet or manifest used by the team:
- asset identifier
- asset type
- title or short description
- source or provenance
- licensing and reuse status
- redaction/privacy status
- expected extraction challenges
- target workflow coverage
- gold reference outputs, if available

## 4. Suggested Evaluation Prompt Coverage

### Summarization prompts
- Summarize the operational risks in a document with embedded charts.
- Produce action items from a scanned report and supporting screenshots.
- Generate an executive brief across mixed document sections and extracted figure captions.

### Extraction prompts
- Extract named entities and compliance-relevant fields from scanned forms.
- Convert a document table into canonical structured records.
- Normalize screenshot captions and visual tags into CIR-compatible fields.

### Retrieval prompts
- Answer a text question using evidence from both OCR text and figure captions.
- Retrieve the most relevant document sections for an image-derived query.
- Compare findings across a text report and a standalone diagram.

## 5. Acceptance Requirements

The sample corpus is ready for Phase 1 once:
- all target asset groups are represented
- provenance and redaction status are tracked for every item
- at least one gold reference exists for each workflow type
- prompt/evaluation coverage spans text, document, and image inputs
