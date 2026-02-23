# Module 5 ADRs — Claude Code Instructions

## Placement

These four ADRs should be created as individual files in:
`modules/rag-knowledge-pilot/architecture/decisions/`

If the `architecture/` and `architecture/decisions/` directories do not exist, create them.

These are the first ADRs for Module 5, so numbering starts at ADR-001.

After creating the files, create `modules/rag-knowledge-pilot/architecture/README.md` with a brief intro and links to all four ADRs. If an architecture README already exists, update it to include links to these decisions.

---

## File 1: ADR-001-phased-retrieval-lexical-baseline-before-embeddings.md

```markdown
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
```

---

## File 2: ADR-002-file-based-vector-index-over-external-database.md

```markdown
# ADR-002: File-Based Vector Index with Swappable Embedding Provider

**Status:** Accepted
**Date:** 2026-02-22
**Module:** RAG Knowledge Pilot (Module 5)
**Relates to:** Global ADR-0003 (Evidence Traceability Standard)

## Context

Module 5 needed a vector storage mechanism for embedding-based retrieval. The original specification called for ChromaDB, a popular vector database. During implementation, ChromaDB was found to be incompatible with the installed Python version (3.14). A decision was needed: fight the dependency, downgrade Python, or take a different approach.

Separately, the embedding layer needed an abstraction that would allow swapping between embedding providers (OpenAI hosted, local models) without rewriting retrieval logic.

## Decision

1. **Use a file-based vector index** (`vector_index.json`) with in-memory cosine similarity search instead of an external vector database. The index is persisted to disk and reused between runs.

2. **Abstract the embedding layer** (commit `33595ec`, Phase 2) behind an `EmbeddingProvider` interface with `embed_texts(list[str]) -> list[list[float]]`. The current implementation uses `OpenAIEmbeddingProvider` in `src/embeddings.py`; the interface supports future providers without changing retrieval logic.

## Rationale

**Dependency minimalism for a pilot.** A vector database adds installation complexity, version constraints, and a runtime dependency — all liabilities for a portfolio artifact that needs to be cloneable and runnable by someone evaluating the author's work. The file-based index uses only `json`, `math`, and the OpenAI SDK. Fewer things to break means a better first impression.

**Same math, fewer moving parts.** Cosine similarity is cosine similarity whether it's computed by ChromaDB, FAISS, or a 10-line Python function. At the scale of this pilot (4 documents, ~20 chunks), there is no performance benefit to a dedicated vector database. The math is identical.

**Adaptation as a design advantage.** The pivot from ChromaDB was initially a workaround, but it produced a cleaner system. The persisted JSON index is human-readable — you can open `vector_index.json` and see exactly what's stored, which supports the traceability principles from Global ADR-0003. A binary database file would not offer that transparency.

**Provider abstraction supports the iteration story.** The `EmbeddingProvider` interface exists so that introducing local embeddings (Sentence Transformers, etc.) becomes a single new class implementation, not a retrieval rewrite. This is directly aligned with the model-agnostic architecture specified in Module 4's component design. It also creates a concrete interview narrative: "I started with hosted embeddings to move fast, then the architecture supports swapping in local models to compare retrieval characteristics."

**Reindex control.** The `--reindex` flag (added in commit `571aa24`, Phase 3) in `main.py` calls `delete_index()` in `retrieval.py` to force a rebuild. This separates index lifecycle from query lifecycle — corpus changes are picked up explicitly, not silently. In a production system this would be a pipeline concern; in a pilot, it's a usability decision.

## Consequences

**Accepted trade-offs:**
- File-based cosine similarity does not scale beyond a few hundred chunks. This is acceptable for a pilot with 4 documents and ~20 chunks.
- No approximate nearest neighbor (ANN) search — all comparisons are brute-force. Again, irrelevant at this scale.
- The vector index is a single JSON file. Concurrent writes would corrupt it. Not a concern for single-user CLI usage.

**What this enables:**
- Zero-infrastructure demo. `pip install openai` + an API key is all that's needed.
- Human-readable index artifact for audit and debugging.
- Clean upgrade path: replace the file-based index with Chroma, FAISS, or Pinecone by implementing a new retrieval backend behind the same function signatures.

## Superseded When

This ADR is superseded when a subsequent ADR introduces an external vector database and documents the scale or feature requirements that justify the additional dependency.
```

---

## File 3: ADR-003-retrieval-classification-without-llm-generation.md

```markdown
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
```

---

## File 4: ADR-004-bounded-agentic-reflection-single-retry.md

```markdown
# ADR-004: Bounded Agentic Reflection — Single-Retry Query Reformulation

**Status:** Accepted
**Date:** 2026-02-22
**Module:** RAG Knowledge Pilot (Module 5)
**Relates to:** ADR-003 (Retrieval Without LLM Generation)

## Context

At grounding threshold 0.60, three borderline queries (similarity scores 0.49, 0.58, 0.59) flipped from GROUNDED to REFUSED, dropping GAR from 100% to 72.7%. These were legitimate compliance questions with relevant corpus content — the retrieval was finding related passages, but the similarity scores fell just below the threshold.

The options were:
1. **Lower the threshold** — accept weaker matches, which risks grounding answers on marginally relevant passages
2. **Improve the corpus** — add more documents or rephrase existing ones to better match query vocabulary
3. **Add query reformulation** — let the system automatically rephrase a weak query and retry once before refusing

## Decision

Implement a single-retry reflection loop (commit `79de6ae`, Phase 4). When the top retrieval score falls below the grounding threshold, the system uses OpenAI chat completion to reformulate the query and retries retrieval once. If the second attempt meets the threshold, the system grounds. If not, it refuses. Maximum one retry. The loop is toggleable via `--no-reflection` flag and `REFLECTION_ENABLED` environment variable. The implementation lives in a dedicated `reflection.py` module (~30 lines), with integration points in `main.py` (classification flow) and `evaluation.py` (reflection statistics tracking).

## Rationale

**Targeted intervention for observed behavior.** This wasn't a speculative feature — it was a direct response to three specific, documented failure cases. The evaluation harness identified the problem; the reflection loop addresses it. This is evaluation-driven development: measure, identify gaps, build targeted fixes, re-measure.

**Agentic behavior with hard boundaries.** The system autonomously decides to try harder — it reformulates its own query without human intervention. That's a genuine agentic pattern. But it's constrained: one retry, one reformulation, deterministic fallback to refusal if the retry doesn't improve results. In a regulated context, unbounded retry loops create unpredictable latency, unbounded API costs, and difficulty reconstructing what happened during an audit. One retry is predictable and auditable.

**Chat completion for reformulation, not embeddings.** The reformulation step calls OpenAI's chat completion API, not the embedding API. These are different capabilities: embeddings convert text to vectors (for searching), chat completion generates new text (for rewriting). The prompt is simple and constrained: "Rewrite this query as a clearer, more specific search query. Return only the rewritten query." The model sees the original query and optionally the top retrieved chunk for context. This targeted use of an LLM serves retrieval quality without introducing LLM-generated answers (consistent with ADR-003).

**Toggleability enables measurement.** The `--no-reflection` flag exists specifically so evaluation can be run both ways in the same session:
- Without reflection at 0.60: GAR 72.7%, RCR 100%
- With reflection at 0.60: GAR 90.9%, RCR 100%

That delta (72.7% → 90.9%) is the measured impact of the reflection loop. Without the toggle, you'd have to modify code to get a before/after comparison. The flag makes the comparison a single CLI argument.

**Refusal correctness preserved.** The reflection loop triggered on 7 of 15 queries — all 4 should-refuse queries and the 3 borderline should-ground queries. It correctly failed to improve the 4 should-refuse queries (their content genuinely isn't in the corpus, so reformulation doesn't help). It recovered 2 of the 3 borderline queries. RCR remained at 100% — the system never incorrectly grounded a query that should have been refused, even after trying harder. This is the critical safety property: the reflection loop improves helpfulness without degrading safety.

## Consequences

**Accepted trade-offs:**
- Adds one additional OpenAI API call (chat completion) for queries below threshold. At the pilot's scale this is pennies, but in production it would need cost monitoring.
- Introduces non-determinism for the reformulated query (the LLM's rewrite may vary). However, the final grounding decision is still based on cosine similarity against the same index, so the classification remains score-based.
- Adds latency for below-threshold queries (embedding call + retrieval + chat completion + second embedding call + second retrieval). For a pilot, this is acceptable. Production would need timeout constraints.

**What this enables:**
- The resume sentence: "Improved grounded answer rate from 72.7% to 90.9% using an agentic reflection loop with zero loss in refusal correctness."
- A concrete demonstration of autonomous, bounded AI behavior — the system improving its own results without human intervention, within hard constraints.
- A measurable before/after comparison that demonstrates evaluation-driven iteration.

**What this means for future work:**
- The one-retry limit is a starting constraint, not a permanent ceiling. Future iterations could experiment with two retries or alternative reformulation strategies, measured against the same evaluation harness.
- The reformulation prompt is deliberately simple. Sophisticated reformulation (decomposing complex queries, expanding abbreviations, adding domain context) could improve recovery further.
- When LLM generation is introduced, the reflection loop should remain at the retrieval layer — reformulating the search query, not regenerating the answer.

## Superseded When

This ADR is superseded when a subsequent ADR introduces a materially different approach to handling below-threshold queries (e.g., multi-step reformulation, human-in-the-loop escalation, or corpus-aware query expansion).
```