# Prompt: Add Agentic Reflection Loop to Module 5

## Context
Module 5 (modules/rag-knowledge-pilot/) is a working RAG retrieval pilot with:
- OpenAI embeddings + cosine similarity retrieval
- Categorical grounding status (GROUNDED / REFUSED)
- Configurable GROUNDING_THRESHOLD (default 0.45)
- Evaluation harness with 15 test queries computing GAR and RCR

At threshold 0.60, three borderline queries (scores 0.49, 0.58, 0.59) flip from GROUNDED to REFUSED, dropping GAR from 100% to 72.7%.

## Task
Add a single-retry **reflection loop**: if the top retrieval score is below the grounding threshold, use OpenAI to reformulate the query and retry retrieval once before falling back to refusal.

This is the "agentic" pattern — the system attempts to improve its own retrieval quality without human intervention.

## Implementation Requirements

### 1. Add query reformulation function (in src/retrieval.py or a new src/reflection.py — your choice)
- Takes: the original query string + the top retrieved chunks from the first attempt
- Uses OpenAI chat completion (not embeddings) to reformulate the query
- Prompt should be simple and deterministic in intent, something like:
  "The following query did not retrieve strong results from a compliance policy corpus. Rewrite it as a clearer, more specific search query. Return only the rewritten query, nothing else."
- Include the original query and optionally the top chunk text for context
- Returns: a single reformulated query string

### 2. Modify classification logic in src/main.py
Current flow:
  query → retrieve → classify → output

New flow:
  query → retrieve → check top score
    → if top score >= threshold: GROUNDED (no change)
    → if top score < threshold:
        → reformulate query using OpenAI
        → retry retrieval with reformulated query
        → check top score again
        → if improved and >= threshold: GROUNDED (log both attempts)
        → else: REFUSED (log both attempts)

### 3. Update output format
When reflection fires, the output should show:
- Original query and retrieval results
- That reflection was triggered
- Reformulated query
- New retrieval results
- Final grounding decision

For --json output, include both attempts in the JSON structure.

### 4. Update evaluation harness (src/evaluation.py)
- Evaluation should work with the reflection loop active
- Add a count of how many queries triggered reflection
- The eval summary should show: "Reflection triggered: X/Y queries"
- GAR and RCR should be computed on the FINAL decision (after reflection if it fired)

### 5. Make reflection toggleable
- Add environment variable: REFLECTION_ENABLED (default "true")
- Add CLI flag: --no-reflection to disable it
- This allows running eval with and without reflection for before/after comparison

## Constraints
- Do NOT add LangChain, LangGraph, or any orchestration framework
- Do NOT add multiple retry attempts — one retry maximum
- Do NOT refactor existing code beyond what's needed for this feature
- Keep the reformulation prompt simple and short
- Use the same OpenAI client already available via OpenAIEmbeddingProvider (or create a minimal chat call alongside it)
- Total new code should be roughly 30-60 lines

## After Implementation
1. Show a concise diff summary
2. Run evaluation WITH reflection at threshold 0.60:
   ```
   $env:GROUNDING_THRESHOLD="0.60"
   python modules/rag-knowledge-pilot/src/main.py --evaluate --reindex
   ```
3. Run evaluation WITHOUT reflection at threshold 0.60:
   ```
   $env:GROUNDING_THRESHOLD="0.60"
   python modules/rag-knowledge-pilot/src/main.py --evaluate --reindex --no-reflection
   ```
4. Show both summaries so we can compare before/after GAR