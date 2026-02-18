# Case Studies

**Decision narratives from the Regulated AI Workflow Toolkit**

---

## What These Are

These case studies document how I approached ambiguous, constrained AI product decisions in regulated environments. They are not implementation walkthroughs — they are narratives of how decisions were framed, evaluated, and made, and why certain paths were chosen over others.

Each case study intentionally focuses on a bounded decision surface rather than end-to-end delivery, mirroring how real product decisions are made within larger programs.

---

## Case Study Structure

Each case study follows a consistent structure designed to make reasoning explicit rather than inferred.

| Section | What It Answers |
|---------|-----------------|
| **TL;DR** | 10-second summary: what, why, how, validation |
| **Problem** | What business need or user problem triggered this work? |
| **Constraints** | What limited the solution space? (regulatory, technical, organizational) |
| **Decision Criteria** | What mattered most? What was explicitly deprioritized? |
| **Options Considered** | What alternatives were evaluated? |
| **Key Decisions** | What specific choices were made and why? |
| **Architecture** | Visual diagrams of the solution structure |
| **Tradeoffs Acknowledged** | What was given up? What risks were accepted? |
| **Outcome & Validation Signals** | What does success look like? How would we know it's working? |
| **Enterprise Scaling Considerations** | What changes at Fortune 500 scale? |
| **Open Questions** | What would I revisit with more data or stakeholder input? |

---

## Why This Format

Senior PM interviews often hinge on one question: *"How did you decide?"*

These case studies are designed to pre-answer that question by making visible:

- Explicit decision criteria (ranked, not inferred after the fact)
- Alternatives that were considered and rejected
- Tradeoffs acknowledged rather than hidden
- Regulatory considerations at decision points, not layered on later
- Open questions that demonstrate intellectual honesty

The intent is to show judgment, not just outcomes.

---

## Case Studies Included

| # | Title | Module | Focus |
|---|-------|--------|-------|
| 01 | [Pre-Invocation Governance as a Product Control](Case%20Study%201%20-%20Pre-Invocation%20Governance%20as%20a%20Product%20Control.md) | Requirements Guardrails | Audit defensibility, controlled model access, pre-generation risk |
| 02 | [Output Governance for Regulated AI](Case%20Study%202%20-%20Output%20Governance%20for%20Regulated%20AI.md) | Output Governance | Post-generation controls, supervisory review, compliance validation |
| 03 | [Retrieval Architecture for Audit-Ready Compliance Workflows](Case%20Study%203%20-%20Retrieval%20Architecture%20for%20Audit-Ready%20Compliance%20Workflows.md) | Compliance Retrieval Assistant | Governance-first RAG design, auditability |

### How They Connect

Case Study #1 establishes the **pre-invocation control plane** — the authorization gate that determines whether a request should reach an LLM at all. If allowed, the request may route into the **compliance retrieval system** documented in Case Study #3. Together, they demonstrate end-to-end governance: from "should we answer?" to "how do we answer safely?"

---

## How to Read These

**If you have 60 seconds:** Read TL;DR → Decision Criteria → Key Decisions

**If you have 5 minutes:** Read the full case study

**If you're an interviewer:** Decision Criteria and Tradeoffs sections are designed to provide probe points

---

## Regulatory References

Where relevant, these case studies reference real regulatory frameworks:

- **SR 11-7** — Model Risk Management (documentation, validation, monitoring)
- **SEC 17a-4** — Books and Records (traceability, retention)
- **FINRA 2210** — Communications with the Public (review, approval, balanced content)
- **OWASP Top 10 for LLM Applications** — Industry security framework (prompt injection, guardrails)

Regulations are cited at decision inflection points, not as decoration. The goal is to reflect how compliance operates in practice — not how it's studied for exams.

---

## Diagrams

Architecture diagrams are located in [docs/diagrams/](./docs/diagrams/) and embedded within each case study:

| Diagram | Case Study | Description |
|---------|------------|-------------|
| [Control Plane Diagram](./docs/diagrams/Case_Study_1_Control_Plane_Diagram.PNG) | #1 | Pre-invocation governance architecture |
| [Routing Decisions](./docs/diagrams/Case_Study_1_Routing_Decisions.PNG) | #1 | Decision flow from request to routing outcome |

---

## Related Artifacts

Each case study links to concrete artifacts elsewhere in this repository:

- [/modules/compliance-retrieval-assistant/](../modules/compliance-retrieval-assistant/) — Compliance Retrieval Assistant
- [/modules/requirements-guardrails/](../modules/requirements-guardrails/) — Requirements Guardrails (Input Analyzer)
- [/modules/roi-engine/](../modules/roi-engine/) — ROI Decision Engine
- [/architecture/](../architecture/) — Cross-cutting architectural decisions
- [/evaluation/](../evaluation/) — Scorecards and test cases

---

## Scope Note

These case studies represent portfolio work demonstrating AI product decision-making in regulated environments. They reflect governance patterns, architectural judgment, and evaluation strategy — not production deployment outcomes.