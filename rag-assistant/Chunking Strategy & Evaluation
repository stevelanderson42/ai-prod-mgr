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
| Overl
