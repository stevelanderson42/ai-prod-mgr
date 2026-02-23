# RAG Knowledge Pilot — Architecture Decisions

This folder contains Architecture Decision Records (ADRs) for Module 5: RAG Knowledge Pilot.

These decisions were made during the initial build on 2026-02-22 and document the reasoning behind the module's retrieval architecture, storage approach, scope boundaries, and agentic behavior.

## Decision Log

| ADR | Title | Status |
|-----|-------|--------|
| [ADR-001](decisions/ADR-001-phased-retrieval-lexical-baseline-before-embeddings.md) | Phased Retrieval — Lexical Baseline Before Embeddings | Accepted (Phase 1 superseded) |
| [ADR-002](decisions/ADR-002-file-based-vector-index-over-external-database.md) | File-Based Vector Index with Swappable Embedding Provider | Accepted |
| [ADR-003](decisions/ADR-003-retrieval-classification-without-llm-generation.md) | Retrieval and Classification Without LLM Response Generation | Accepted |
| [ADR-004](decisions/ADR-004-bounded-agentic-reflection-single-retry.md) | Bounded Agentic Reflection — Single-Retry Query Reformulation | Accepted |
