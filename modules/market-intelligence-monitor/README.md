# Market Intelligence Monitor

## What This Module Is

The Market Intelligence Monitor represents the **external strategic awareness layer** of a regulated AI product system.

Its purpose is to continuously track **external signals**—such as competitor AI releases, regulatory developments, and industry adoption patterns—so that AI initiatives are grounded in **market reality**, not hype or internal enthusiasm.

This module exists to answer a foundational question that many AI programs skip:

> *“Why should we build this AI capability now?”*

---

## Why This Matters in Regulated Environments

In regulated industries, AI initiatives carry **asymmetric risk**:

- moving too slowly can erode competitive position
- moving too quickly can trigger regulatory, legal, or reputational damage

Unlike consumer tech, regulated organizations cannot afford to “ship and iterate” without context.

This module helps organizations:

- avoid chasing high-visibility but low-viability AI trends
- understand how peers and competitors are deploying AI responsibly
- anticipate regulatory direction before it becomes enforcement
- align AI strategy with risk tolerance and governance posture

In short, it prevents AI investment decisions from being driven by hype, fear, or isolated internal champions.

---

## Key Decisions This Module Enables

This module supports decisions such as:

- Which AI capabilities are becoming **table stakes** versus true differentiators
- When competitive pressure justifies AI investment
- Which regulatory signals should accelerate or pause initiatives
- Where internal AI proposals may be misaligned with market or policy reality

These decisions are typically owned by **Product Leadership**, **Strategy**, and **Executive Sponsors**, with input from Risk and Compliance.

---

## How This Module Fits Into the Overall System

The Market Intelligence Monitor is the **entry point** to the Regulated AI Workflow Toolkit.

Insights from this module feed directly into the **ROI Decision Engine**, where opportunities are evaluated more rigorously for value, feasibility, and regulatory complexity.

By design, no AI initiative advances without first passing through this external reality check.

This module includes a lightweight code scaffold to support repeatable signal ingestion, normalization, and synthesis over time; implementation is intentionally incremental.

---

## Product Scope & PM Decisions (MVP)

This section documents explicit product decisions made during development of the Market Intelligence Monitor MVP.  
Decisions are recorded to demonstrate scope control, trade-off reasoning, and acceptance criteria — not to drive runtime behavior.

### Decision Index

| Decision ID | Area        | Summary                                              | Status   |
|------------|-------------|------------------------------------------------------|----------|
| MID-001    | Scope       | Limit MVP to 2–3 representative signal sources       | Approved |
| MID-002    | Sources     | Include Fidelity press releases (list-level only)    | Approved |
| MID-003    | Sources     | Include FINRA RSS as regulatory signal source         | Approved |
| MID-004    | Hydration   | Defer detail-page hydration pending demonstrated downstream decision value   | Approved |

The following gating decisions operationalize the approved MVP scope and source choices listed in the Decision Index above.

### MVP Gating Decisions

| Decision Area | Decision | Rationale |
|--------------|----------|-----------|
| Source Scope | Limit MVP to a small number of representative sources | Validates decision usefulness without incurring high ingestion complexity |
| Source Mix | Include at least one market-driven source | Ensures competitive and industry pressure signals are represented |
| Ingestion Depth | Prioritize listing-level ingestion over full detail hydration | Sufficient for market timing and trend detection in MVP |
| Robustness Threshold | Defer hardening once acceptance criteria are met | Marginal robustness gains do not justify additional MVP cost |

### Source Decisions (MVP)

#### Fidelity Investments — Market Signal Source

**Decision:** Included in MVP

**Rationale:**
- High credibility and frequent publication cadence
- Representative example of a corporate newsroom source
- Direct relevance to competitive and industry signaling in regulated financial services

**MVP Acceptance Criteria (Met):**
- Stable, deduplicated signal identifiers
- Canonical publication dates captured
- Traceable raw evidence preserved
- Normalized signals suitable for downstream synthesis

**Close-Out Statement:**
> Fidelity ingestion meets MVP acceptance criteria for market-intel signal capture. Further robustness improvements are deferred pending demonstrated decision value and scale requirements.

#### FINRA — Regulatory Signal Source

**Decision:** Included in MVP (constrained scope)

**Rationale:**
- Authoritative regulatory body with direct influence on financial services behavior
- High signal-to-noise for compliance posture, enforcement trends, and supervisory priorities
- Provides necessary regulatory counterbalance to market-driven sources (e.g., Fidelity)

**MVP Scope Constraints:**
- Source treated as **low-frequency, high-impact**
- Ingestion prioritized for **official notices, rule updates, and guidance**
- Full historical backfill and deep semantic parsing explicitly deferred

**MVP Acceptance Criteria:**
- Reliable capture of published title, date, and canonical URL
- Clear source attribution (FINRA)
- Traceable raw evidence preserved
- Normalized signals suitable for regulatory posture synthesis

**MVP Scope Note:**
> FINRA ingestion is intentionally constrained to authoritative updates sufficient for regulatory awareness and decision context. Expanded parsing and historical depth are deferred pending demonstrated decision impact.

FINRA RSS ingestion meets MVP acceptance criteria, providing stable regulatory signals with deterministic identifiers and full evidence traceability. Hydration of detail pages deferred until we confirm downstream decision value.


#### Deferred Sources

Additional candidate sources were evaluated but intentionally deferred from the MVP due to ingestion complexity, low update cadence, or limited incremental decision value.

These sources may be reconsidered in future iterations once MVP signal synthesis demonstrates clear downstream impact.

---

## Entry Artifacts (Curated)

This module intentionally separates **decision-facing artifacts** from raw research.

Primary artifacts include:

- **Context Diagram**  
  High-level system flow showing how market signals enter the regulated AI workflow.  
  → ![Market Intelligence Monitor - Context Diagram](docs/diagrams/context-diagram.PNG)

- **Configuration & Signal Definitions**  
  Source and categorization scaffolding used to structure incoming external signals.  
  → `config/`

Additional working notes and evolving structures live in:

- `../../market-intel/` — exploratory research, raw signal analysis, and drafts

---

## What This Module Is Not

This module does **not**:

- approve AI initiatives
- calculate ROI or feasibility
- replace compliance, legal, or risk review
- act as an execution engine for AI workloads

Its role is to ensure those downstream decisions are informed by **external reality** before significant investment or risk is assumed.

---

## Where to Go Deeper

For additional context and supporting material:

- `../../market-intel/` — working notes, evolving structures, and raw signal analysis
- Public Notion Portfolio — strategic framing and cross-module connections

---

## Status

Architecture and decision framing are stable.  
Code scaffolding is in place; implementation will evolve incrementally as signals, sources, and synthesis needs are formalized.

This module is intentionally lightweight, reflecting its role as a **strategic input** rather than a delivery engine.
