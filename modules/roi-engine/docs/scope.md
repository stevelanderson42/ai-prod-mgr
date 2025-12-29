# ROI Decision Engine — Scope Definition

## Purpose

This document defines the boundaries between MVP, Strong MVP, and backlog functionality for the ROI Decision Engine.

---

## MVP (Minimum Viable Product)

**Goal:** A working engine that evaluates a single AI opportunity and produces a meeting-ready Decision Memo.

### MVP Includes

| Component | Description |
|-----------|-------------|
| Manual intake | All inputs entered via structured templates |
| Three-dimension scoring | Business Value, Feasibility, Regulatory Complexity |
| Configurable weights | Weights adjustable per organization/context |
| Decision Memo output | Markdown format, meeting-ready |
| Score rationale | Explanation of key drivers per dimension |
| Assumption visibility | All inputs treated as "declared assumptions, subject to review" |
| Governance questions | Generated list of questions for compliance to validate |
| Evidence references | Links from memo sections to input sources |

### MVP Does NOT Include

- Automated data ingestion
- Integration with Market Intel module
- Multi-opportunity comparison
- Historical tracking
- Workflow states or approvals

---

## Strong MVP

**Goal:** Extend MVP to support portfolio-level prioritization across multiple opportunities.

### Strong MVP Adds

| Component | Description |
|-----------|-------------|
| Batch input | Accept multiple opportunities in a single session |
| Comparison table | Ranked table showing all opportunities with dimension scores |
| Portfolio view | Side-by-side comparison for Advisory Product Council review |

### Strong MVP Does NOT Include

- Automated ingestion
- Historical decision tracking
- Sensitivity analysis

---

## Backlog (Future)

These features are explicitly deferred—sophistication layers, not credibility layers.

| Feature | Rationale for Deferral |
|---------|------------------------|
| Market Intel integration | Requires Market Intel module to be stable first |
| Historical tracking | Adds storage complexity; not needed for initial demo |
| Sensitivity analysis | Nice-to-have for mature usage; not MVP signal |
| Multi-role workflows | Adds user management complexity |
| Approval states | Governance partnership ≠ formal approval workflow |
| Automated ingestion | Manual entry is preferable for MVP (signals intentional decision-making) |

---

## Design Principles

1. **Manual inputs are preferable for MVP** — Signals intentional decision-making; avoids pretending we have data precision we don't

2. **Governance is embedded, not bolted on** — Compliance participates by providing inputs and receiving questions, not by appearing as a final gate

3. **Outputs support conversation** — Decision Memos are meeting-ready, not just computational

4. **Auditability emerges from transparency** — Explicit assumptions and evidence references, not process overhead

---

## Related ADRs

- [ADR-0003 - Evidence Traceability Standard](../../../architecture/decisions/ADR-0003%20-%20Evidence%20Traceability%20Standard.md)
- [ADR-0004 - ROI Scoring Model Design](../../../architecture/decisions/ADR-0004%20-%20ROI%20Scoring%20Model%20Design.md)