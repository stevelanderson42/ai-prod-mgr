# ADR-001: Phased Retrieval Implementation — Lexical Baseline Before Embeddings

**Status:** Accepted (Phase 1 superseded by Phase 2 embedding implementation)
**Date:** 2026-02-22
**Module:** RAG Knowledge Pilot (Module 5)
**Relates to:** Module 4 ADR-001 (Grounding Status over Confidence Scores), Module 3 ADR-001 (Deterministic Routing Logic)

## Context

Module 5 is the first executable module in the portfolio — designed to demonstrate measurable retrieval behavior, not just architecture. A retrieval mechanism was needed to match user queries against a small synthetic compliance corpus (4 policy documents).

The implementation could have started with embeddings from the beginning. OpenAI's embedding API was available and the corpus was small enough that cost and latency were not concerns. The alternative was to start with deterministic lexical retrieval (token overlap scoring), validate the full pipeline end-to-end, and then upgrade to embeddings as a second phase.

## Decision

Start with deterministic token overlap retrieval in Phase 1. Replace it with OpenAI embedding-based retrieval in Phase 2, once the pipeline shape (query → retrieve → classify → output → evaluate) was validated and running without errors.

## Rationale

**Pipeline validation before retrieval optimization.** The first prompt to Claude Code created the entire module scaffold — folder structure, corpus, test queries, evaluation harness, CLI, and README — with simple lexical retrieval. This meant the system ran immediately. Every subsequent change (embeddings, usability fixes, reflection loop) was made against a working baseline, not a half-built system.

**Debugging one layer at a time.** If the first implementation used embeddings and something failed — was it the embedding call? The vector index? The scoring? The chunking? Starting lexical isolated those variables. When embeddings were introduced in Phase 2, the rest of the pipeline was already proven correct. Any new failures were attributable to the embedding layer alone.

**Portfolio consistency.** Module 3 uses deterministic routing (ADR-001) and Module 4 uses categorical grounding (ADR-001). Starting Module 5 with deterministic retrieval before introducing statistical methods follows the same pattern: prove the governance contract works with interpretable behavior first, then layer in sophistication.

**Build cadence.** Module 5 was built in four sequential prompts across a single day. Each prompt produced a working system with measurably different capabilities. Starting lexical made the first prompt fast and dependency-free (standard library only), which created momentum for the subsequent phases.

## What Happened

Phase 1 — commit `e172ccc` (Prompt 1): Token overlap retrieval. System ran immediately. Placeholder metrics. Created 4 corpus documents, 15 test queries with expected outcomes, and 4 source files (main.py, retrieval.py, embeddings.py, evaluation.py).

Phase 2 — commit `33595ec` (Prompt 2): OpenAI embeddings with cosine similarity retrieval replaced token overlap entirely. ChromaDB was initially specified but was incompatible with the installed Python version (3.14). Claude Code pivoted to a lightweight file-based vector index using the same cosine similarity math — fewer dependencies, same behavior. This adaptation became its own architectural advantage (see ADR-002).

The lexical implementation no longer exists in the codebase. Its value was as a validation step, not a permanent layer.

The prompts that drove each phase are preserved in `session-prompts/` at the repository root for reproducibility.

## Consequences

**What this enabled:**
- A system that worked at every stage of its construction — no "trust me, it'll work when I'm done" phases
- Clean attribution of the GAR improvement from lexical to embeddings to reflection, because each was introduced independently
- A build story that demonstrates phased, evaluation-driven development — not a big-bang implementation

**What this pattern means for future work:**
- When hybrid retrieval is introduced (lexical shortlist → embedding re-rank), the same phasing discipline applies: validate the hybrid pipeline with the existing evaluation harness before tuning parameters
- Lexical retrieval could be reintroduced as a deterministic fallback for incident response or audit reconstruction

## Superseded When

Phase 1 (lexical) was superseded by Phase 2 (embeddings) during the initial build. The ADR documents the phasing decision as an architectural principle, not a permanent constraint.
