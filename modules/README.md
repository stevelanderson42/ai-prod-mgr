# Modules — Regulated AI Workflow Toolkit

This folder contains the six modules of the portfolio. Each is a capability in a system for building and operating LLM applications in regulated environments — from strategic prioritization through governed retrieval and agentic orchestration.

For the full portfolio narrative, positioning, and featured walkthroughs, see the [portfolio root README](../).

---

## The Six Modules

| Module | Status | What It Does |
|--------|--------|--------------|
| 1. [Market Intelligence Monitor](./market-intelligence-monitor/) | 📄 Design artifact | Tracks competitor AI releases, regulatory signals, and industry trends to inform strategic prioritization |
| 2. [ROI Decision Engine](./roi-engine/) | 📄 Design artifact | Risk-aware scoring framework for prioritizing AI initiatives by business value, feasibility, and regulatory complexity |
| 3. [Requirements Guardrails](./requirements-guardrails/) | ⚡ Working classifier + live demo | Pre-invocation control — deterministic routing (PROCEED / CLARIFY / ESCALATE / BLOCK) with an interactive Compare Mode |
| 4. [Compliance Retrieval Assistant](./compliance-retrieval-assistant/) | 📘 Architectural specification | Governance architecture for citation-first retrieval in high-risk workflows requiring grounding, traceability, and audit-ready responses |
| 5. [RAG Knowledge Pilot](./rag-knowledge-pilot/) | ⚡ Working pilot + live demo | Measured retrieval system — 90.9% grounded answer rate, 100% refusal correctness, agentic reflection |
| 6. [AI Case Triage Workflow](./agentic-case-triage/) | ⚡ Working agent + live demo | LangGraph six-node agentic pipeline with live policy retrieval and full execution trace |

---

## How the Modules Relate

The modules fall into two veins:

- **Working systems** (Modules 3, 5, 6) — shipped, tested, deployed, with interactive demos
- **Design and architecture artifacts** (Modules 1, 2, 4) — establish the governance framework the working systems operate within

A specific architectural chain runs through the working layer:

- **Module 4** specifies the governance architecture (control-plane thinking, refusal taxonomy)
- **Module 5** operationalizes and measures it (embedding retrieval, grounding, structured refusal)
- **Module 6** consumes Module 5's retrieval as a tool inside a bounded agentic orchestration

**Module 3** sits alongside this chain as the pre-invocation control surface. It governs what reaches a model at all — complementary to Module 4's governance of what a model retrieves and returns. The two are distinct loci of control, not stages of a pipeline.

---

## Navigating

Each module folder contains its own README with scope, design rationale, tradeoffs, architecture diagrams, and artifacts. Start with the [working systems](./requirements-guardrails/) (Modules 3, 5, 6) for live demos, or the [governance architecture](./compliance-retrieval-assistant/) (Module 4) for the design thinking the system is built on.