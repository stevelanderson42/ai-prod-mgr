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
