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
| Tables | Limits, thresholds, matrices | Atomic chunks | Prevent semantic corruption |
| Policies | Compliance manuals, regulatory guidance | Semantic + section-aware | Preserve rule boundaries |
| Procedures | SOPs, operational playbooks | Recursive + overlap | Preserve step sequences |
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
```

---

### Policies & Regulatory Text

#### Why Policies Require Specialized Chunking

Policy and regulatory documents encode **authoritative rules**, interpretations, and exceptions that must be applied consistently. Unlike tables, meaning is often distributed across:

- Section headers and subheaders
- Enumerated clauses
- Cross-references and exceptions
- Qualifying language (“unless,” “except,” “subject to”)

Naive fixed-size chunking frequently separates these elements, resulting in **partial rule retrieval** and misleading answers.

---

#### Failure Modes Addressed

This strategy mitigates the following failure modes from the RAG Failure Modes Checklist:

- Semantic fragmentation
- Chunk boundary violations
- Section/header detachment
- Context underfill
- Citation hallucination

---

#### Chunking Strategy for Policies

**Primary Strategy:**  
**Semantic + section-aware chunking**, aligned to the document’s logical structure.

##### Approach

- Preserve section and subsection boundaries as natural chunk units.
- Use semantic chunking *within* sections when length exceeds target limits.
- Ensure that:
  - Headers remain attached to governing text.
  - Exceptions and qualifying clauses are not separated from primary rules.
- Apply limited overlap when needed to preserve cross-sentence meaning.

This approach prioritizes **rule completeness over uniform chunk size**.

---

#### Chunk Size & Overlap Guidance

- Target chunk sizes may vary by document but generally fall within a moderate range (e.g., 400–800 tokens).
- Overlap is applied selectively to:
  - Preserve exception logic
  - Maintain continuity across enumerated clauses
- Excessive overlap is avoided to reduce retrieval noise.

Exact parameters are validated empirically through retrieval evaluation.

---

#### Metadata Enrichment for Policy Chunks

Each policy chunk is enriched with metadata to support traceability and audit reconstruction:

- Document identifier
- Version and effective date
- Section and subsection identifiers
- Jurisdiction or regulatory regime (if applicable)
- Applicability scope (e.g., account type, customer segment)

This metadata enables:
- Accurate citation
- Version-correct retrieval
- Regulatory context awareness

---

#### Retrieval Considerations

Policy chunks are retrieved using **hybrid search**:

- Keyword matching for precise rule language
- Semantic embeddings for interpretive queries

During generation:
- The system favors **fewer, higher-precision chunks**.
- If multiple policy sections are retrieved, the model is instructed to:
  - Identify conflicts or exceptions
  - Explicitly cite all relied-upon sections

---

#### Evaluation Criteria for Policy Chunking

Policy chunking effectiveness is evaluated using:

##### Retrieval Metrics
- Precision@k for authoritative policy sections
- Rule completeness rate (single vs multi-chunk dependency)
- Header retention accuracy

##### Generation Risk Indicators
- Partial rule hallucination rate
- Exception omission rate
- Citation completeness and accuracy

---

#### Known Tradeoffs

- Semantic chunking increases indexing complexity
- Section-aware chunking may produce uneven chunk sizes
- Some regulatory documents require manual preprocessing

These tradeoffs are accepted because **policy misinterpretation carries high compliance risk**.

---

#### Design Decision Summary (Policies)

> **Decision:** Use semantic, section-aware chunking for policy and regulatory text.  
> **Rationale:** Preserve rule integrity, exceptions, and interpretive context.  
> **Risk Mitigated:** Incomplete or misleading compliance guidance caused by fragmented policy retrieval.

---

### Procedures & Playbooks

#### Why Procedures Require a Different Chunking Approach

Procedures and playbooks describe **how work is performed**, often as ordered steps, decision trees, or operational workflows. Unlike policies, correctness depends less on precise wording and more on **sequence, continuity, and completeness**.

Common characteristics include:

- Step-by-step instructions
- Conditional branching (“if X, then do Y”)
- Operational guardrails and escalation paths
- Embedded references to systems, roles, or tools

Naive chunking that breaks step sequences or separates conditionals from actions can lead to **operationally unsafe guidance**, even if individual chunks are factually correct.

---

#### Failure Modes Addressed

This strategy mitigates the following failure modes from the RAG Failure Modes Checklist:

- Semantic fragmentation
- Chunk boundary violations
- Context underfill
- Multi-hop reasoning failure
- Incomplete synthesis

---

#### Chunking Strategy for Procedures

**Primary Strategy:**  
**Recursive chunking with controlled overlap**, aligned to procedural boundaries.

##### Approach

- Identify natural procedural units:
  - Numbered steps
  - Sub-steps
  - Decision blocks
- Chunk along these boundaries rather than arbitrary token limits.
- Apply **limited overlap** to:
  - Preserve step transitions
  - Maintain conditional context across steps
- Avoid splitting:
  - Conditional logic from the actions it governs
  - Escalation criteria from escalation actions

This approach favors **procedural continuity over strict chunk uniformity**.

---

#### Chunk Size & Overlap Guidance

- Chunk sizes may be uneven, reflecting real procedural structure.
- Overlap is used sparingly to preserve:
  - “If / then” logic
  - Multi-step dependencies
- Excessive overlap is avoided to prevent retrieval noise and redundant context.

Exact parameters are validated through retrieval and synthesis evaluation.

---

#### Metadata Enrichment for Procedural Chunks

Each procedural chunk includes metadata to support correct application and traceability:

- Document identifier and version
- Procedure name and step range
- Applicable role or function
- Preconditions or assumptions (if defined)
- Escalation or exception indicators

This metadata helps ensure that retrieved guidance is **context-appropriate**, not just textually relevant.

---

#### Retrieval Considerations

Procedural chunks are retrieved using **semantic-first search**, with keyword reinforcement for:

- Step numbers
- System names
- Role identifiers

During generation:
- Retrieved chunks are ordered to preserve procedural flow.
- The model is instructed to:
  - Avoid skipping steps
  - Flag missing or partial procedures
  - Defer when insufficient context is retrieved

---

#### Evaluation Criteria for Procedural Chunking

##### Retrieval Metrics
- Step continuity rate (complete vs fragmented procedures)
- Correct step ordering rate
- Over-retrieval rate (irrelevant procedures retrieved)

##### Generation Risk Indicators
- Step omission rate
- Step reordering errors
- Conditional misapplication rate

---

#### Known Tradeoffs

- Recursive chunking increases indexing complexity
- Overlap increases token usage
- Some procedures require manual boundary tuning

These tradeoffs are accepted because **operational misuse carries real-world risk**, even when policies are technically correct.

---

#### Design Decision Summary (Procedures)

> **Decision:** Use recursive chunking with controlled overlap for procedures and playbooks.  
> **Rationale:** Preserve step order, conditional logic, and operational continuity.  
> **Risk Mitigated:** Unsafe or incomplete operational guidance caused by fragmented procedural retrieval.


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