# Verification Index

This document maps portfolio claims to supporting artifacts, enabling verification of authentic work and decision-making. It addresses a key concern in AI-adjacent portfolios: distinguishing genuine skill development from AI-generated content.

**Verification approach:**
- Every claim links to concrete artifacts
- Artifacts include commit history showing iterative development
- Decision rationale is documented in ADRs and inline comments
- Architecture diagrams, configs, and contracts demonstrate depth beyond surface-level generation

---

## Toolkit Overview

| Claim | Evidence |
|-------|----------|
| Four-module integrated system | [Root README](./README.md), [modules/](./modules/) directory structure |
| Governance-first design philosophy | Module READMEs, ADRs, threat models across all modules |
| Regulatory domain expertise | FINRA/SEC/SR 11-7 references throughout artifacts |
| System-level thinking | Context diagrams, component diagrams, sequence diagrams |

---

## Module 4: Compliance Retrieval Assistant

**Status:** 🟡 Architecture Complete

| Claim | Evidence |
|-------|----------|
| Governance-first RAG architecture | [README.md](./modules/compliance-retrieval-assistant/README.md), [Context Diagram](./modules/compliance-retrieval-assistant/docs/diagrams/Compliance-Retrieval-Assistant%20Context%20Diagram.PNG) |
| 8-component pipeline design | [component-design.md](./modules/compliance-retrieval-assistant/architecture/component-design.md), [Component Diagram](./modules/compliance-retrieval-assistant/docs/diagrams/Compliance-Retrieval-Assistant%20Component%20Diagram.png) |
| Policy-as-data pattern | [config/](./modules/compliance-retrieval-assistant/config/) directory, [ADR-002](./modules/compliance-retrieval-assistant/architecture/decisions/ADR-002-refusal-taxonomy-as-configuration.md) |
| Dual contract design (user + auditor) | [response-contract.md](./modules/compliance-retrieval-assistant/docs/response-contract.md), [trace-schema.md](./modules/compliance-retrieval-assistant/docs/trace-schema.md) |
| Grounding over confidence scores | [ADR-001](./modules/compliance-retrieval-assistant/architecture/decisions/ADR-001-grounding-status-over-confidence-scores.md) |
| 5-code refusal taxonomy | [refusal-taxonomy.yaml](./modules/compliance-retrieval-assistant/config/refusal-taxonomy.yaml) |
| Role-based access control design | [role-permissions.yaml](./modules/compliance-retrieval-assistant/config/role-permissions.yaml) |
| Corpus versioning for audit | [corpus-registry.yaml](./modules/compliance-retrieval-assistant/config/corpus-registry.yaml) |
| Threat modeling | [threat-model.md](./modules/compliance-retrieval-assistant/docs/threat-model.md) |
| Evaluation framework | [scorecard.md](./modules/compliance-retrieval-assistant/evaluation/scorecard.md) |
| Request lifecycle documentation | [Sequence Diagram](./modules/compliance-retrieval-assistant/docs/diagrams/Compliance-Retrieval-Assistant%20Sequence%20Diagram.PNG) |

**Key decisions documented:**
- ADR-001: Why categorical grounding status instead of numeric confidence
- ADR-002: Why refusal logic lives in config, not code

---

## Module 3: Requirements Guardrails

**Status:** 🟢 Complete

| Claim | Evidence |
|-------|----------|
| Pre-flight validation for AI workflows | [README.md](./modules/requirements-guardrails/README.md) |
| Risk classification system | [config/](./modules/requirements-guardrails/config/) |
| FINRA 2210 alignment | Regulatory references in documentation |
| Deterministic routing before model invocation | Architecture documentation |

---

## Module 2: ROI Decision Engine

**Status:** 🟢 Complete

| Claim | Evidence |
|-------|----------|
| Risk-weighted scoring framework | [README.md](./modules/roi-decision-engine/README.md) |
| Multi-factor prioritization | Scoring logic and weights documentation |
| Enterprise constraint modeling | Regulatory and operational factors |

---

## Module 1: Market Intelligence Monitor

**Status:** 🟢 Complete

| Claim | Evidence |
|-------|----------|
| Competitive signal tracking | [README.md](./modules/market-intelligence-monitor/README.md) |
| Strategic input for prioritization | Integration with ROI Engine |

---

## Cross-Cutting Evidence

### Architectural Decision Records (ADRs)

| ADR | Decision | Location |
|-----|----------|----------|
| ADR-001 | Grounding Status over Confidence Scores | [Module 4](./modules/compliance-retrieval-assistant/architecture/decisions/ADR-001-grounding-status-over-confidence-scores.md) |
| ADR-002 | Refusal Taxonomy as Configuration | [Module 4](./modules/compliance-retrieval-assistant/architecture/decisions/ADR-002-refusal-taxonomy-as-configuration.md) |

### Diagrams

| Diagram | Type | Location |
|---------|------|----------|
| CRA Context Diagram | System-in-the-world | [Module 4](./modules/compliance-retrieval-assistant/docs/diagrams/) |
| CRA Component Diagram | Internal structure | [Module 4](./modules/compliance-retrieval-assistant/docs/diagrams/) |
| CRA Sequence Diagram | Request lifecycle | [Module 4](./modules/compliance-retrieval-assistant/docs/diagrams/) |

### Configuration as Documentation

| Config File | Documents | Location |
|-------------|-----------|----------|
| policy-constraints.yaml | Runtime behavior thresholds | [Module 4](./modules/compliance-retrieval-assistant/config/policy-constraints.yaml) |
| refusal-taxonomy.yaml | When and how to refuse | [Module 4](./modules/compliance-retrieval-assistant/config/refusal-taxonomy.yaml) |
| role-permissions.yaml | Access control model | [Module 4](./modules/compliance-retrieval-assistant/config/role-permissions.yaml) |
| corpus-registry.yaml | Versioning and audit | [Module 4](./modules/compliance-retrieval-assistant/config/corpus-registry.yaml) |

---

## Verification Methods

### For Reviewers

1. **Check commit history** — Artifacts show iterative development, not single-commit generation
2. **Read ADRs** — Decision rationale demonstrates genuine reasoning, not template filling
3. **Examine configs** — Detailed, internally consistent configurations show domain understanding
4. **Review cross-references** — Artifacts reference each other accurately, showing system thinking
5. **Look for non-obvious choices** — "What we don't do" sections, rejected alternatives, tradeoffs

### Authenticity Signals

| Signal | What It Demonstrates |
|--------|---------------------|
| PM DECISION callouts | Explicit rationale for choices |
| "Non-Goals" sections | Knowing what to exclude |
| Alternatives Considered | Evaluated options before deciding |
| Regulatory anchors | Domain expertise, not generic content |
| Internal consistency | Configs, contracts, and docs align |

---

## Planned Additions

As the toolkit matures, this index will expand to include:

- [ ] Evaluation run results with timestamps
- [ ] Sample corpus documents for CRA
- [ ] Test case execution logs
- [ ] Implementation code with inline documentation

---

*Last updated: 2026-01-05*

