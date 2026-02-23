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
