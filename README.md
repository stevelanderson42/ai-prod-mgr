# Regulated AI Workflow Toolkit

A portfolio demonstrating how a Product Manager designs **safe, auditable AI workflows** for regulated environments such as financial services, healthcare, and insurance.

*Designed as a portfolio artifact for senior AI Product Manager roles in regulated industries.*

---

## The Core Challenge

> **How do you enable real business value from AI while enforcing governance, traceability, and risk controls across the full lifecycle?**

In regulated environments, AI initiatives rarely fail because models are weak.  
They fail because governance, accountability, and decision traceability are not designed into the product from day one.

Rather than a collection of disconnected demos, this repository is organized as a **four-module system** that addresses this challenge through concrete product design decisions — not policy documents alone.

---

## The Four Modules

| Module | Purpose | Status |
|--------|---------|--------|
| [Market Intelligence Monitor](./modules/market-intelligence-monitor/) | Tracks competitor AI releases and regulatory signals to inform strategic prioritization | ✅ MVP Complete |
| [ROI Decision Engine](./modules/roi-engine/) | Structured, risk-aware scoring model for prioritizing AI opportunities | ✅ MVP Complete |
| [Requirements Guardrails](./modules/requirements-guardrails/) | Detects ambiguity and compliance risk before model invocation | ✅ MVP Complete |
| [Compliance RAG Assistant](./modules/compliance-retrieval-assistant/) | Citation-first retrieval for high-risk workflows requiring traceability | 🔄 Architecture Complete |

> Each module is intentionally scoped as an MVP — the **smallest defensible, auditable system** that a regulated organization could realistically approve as a first iteration.

---

## How the Modules Connect

```
Market Intelligence    →    ROI Engine    →    Guardrails    →    RAG Assistant
 (surfaces opportunities)   (prioritizes)      (enforces safety)   (delivers grounded outputs)
```

This mirrors how regulated organizations actually deploy AI: with governance embedded across the **entire lifecycle**, not bolted on after deployment.

---

## Governance-by-Design Approach

This portfolio applies a **governance-by-design** philosophy aligned with established AI frameworks (Microsoft AI-900, Google Responsible AI).

Rather than treating governance as a post-deployment control, responsible AI principles are embedded at each stage:

- **Opportunity selection** — regulatory-aware prioritization (ROI Engine)
- **Requirements definition** — ambiguity and compliance detection (Guardrails)
- **Model invocation** — routing, escalation, refusal logic (Guardrails)
- **Output grounding** — citation-first retrieval with traceable sources (RAG Assistant)

---

## Regulatory Context

AI products in regulated industries are constrained by external obligations long before models are selected.

The [/regulatory-context/](./regulatory-context/) folder documents the **specific regulations that shaped system design decisions**:

| Regulation | What It Governs | Design Implications |
|------------|-----------------|---------------------|
| [SR 11-7](./regulatory-context/finserv/sr-11-7-model-risk.md) | Model risk management | Documentation standards, validation artifacts |
| [FINRA 2210](./regulatory-context/finserv/finra-2210-communications.md) | Communications with the public | Fair-and-balanced language checks in Guardrails |
| [SEC 17a-4](./regulatory-context/finserv/sec-17a-4-books-records.md) | Books and records | Trace schema, immutable audit trails |
| [Reg BI](./regulatory-context/finserv/reg-bi-suitability.md) | Suitability requirements | Mandatory clarification or refusal paths |

These constraints are treated as **product inputs**, not after-the-fact compliance checks.

---

## Repository Structure

```
/modules/                  → The four-module system (start here)
/regulatory-context/       → Regulations informing design decisions
/architecture/             → System-level decisions and ADRs
/evaluation/               → Shared evaluation framework
/case-studies/             → Decision narratives from module development
/prompt-experiments/       → Structured experiments testing behavior
EXECUTION_LOG.md           → Weekly progress through the 17-week plan
```

Each module includes its own README documenting scope, design rationale, tradeoffs, and artifacts.

---

## Key Artifacts by Module

| Module | Representative Artifacts |
|--------|--------------------------|
| **Market Intelligence** | Signal ingestion pipeline, categorization logic, ADRs |
| **ROI Engine** | Scoring framework, regulatory risk weighting, sample evaluations |
| **Guardrails** | Classification rules, routing logic, escalation design, refusal paths |
| **RAG Assistant** | Policy configuration files, ADRs, evaluation scorecard, trace schema, response contract |

Artifacts emphasize **decision accountability and auditability**, not model optimization.

---

## Status Overview

| Phase | Scope | Status |
|-------|-------|--------|
| Foundation | Market Intelligence, ROI Engine | ✅ MVP Complete |
| Build | Guardrails, RAG Assistant (Architecture & Evaluation) | ✅ MVP Complete |
| Polish | Integration, Expanded Case Studies | 🔄 In Progress |

Future iterations focus on **integration depth and narrative clarity**, not expanding model complexity.

---

## Supporting Credentials

Formal training completed during this transition, reinforcing the governance and lifecycle concepts applied throughout this repository:

- Microsoft Azure AI-900 (Score: 794)
- Google Cloud Generative AI
- DeepLearning.AI Prompt Engineering

---

## Local Setup

- API keys stored in `.env` (not committed)
- See `requirements.txt` for Python dependencies