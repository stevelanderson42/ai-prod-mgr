# ROI Decision Engine

## Overview

In regulated industries, AI initiatives frequently stall in prioritization limbo. Business teams see value, technology teams assess feasibility, but regulatory and compliance considerations often enter late—stalling promising projects or, worse, letting risky ones proceed without the guidance they need. The ROI Decision Engine addresses this by providing a structured, multi-criteria scoring model that evaluates AI opportunities across three dimensions simultaneously: business value, implementation feasibility, and regulatory complexity. Rather than treating compliance as a one-meeting checkpoint, the engine brings governance in as a day-one partner—surfacing trade-offs early, making risk visible and measurable, and giving business sponsors and compliance teams a shared language for investment decisions.

## Why This Matters in Regulated Environments

Traditional AI ROI models underestimate regulatory and operational risk, leading to:
- Stalled initiatives when compliance concerns surface late
- Executive mistrust in AI programs
- "Pilot purgatory" with no clear path to production

This module introduces explicit structure and transparency into AI prioritization, enabling organizations to move forward with confidence—or deliberately choose not to.

## Context Diagram

![ROI Decision Engine Context Diagram](docs/context-diagram.png)

## Module Structure

| Folder | Purpose |
|--------|---------|
| `/docs` | Context diagram, scope definition |
| `/intake` | Opportunity packet schema and intake templates |
| `/scoring` | Scoring model documentation |
| `/evidence` | Evidence traceability templates (per ADR-0003) |
| `/outputs` | Decision Memo template |
| `/samples` | Complete example: intake → scoring → memo |

## Key Concepts

### Three Scoring Dimensions

| Dimension | What It Measures | Direction |
|-----------|------------------|-----------|
| **Business Value** | Impact on KPIs, revenue, cost, CX | Higher = stronger |
| **Implementation Feasibility** | Technical complexity, data, effort | Higher = more feasible |
| **Regulatory Complexity** | Compliance burden, data sensitivity | Higher = more complex |

See [ADR-0004 - ROI Scoring Model Design](../../architecture/decisions/ADR-0004%20-%20ROI%20Scoring%20Model%20Design.md) for design rationale.

### Governance as Partner

The engine treats compliance as a day-one partner, not a gate:
- Governance inputs captured alongside business and technical inputs
- Open questions surfaced for compliance to validate
- Assumptions explicitly declared, not hidden

### Primary Output: Decision Memo

A meeting-ready markdown document containing:
- Opportunity summary and scope
- Score breakdown with rationale
- Risk drivers and mitigations
- Open questions for governance review
- Recommendation (pursue / defer / explore)
- Evidence references

See [`/samples/ai-assisted-customer-routing/`](samples/ai-assisted-customer-routing/) for a complete example.

## MVP Scope

See [docs/scope.md](docs/scope.md) for detailed boundaries.

**MVP includes:**
- Manual opportunity intake
- Three-dimension scoring with configurable weights
- Decision Memo generation (markdown)
- Evidence traceability stub

**Strong MVP adds:**
- Batch comparison mode
- Ranked comparison table

**Backlog:**
- Market Intel module integration
- Historical decision tracking
- Sensitivity analysis

## Related ADRs

- [ADR-0003 - Evidence Traceability Standard](../../architecture/decisions/ADR-0003%20-%20Evidence%20Traceability%20Standard.md)
- [ADR-0004 - ROI Scoring Model Design](../../architecture/decisions/ADR-0004%20-%20ROI%20Scoring%20Model%20Design.md)

## Related Modules

| Module | Relationship |
|--------|--------------|
| Market Intel | Future integration — opportunity suggestions feed into intake |
| Guardrails | Consumes regulatory posture outputs |
| RAG Assistant | May reference Decision Memos for compliance Q&A |

---

*Part of the Regulated AI Workflow Toolkit*