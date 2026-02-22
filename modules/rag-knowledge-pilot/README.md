# RAG Knowledge Pilot — Measured Retrieval System

## Performance Summary

| Metric                  | Value | Notes                        |
|-------------------------|-------|------------------------------|
| Grounding Accuracy      | XX%   | Correct retrieval on should-ground queries |
| Refusal Accuracy        | XX%   | Correct refusal on should-refuse queries   |
| Top-3 Chunk Relevance   | XX%   | Retrieved chunk contains answer passage     |
| End-to-End Pass Rate    | XX%   | Combined across all 15 eval queries         |

> Metrics will be populated after evaluation harness is connected to vector retrieval.

## Quick Start

```bash
python modules/rag-knowledge-pilot/src/main.py --query "What are the margin requirements for a new customer account?"
```

---

## What It Does

- **Retrieves** relevant compliance policy chunks from a small internal corpus using measured, deterministic retrieval
- **Grounds** answers to source documents with citation traceability
- **Refuses** queries that fall outside corpus scope or lack sufficient evidence, returning structured refusal codes
- **Evaluates** retrieval quality against a curated set of 15 domain-realistic test queries with expected outcomes

## How It's Structured

The module is organized as a standalone pilot with source code in `src/`, a synthetic compliance corpus in `corpus/`, evaluation fixtures in `evaluation/`, and scored run outputs in `results/`. Each component is deliberately minimal — standard-library Python only — so the scaffolding runs immediately and can be incrementally upgraded to vector embeddings without restructuring.

## How Evaluation Works

- 15 test queries in `evaluation/test_queries.json` simulate real compliance/business-partner questions
- Each query has an expected action (`ground` or `refuse`) and, for refusals, a reason code and rationale in `evaluation/expected_outcomes.json`
- The evaluation harness in `src/evaluation.py` compares actual retrieval results against expected outcomes and produces a scored report
- Query mix: 9 should-ground, 4 should-refuse, 2 ambiguous/edge — reflecting realistic distribution

## Not Production

This is a **pilot / demo / evaluation harness**. It is not a production system and makes no production-readiness claims. Its purpose is to demonstrate measured retrieval behavior, validate evaluation methodology, and provide a concrete artifact for iterative improvement.

## Relationship to Module 4

This pilot operationalizes the governance architecture defined in [Module 4 — Compliance Retrieval Assistant](../compliance-retrieval-assistant/).
