# Regulated AI Workflow Architecture & Demos

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
| [Market Intelligence Monitor](./modules/market-intelligence-monitor/) | Tracks competitor AI releases and regulatory signals to inform strategic prioritization | 🟡 MVP build artifacts (varies by module) |
| [ROI Decision Engine](./modules/roi-engine/) | Structured, risk-aware framework for prioritizing AI opportunities | 🟡 Framework + examples (non-executable scoring) |
| [Requirements Guardrails](./modules/requirements-guardrails/) | Detects ambiguity and compliance risk before model invocation | 🟡 Designed (not yet wired end-to-end) |
| [Compliance Retrieval Assistant](./modules/compliance-retrieval-assistant/) | Citation-first retrieval for high-risk workflows requiring traceability | 🟢 Runnable demo (lexical retrieval + evidence package) |

> Each module is intentionally scoped as an MVP — the **smallest defensible, auditable system** that a regulated organization could realistically approve as a first iteration.

---

## Current State: What Runs vs. What's Designed

This portfolio contains both architecture documentation and working code. Being explicit about which is which:

| Layer | Status |
|-------|--------|
| Architecture, config, and contracts | ✅ Defined across all four modules |
| Compliance Retrieval Assistant — minimal retrieval demo | ✅ Runs locally and generates evidence packages |
| Grounding thresholds, refusal logic, access control | 🧩 Designed + evaluated, not implemented in the demo runner yet |
| Cross-module integration | 🔄 In progress |

The compliance-retrieval-assistant module includes a [minimal runnable demo](./modules/compliance-retrieval-assistant/README.md#minimal-runnable-demo) that loads a 10-document sample corpus, performs deterministic lexical retrieval, and writes a full evidence package (user response, auditor response, trace, and a human-readable bundle). Six evaluation test cases were executed against the demo runner to surface ambiguity, insufficient grounding, scope gaps, and policy-blocked scenarios. The same module's evaluation scorecard is used to document where retrieval alone is insufficient.

---

## How the Modules Connect

```
Market Intelligence    →    ROI Engine    →    Guardrails    →    Retrieval Assistant
 (surfaces opportunities)   (prioritizes)      (enforces safety)   (delivers grounded outputs)
```

This mirrors how regulated organizations deploy AI: with governance embedded across the **entire lifecycle**, not bolted on after deployment.

---

## Governance-by-Design Approach

This portfolio applies a **governance-by-design** philosophy grounded in model risk management lifecycle thinking (e.g., SR 11-7 style controls) and responsible AI design patterns.

Rather than treating governance as a post-deployment control, responsible AI principles are embedded at each stage:

- **Opportunity selection** — regulatory-aware prioritization (ROI Engine)
- **Requirements definition** — ambiguity and compliance detection (Guardrails)
- **Model invocation** — routing, escalation, refusal paths (Guardrails)
- **Output grounding** — citation-first retrieval with traceable sources (Retrieval Assistant)

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
/modules/                  → The four-module system (start here)
/regulatory-governance/    → Regulations informing design decisions
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
| **Market Intelligence** | Signal ingestion pipeline design, categorization logic, ADRs |
| **ROI Engine** | Scoring framework, regulatory risk weighting, sample evaluations |
| **Guardrails** | Classification rules, routing logic, escalation design, refusal paths (designed) |
| **Retrieval Assistant** | Policy-as-data configs, ADRs, evaluation scorecard, trace schema, response contract, **runnable `minirag.py` demo**, sample corpus (10 docs), evidence package outputs |

Artifacts emphasize **decision accountability and auditability**, not model optimization.

---

## Progress

| Phase | Focus | Current State |
|-------|-------|---------------|
| Foundation | Opportunity discovery and prioritization frameworks | 🟡 Artifacts and design complete; not fully executable |
| Build | Safety enforcement and grounded retrieval | ✅ Retrieval demo operational; guardrails designed |
| Polish | Integration, case studies, evaluation depth | 🔄 In progress |

Future iterations focus on **integration depth and narrative clarity**, not expanding model complexity.

---

## Supporting Credentials

Formal training completed during this transition, reinforcing the governance and lifecycle concepts applied throughout this repository:

- Microsoft Azure AI-900
- Google Cloud Generative AI
- DeepLearning.AI Prompt Engineering

---

## Local Setup

- See `requirements.txt` for Python dependencies
- This repo includes a deterministic demo runner that does not require external APIs