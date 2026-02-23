# ADR-003: Retrieval and Classification Without LLM Response Generation

**Status:** Accepted
**Date:** 2026-02-22
**Module:** RAG Knowledge Pilot (Module 5)
**Relates to:** ADR-001 (Phased Retrieval), Module 4 ADR-001 (Grounding Status over Confidence Scores)

## Context

The RAG Knowledge Pilot retrieves relevant document passages and classifies whether the evidence is sufficient to answer (GROUNDED) or should be refused (REFUSED with a reason code). A full RAG system would add a third step: passing the retrieved passages to an LLM to generate a natural language answer.

The question was whether Module 5 should include LLM-based answer generation, or stop at retrieval and classification.

Note: Module 5 *does* use an LLM (OpenAI chat completion) for one targeted purpose — query reformulation in the reflection loop (see ADR-004). This ADR addresses the separate decision to not use an LLM for response generation.

## Decision

Do not use an LLM to generate natural language answers from retrieved passages. The system retrieves chunks, scores them, classifies grounding status, and reports the results with source attribution. The output is a structured classification (grounding status, refusal code, retrieved sources with scores), not a generated answer.

## Rationale

**Evaluation precision.** Module 5's metrics — Grounded Answer Rate (GAR) and Refusal Correctness Rate (RCR) — measure retrieval quality and classification accuracy. If an LLM generated the final answer, evaluation would conflate retrieval quality with generation quality. A system could retrieve the right passages and still generate a bad answer, or retrieve mediocre passages and generate a plausible-sounding answer that masks retrieval weakness. Keeping them separate means the metrics measure one thing cleanly.

**Reproducibility.** The evaluation harness tests 15 queries (11 should-ground, 4 should-refuse) against a fixed corpus and known expected outcomes. At threshold 0.45, GAR is 100% and RCR is 100%. At threshold 0.60 with reflection, GAR is 90.9% and RCR is 100%. These numbers are reproducible: given the same corpus, queries, and embeddings, anyone running the evaluation gets the same results. LLM generation would introduce stochasticity — even with temperature=0, outputs vary across runs and model versions. The metrics would become approximations rather than facts.

**Scope discipline.** Module 5 is positioned as a "Retrieval Pilot" — the README title says so explicitly. Retrieval, grounding classification, and refusal logic are the capabilities being demonstrated. Adding answer generation would shift it toward a "full RAG assistant," which is Module 4's architectural scope. Module 5 operationalizes specific layers of Module 4's design, not the entire pipeline.

**The reflection loop is a bounded exception.** The agentic reflection loop (ADR-004) uses chat completion to reformulate queries — a targeted, bounded LLM call that serves retrieval, not generation. It rewrites the search query, not the user-facing answer. This distinction is intentional: the LLM assists the retrieval process without controlling the output.

## Consequences

**Accepted trade-offs:**
- The system does not produce human-readable answers. A reviewer expecting a conversational response will see structured output (rank, score, source, grounding status) instead.
- The README and evaluation output frame this explicitly as a retrieval and classification pilot, which sets correct expectations.

**What this enables:**
- Deterministic, reproducible evaluation metrics that can be compared across threshold values, with/without reflection, and across corpus changes.
- Clear separation between "did we find the right evidence?" (Module 5's scope) and "did we generate a good answer?" (a future capability).
- When LLM generation is eventually added, the improvement in user experience will be measurable against the existing retrieval baseline.

## Upgrade Path

When LLM generation is introduced:
- Generation must consume the same chunk IDs and scores produced by the current retrieval layer
- Grounding classification must remain categorical (GROUNDED / REFUSED), not be overridden by generation confidence
- Evaluation must separately score retrieval quality and generation quality — GAR/RCR remain retrieval metrics; new metrics are needed for generation
- A deterministic retrieval-only mode should be preserved for audit reconstruction and regression testing

## Superseded When

This ADR is superseded when a subsequent ADR introduces LLM-based response generation and documents the evaluation framework for assessing generation quality independently of retrieval quality.
