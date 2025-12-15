# RAG Failure Modes Checklist v0.1

## Purpose

Pre-build checklist of failure modes to design against when constructing the Compliance Retrieval Assistant. This checklist was compiled from industry research on why RAG systems fail in production — particularly in regulated environments.

**Key insight:** Up to 70% of RAG systems fail in production. The failures that matter most in regulated environments aren't just accuracy issues — they're **traceability issues**.

---

## Retrieval Failures

### Content Selection Problems
- [ ] **Wrong chunk retrieved** — Semantically similar but factually incorrect content returned
- [ ] **Chunk boundary issues** — Answer split across chunks, incomplete information retrieved
- [ ] **Retrieval decay** — System worked with small dataset but fails as corpus grows (can't find needle in haystack)
- [ ] **Retrieval overload** — Too many documents retrieved, introducing noise that confuses generation
- [ ] **Missing document** — Required policy/document not in corpus at all
- [ ] **Cross-document contradictions** — Retrieved documents contain conflicting information, no resolution mechanism

### Staleness & Drift Problems
- [ ] **Stale index** — Policy updated but embeddings not refreshed
- [ ] **Knowledge drift** — Information was accurate when indexed but world has changed (e.g., interest rates, regulations)
- [ ] **Temporal staleness without detection** — System confidently returns outdated information with no uncertainty indicator
- [ ] **Embedding drift** — Embedding model updated but document index not re-synced, causing retrieval quality degradation

### Technical/Architecture Problems
- [ ] **Retrieval timing attacks** — Async retrieval completes after generation timeout, system generates without context
- [ ] **Context position bias** — Model disproportionately weights content appearing early/late in context window
- [ ] **Retrieval-generation model mismatch** — Different tokenization between embedding and generation models causes subtle quality issues
- [ ] **Recursive retrieval loops** — Iterative retrieval repeatedly fetches same content without progress

---

## Generation Failures

### Hallucination & Accuracy
- [ ] **Hallucination despite retrieval** — Model ignores retrieved content and generates from training data
- [ ] **Citation hallucination** — Model cites retrieved documents but attributes claims to wrong sources
- [ ] **Overconfident tone** — Uncertain answers presented with inappropriate certainty
- [ ] **Incomplete synthesis** — Model uses one chunk, ignores others that contain relevant information

### Reasoning Failures
- [ ] **Multi-hop reasoning failure** — Model retrieves all necessary facts but fails to connect them for complex queries
- [ ] **Irrelevant chunk overload** — Too much context confuses model, leading to hallucination or wrong answers

---

## Governance & Compliance Failures

### Auditability Problems
- [ ] **No citations provided** — Answers generated without linking to source documents
- [ ] **Unverifiable outputs** — No internal proof of where answer came from (no doc ID, no timestamp, no version)
- [ ] **Audit/dispute blind spots** — Cannot reconstruct what the system saw and relied on 6 months later
- [ ] **No audit trail** — Retrieved chunks and model decisions not logged
- [ ] **Unclear source of truth** — Which document version was used? When was it last updated?

### Regulatory & Access Problems
- [ ] **Regulatory mismatch** — System fetches from stale guidance, gives correct answers for last year's regime
- [ ] **Access control violations** — RAG system doesn't respect RBAC, could leak confidential content
- [ ] **Data freshness gaps** — Document collections change but sync is infrequent, stale information served

### Enterprise Data Problems
- [ ] **Unstructured data handling failures** — PDFs with tables, multi-column layouts, images, graphs not parsed correctly
- [ ] **Decentralized data gaps** — Content spread across SharePoint, Slack, Confluence, etc. — not all sources connected
- [ ] **Format diversity** — Pipeline only handles "nice" text, misses knowledge in spreadsheets, slides, diagrams

---

## Evaluation & Monitoring Failures

- [ ] **The evaluation gap** — No feedback loop; system deteriorates without detection until users abandon it
- [ ] **Flying blind on quality** — No systematic measurement of retrieval relevance, generation accuracy, or hallucination rate
- [ ] **No baseline metrics** — Can't detect degradation because normal performance was never measured

---

## Mitigations I'll Use in My Build

| Failure Category | Failure Mode | Mitigation Strategy |
|------------------|--------------|---------------------|
| **Retrieval** | Wrong chunk | Top-k tuning, relevance threshold, hybrid search (semantic + keyword) |
| **Retrieval** | Stale index | Document versioning, freshness metadata, scheduled re-indexing |
| **Retrieval** | Retrieval overload | Adaptive context sizing based on query intent |
| **Retrieval** | Position bias | Randomize/reorder retrieved docs, test for position sensitivity |
| **Generation** | Hallucination | Strict grounding rules, citation requirement, "NOT_IN_DOCUMENT" fallback |
| **Generation** | Citation errors | Span-level attribution validation (verify each citation against source) |
| **Generation** | Multi-hop failure | Explicit reasoning steps in prompt, chain-of-thought for complex queries |
| **Governance** | No audit trail | Log retrieved chunks + model response + timestamps per 17a-4 |
| **Governance** | Unverifiable output | Evidence bundles with every response (see architecture below) |
| **Governance** | Regulatory mismatch | Document version tracking, freshness thresholds, explicit staleness warnings |
| **Evaluation** | No feedback loop | Automated evaluation using RAGAS or similar, synthetic test data from real queries |

---

## FinServ-Specific Design Pattern: Evidence Bundles

Instead of returning just an answer, return an **evidence bundle** — a mini dossier that travels with every response:

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
      {"doc_id": "POLICY-CC-001", "section": "4.2.3"}
    ],
    "model_trace": {
      "model": "model-version",
      "prompt_template_version": "v3",
      "timestamp": "2025-12-15T09:10:00Z"
    }
  }
}
```

**Why this matters:** The customer sees the answer. The compliance officer sees the bundle. Six months later, when a dispute lands on someone's desk, you can reconstruct exactly what the system saw and relied on.

---

## Questions to Answer Before Building

### Chunking Strategy
- What chunk size works best for compliance documents?
- How do I handle documents with tables, multi-column layouts?
- Should I use overlapping chunks to avoid boundary issues?

### Freshness & Versioning
- How often do source documents change?
- How do I detect when a document has been updated?
- How do I handle queries about "current" policy vs. "policy at time X"?

### Retrieval Quality
- What's the right balance between recall (find everything) and precision (find only relevant)?
- How many documents should I retrieve? (Research shows diminishing returns beyond 5-10)
- Should I use hybrid search (semantic + keyword)?

### Evaluation
- How will I measure retrieval relevance over time?
- How will I detect hallucinations automatically?
- What's my feedback loop for continuous improvement?

---

## Sources Read

1. **"Ten Failure Modes of RAG Nobody Talks About"** — Kuldeep Paul / Maxim AI
   - Retrieval timing attacks, position bias, embedding drift, multi-hop failures, citation hallucination, model mismatch, temporal staleness, cross-document contradictions, recursive loops

2. **"Why RAG Fails in Production (And How to Fix It)"** — Shubham Maurya, Mastercard
   - Knowledge drift, retrieval decay, irrelevant chunks, evaluation gap
   - Solutions: hybrid search, graph-based RAG, schema evolution tracking, adaptive context sizing

3. **"RAG in Regulated Markets: Evidence Bundles and External Links"**
   - Unverifiable outputs, regulatory mismatch, audit blind spots
   - Evidence bundle pattern, structured citations, audit trail design

4. **"Why GenAI Pilots Fail: Common Challenges with Enterprise RAG"** — Zeta Alpha
   - Unstructured data, decentralized sources, RBAC requirements, data freshness
   - "Enterprise search is never turnkey — it requires deep customization"

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v0.1 | Dec 2025 | Initial checklist compiled from 4 industry sources |