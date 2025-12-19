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

| Document Type | Examples | Chunking Strategy | Rationale |
|--------------|----------|-------------------|-----------|
| Policies | Compliance manuals, regulatory guidance | Semantic + section-aware | Preserve rule boundaries |
| Procedures | SOPs, operational playbooks | Recursive + overlap | Preserve step sequences |
| Tables | Limits, thresholds, matrices | Atomic chunks | Prevent semantic corruption |
| FAQs | Interpretive guidance | Fixed-size semantic | Optimize retrieval precision |
| Code / Logic | Pseudocode, rules engines | Recursive | Preserve logic blocks |

---

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