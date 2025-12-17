# Regulated AI Workflow Toolkit (AI Product Manager Portfolio)

This repository is a cohesive portfolio demonstrating how a Product Manager designs **safe, auditable AI workflows** for regulated environments such as financial services, healthcare, and insurance.

*Designed as a portfolio artifact for senior AI Product Manager roles in regulated industries.*

Rather than a collection of disconnected demos, this work is organized as a **four-module system** focused on the core product challenge in regulated AI:

> **How do you enable real business value from AI while enforcing governance, traceability, and risk controls across the full lifecycle?**


---

## The Four Modules (Start Here)

The main narrative lives under:

→ [`/modules/`](./modules)

Each module has its own README with the “why,” scope, and entry artifacts:

1. **Market Intelligence Monitor**  
   Tracks competitor AI releases and regulatory signals to inform strategic prioritization.  
   → `modules/market-intelligence-monitor/`

2. **ROI Decision Engine**  
   A structured, risk-aware scoring model for prioritizing AI opportunities based on value, feasibility, and regulatory complexity.  
   → `modules/roi-decision-engine/`

3. **Requirements Guardrails (Input Analyzer)**  
   Identifies ambiguity, risk factors, and compliance concerns **before model invocation** to route, escalate, or block requests safely.  
   → `modules/requirements-guardrails/`

4. **Compliance Retrieval Assistant (RAG)**  
   A citation-first assistant for high-risk workflows requiring grounding, traceability, and refusal behavior when evidence is missing.  
   → `modules/compliance-retrieval-assistant/`

---

## How the Modules Connect

These modules form an integrated workflow:

**Market Intelligence** surfaces opportunities → **ROI Engine** prioritizes them →  
**Guardrails** enforce safe execution → **RAG Assistant** delivers compliant, grounded outputs.

This structure is designed to mirror how regulated organizations build AI-enabled products: with governance embedded, not bolted on.

---

## Repository Map (Narrative vs Supporting Artifacts)

This repo separates **portfolio narrative** from **supporting depth**:

### Narrative Layer (what most readers should start with)
- `/modules/` — the four-module system, entry artifacts, and portfolio-ready explanations

### Supporting Layers (depth for reviewers who want evidence)
- `/evaluation/` — shared evaluation framework (datasets, rubrics, run logs, artifacts)
- `/guardrails/` — design + implementation artifacts (heuristics, model card, privacy/security notes)
- `/market-intel/` — working notes and raw signal analysis that inform the Market Intelligence module
- `/prompt-experiments/` — structured experiments used to test behaviors and refine guardrail/eval approaches
- `/architecture/` — system-level architecture context and decision records (ADRs)

---

## Architecture & Diagrams (Optional)

If you prefer a visual walkthrough, the system lifecycle and sequence diagrams are also documented in my public Notion workspace:

- **FinServ AI Query Lifecycle (Notion)**  
  https://www.notion.so/stevelanderson42/FinServ-AI-Query-Lifecycle-2bea7858746d809c86acdd89cd9f7e86

This GitHub repository is the source of record for decisions and supporting artifacts; Notion provides annotated narrative context.

---

## Status

This portfolio is actively evolving. The structure is intentionally designed to remain readable to first-time reviewers while still providing depth for technical, risk, and governance stakeholders.

---

## Notes on Local Setup (Minimal)

- API keys are stored locally in `.env` and are not committed.
- See `requirements.txt` for Python dependencies when relevant.

