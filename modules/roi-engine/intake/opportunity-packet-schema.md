# Opportunity Packet Schema

## Purpose

This document defines the structure of an **Opportunity Packet** — the complete set of inputs required by the ROI Decision Engine to evaluate an AI opportunity.

---

## Schema Overview

An Opportunity Packet contains four sections:

| Section | Purpose |
|---------|---------|
| Identification | Who, what, when |
| Business Value Inputs | Value hypothesis and impact estimates |
| Feasibility Inputs | Technical complexity and delivery estimates |
| Governance Inputs | Regulatory posture and compliance considerations |

---

## Schema Definition

### Identification

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier (e.g., "OPP-2025-001") |
| `title` | string | Yes | Short descriptive name |
| `owner` | string | Yes | Responsible PM / Business Sponsor |
| `date_created` | date | Yes | When packet was created |
| `version` | string | Yes | Version number (e.g., "v1") |

### Business Value Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `description` | string | Yes | What the AI initiative does |
| `problem_statement` | string | Yes | What problem it solves |
| `target_outcomes` | string[] | Yes | List of expected outcomes |
| `target_kpis` | string[] | Yes | Metrics expected to improve |
| `value_type` | enum | Yes | `cost_reduction`, `revenue_growth`, `cx_improvement`, `risk_reduction` |
| `impact_estimate` | string | No | Expected magnitude (range acceptable) |
| `impact_confidence` | enum | Yes | `low`, `medium`, `high` |
| `assumptions` | string[] | No | Key assumptions underlying value estimate |

### Feasibility Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `systems_touched` | string[] | Yes | Integration points |
| `data_required` | string[] | Yes | What data the model needs |
| `data_availability` | enum | Yes | `available`, `partial`, `not_available` |
| `data_notes` | string | No | Details on data gaps or quality |
| `delivery_effort` | enum | Yes | `small`, `medium`, `large` |
| `timeline_estimate` | string | Yes | Expected duration (range acceptable) |
| `key_dependencies` | string[] | No | Blockers or prerequisites |
| `assumptions` | string[] | No | Key assumptions underlying feasibility |

### Governance Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `customer_facing` | boolean | Yes | Does it affect customers directly? |
| `model_role` | enum | Yes | `advisory`, `automated` |
| `data_sensitivity` | enum[] | Yes | `pii`, `financial`, `health`, `none` |
| `decision_impact` | enum | Yes | `low`, `medium`, `high` |
| `explainability_requirement` | enum | Yes | `low`, `medium`, `high` |
| `known_constraints` | string[] | No | Regulatory requirements |
| `open_questions` | string[] | No | Unknowns for compliance to resolve |
| `assumptions` | string[] | No | Key governance assumptions |

---

## Field Guidance

### Required vs. Optional

**Required fields** are the minimum needed to produce a scored Decision Memo.

**Optional fields** (assumptions, notes, dependencies) are strongly encouraged — they support transparency and traceability.

### Assumptions Fields

Every section includes an `assumptions` array. These are critical for:
- Transparency about what scores are based on
- Identifying what needs validation
- Supporting the "declared assumptions" philosophy

### Open Questions

The `governance.open_questions` field flows directly into the Decision Memo's "Questions for Governance Review" section. This is where governance partnership becomes tangible.

---

## Example (Minimal)

```yaml
identification:
  id: "OPP-2025-001"
  title: "AI-Assisted Customer Service Routing"
  owner: "Product Manager, Customer Experience"
  date_created: "2025-01-15"
  version: "v1"

business_value:
  description: "AI model recommends optimal queue/agent routing"
  problem_statement: "High transfer rate (18%) increases AHT and reduces CSAT"
  target_outcomes:
    - "Reduce transfer rate to under 10%"
    - "Improve first-contact resolution by 12-15%"
  target_kpis: ["AHT", "transfer_rate", "FCR", "CSAT"]
  value_type: "cost_reduction"
  impact_estimate: "$1.2-1.8M annually"
  impact_confidence: "medium"

feasibility:
  systems_touched: ["Genesys", "Salesforce", "Case Management"]
  data_required: ["call_reason_codes", "customer_segment", "agent_skills"]
  data_availability: "partial"
  data_notes: "Agent skill taxonomy needs standardization"
  delivery_effort: "medium"
  timeline_estimate: "10-14 weeks"
  key_dependencies:
    - "Agent skill taxonomy remediation"

governance:
  customer_facing: true
  model_role: "advisory"
  data_sensitivity: ["pii"]
  decision_impact: "low"
  explainability_requirement: "medium"
  known_constraints:
    - "Must log all routing recommendations"
  open_questions:
    - "Does advisory routing count as customer-impacting decision?"
    - "What monitoring is required post-deployment?"
```

---

## Templates

- [Opportunity Intake Form](templates/opportunity-intake-form.md) — Blank template for capturing all inputs
- [Governance Intake Questions](templates/governance-intake-questions.md) — Focused template for governance inputs

---

*See [README](README.md) for input category overview.*