# Architecture — Requirements Guardrails

This folder contains architecture decision records (ADRs) and system diagrams for the Requirements Guardrails module.

---

## Architecture Decision Records

| ADR | Title | Status |
|-----|-------|--------|
| [ADR-001](./ADR-001-routing-logic.md) | Deterministic Routing Logic | Accepted |
| ADR-002 | Escalation Design | Planned |

---

## Diagrams

| Diagram | Description |
|---------|-------------|
| [Context Diagram](./Module%203%20-%20Requirements%20Guardrails%20-%20Context%20Diagram.PNG) | System position and internal flow |

---

## ADR Format

Each ADR follows this structure:

- **Context** — What situation requires a decision?
- **Decision** — What did we decide?
- **Rationale** — Why this choice over alternatives?
- **Alternatives Considered** — What else was evaluated?
- **Consequences** — What are the tradeoffs?
- **Implementation Notes** — How does this affect the build?

---

## Key Architectural Principles

These principles guide all architectural decisions in this module:

1. **Deterministic over probabilistic** — Routing decisions use rules, not models
2. **Explainability first** — Every decision must be auditable
3. **Fail-safe defaults** — Unknown inputs escalate to humans
4. **Interface-first design** — Define contracts before implementation
5. **Compliance reviewable** — Non-technical stakeholders can validate logic