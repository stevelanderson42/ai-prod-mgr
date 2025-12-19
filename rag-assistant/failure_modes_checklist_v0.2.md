# RAG Failure Modes Checklist v0.2

## Purpose

This document is a **pre-build checklist of failure modes** to explicitly design against when constructing a **Compliance Retrieval Assistant** using Retrieval-Augmented Generation (RAG).

It consolidates known failure patterns observed in production RAG systems — with particular emphasis on **regulated environments** (e.g., Financial Services), where correctness, traceability, and auditability matter more than raw fluency.

**Key insight:**  
Up to 70% of RAG systems fail in production. In regulated environments, the most damaging failures are not model hallucinations alone, but **retrieval and traceability failures** — often introduced upstream through poor document segmentation and chunking decisions.

---

## Retrieval Failures

### Content Selection Problems

- [ ] **Wrong chunk retrieved**  
  Semantically similar but factually incorrect content is returned.

- [ ] **Chunk boundary violations**  
  A complete answer spans multiple chunks due to improper segmentation, resulting in incomplete or misleading retrieval.

- [ ] **Retrieval decay**  
  The system performs well with a small corpus but degrades as content grows (needle-in-a-haystack problem).

- [ ] **Retrieval overload**  
  Too many documents or chunks are retrieved, introducing noise that confuses generation.

- [ ] **Missing document**  
  A required policy, procedure, or authoritative document is not present in the corpus.

- [ ] **Cross-document contradictions**  
  Retrieved documents conflict with one another and no resolution or prioritization mechanism exists.

---

### Chunking & Segmentation Failures (Retrieval-Critical)

Chunking is an **index-time design decision** that directly determines retrieval quality. Poor chunking silently propagates downstream failures that appear to be “model issues” but are actually data pipeline defects.

- [ ] **Semantic fragmentation**  
  A single policy rule or regulatory concept is split across multiple chunks, preventing complete retrieval.

- [ ] **Overly coarse chunks**  
  Chunks are too large, causing retrieval to return excessive irrelevant context that dilutes signal.

- [ ] **Overly fine chunks**  
  Chunks are too small to preserve meaning, forcing multi-hop synthesis the model cannot reliably perform.

- [ ] **Boundary violations**  
  Chunking cuts through sentences, numbered rules, clauses, or exception blocks.

- [ ] **Section / header detachment**  
  Headings are separated from the content they govern, breaking interpretability and legal meaning.

- [ ] **Table fragmentation**  
  Tables are split across chunks, destroying row/column semantics and regulatory intent.

- [ ] **Mixed-content chunking**  
  Prose, tables, and code are chunked uniformly despite different structural requirements.

- [ ] **Context window underfill**  
  Retrieved chunks lack sufficient surrounding context to answer compliance-grade questions.

- [ ] **Inconsistent chunking strategy**  
  Different chunking approaches are applied across document sources, degrading retrieval consistency.

---

### Staleness & Drift Problems

- [ ] **Stale index**  
  Source documents change but embeddings are not refreshed.

- [ ] **Knowledge drift**  
  Information was accurate at indexing time, but regulations or business rules have changed.

- [ ] **Temporal staleness without detection**  
  The system confidently returns outdated information with no uncertainty signal.

- [ ] **Embedding drift**  
  Embedding models are updated without re-indexing documents, degrading retrieval quality.

---

### Technical / Architecture Problems

- [ ] **Retrieval timing attacks**  
  Asynchronous retrieval completes after generation timeout; the model responds without context.

- [ ] **Context position bias**  
  The model disproportionately weights content appearing early or late in the context window.

- [ ] **Retrieval–generation model mismatch**  
  Tokenization or representation differences between embedding and generation models cause subtle failures.

- [ ] **Recursive retrieval loops**  
  Iterative retrieval repeatedly fetches the same content without progress.

---

## Generation Failures

### Hallucination & Accuracy

- [ ] **Hallucination despite retrieval**  
  The model ignores retrieved content and generates from training data.

- [ ] **Citation hallucination**  
  The model cites documents but attributes claims to incorrect sources.

- [ ] **Overconfident tone**  
  Uncertain or partial answers are presented with inappropriate certainty.

- [ ] **Incomplete synthesis**  
  The model uses one retrieved chunk while ignoring others that contain required context.

---

### Reasoning Failures

- [ ] **Multi-hop reasoning failure**  
  All required facts are retrieved, but the model fails to connect them correctly.

- [ ] **Irrelevant chunk overload**  
  Excess context overwhelms the model, leading to incorrect synthesis or hallucination.

---

## Governance & Compliance Failures

### Auditability Problems

- [ ] **No citations provided**  
  Answers are generated without links to source documents.

- [ ] **Unverifiable outputs**  
  There is no internal proof of which documents or versions were used.

- [ ] **Audit / dispute blind spots**  
  The system’s behavior cannot be reconstructed months later.

- [ ] **No audit trail**  
  Retrieved chunks and model decisions are not logged.

- [ ] **Unclear source of truth**  
  Document authority, version, or timestamp is missing.

---

### Regulatory & Access Problems

- [ ] **Regulatory mismatch**  
  Guidance is retrieved from the wrong regulatory regime or time period.

- [ ] **Access control violations**  
  The RAG pipeline ignores RBAC and exposes restricted content.

- [ ] **Data freshness gaps**  
  Document updates occur faster than index refresh cycles.

---

### Enterprise Data Problems

- [ ] **Unstructured data handling failures**  
  PDFs with tables, images, or multi-column layouts are parsed incorrectly.

- [ ] **Decentralized data gaps**  
  Knowledge is spread across SharePoint, Confluence, Slack, etc., with partial coverage.

- [ ] **Format diversity blind spots**  
  The pipeline handles clean text but misses spreadsheets, slides, diagrams, or code blocks.

---

## Evaluation & Monitoring Failures

- [ ] **The evaluation gap**  
  No feedback loop exists; quality degradation is unnoticed until user trust collapses.

- [ ] **Flying blind on quality**  
  Retrieval relevance and answer correctness are not systematically measured.

- [ ] **No baseline metrics**  
  Performance degradation cannot be detected due to lack of initial benchmarks.

---

## Mitigations I’ll Use in My Build

| Failure Category | Failure Mode | Mitigation Strategy |
|-----------------|--------------|---------------------|
| Retrieval | Wrong chunk | Top-k tuning, relevance thresholds, hybrid search |
| Retrieval | Semantic fragmentation | Semantic or recursive chunking aligned to document structure |
| Retrieval | Boundary violations | Sentence-aware and section-aware chunking |
| Retrieval | Table fragmentation | Preserve tables as atomic chunks or structured embeddings |
| Retrieval | Mixed-content chunking | Hybrid chunking (prose, tables, code) |
| Retrieval | Stale index | Document versioning, freshness metadata, scheduled re-indexing |
| Retrieval | Retrieval overload | Adaptive context sizing based on query intent |
| Generation | Hallucination | Strict grounding rules, citation requirements, NOT_IN_DOCUMENT fallback |
| Generation | Citation errors | Span-level attribution validation |
| Governance | No audit trail | Log retrieved chunks, responses, timestamps (17a-4 compatible) |
| Governance | Unverifiable output | Evidence bundles with every response |
| Evaluation | No feedback loop | Automated evaluation (e.g., RAGAS), synthetic test queries |

---

## FinServ-Specific Design Pattern: Evidence Bundles

Instead of returning only an answer, return an **evidence bundle** — a structured dossier that travels with every response.

```json
{
  "answer": "string",
  "evidence_bundle": {
    "query": "original user query",
    "retrieved_documents": [
      {
        "doc_id": "POLICY-CC-001",
        "version": "2025-08-01",
        "section": "4.2.3",
        "snippet": "exact text retrieved..."
      }
    ],
    "relied_on_evidence": [
      { "doc_id": "POLICY-CC-001", "section": "4.2.3" }
    ],
    "model_trace": {
      "model": "model-version",
      "prompt_template_version": "v3",
      "timestamp": "2025-12-15T09:10:00Z"
    }
  }
}

## Version History

| Version | Date | Summary of Changes |
|--------|------|--------------------|
| v0.1 | Dec 2025 | Initial RAG failure checklist compiled from industry research on production RAG failures |
| v0.2 | Dec 2025 | Added chunking as a first-order retrieval failure domain; clarified index-time vs generation-time failure modes; incorporated Databricks chunking research |

