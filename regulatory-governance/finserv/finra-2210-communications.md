# FINRA Rule 2210 — Communications with the Public

**Regulatory Citation:** FINRA Rule 2210  
**Effective Date:** February 4, 2013 (consolidated prior rules)  
**Regulator:** Financial Industry Regulatory Authority (FINRA)  
**Type:** Self-Regulatory Organization (SRO) Rule — enforceable via examination and disciplinary action

---

## Summary

FINRA Rule 2210 governs **how broker-dealers communicate with customers and the public**. It establishes content standards, approval workflows, and recordkeeping requirements for all firm communications — from marketing materials to AI-generated responses.

The core principle: **fair, balanced, and not misleading**. Every communication must present a balanced picture, avoid exaggeration, and not omit material information that would change how a reasonable investor understands the message.

For AI systems, FINRA 2210 means: if the model generates customer-facing content, that content must meet the same standards as any other firm communication — and someone must be accountable for it.

> *This document interprets FINRA 2210 from a product and architecture perspective, not as a legal or compliance directive.*

---

## Key Regulatory Language

### On Content Standards

> "All member communications must be based on principles of fair dealing and good faith, must be fair and balanced, and must provide a sound basis for evaluating the facts in regard to any particular security or type of security, industry, or service."
>
> — *FINRA Rule 2210(d)(1)(A)*

### On Misleading Communications

> "No member may make any false, exaggerated, unwarranted, promissory or misleading statement or claim in any communication."
>
> — *FINRA Rule 2210(d)(1)(B)*

### On Balanced Presentation

> "Communications must not omit any material fact or qualification if the omission, in light of the context of the material presented, would cause the communication to be misleading."
>
> — *FINRA Rule 2210(d)(1)(A)*

### On Predictions and Guarantees

> "Communications may not predict or project performance, imply that past performance will recur, or make any exaggerated or unwarranted claim, opinion or forecast."
>
> — *FINRA Rule 2210(d)(1)(F)*

### On Pre-Use Approval

> "An appropriately qualified registered principal of the member must approve each retail communication before the earlier of its use or filing with FINRA's Advertising Regulation Department."
>
> — *FINRA Rule 2210(b)(1)(A)*

### On Recordkeeping

> "Members must maintain all retail communications... in a file for a period of at least three years from the date of last use. The file must include: a copy of the communication and the dates of first and last use; the name of any registered principal who approved the communication and the date that approval was given."
>
> — *FINRA Rule 2210(b)(4)(A)*

---

## Core Expectations

From an examiner's perspective, FINRA 2210 requires:

### Content Standards
- **Fair and balanced** — Benefits and risks presented together
- **No misleading omissions** — Material facts cannot be left out
- **No exaggeration** — Claims must be supportable and reasonable
- **No guarantees or predictions** — Future performance cannot be promised or implied
- **Sound basis** — Statements must be grounded in fact, not speculation

### Communication Categories
| Category | Definition | Approval Requirement |
|----------|------------|---------------------|
| **Retail Communication** | Any written communication distributed to more than 25 retail investors within 30 days | Pre-use principal approval required |
| **Correspondence** | Written communication to 25 or fewer retail investors within 30 days | Supervision required; pre-approval may be required by firm policy |
| **Institutional Communication** | Written communication to institutional investors only | No pre-approval required, but subject to supervision |

### Approval Workflow
- **Pre-use approval** for retail communications by a registered principal
- **Documented approval** with approver name and date
- **Filing requirements** for certain communications with FINRA Advertising Regulation

### Recordkeeping
- **Retain communications** for at least 3 years from last use
- **Document approval chain** — who approved, when
- **Preserve source materials** — charts, graphs, statistical sources
- **Track usage dates** — first and last use documented

---

## Product & Architecture Implications

For AI systems that generate or assist with customer communications, FINRA 2210 creates concrete design requirements:

| Expectation | What It Means for AI Systems |
|-------------|------------------------------|
| **"Fair and balanced"** | Systems cannot present only benefits; risk disclosure must be included or flagged |
| **No predictions or guarantees** | Language patterns like "will increase" or "guaranteed returns" must be blocked |
| **Pre-use approval** | AI-generated retail content requires human review before delivery |
| **Recordkeeping** | All generated communications must be logged with timestamps and approval records |
| **Material omissions** | Systems must either include required context or refuse to generate incomplete responses |
| **Sound basis** | Claims must be grounded in retrievable sources, not model inference |

### The "Fair and Balanced" Standard

This is the most common FINRA 2210 violation — and the hardest for AI systems to get right.

A response is **unbalanced** if it:
- Presents benefits without corresponding risks
- Emphasizes upside while minimizing downside
- Uses superlatives ("best," "safest," "highest") without qualification
- Omits material limitations that would affect investor decisions

For RAG systems, this means: **grounding alone isn't sufficient**. Even a factually accurate response can violate 2210 if it presents an unbalanced picture.

---

## Where This Shows Up in the Portfolio

| Artifact | How FINRA 2210 Informed It |
|----------|----------------------------|
| **Requirements Guardrails** | "Compliance Triggers" category — detects unbalanced claims, predictions, guarantees |
| **Guardrails Output Contract** | Classification includes `compliance` category with specific 2210 triggers |
| **Compliance Retrieval Assistant** | Refusal taxonomy includes content that cannot be safely balanced |
| **Trace Schema** | Preserves generated content + approval metadata for recordkeeping |
| **Response Contract** | Citations enable "sound basis" verification |

### Specific Design Decisions Driven by FINRA 2210

| Decision | FINRA 2210 Driver |
|----------|-------------------|
| Guardrails check for "guarantees/predictions" | 2210(d)(1)(F) prohibits performance predictions |
| Guardrails check for "unbalanced claims" | 2210(d)(1)(A) requires fair and balanced presentation |
| Human escalation path for retail communications | 2210(b)(1)(A) requires principal approval |
| Trace logging with timestamps | 2210(b)(4)(A) recordkeeping requirements |
| Refusal over speculation | Ungrounded claims violate "sound basis" requirement |

---

## Common Examiner Questions (Applied Lens)

Based on FINRA 2210, examiners may ask:

1. **"How do you ensure communications are fair and balanced?"**  
   → Guardrails detect unbalanced language patterns; escalation routes edge cases to human review.

2. **"Who approved this communication before it was sent?"**  
   → Trace schema captures approval metadata; retail communications require principal sign-off.

3. **"Show me your recordkeeping for AI-generated content."**  
   → Trace logs preserve content, timestamps, approvals, and source citations.

4. **"How do you prevent the system from making predictions?"**  
   → Compliance triggers flag prediction language; refusal taxonomy blocks prohibited patterns.

5. **"What happens if the system can't provide a balanced response?"**  
   → System refuses rather than generating non-compliant content; user receives explanation.

---

## Key Distinction: Content vs. Delivery

FINRA 2210 governs **what you say**, not just **how you say it**.

A common misconception: "If the AI just retrieves information, 2210 doesn't apply."

This is incorrect. The rule applies to:
- Original content generated by the firm
- Curated or selected content presented to customers
- AI-assisted responses that constitute firm communications

If an AI system generates a response that a customer receives as firm communication, that response must meet 2210 standards — regardless of whether a human typed it.

For purposes of this portfolio, any AI-generated content delivered to a customer as part of a firm workflow is treated as a firm communication.

For portfolio purposes, treat FINRA 2210 as: **the content standard that AI-generated customer communications must meet, with the same approval and recordkeeping requirements as any other firm communication.**

---

## Relationship to Other Regulations

| Regulation | Relationship to FINRA 2210 |
|------------|---------------------------|
| **Reg BI** | 2210 governs *how* you communicate; Reg BI governs *what* you recommend |
| **SEC 17a-4** | 2210 requires recordkeeping; 17a-4 specifies retention format and duration |
| **SR 11-7** | 2210 is content-focused; SR 11-7 governs the model generating that content |

These regulations work together. A communication can be:
- ✅ 2210 compliant (fair and balanced) but ❌ Reg BI non-compliant (unsuitable recommendation)
- ✅ Properly retained per 17a-4 but ❌ Missing required 2210 approvals
- ✅ Generated by a well-documented model (SR 11-7) but ❌ Producing unbalanced content (2210 violation)

---

## References

- [FINRA Rule 2210 (Full Text)](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2210)
- [FINRA Regulatory Notice 12-29 (2210 Implementation Guidance)](https://www.finra.org/rules-guidance/notices/12-29)
- [FINRA Advertising Regulation FAQ](https://www.finra.org/rules-guidance/guidance/faqs/advertising-regulation)
- [FINRA Communications with the Public Resource Page](https://www.finra.org/rules-guidance/key-topics/communications-public)



See the [Regulatory Context README](../README.md) for scope and interpretation notes.

---

*Part of the Regulatory Governance Context*
