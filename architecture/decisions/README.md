# Architecture Decisions (ADRs)

This folder contains **Architecture Decision Records (ADRs)** documenting key design and product decisions made while building the Regulated AI Workflow Toolkit.

ADRs capture **why a decision was made**, not just what was implemented — including tradeoffs, alternatives considered, and downstream implications.

In regulated AI systems, this decision trail is as important as the code itself.

---

## Why ADRs Exist in This Repository

AI systems in regulated environments must be:

- explainable  
- auditable  
- repeatable  
- defensible months or years later  

ADRs provide a lightweight but durable way to:

- preserve decision rationale over time  
- avoid re-litigating the same tradeoffs  
- support governance, compliance, and review conversations  
- show *product-level thinking*, not just implementation detail  

This folder exists to make **decision-making visible**, not implicit.

---

## What Gets an ADR (and What Does Not)

An ADR is created when a decision:

- materially affects **risk, compliance, or governance**
- establishes a **pattern or constraint** used across modules
- impacts **evaluation, traceability, or auditability**
- represents a **non-obvious tradeoff** (speed vs safety, flexibility vs control)

Examples:
- choosing an evaluation workflow that favors traceability over raw accuracy
- defining where guardrails operate in the request lifecycle
- standardizing how refusal or escalation behavior is handled

An ADR is *not* needed for:
- minor refactors
- experimental drafts
- purely cosmetic or organizational changes

---

## How ADRs Are Used

ADRs in this repository are intended to:

- support internal review and future iteration
- anchor discussions with engineering, risk, or compliance partners
- provide context for why the system looks the way it does
- demonstrate senior-level product judgment in interviews and portfolio reviews

They are written to be understandable by:
- product managers
- engineers
- risk/compliance stakeholders

Not just the original author.

---

## Structure and Naming

- Each ADR is numbered sequentially: `ADR-000X`
- New ADRs should be created by copying:  
  `ADR-0001_template.md`
- Increment the number and fill in all sections, even if briefly

Once created, ADRs are **append-only**:
- decisions may be superseded, but not rewritten
- follow-up decisions should reference earlier ADRs

This preserves historical accuracy and intent.

---

## Status

Active and evolving.

New ADRs are added as system-level decisions emerge across modules, particularly where governance, evaluation, or risk boundaries are involved.
