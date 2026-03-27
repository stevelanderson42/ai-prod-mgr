# Governance-First AI Product Portfolio | Steve Anderson

Senior Product Manager with 20+ years in regulated financial services, including 12 years at Charles Schwab. I'm now focused on AI product management where governance, traceability, and decision accountability must be designed in from the start — not bolted on after deployment. This portfolio demonstrates that approach through six connected modules mirroring how regulated organizations evaluate, prioritize, govern, and deploy AI — culminating in a working retrieval system with measured grounding and refusal performance, and a live agentic orchestration workflow.

---

## The Core Challenge

> **How do you enable real business value from AI while enforcing governance, traceability, and risk controls across the full lifecycle?**

In regulated environments, AI initiatives rarely fail because models are weak.
They fail because governance, accountability, and decision traceability are not designed into the product from day one.

Rather than a collection of disconnected demos, this repository is organized as a **six-module system** that addresses this challenge through concrete product design decisions — not policy documents alone.

---

## The Modules

| Module | Purpose | Status |
|--------|---------|--------|
| [Market Intelligence Monitor](./modules/market-intelligence-monitor/) | Tracks competitor AI releases and regulatory signals to inform strategic prioritization | 🟡 MVP build artifacts |
| [ROI Decision Engine](./modules/roi-engine/) | Structured, risk-aware framework for prioritizing AI opportunities | 🟡 Framework + examples |
| [Requirements Guardrails](./modules/requirements-guardrails/) | Detects ambiguity and compliance risk before model invocation | 🟡 Designed (not yet wired end-to-end) |
| [Compliance Retrieval Assistant](./modules/compliance-retrieval-assistant/) | Governance architecture for citation-first retrieval in high-risk workflows | 🟢 Architecture complete with evidence packages |
| [**RAG Knowledge Pilot**](./modules/rag-knowledge-pilot/) | **Working retrieval system with measured grounding, refusal logic, and agentic reflection** | **🟢 Live deployed — rag-knowledge-pilot.streamlit.app** |
| [**AI Case Triage Workflow**](./modules/agentic-case-triage/) | **LangGraph-orchestrated six-node agentic pipeline with live policy retrieval and execution trace** | **🟢 Live deployed — ai-case-triage-workflow.streamlit.app** |

> Modules 1–4 define the governance architecture. Module 5 executes and measures it. Module 6 orchestrates it agentically.

---

## Featured: RAG Knowledge Pilot (Module 5)

The [RAG Knowledge Pilot](./modules/rag-knowledge-pilot/) is the primary retrieval artifact in this portfolio — a working retrieval system built on the governance principles defined in Modules 1–4.

| Metric | Threshold 0.45 | Threshold 0.60 (no reflection) | Threshold 0.60 (with reflection) |
|---|---:|---:|---:|
| Grounded Answer Rate (GAR) | **100.0%** (11/11) | 72.7% (8/11) | **90.9%** (10/11) |
| Refusal Correctness Rate (RCR) | **100.0%** (4/4) | **100.0%** (4/4) | **100.0%** (4/4) |

Key capabilities:
- OpenAI embedding-based vector retrieval over a compliance policy corpus
- Categorical grounding decisions (GROUNDED / REFUSED) with structured reason codes
- Configurable threshold to explore precision/recall tradeoffs
- Agentic reflection loop that reformulates borderline queries and retries once — improving GAR from 72.7% to 90.9% with zero loss in refusal correctness
- Evaluation harness computing GAR, RCR, and retrieval characteristics across 15 domain-realistic test queries

→ [See full README with diagrams, results, and quick start](./modules/rag-knowledge-pilot/)

---

## Featured: AI Case Triage Workflow (Module 6)

The [AI Case Triage Workflow](./modules/agentic-case-triage/) is the agentic orchestration artifact in this portfolio — a LangGraph-orchestrated six-node pipeline that classifies operational cases, retrieves live compliance policy from the Module 5 RAG corpus, and drives structured routing decisions with a full execution trace.

Key capabilities:
- Six-node LangGraph state machine with shared state flowing through every node
- Live GPT-4o inference at five nodes — classification, entity extraction, priority scoring, internal note generation, and routing decision
- Policy retrieval node directly consumes Module 5's RAG retrieval layer as a workflow tool — creating a true cross-module system dependency
- Full execution trace logging every node's input, output, and rationale
- Five pre-loaded regulatory scenarios (Reg BI, FINRA 2210, KYC/AML) demonstrating adaptive pipeline behavior across case types

→ [See full README with sequence diagram and live demo](./modules/agentic-case-triage/)

---

## Current State: What Runs vs. What's Designed

This portfolio contains both architecture documentation and working code. Being explicit about which is which:

| Layer | Status |
|-------|--------|
| Architecture, config, and contracts | ✅ Defined across all modules |
| RAG Knowledge Pilot — embedding retrieval, grounding, refusal, reflection | ✅ Live deployed with real metrics |
| Compliance Retrieval Assistant — lexical retrieval demo + evidence packages | ✅ Runs locally |
| Grounding thresholds, refusal logic, access control | ✅ Implemented and measured in Module 5; designed in Module 4 |
| AI Case Triage Workflow — LangGraph orchestration, live GPT-4o, RAG integration | ✅ Live deployed with execution trace |
| Cross-module integration (Module 6 → Module 5) | ✅ Implemented — Module 6 consumes Module 5 retrieval layer |

---

## How the Modules Connect

```
Market Intelligence  →  ROI Engine  →  Guardrails  →  Retrieval Assistant  →  RAG Knowledge Pilot  →  AI Case Triage Workflow
(surfaces              (prioritizes)   (enforces       (defines                (executes +              (orchestrates
 opportunities)                         safety)         governance)             measures)                agentically)
```

This mirrors how regulated organizations deploy AI: with governance embedded across the **entire lifecycle**, not bolted on after deployment. Modules 1–4 represent the architecture and governance design. Module 5 operationalizes that design into a working, measured retrieval system. Module 6 orchestrates the full pipeline agentically — consuming Module 5 as a live retrieval tool.

---

## Governance-by-Design Approach

This portfolio applies a **governance-by-design** philosophy grounded in model risk management lifecycle thinking (e.g., SR 11-7 style controls) and responsible AI design patterns.

Rather than treating governance as a post-deployment control, responsible AI principles are embedded at each stage:

- **Opportunity selection** — regulatory-aware prioritization (ROI Engine)
- **Requirements definition** — ambiguity and compliance detection (Guardrails)
- **Model invocation** — routing, escalation, refusal paths (Guardrails)
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
| **Guardrails** | Classification rules, routing logic, escalation design, refusal paths (designed) |
| **Retrieval Assistant** | Policy-as-data configs, ADRs, evaluation scorecard, trace schema, response contract, runnable `minirag.py` demo, sample corpus, evidence package outputs |
| **RAG Knowledge Pilot** | OpenAI embedding retrieval, cosine similarity search, categorical grounding, agentic reflection loop, evaluation harness (GAR/RCR), threshold experimentation, Mermaid diagrams |
| **AI Case Triage Workflow** | LangGraph six-node state machine, live GPT-4o inference, Module 5 RAG integration, execution trace, five regulatory scenarios, Streamlit UI, sequence diagram |

Artifacts emphasize **decision accountability and auditability**, not model optimization.

---

## Progress

| Phase | Focus | Current State |
|-------|-------|---------------|
| Foundation | Opportunity discovery and prioritization frameworks | 🟡 Artifacts and design complete; not fully executable |
| Build | Safety enforcement and grounded retrieval | ✅ Retrieval demo operational; guardrails designed |
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
- Module 5 (RAG Knowledge Pilot) requires an OpenAI API key — see [Module 5 Setup](./modules/rag-knowledge-pilot/#setup)
- Module 6 (AI Case Triage Workflow) requires an OpenAI API key — see [Module 6 Setup](./modules/agentic-case-triage/#setup)
- Module 4 (Compliance Retrieval Assistant) includes a deterministic demo runner that does not require external APIs