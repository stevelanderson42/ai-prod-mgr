# ROI Decision Engine

**Structured Prioritization for Regulated AI Initiatives**

**Status:** 🟢 MVP Complete  
**Module:** 2 of 4 in the Regulated AI Workflow Toolkit

---

## Purpose

The ROI Decision Engine provides a **structured, governance-aware prioritization layer** for AI initiatives in regulated environments.

It evaluates opportunities across **business value, implementation feasibility, and regulatory complexity** simultaneously — making trade-offs explicit *before* organizations commit significant resources or risk.

> **Core insight:**  
> In regulated environments, the hardest AI decision is not *how* to build — it's *whether to proceed at all*.

---

## The Problem This Solves

AI initiatives in regulated organizations frequently stall or fail due to poor prioritization:

- **Compliance risk surfaces late.** Promising initiatives get cancelled after significant investment when governance issues emerge.
- **Executive sponsors lack defensible rationale.** "We should do AI" isn't a strategy — it's a liability.
- **Pilot purgatory is endemic.** Projects linger without clear go/no-go criteria.
- **Governance is treated as a gate, not a partner.** Risk teams are consulted too late to shape decisions.

Traditional ROI models optimize for value and feasibility while **underestimating regulatory complexity**.  
This module corrects that imbalance by treating governance inputs as first-class decision criteria.

> **PM DECISION:**  
> Prioritization without governance inputs is not prioritization — it's hope. This module makes risk visible before momentum builds.

---

## Where It Sits in the Workflow

```
Market Intelligence → [ROI Engine] → Guardrails → RAG Assistant
   (surfaces signals)    (prioritizes)   (validates)   (executes safely)
```

**Upstream:**  
Market Intelligence surfaces competitive pressure, regulatory posture, and peer behavior.

**This module:**  
Evaluates whether an AI opportunity is *worth pursuing now*, based on value, feasibility, and risk.

**Downstream:**  
Approved opportunities flow into Requirements Guardrails for input validation and execution constraints.

> **PM DECISION:**  
> The ROI Engine determines *whether to invest further* — not whether to execute. Prioritization and execution are separate concerns.

---

## Architecture Overview

### Context Diagram (System-in-the-World)

![ROI Decision Engine Context Diagram](docs/diagrams/ROI_Engine_Context_Diagram.PNG)

The context diagram shows how opportunity inputs, governance perspectives, and scoring outputs interact — and how decision artifacts feed downstream controls.

---

### Sequence Diagram (Decision Lifecycle)

![ROI Decision Engine Sequence Diagram](docs/diagrams/ROI_Engine_Sequence_Diagram.PNG)

*End-to-end flow showing how AI opportunities move from intake to a defensible decision memo.*

**High-level steps:**

1. **Opportunity Intake** — Business and technical context captured
2. **Evidence Collection** — Assumptions documented, data sources identified
3. **Multi-Dimensional Scoring** — Value, feasibility, and regulatory complexity assessed
4. **Governance Inputs** — Compliance and risk perspectives incorporated
5. **Decision Memo Generated** — Meeting-ready artifact with rationale
6. **Output Routed Downstream** — Approved opportunities flow to Guardrails

> **Key pattern:**  
> Risk is surfaced *before* execution begins, not after momentum builds.

> **PM DECISION:**  
> If a decision cannot be defended in a memo, it should not proceed to implementation.

---

## Core Concepts

### Three Scoring Dimensions

| Dimension | What It Measures | Direction |
|-----------|------------------|-----------|
| **Business Value** | Revenue impact, cost reduction, customer experience | Higher = stronger case |
| **Implementation Feasibility** | Data readiness, technical complexity, effort | Higher = more feasible |
| **Regulatory Complexity** | Compliance burden, data sensitivity, approval requirements | Higher = more complex |

> **PM DECISION:**  
> Regulatory complexity is scored *alongside* value and feasibility, not as an afterthought. This prevents the "we'll figure out compliance later" failure mode.

Design rationale: **ADR-0004 — ROI Scoring Model Design**

---

### Governance as a Partner

Governance is integrated, not bolted on:

- Compliance inputs captured alongside business inputs
- Assumptions made explicit and documented
- Open regulatory questions surfaced early
- Shared artifact serves business, tech, and risk teams equally

---

## Primary Output: Decision Memo

A meeting-ready Markdown artifact containing:

| Section | Purpose |
|---------|---------|
| **Opportunity Summary** | What we're evaluating and why |
| **Score Breakdown** | Value, feasibility, complexity with rationale |
| **Key Risk Drivers** | What could derail this initiative |
| **Mitigation Assumptions** | What we're assuming will be handled |
| **Open Governance Questions** | Unresolved compliance or risk items |
| **Recommendation** | Pursue / Defer / Explore further |
| **Evidence References** | Traceability to inputs |

Example: `samples/ai-assisted-customer-routing/`

> **PM DECISION:**  
> The memo format ensures decisions are defensible in stakeholder reviews. "We scored it high" isn't sufficient — the *reasoning* must be visible.

---

## What This Module Does NOT Do

This module intentionally does **not**:

- ❌ Validate execution inputs (handled by Guardrails)
- ❌ Enforce runtime policy constraints
- ❌ Perform technical design or modeling
- ❌ Make final approval decisions
- ❌ Replace legal, compliance, or risk review
- ❌ Execute AI workloads
- ❌ Track historical decisions over time (deferred)

> **PM DECISION:**  
> Prioritization and execution are separate concerns — conflating them increases risk. This module answers "should we proceed?" not "how do we proceed?"

---

## MVP Scope

**Included:**
- Manual opportunity intake
- Configurable multi-dimension scoring
- Decision Memo generation
- Evidence traceability stub

**Deferred:**
- Market Intelligence auto-ingestion
- Historical decision tracking
- Sensitivity analysis
- Portfolio-level optimization

See `docs/scope.md` for detailed boundaries.

---

## Repository Map

| Artifact / Path | Purpose |
|-----------------|---------|
| 🟦 **docs/** | Specifications and architecture visualizations |
| `docs/diagrams/` | Visual architecture artifacts |
| `docs/diagrams/ROI_Engine_Context_Diagram.PNG` | System-in-the-world view — external actors and boundaries |
| `docs/diagrams/ROI_Engine_Sequence_Diagram.PNG` | Decision lifecycle flow |
| `docs/scope.md` | MVP boundaries and deferred scope |
| 🟦 **evidence/** | Evidence collection artifacts and traceability |
| 🟦 **intake/** | Opportunity intake templates and captured inputs |
| 🟦 **outputs/** | Generated decision memos |
| 🟦 **samples/** | Worked examples |
| `samples/ai-assisted-customer-routing/` | Complete decision memo example |
| 🟦 **scoring/** | Scoring logic, weights, and rationale |

---

## Success Criteria

This module is complete when:

- [x] Context diagram showing system boundaries
- [x] Sequence diagram showing decision lifecycle
- [x] Three-dimension scoring model defined
- [x] Decision Memo template with all sections
- [x] Sample decision memo (worked example)
- [x] ADRs documenting key design decisions
- [ ] Integration contract with Market Intelligence (upstream)
- [ ] Integration contract with Requirements Guardrails (downstream)

---

## Key PM Decisions Documented

| Decision | Rationale |
|----------|-----------|
| **Three dimensions, not two** | Traditional ROI ignores regulatory complexity; we score it explicitly |
| **Governance inputs at intake** | Risk teams participate in framing, not just approval |
| **Memo as primary artifact** | Forces articulation of reasoning, not just scores |
| **Evidence traceability** | Every score should trace to documented inputs |
| **Categorical recommendations** | "Pursue / Defer / Explore" is actionable; numeric scores alone are not |

---

## Relationship to Other Modules

| Module | Relationship |
|--------|--------------|
| **Market Intelligence** (Module 1) | Feeds opportunity signals and timing context into intake |
| **Requirements Guardrails** (Module 3) | Consumes approved initiatives for input validation |
| **Compliance Retrieval Assistant** (Module 4) | May reference Decision Memos for audit or inquiry |

---

## Closing Note

The ROI Decision Engine is intentionally **judgment-forward**.

Its value is not in automation — it's in making the *reasoning behind prioritization* visible, defensible, and shared across business, technical, and governance stakeholders.

In regulated environments, "we decided to build this" must be followed by "and here's why it was the right call." This module ensures that answer exists.

---

*Part of the Regulated AI Workflow Toolkit — demonstrating governance-first AI product design for regulated industries.*