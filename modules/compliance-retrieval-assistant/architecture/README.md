# Architecture

**Design documentation for the Compliance Retrieval Assistant**

---

## Purpose

This folder contains architectural documentation that explains *how* the CRA is designed and *why* key decisions were made. It serves both as implementation guidance and as evidence of deliberate, governance-aware design thinking.

---

## Contents

```
architecture/
├── README.md              # This file
├── component-design.md    # 8-component pipeline specification
└── decisions/
    ├── ADR-001-grounding-status-over-confidence-scores.md
    └── ADR-002-refusal-taxonomy-as-configuration.md
```

---

## Component Design

**[component-design.md](component-design.md)** — The internal decomposition of the CRA into 8 pipeline components.

### Pipeline Overview

```
Query → Preprocess → Retrieve → Ground → Build Prompt → Generate → Decide → Assemble → Response
                                                              │
                                               [Trace Writer throughout]
```

### Components

| Component | Location | Responsibility |
|-----------|----------|----------------|
| Query Preprocessor | src/preprocess/ | Normalize, extract terms, detect injection |
| Retrieval Client | src/retrieval/ | Hybrid search, access control, threshold filtering |
| Grounding Checker | src/grounding/ | Assess coverage, detect conflicts |
| Prompt Builder | src/prompt/ | Assemble instructions + context + passages |
| LLM Provider | src/llm/ | Model-agnostic API interface |
| Refusal Gate | src/decision/ | Final decision logic, post-generation validation |
| Response Assembler | src/response/ | Package response per contract |
| Trace Writer | src/logging/ | Continuous audit logging |

Each component specification includes:
- Inputs and outputs
- Operations performed
- Failure modes and handling
- PM decision rationale

---

## Architectural Decision Records (ADRs)

The `decisions/` folder contains ADRs documenting significant design choices.

### What's an ADR?

A lightweight record of a decision that:
- Had multiple options
- Has lasting consequences
- Is worth explaining to future readers

### Current ADRs

| ADR | Decision | Status |
|-----|----------|--------|
| [ADR-001](decisions/ADR-001-grounding-status-over-confidence-scores.md) | Use categorical grounding status, not numeric confidence scores | Accepted |
| [ADR-002](decisions/ADR-002-refusal-taxonomy-as-configuration.md) | Define refusal logic in config (policy-as-data), not code | Accepted |

### ADR Format

Each ADR follows a standard structure:

1. **Context** — What problem we faced
2. **Decision** — What we chose
3. **Rationale** — Why we chose it (multiple reasons)
4. **Consequences** — Positive, negative, and mitigations
5. **Alternatives Considered** — What we rejected and why

---

## Diagrams

Visual architecture documentation lives in [docs/diagrams/](../docs/diagrams/):

| Diagram | Shows |
|---------|-------|
| Context Diagram | System-in-the-world — external actors and boundaries |
| Component Diagram | Internal structure — 8 components and data flow |
| Sequence Diagram | Request lifecycle — temporal flow through pipeline |

---

## Design Principles

The CRA architecture follows these principles:

| Principle | Implementation |
|-----------|----------------|
| **Retrieval before generation** | Grounding Checker runs before LLM |
| **Citation by default** | Every claim must map to a source |
| **Refusal over speculation** | When in doubt, refuse with guidance |
| **Grounding status over confidence** | Categorical, not numeric (ADR-001) |
| **Policy as data** | Refusal logic in config, not code (ADR-002) |
| **Trace before respond** | Audit log committed before response returned |
| **Model-agnostic** | LLM Provider interface supports multiple vendors |

---

## Future ADR Candidates

Decisions that may warrant ADRs as implementation progresses:

- [ ] Choice of vector store (ChromaDB vs. Pinecone vs. others)
- [ ] Chunking strategy for compliance documents
- [ ] Escalation queue implementation
- [ ] Evidence package storage approach

---

## Related Artifacts

- [docs/diagrams/](../docs/diagrams/) — Visual architecture
- [docs/response-contract.md](../docs/response-contract.md) — Output contract
- [docs/trace-schema.md](../docs/trace-schema.md) — Audit contract
- [config/](../config/) — Policy configuration files
- [src/](../src/) — Implementation stubs (organized by component)

---

*This folder documents architectural decisions and design rationale for the Compliance Retrieval Assistant.*