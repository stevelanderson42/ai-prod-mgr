# Governance-First AI Product Portfolio | Steve L. Anderson

Senior Product Manager with 20+ years in regulated financial services, including 12 years at Charles Schwab, now focused on AI product management for environments where governance, traceability, and decision accountability have to be designed in from the start rather than added after deployment.

This portfolio is a six-module system that mirrors how regulated organizations evaluate, prioritize, govern, and deploy AI across the full lifecycle. Three modules are live and interactive: a pre-invocation guardrail classifier, a measured retrieval system, and an agentic orchestration workflow. The other three are design and architecture artifacts that establish the governance framework the working modules operate within.

---

## The Core Challenge

> **How do you enable real business value from AI while enforcing governance, traceability, and risk controls across the full lifecycle?**

In regulated environments, AI initiatives rarely fail because the models are weak. They fail because governance, accountability, and decision traceability weren't designed into the product from day one — and retrofitting them after deployment is expensive, slow, and often incomplete.

This portfolio addresses that gap as a six-module system. Each module is a concrete product-design decision about how governance gets built in at a specific stage of the lifecycle — from opportunity selection through agentic orchestration.

---

## The Modules

| Module | Status | Purpose |
|--------|--------|---------|
| 1. [Market Intelligence Monitor](./modules/market-intelligence-monitor/) | 📄 Design artifact | Tracks competitor AI releases and regulatory signals to inform strategic prioritization |
| 2. [ROI Decision Engine](./modules/roi-engine/) | 📄 Design artifact | Structured, risk-aware framework for prioritizing AI opportunities |
| 3. [**Requirements Guardrails**](./modules/requirements-guardrails/) | ⚡ **Working classifier + live demo** | Pre-invocation control — deterministic routing (PROCEED / CLARIFY / ESCALATE / BLOCK) with an interactive Compare Mode that exposes the governance mechanisms |
| 4. [Compliance Retrieval Assistant](./modules/compliance-retrieval-assistant/) | 📘 Architectural specification | Governance architecture for citation-first retrieval in high-risk workflows |
| 5. [**RAG Knowledge Pilot**](./modules/rag-knowledge-pilot/) | ⚡ **Working pilot + live demo** | Measured retrieval system — 90.9% grounded answer rate, 100% refusal correctness, agentic reflection |
| 6. [**AI Case Triage Workflow**](./modules/agentic-case-triage/) | ⚡ **Working agent + live demo** | LangGraph six-node agentic pipeline with live policy retrieval and full execution trace |

> Modules 1, 2, and 4 establish the governance architecture. Modules 3, 5, and 6 are live, interactive systems that operate within it.

---

## Featured: Requirements Guardrails (Module 3)

The [Requirements Guardrails classifier](./modules/requirements-guardrails/) is the pre-invocation control layer of the portfolio — a deterministic classifier that decides whether an AI request can safely proceed before any model is invoked, returning one of four routing decisions: PROCEED, CLARIFY, ESCALATE, or BLOCK.

[![Live Demo](https://img.shields.io/badge/Live_Demo-requirements--guardrails.streamlit.app-FF4B4B?logo=streamlit)](https://requirements-guardrails.streamlit.app)

What makes it distinct is the **Compare Mode** in the live demo: a single toggle that runs the classifier with and without its two governance mechanisms, side by side, so a reviewer can see exactly how the architecture changes the outcome. The same query that routes to ESCALATE under literal priority routing routes to CLARIFY once the context-first override applies — and the demo shows both, with the relevant architectural decision linked inline.

Key capabilities:
- Deterministic routing with no general-purpose LLM at the decision boundary — every classification traces to a rule firing or a documented mechanism
- Context-first override (ADR-003) — suppresses premature escalation when the request lacks the context a human reviewer would need anyway
- Produce-intent upgrade (ADR-004) — distinguishes a request that *contains* prohibited language from one that asks the system to *generate* it, and routes them differently
- Full audit trail on every decision, including rules suppressed by the override — the transparency a compliance reviewer or auditor would expect
- Deliberately scoped v1 (ADR-005) — three of five guardrail categories implemented, the other two deferred with documented engineering-complexity and duty-of-care reasoning
- 21 passing tests covering routing behavior and mechanism effects

→ [See full README with architecture diagrams, ADR index, and Compare Mode walkthrough](./modules/requirements-guardrails/)

---

## Featured: RAG Knowledge Pilot (Module 5)

The [RAG Knowledge Pilot](./modules/rag-knowledge-pilot/) is the measured retrieval artifact of the portfolio — a working retrieval system that operationalizes the governance principles specified in Module 4, and the layer that Module 6 consumes as a tool.

[![Live Demo](https://img.shields.io/badge/Live_Demo-rag--knowledge--pilot.streamlit.app-FF4B4B?logo=streamlit)](https://rag-knowledge-pilot.streamlit.app)

| Metric | Threshold 0.45 | Threshold 0.60 (no reflection) | Threshold 0.60 (with reflection) |
|---|---:|---:|---:|
| Grounded Answer Rate (GAR) | **100.0%** (11/11) | 72.7% (8/11) | **90.9%** (10/11) |
| Refusal Correctness Rate (RCR) | **100.0%** (4/4) | **100.0%** (4/4) | **100.0%** (4/4) |

Key capabilities:
- OpenAI embedding-based vector retrieval over a compliance policy corpus
- Categorical grounding decisions (GROUNDED / REFUSED) with structured reason codes — refusal treated as a first-class output, not an error
- Configurable grounding threshold to explore the precision/recall tradeoff
- Agentic reflection loop that reformulates borderline queries and retries once — improving GAR from 72.7% to 90.9% with zero loss in refusal correctness
- Evaluation harness computing GAR, RCR, and retrieval characteristics across 15 domain-realistic test queries

→ [See full README with diagrams, results, and quick start](./modules/rag-knowledge-pilot/)

---

## Featured: AI Case Triage Workflow (Module 6)

The [AI Case Triage Workflow](./modules/agentic-case-triage/) is the agentic orchestration artifact of the portfolio — a LangGraph six-node pipeline that classifies operational cases, retrieves live compliance policy from Module 5's RAG layer, and drives structured routing decisions with a full execution trace. It is the most downstream layer of the architectural chain: Module 4 specifies the governance, Module 5 operationalizes and measures it, Module 6 consumes it as a tool inside a bounded orchestration.

[![Live Demo](https://img.shields.io/badge/Live_Demo-ai--case--triage--workflow.streamlit.app-FF4B4B?logo=streamlit)](https://ai-case-triage-workflow.streamlit.app)

Key capabilities:
- Six-node LangGraph state machine with shared state flowing through every node
- Live GPT-4o inference at five nodes — classification, entity extraction, priority scoring, internal note generation, and routing decision
- Policy retrieval node consumes Module 5's RAG layer as a live workflow tool — a real cross-module dependency, not a standalone demo
- Full execution trace logging every node's input, output, and rationale — the audit trail is the architecture, not an afterthought
- Five regulatory scenarios (Reg BI, FINRA 2210, KYC/AML) exercising different pipeline paths across case types

→ [See full README with sequence diagram and live demo](./modules/agentic-case-triage/)

---

## How the Modules Connect

```
Market Intelligence  →  ROI Engine  →  Guardrails  →  Retrieval Assistant  →  RAG Knowledge Pilot  →  AI Case Triage Workflow
(surfaces              (prioritizes)   (pre-invocation (specifies              (operationalizes +       (orchestrates
 opportunities)                         control)        governance)             measures)                agentically)
```

The sequence mirrors how regulated organizations deploy AI: governance embedded across the lifecycle rather than added after deployment. The modules also fall into two veins. **Modules 1, 2, and 4** are design and architecture artifacts — they establish the framework. **Modules 3, 5, and 6** are live, interactive systems that operate within it.

A specific chain runs through the working layer: Module 4 specifies the governance architecture, Module 5 operationalizes and measures it, and Module 6 consumes Module 5's retrieval as a tool inside a bounded orchestration. Module 3 sits alongside this chain as the pre-invocation control surface — it governs what reaches a model at all, complementary to Module 4's governance of what a model retrieves and returns.

---

## Governance-by-Design Approach

This portfolio applies a **governance-by-design** philosophy grounded in model risk management lifecycle thinking (e.g., SR 11-7 style controls) and responsible AI design patterns.

Rather than treating governance as a post-deployment control, responsible AI principles are embedded at each stage:

- **Opportunity selection** — regulatory-aware prioritization (ROI Engine)
- **Requirements definition** — ambiguity and compliance detection (Guardrails, live)
- **Model invocation** — deterministic routing, escalation, and refusal paths with an interactive Compare Mode (Guardrails, live)
- **Output grounding** — citation-first retrieval with traceable sources (Retrieval Assistant)
- **Measured execution** — evaluation-driven iteration with real metrics (RAG Knowledge Pilot)
- **Agentic orchestration** — bounded multi-step workflows with full execution trace (AI Case Triage Workflow)

---

## Regulatory Context

AI products in regulated industries operate within external constraints long before models are selected or features are shipped. This portfolio treats regulation as shared context that informs product design decisions such as auditability, traceability, escalation paths, and defensible outputs. To avoid duplicating legal text across modules, regulatory considerations are maintained centrally and referenced where relevant.

The [/regulatory-governance/](./regulatory-governance/) folder documents representative regulations that influenced system design decisions across modules:

| Regulation | What It Governs | Design Implications |
|------------|-----------------|---------------------|
| [SR 11-7](./regulatory-governance/finserv/sr-11-7-model-risk.md) | Model risk management | Documentation standards, validation artifacts |
| [FINRA 2210](./regulatory-governance/finserv/finra-2210-communications.md) | Communications with the public | Fair-and-balanced language checks in Guardrails |
| [SEC 17a-4](./regulatory-governance/finserv/sec-17a-4-books-records.md) | Books and records | Trace schema, immutable audit trails |
| [Reg BI](./regulatory-governance/finserv/reg-bi-suitability.md) | Suitability requirements | Mandatory clarification or refusal paths |

---

## Repository Structure

```
/modules/                  → The six-module system (start here)
/regulatory-governance/    → Regulations informing design decisions
/session-prompts/          → Claude Code session prompts and structured prompt experiments
/architecture/             → System-level decisions and ADRs
/evaluation/               → Shared evaluation framework
/case-studies/             → Decision narratives from module development
EXECUTION_LOG.md           → Weekly progress through the 17-week plan
```

Each module includes its own README documenting scope, design rationale, tradeoffs, and artifacts.

---

## Key Artifacts by Module

| Module | Representative Artifacts |
|--------|--------------------------|
| **Market Intelligence** | Signal ingestion pipeline design, categorization logic, ADRs |
| **ROI Engine** | Scoring framework, regulatory risk weighting, sample evaluations |
| **Guardrails** | Working classifier (3 categories), deterministic routing, context-first override + produce-intent upgrade mechanisms, Compare Mode UI, 21 passing tests, 5 ADRs, live Streamlit demo |
| **Retrieval Assistant** | Policy-as-data configs, ADRs, evaluation scorecard, trace schema, response contract, runnable `minirag.py` demo, sample corpus, evidence package outputs |
| **RAG Knowledge Pilot** | OpenAI embedding retrieval, cosine similarity search, categorical grounding, agentic reflection loop, evaluation harness (GAR/RCR), threshold experimentation, Mermaid diagrams |
| **AI Case Triage Workflow** | LangGraph six-node state machine, live GPT-4o inference, Module 5 RAG integration, execution trace, five regulatory scenarios, Streamlit UI, sequence diagram |

Artifacts emphasize **decision accountability and auditability**, not model optimization.

---

## Progress

| Phase | Focus | Current State |
|-------|-------|---------------|
| Foundation | Opportunity discovery and prioritization frameworks | 📄 Design artifacts complete (Modules 1–2) |
| Build | Pre-invocation control and grounded retrieval | ⚡ Guardrails classifier live with Compare Mode; retrieval operational |
| Execute | Working AI feature with measured performance | ✅ RAG Knowledge Pilot live with real metrics |
| Orchestrate | Agentic workflow with cross-module integration | ✅ AI Case Triage Workflow live with execution trace |

---

## Credentials & Continuing Education

Formal certifications and applied training completed during this transition:

| Credential | Issuer | Status |
|---|---|---|
| Azure AI-900 — AI Fundamentals | Microsoft | ✅ Completed |
| AI Essentials | Google | ✅ Completed |
| Prompt Engineering for Developers | DeepLearning.AI | ✅ Completed |
| AI Agentic Design Patterns with AutoGen | DeepLearning.AI | ✅ Completed |
| AI Agents in LangGraph | DeepLearning.AI | ✅ Completed |

---

## Local Setup

- See `requirements.txt` for Python dependencies
- Module 3 (Requirements Guardrails) runs with no external API — deterministic classifier; `streamlit run app.py` from the module folder, or use the [live demo](https://requirements-guardrails.streamlit.app)
- Module 4 (Compliance Retrieval Assistant) includes a deterministic demo runner that does not require external APIs
- Module 5 (RAG Knowledge Pilot) requires an OpenAI API key — see [Module 5 Setup](./modules/rag-knowledge-pilot/#setup)
- Module 6 (AI Case Triage Workflow) requires an OpenAI API key — see [Module 6 Live Demo](./modules/agentic-case-triage/#live-demo)