# RAG Knowledge Pilot — Measured Retrieval System

A feature-level Retrieval-Augmented Generation (RAG) pilot designed to demonstrate measurable retrieval behavior, structured refusal logic, and evaluation-driven iteration.

This module is intentionally executable, minimal, and instrumented — built to simulate how an internal AI knowledge feature would be piloted and evaluated inside a business team.

---

## Performance Summary

| Metric | Threshold 0.45 | Threshold 0.60 (no reflection) | Threshold 0.60 (with reflection) |
|---|---:|---:|---:|
| Grounded Answer Rate (GAR) | **100.0%** (11/11) | 72.7% (8/11) | **90.9%** (10/11) |
| Refusal Correctness Rate (RCR) | **100.0%** (4/4) | **100.0%** (4/4) | **100.0%** (4/4) |
| Avg Top-Chunk Similarity | 0.5854 | 0.5854 | 0.5911 |
| Reflection triggered | — | — | 7/15 queries |

**Evaluation dataset:** 15 domain-realistic compliance queries
**Query mix:** 11 should-ground · 4 should-refuse

**Threshold tradeoff:** Raising the grounding threshold from 0.45 to 0.60 increases conservatism — three borderline queries (scores 0.49, 0.58, 0.59) flip to refusal, dropping GAR to 72.7%.

**Reflection recovery:** With the agentic reflection loop enabled, the system reformulates borderline queries and retries retrieval once. This recovers 2 of 3 borderline queries, raising GAR from 72.7% to 90.9% — with no loss in refusal correctness. The remaining miss (score 0.49) is appropriately refused even after reformulation.

### Reproduce These Results

```bash
# Threshold 0.45 (default)
python modules/rag-knowledge-pilot/src/main.py --evaluate --reindex

# Threshold 0.60, with reflection (default)
GROUNDING_THRESHOLD=0.60 python modules/rag-knowledge-pilot/src/main.py --evaluate --reindex

# Threshold 0.60, without reflection
GROUNDING_THRESHOLD=0.60 python modules/rag-knowledge-pilot/src/main.py --evaluate --reindex --no-reflection
```

PowerShell:
```powershell
$env:GROUNDING_THRESHOLD="0.60"
# With reflection (default)
python modules/rag-knowledge-pilot/src/main.py --evaluate --reindex
# Without reflection
python modules/rag-knowledge-pilot/src/main.py --evaluate --reindex --no-reflection
```

---

## Quick Start

Run a sample query from the repository root:

```bash
python modules/rag-knowledge-pilot/src/main.py --query "Can a client trade options without a signed options agreement?"
```

**Example output:**

```
query: "Can a client trade options without a signed options agreement?"

retrieved_chunks:
  - rank=1  score=0.78  source=policy_options_approval.md
  - rank=2  score=0.64  source=policy_margin.md
  - rank=3  score=0.59  source=policy_suitability.md

grounding_status: GROUNDED
refusal_code: NONE
```

The system prints ranked retrieved chunks with similarity scores, a categorical grounding decision, and a structured refusal code when applicable.

---

## What This Pilot Demonstrates

- **Retrieval architecture** with swappable embedding provider abstraction (hosted vs. local models)
- **Agentic reflection loop** — automatic query reformulation and single-retry retrieval for borderline results
- **Measured grounding performance** using Grounded Answer Rate (GAR) and Refusal Correctness Rate (RCR)
- **Configurable grounding threshold** to explore precision/recall tradeoffs
- **Structured refusal behavior** with explicit reason codes and logged decisions
- **Traceable retrieval outputs** — every query produces inspectable chunk rankings, scores, and decisions

---

## Architecture Overview

```
rag-knowledge-pilot/
  src/
    main.py          # Entry point and CLI
    embeddings.py    # Embedding provider abstraction layer
    retrieval.py     # Chunking and retrieval logic
    reflection.py    # Agentic query reformulation (single-retry)
    evaluation.py    # Evaluation harness and scoring
  corpus/            # Synthetic internal compliance policy excerpts
  evaluation/        # Test queries and expected outcomes
  results/           # Scored evaluation run outputs
```

The structure is designed so retrieval strategy can evolve — lexical baseline → vector embeddings → provider swap → controlled retry logic — without changing module shape.

### How Corpus Documents Become Searchable

```mermaid
flowchart LR
    A["corpus/<br/>policy_margin.md<br/>policy_options_approval.md<br/>policy_suitability.md<br/>policy_comms_standard.md"] --> B["retrieval.py<br/>load_corpus()"]
    B --> C["retrieval.py<br/>chunk_document()<br/>500 chars, 100 overlap"]
    C --> D["~15-20 chunks<br/>with metadata:<br/>source_file, chunk_id,<br/>start_char, end_char"]
    D --> E["embeddings.py<br/>embed_texts(all chunks)"]
    E --> F["OpenAI API<br/>text-embedding-3-small<br/>→ 1536-dim vectors"]
    F --> G["retrieval.py<br/>build_index()"]
    G --> H["vector_index.json<br/>(persisted to disk)<br/>chunks + vectors + metadata"]

    style A fill:#fff3cd,stroke:#ffc107
    style H fill:#d4edda,stroke:#28a745
```

---

## Evaluation Design

The evaluation harness simulates realistic business partner usage.

Each of the 15 test queries includes:

- Query text
- Expected action (`ground` or `refuse`)
- For refusals: a structured reason code and rationale

The harness computes:

- **Grounded Answer Rate (GAR)** — % of groundable queries that return a grounded, cited response
- **Refusal Correctness Rate (RCR)** — % of refusal-worthy queries that correctly refuse with the right reason code
- **Retrieval characteristics** — similarity score distribution, top-1 vs. top-k reliance

This enables before/after comparisons when embedding models or thresholds change.

---

## Threshold Experimentation

Grounding decisions are threshold-driven. Running evaluation at multiple threshold values surfaces:

- Precision vs. recall tradeoffs in grounding decisions
- Retrieval sensitivity to similarity cutoffs
- Refusal rate changes under tighter constraints

At **0.45**, the system grounds all 11 groundable queries — including borderline cases with similarity scores as low as 0.49. At **0.60**, three borderline queries (scores 0.49, 0.58, 0.59) flip to refusal, reducing GAR to 72.7% while refusal correctness remains at 100%.

This models how real AI features are tuned during pilot phases before broader rollout.

---

## Agentic Reflection Loop

When the top retrieval score falls below the grounding threshold, the system can automatically reformulate the query and retry retrieval once before falling back to refusal. This is the "agentic" pattern — the system attempts to improve its own retrieval quality without human intervention.

### Without Reflection

```mermaid
flowchart TD
    A["User Query<br/><i>--query 'Can a client trade options...'</i>"] --> B["main.py<br/>parse arguments"]
    B --> C["embeddings.py<br/>OpenAIEmbeddingProvider<br/>embed query → 1536-dim vector"]
    C --> D["retrieval.py<br/>cosine similarity search<br/>against vector_index.json"]
    D --> E["Top 3 chunks returned<br/>with similarity scores"]
    E --> F{"main.py<br/>classify_result()<br/>top score ≥ threshold?"}
    F -- "Yes" --> G["✅ GROUNDED<br/>refusal_code: NONE<br/>return chunks + scores"]
    F -- "No" --> H["🛑 REFUSED<br/>refusal_code: INSUFFICIENT_EVIDENCE<br/>log reason + scores"]

    style G fill:#d4edda,stroke:#28a745
    style H fill:#f8d7da,stroke:#dc3545
```

### With Reflection

```mermaid
flowchart TD
    A["User Query"] --> B["main.py<br/>parse arguments"]
    B --> C["embeddings.py<br/>OpenAIEmbeddingProvider<br/>embed query"]
    C --> D["retrieval.py<br/>cosine similarity search<br/>against vector_index.json"]
    D --> E["Top 3 chunks returned<br/>with similarity scores"]
    E --> F{"main.py<br/>top score ≥ threshold?"}
    F -- "Yes" --> G["✅ GROUNDED<br/>refusal_code: NONE"]
    F -- "No" --> R["reflection.py<br/>reformulate_query()<br/>OpenAI chat completion<br/><i>gpt-4o-mini</i>"]
    R --> R2["Reformulated query returned"]
    R2 --> C2["embeddings.py<br/>embed reformulated query"]
    C2 --> D2["retrieval.py<br/>cosine similarity search<br/>(second attempt)"]
    D2 --> E2["New top 3 chunks<br/>with updated scores"]
    E2 --> F2{"main.py<br/>top score ≥ threshold?"}
    F2 -- "Yes" --> G2["✅ GROUNDED<br/>(via reflection)<br/>both attempts logged"]
    F2 -- "No" --> H2["🛑 REFUSED<br/>refusal_code: INSUFFICIENT_EVIDENCE<br/>both attempts logged"]

    style G fill:#d4edda,stroke:#28a745
    style G2 fill:#d4edda,stroke:#28a745
    style H2 fill:#f8d7da,stroke:#dc3545
    style R fill:#fff3cd,stroke:#ffc107
```

With reflection enabled, the system recovers 2 of 3 borderline queries at threshold 0.60, raising GAR from 72.7% to 90.9% while maintaining 100% refusal correctness.

### Detailed View: Borderline Query With Reflection

```mermaid
sequenceDiagram
    actor User
    participant main as main.py
    participant emb as embeddings.py<br/>OpenAIEmbeddingProvider
    participant api_emb as OpenAI API<br/>(text-embedding-3-small)
    participant ret as retrieval.py
    participant idx as vector_index.json
    participant ref as reflection.py
    participant api_chat as OpenAI API<br/>(gpt-4o-mini)

    User->>main: --query "Are there restrictions on<br/>margin for new accounts?"
    
    Note over main,idx: First Attempt
    main->>emb: embed_texts([query])
    emb->>api_emb: POST /v1/embeddings
    api_emb-->>emb: query vector
    main->>ret: retrieve(query, top_k=3)
    ret->>idx: load index
    ret->>ret: cosine similarity search
    ret-->>main: top score: 0.58

    main->>main: classify_result()<br/>0.58 < threshold 0.60

    Note over main,api_chat: Reflection Triggered
    main->>ref: reformulate_query(query, chunks)
    ref->>api_chat: POST /v1/chat/completions<br/>"Rewrite this query to better match<br/>a compliance policy corpus"
    api_chat-->>ref: "What are the specific margin<br/>account requirements and restrictions<br/>for customer accounts?"
    ref-->>main: reformulated query

    Note over main,idx: Second Attempt
    main->>emb: embed_texts([reformulated_query])
    emb->>api_emb: POST /v1/embeddings
    api_emb-->>emb: new query vector
    main->>ret: retrieve(reformulated_query, top_k=3)
    ret->>idx: load index
    ret->>ret: cosine similarity search
    ret-->>main: top score: 0.70

    main->>main: classify_result()<br/>0.70 ≥ threshold 0.60
    main-->>User: grounding_status: GROUNDED (via reflection)<br/>refusal_code: NONE<br/>both attempts logged
```

**Controls:**
- Enabled by default. Disable with `--no-reflection` or `REFLECTION_ENABLED=false`
- Maximum one retry — no recursive loops
- Reformulation uses OpenAI chat completion (gpt-4o-mini), not embeddings
- Evaluation harness tracks how many queries triggered reflection

---

## Setup

Requires an OpenAI API key for embeddings:

```powershell
# PowerShell (session)
$env:OPENAI_API_KEY="sk-..."

# Bash
export OPENAI_API_KEY=sk-...
```

If the key is missing, the system exits gracefully with setup instructions (no stack trace).

---

## Limitations

This module is a pilot and evaluation harness. It is not production software and makes no claims about scale, latency, security, or enterprise hardening.

Its purpose is to demonstrate measurable retrieval behavior and support controlled, evaluation-driven iteration of AI feature design.

---

## Relationship to Module 4

This pilot operationalizes the governance architecture defined in [Module 4 — Compliance Retrieval Assistant](../compliance-retrieval-assistant/).

Module 4 defines the control-plane thinking and refusal taxonomy.
Module 5 executes retrieval behavior and measures it.

Together they illustrate progression:

**Architecture → Executable Pilot → Measured Iteration**