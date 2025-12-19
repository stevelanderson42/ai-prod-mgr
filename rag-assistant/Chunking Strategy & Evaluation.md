# Chunking Strategy & Evaluation v0.1

## Purpose

This document defines the **chunking strategies** used in the RAG Assistant and explains **why** they were selected, **what risks they mitigate**, and **how their effectiveness will be evaluated**.

Chunking is treated as an **index-time design decision** that directly impacts retrieval precision, recall, traceability, and downstream hallucination risk.

---

## Relationship to Failure Modes

This document operationalizes mitigation strategies for the following failure classes:

- Semantic fragmentation
- Chunk boundary violations
- Table fragmentation
- Context underfill
- Retrieval overload

(See: `rag-assistant/failure_modes_checklist_latest.md`)

---

## Design Principles

- Chunking is **content-aware**, not one-size-fits-all
- Chunk boundaries must preserve **regulatory meaning**
- Retrieval must favor **precision over recall** in compliance contexts
- Chunking decisions must be **evaluatable and auditable**

---

## Document Classes & Chunking Approach

This section defines how different document types are chunked, indexed, and evaluated.
Chunking strategies are selected based on content structure, regulatory risk, and retrieval behavior.

| Document Type | Examples | Chunking Strategy | Rationale |
|--------------|----------|-------------------|-----------|
| Policies | Compliance manuals, regulatory guidance | Semantic + section-aware | Preserve rule boundaries |
| Procedures | SOPs, operational playbooks | Recursive + overlap | Preserve step sequences |
| Tables | Limits, thresholds, matrices | Atomic chunks | Prevent semantic corruption |
| FAQs | Interpretive guidance | Fixed-size semantic | Optimize retrieval precision |
| Code / Logic | Pseudocode, rules engines | Recursive | Preserve logic blocks |

---

### Tables (High-Risk, Atomic Content)

#### Why Tables Are High-Risk in Regulated RAG

Tables in compliance and financial documents often encode **binding rules**, not reference data. Common examples include:

- Thresholds (limits, caps, eligibility cutoffs)
- Rate matrices (fees, interest rates, penalties)
- Conditional logic expressed across rows and columns
- Exceptions and footnotes with regulatory impact

Naive chunking that splits tables across chunks or linearizes them improperly leads to **semantic corruption**, where individual values lose their governing context. In regulated environments, this creates **material compliance risk**, not merely degraded answer quality.

---

#### Failure Modes Addressed

This strategy directly mitigates the following failure modes identified in the RAG Failure Modes Checklist:

- Table fragmentation
- Semantic fragmentation
- Chunk boundary violations
- Context underfill
- Citation hallucination

---

#### Chunking Strategy for Tables

**Primary Rule:**  
Tables are treated as **atomic semantic units** and must never be split across chunks.

##### Approach

- Detect tables during document ingestion (PDF parsing, HTML structure analysis, markdown detection).
- Extract each table as a **single chunk**, regardless of token length (within operational limits).
- Preserve:
  - Row and column structure
  - Column headers
  - Footnotes and inline annotations
- Attach surrounding context as **metadata**, not inline prose.

---

#### Example Metadata for Table Chunks

```json
{
  "content_type": "table",
  "doc_id": "POLICY-CC-001",
  "version": "2025-08-01",
  "section": "4.2.3",
  "table_title": "Credit Limit Thresholds",
  "applies_to": "Retail Brokerage Accounts",
  "effective_date": "2025-08-01"
}


---

### Policies & Regulatory Text

(TBD – semantic + section-aware chunking)

---

### Procedures & Playbooks

(TBD – recursive chunking with overlap)

---

### FAQs & Interpretive Guidance

(TBD – fixed-size semantic chunking)

---

### Code, Rules & Logic

(TBD – recursive chunking preserving logical blocks)

## Chunk Size & Overlap Guidelines

| Parameter | Guideline | Rationale |
|---------|----------|-----------|
| Target chunk size | TBD (e.g., 300–600 tokens) | Balance precision vs context |
| Overlap | TBD (e.g., 10–20%) | Prevent rule fragmentation |
| Max chunk size | TBD | Avoid retrieval overload |

(Exact values validated through evaluation — see below)

---

## Index-Time Safeguards

- Sentence-aware splitting
- Section/header preservation
- Table detection and isolation
- Metadata enrichment (document ID, version, section)

---

## Evaluation Strategy

### Retrieval Quality Metrics
- Top-k recall
- Precision@k
- Fragmentation rate (answers spanning >1 chunk)
- Context sufficiency score

### Generation Risk Indicators
- Citation coverage
- Hallucination rate
- NOT_IN_DOCUMENT fallback frequency

---

## Validation Approach

- Golden set of compliance queries
- Synthetic queries derived from real usage
- Regression testing on chunking changes
- Manual spot audits for high-risk queries

---

## Known Tradeoffs & Open Questions

- Recall vs precision tension
- Performance impact of overlap
- Handling multi-table documents
- Long-tail document formats

---

## Future Enhancements

- Adaptive chunk sizing
- Graph-based retrieval augmentation
- Document-type–specific retrievers

---

## References

- Databricks — *The Ultimate Guide to Chunking Strategies for RAG Applications*
- Internal failure mode analysis