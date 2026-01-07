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
| **Problem** | What business need or user problem triggered this work? |
| **Constraints** | What limited the solution space? (regulatory, technical, organizational) |
| **Decision Criteria** | What mattered most? What was explicitly deprioritized? |
| **Options Considered** | What alternatives were evaluated? |
| **Key Decisions** | What specific choices were made and why? |
| **Tradeoffs Acknowledged** | What was given up? What risks were accepted? |
| **Outcome & Validation Signals** | What does success look like? How would we know it's working? |
| **Enterprise Scaling Considerations** | What changes at Fortune 500 scale? |

---

## Why This Format

Senior PM interviews often hinge on one question: *"How did you decide?"*

These case studies are designed to pre-answer that question by making visible:

- Explicit decision criteria (not inferred after the fact)
- Alternatives that were considered and rejected
- Tradeoffs acknowledged rather than hidden
- Regulatory considerations at decision points, not layered on later

The intent is to show judgment, not just outcomes.

---

## Case Studies Included

| # | Title | Module | Focus |
|---|-------|--------|-------|
| 01 | *Prioritizing AI Opportunities in Resource-Constrained Environments* | ROI Decision Engine | Prioritization, stakeholder tradeoffs |
| 02 | *Designing Input Guardrails for Customer-Facing AI in FinServ* | Requirements Guardrails | Compliance, safety, UX tension |
| 03 | [Retrieval Architecture for Audit-Ready Compliance Workflows](03-audit-ready-retrieval.md) | Compliance Retrieval Assistant | Governance-first design, auditability |

---

## How to Read These

**If you have 60 seconds:** Read Problem → Decision Criteria → Key Decisions

**If you have 5 minutes:** Read the full case study

**If you're an interviewer:** Decision Criteria and Tradeoffs sections are designed to provide probe points

---

## Regulatory References

Where relevant, these case studies reference real regulatory frameworks:

- **SR 11-7** — Model Risk Management (documentation, validation, monitoring)
- **SEC 17a-4** — Books and Records (traceability, retention)
- **FINRA 2210** — Communications with the Public (review, approval, balanced content)

Regulations are cited at decision inflection points, not as decoration. The goal is to reflect how compliance operates in practice — not how it's studied for exams.

---

## Related Artifacts

Each case study links to concrete artifacts elsewhere in this repository:

- [/modules/rag-assistant/](../modules/rag-assistant/) — Compliance Retrieval Assistant
- [/modules/requirements-guardrails/](../modules/requirements-guardrails/) — Input Guardrails
- [/modules/roi-engine/](../modules/roi-engine/) — ROI Decision Engine
- [/architecture/](../architecture/) — Cross-cutting decisions
- [/evaluation/](../evaluation/) — Scorecards and test cases

---

## Scope Note

These case studies represent portfolio work demonstrating AI product decision-making in regulated environments. They reflect governance patterns, architectural judgment, and evaluation strategy — not production deployments.