# SEC Rule 17a-4 — Books and Records

**Regulatory Citation:** 17 C.F.R. § 240.17a-4  
**Authority:** Securities Exchange Act of 1934  
**Regulator:** U.S. Securities and Exchange Commission (SEC)  
**Type:** Federal Regulation — legally binding, examiner-enforced

---

## Summary

SEC Rule 17a-4 establishes **recordkeeping and retention requirements** for broker-dealers. It specifies what records must be preserved, for how long, in what format, and how they must be produced to regulators.

The core premise: **if it happened, there must be a record — and that record must be reconstructable**. This applies to communications, transactions, approvals, and increasingly, AI-generated outputs that constitute firm activity.

For AI systems, 17a-4 means: every interaction that could be subject to regulatory inquiry must produce an immutable, time-stamped, retrievable audit trail. "The system said it" is not an answer — "here is the trace of what the system knew, decided, and produced" is.

> *This document interprets SEC 17a-4 from a product and architecture perspective, not as a legal or compliance directive.*

---

## Key Regulatory Language

### On Preservation Requirements

> "Every member, broker, or dealer subject to § 240.17a-3 shall preserve for a period of not less than six years, the first two years in an easily accessible place..."
>
> — *17 C.F.R. § 240.17a-4(a)*

### On Communications Records

> "Originals of all communications received and copies of all communications sent (and any approvals thereof) by the member, broker or dealer (including inter-office memoranda and communications) relating to its business as such..."
>
> — *17 C.F.R. § 240.17a-4(b)(4)*

### On Electronic Recordkeeping Systems

> "An electronic recordkeeping system must preserve a record... in a manner that maintains a complete time-stamped audit trail that includes:
> 
> (i) All modifications to and deletions of the record or any part thereof;  
> (ii) The date and time of actions that create, modify, or delete the record;  
> (iii) If applicable, the identity of the individual creating, modifying, or deleting the record;  
> (iv) Any other information needed... to permit re-creation of the original record..."
>
> — *17 C.F.R. § 240.17a-4(f)(2)*

### On Accessibility and Format

> "Have the capacity to readily download and transfer copies of a record and its audit trail... in both a human readable format and in a reasonably usable electronic format..."
>
> — *17 C.F.R. § 240.17a-4(f)(2)*

### On Regulatory Access

> "Furnish promptly to a representative of the Commission... legible, true, complete, and current copies of those records..."
>
> — *17 C.F.R. § 240.17a-4(f)(3)*

---

## Core Expectations

From an examiner's perspective, 17a-4 requires:

### Retention Periods
| Record Type | Retention Period | Accessibility |
|-------------|------------------|---------------|
| Most business records | 6 years | First 2 years: easily accessible |
| Communications | 3-6 years depending on type | Must be retrievable on request |
| Audit trails | Life of the record | Must accompany the record |

### Audit Trail Requirements
- **Time-stamped** — Date and time of every action
- **Immutable** — Modifications tracked, not overwritten
- **Attributable** — Identity of actor recorded (human or system)
- **Complete** — Sufficient to reconstruct the original record
- **Accessible** — Human-readable and electronically usable

### Format Requirements
- **WORM compliance** — Write Once, Read Many (for certain records)
- **Human-readable** — Must be viewable and interpretable by regulators without proprietary tools
- **Machine-readable** — Must be exportable in usable electronic format
- **Indexable** — Must be searchable and retrievable by relevant criteria

Not all records require WORM storage, but records subject to SEC 17a-4(f) must meet non-rewriteable, non-erasable requirements through WORM or equivalent controls.

### Regulatory Production
- **Prompt availability** — Records must be producible on request
- **Complete and accurate** — No gaps, no alterations
- **With audit trail** — The record's history must accompany it

---

## Product & Architecture Implications

For AI systems operating in broker-dealer contexts, 17a-4 creates concrete design requirements:

| Expectation | What It Means for AI Systems |
|-------------|------------------------------|
| **Time-stamped audit trail** | Every AI interaction must log: timestamp, inputs, outputs, decisions, sources |
| **Immutability** | Logs cannot be edited or deleted; corrections must be additive |
| **Reconstruction capability** | Must be able to answer "what did the system know and produce at time X?" |
| **Identity attribution** | System must record who/what initiated each action |
| **Human-readable output** | Trace logs must be interpretable without specialized tools |
| **Retention architecture** | Logging infrastructure must support 6-year retention with tiered accessibility |

### The Reconstruction Standard

17a-4's "permit re-creation of the original record" standard is the bar:

> If a regulator asks "show me what happened on this date with this customer," can you produce:
> - The original query
> - The corpus version at that time
> - The retrieved passages
> - The generated response
> - The routing decisions
> - The approval chain (if applicable)

If any link in that chain is missing, the audit trail is incomplete.

---

## Where This Shows Up in the Portfolio

| Artifact | How 17a-4 Informed It |
|----------|----------------------|
| **Trace Schema** | Core design — preserves inputs, outputs, decisions, timestamps, corpus version |
| **Compliance Retrieval Assistant** | `corpus_release_id` enables point-in-time reconstruction |
| **Response Contract** | `trace_id` links every user response to its audit record |
| **Dual Contracts (user + audit)** | Audit-facing trace serves 17a-4; user-facing response serves UX |
| **Requirements Guardrails** | All routing decisions logged with timestamps and rationale |
| **ROI Decision Engine** | Decision Memos create auditable prioritization records |

### Specific Design Decisions Driven by 17a-4

| Decision | 17a-4 Driver |
|----------|--------------|
| `corpus_release_id` in every trace | Enables "what did the system know when?" reconstruction |
| Trace committed before response returned | Ensures no interaction exists without a record |
| Immutable logging architecture | Modifications tracked, not overwritten |
| Human-readable trace format (JSON + Markdown) | Meets "human readable format" requirement |
| `trace_id` returned in every response | Links user experience to audit trail |
| Separate audit contract from user contract | Serves different audiences with different retention needs |

---

## Common Examiner Questions (Applied Lens)

Based on 17a-4, examiners may ask:

1. **"Show me the record of this AI interaction."**  
   → Trace schema produces complete record: query, retrieval, generation, decision, timestamp.

2. **"What version of your knowledge base was active on [date]?"**  
   → `corpus_release_id` versioning enables point-in-time reconstruction.

3. **"Can you produce this in a format I can read?"**  
   → Trace logs are JSON (machine-readable) with Markdown summaries (human-readable).

4. **"How do I know this record hasn't been altered?"**  
   → Immutable logging architecture; modifications are additive, not destructive.

5. **"Who or what generated this response?"**  
   → Trace includes system identifier, model version, and (if applicable) human approver.

---

## Key Distinction: Records vs. Logs

Not all system logs are "records" under 17a-4 — but any log that documents firm business activity likely is.

For AI systems, the line is:
- **Debug logs** (system performance, error traces) — probably not 17a-4 records
- **Interaction logs** (customer queries, generated responses) — almost certainly 17a-4 records
- **Decision logs** (routing decisions, approvals, escalations) — likely 17a-4 records

When in doubt, treat it as a record. The cost of over-retention is storage; the cost of under-retention is regulatory findings.

For purposes of this portfolio, all AI-generated outputs and their supporting traces are treated as records subject to 17a-4 retention and production requirements.

For portfolio purposes, treat 17a-4 as: **the audit trail standard that determines whether your AI system's activity is reconstructable, defensible, and producible to regulators.**

---

## Relationship to Other Regulations

| Regulation | Relationship to 17a-4 |
|------------|----------------------|
| **FINRA 2210** | 2210 requires communications recordkeeping; 17a-4 specifies how and how long |
| **Reg BI** | Reg BI requires documentation of recommendation basis; 17a-4 governs retention |
| **SR 11-7** | SR 11-7 requires model documentation; 17a-4 governs how that documentation is preserved |

These regulations layer:
- **FINRA 2210** says *what* must be recorded (communications, approvals)
- **17a-4** says *how* it must be preserved (format, duration, accessibility)
- **SR 11-7** adds *model-specific* documentation requirements
- **Reg BI** adds *recommendation-specific* documentation requirements

A compliant system must satisfy all layers simultaneously.

---

## References

- [17 C.F.R. § 240.17a-4 (eCFR Full Text)](https://www.ecfr.gov/current/title-17/chapter-II/part-240/section-240.17a-4)
- [17 C.F.R. § 240.17a-4 (Cornell Law)](https://www.law.cornell.edu/cfr/text/17/240.17a-4)
- [FINRA Interpretations of SEA Rule 17a-4](https://www.finra.org/rules-guidance/guidance/interpretations-financial-operational-rules/sea-rule-17a-4-and-related-interpretations)
- [SEC Recordkeeping Requirements FAQ](https://www.sec.gov/divisions/marketreg/recordkeeping.htm)

---

*Part of the [Regulatory Governance Context](../README.md) — documenting the external constraints that shape AI product design.*