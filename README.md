# Regulated AI Workflow Toolkit

A portfolio demonstrating how a Product Manager designs **safe, auditable AI workflows** for regulated environments such as financial services, healthcare, and insurance.

*Designed as a portfolio artifact for senior AI Product Manager roles in regulated industries.*

---

## The Core Challenge

> **How do you enable real business value from AI while enforcing governance, traceability, and risk controls across the full lifecycle?**

Rather than a collection of disconnected demos, this repository is organized as a **four-module system** that addresses this question through product design decisions, not policy documents alone.

---

## The Four Modules

| Module | Purpose | Status |
|--------|---------|--------|
| [Market Intelligence Monitor](./modules/market-intelligence-monitor/) | Tracks competitor AI releases and regulatory signals to inform strategic prioritization | ✅ Complete |
| [ROI Decision Engine](./modules/roi-engine/) | Structured, risk-aware scoring model for prioritizing AI opportunities | ✅ Complete |
| [Requirements Guardrails](./modules/requirements-guardrails/) | Identifies ambiguity and compliance concerns before model invocation | 🔲 Planned |
| [Compliance RAG Assistant](./modules/compliance-retrieval-assistant/) | Citation-first retrieval for high-risk workflows requiring traceability | 🔲 Planned |

---

## How the Modules Connect
```
Market Intelligence    →    ROI Engine    →    Guardrails    →    RAG Assistant
 (surfaces opportunities)   (prioritizes)      (enforces safety)   (delivers outputs)
```

This structure mirrors how regulated organizations build AI-enabled products: with governance embedded across the **full lifecycle**, not bolted on after deployment.

---

## Governance-by-Design Approach

This portfolio applies a **governance-by-design** philosophy aligned with established AI frameworks (Microsoft AI-900, Google Responsible AI).

Rather than treating governance as a post-deployment control, the system embeds responsible AI principles across:

- **Opportunity selection** — risk-aware prioritization (ROI Engine)
- **Requirements definition** — ambiguity and compliance detection (Guardrails)
- **Model invocation** — routing, escalation, refusal (Guardrails)
- **Output grounding** — citation-first retrieval and traceability (RAG Assistant)

---

## Repository Structure
```
/modules/                  → The four-module system (start here)
/architecture/             → System-level decisions and ADRs
/evaluation/               → Shared evaluation framework
/prompt-experiments/       → Structured experiments for testing behaviors
```

Each module has its own README with scope, design rationale, and artifacts.

---

## Alignment with Responsible AI Frameworks

**AI-900 Concepts:**
- Responsible AI principles → implemented via guardrails, routing, and refusal logic
- Model lifecycle → reflected across opportunity intake, evaluation, and deployment artifacts

**Google Responsible AI:**
- Fairness, safety, and accountability treated as *product constraints*, not model features
- Human review and escalation paths explicit for high-risk use cases

---

## Status

| Phase | Modules | Timeline |
|-------|---------|----------|
| ✅ Foundation | Market Intelligence, ROI Engine | Complete |
| 🔲 Build | Guardrails, RAG Assistant | In Progress |
| 🔲 Polish | Integration, case studies | Planned |

---

## Local Setup

- API keys stored in `.env` (not committed)
- See `requirements.txt` for Python dependencies