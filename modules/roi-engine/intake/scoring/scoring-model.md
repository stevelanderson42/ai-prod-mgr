# Scoring Model

## Overview

The ROI Decision Engine evaluates AI opportunities across three dimensions, producing both individual dimension scores and a weighted composite score. This document describes the scoring logic, scale anchors, and weight configuration.

For design rationale, see [ADR-0004 - ROI Scoring Model Design](../../../architecture/decisions/ADR-0004%20-%20ROI%20Scoring%20Model%20Design.md).

---

## Scoring Dimensions

### 1. Business Value

**What it measures:** Potential impact on KPIs, revenue, cost reduction, customer experience, or risk mitigation.

**Direction:** Higher = stronger opportunity

| Score | Label | Anchor |
|-------|-------|--------|
| 1 | Very Low | Marginal or unclear value; nice-to-have |
| 2 | Low | Minor improvement; limited strategic relevance |
| 3 | Medium | Meaningful impact; aligns with team-level goals |
| 4 | High | Significant impact; aligns with org-level priorities |
| 5 | Very High | Transformative; clear executive-level strategic value |

**Key inputs:** Target KPIs, impact estimate, value type, confidence level

---

### 2. Implementation Feasibility

**What it measures:** Technical complexity, data availability, integration effort, and delivery risk.

**Direction:** Higher = more feasible

| Score | Label | Anchor |
|-------|-------|--------|
| 1 | Very Low | Major unknowns; new technology; data unavailable |
| 2 | Low | Significant gaps; multiple dependencies; high effort |
| 3 | Medium | Some challenges; partial data; moderate effort |
| 4 | High | Manageable scope; data mostly available; clear path |
| 5 | Very High | Straightforward; proven patterns; data ready |

**Key inputs:** Systems touched, data availability, delivery effort, timeline, dependencies

---

### 3. Regulatory Complexity

**What it measures:** Compliance burden, data sensitivity, required controls, and governance overhead.

**Direction:** Higher = more complex (inverted for composite calculation)

| Score | Label | Anchor |
|-------|-------|--------|
| 1 | Very Low | Internal only; no sensitive data; minimal oversight |
| 2 | Low | Limited exposure; standard controls sufficient |
| 3 | Medium | Customer-adjacent; PII involved; monitoring required |
| 4 | High | Customer-facing decisions; multiple regulations apply |
| 5 | Very High | Automated decisions on sensitive matters; novel regulatory territory |

**Key inputs:** Customer-facing impact, model role, data sensitivity, decision impact, explainability requirements

---

## Composite Score Calculation

The composite score combines all three dimensions using configurable weights:

```
Composite = (Value × W_v) + (Feasibility × W_f) + ((6 - Regulatory) × W_r)
```

**Why invert regulatory?** "Complexity" naturally reads as "more = harder." Subtracting from 6 converts it so that lower complexity contributes positively to the composite, while preserving the intuitive 1–5 scoring direction.

**Example:**
- Business Value: 4
- Feasibility: 3
- Regulatory Complexity: 2
- Weights: 40% / 30% / 30%

```
Composite = (4 × 0.40) + (3 × 0.30) + ((6 - 2) × 0.30)
          = 1.6 + 0.9 + 1.2
          = 3.7
```

---

## Weight Configuration

### Default Weights

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| Business Value | 40% | Value realization is typically the primary driver |
| Feasibility | 30% | Delivery risk is a common failure mode |
| Regulatory Complexity | 30% | Compliance elevated to first-class concern |

### When to Adjust Weights

| Profile | Value | Feasibility | Regulatory | When to Use |
|---------|-------|-------------|------------|-------------|
| **Balanced** (default) | 40% | 30% | 30% | Most organizations |
| **Aggressive Growth** | 50% | 25% | 25% | Growth mode; similar risk profiles across opportunities |
| **Risk-Averse** | 30% | 30% | 40% | Regulatory scrutiny; recent compliance incidents |
| **Delivery-Focused** | 35% | 40% | 25% | History of delivery failures; "quick wins" valued |

### Weight Configuration Principles

1. **Weights must sum to 100%**
2. **Document your rationale** when departing from defaults
3. **Be consistent** within a prioritization cycle
4. **Avoid extreme skew** — no single weight below 20% or above 50%
5. **Involve all stakeholders** — weight selection should include Business, Engineering, and Compliance voices

---

## Scoring Process

### Step 1: Review Inputs

Review the Opportunity Packet for each dimension:
- Business Value inputs → Business Value score
- Feasibility inputs → Feasibility score
- Governance inputs → Regulatory Complexity score

### Step 2: Assign Dimension Scores

For each dimension:
1. Compare inputs against scale anchors
2. Assign a 1–5 score
3. Document key drivers (what pushed the score up or down)
4. Note assumptions the score depends on

### Step 3: Calculate Composite

Apply configured weights to calculate composite score.

### Step 4: Document Rationale

For each dimension, the Decision Memo should include:
- **Score:** The 1–5 rating
- **Key drivers:** What influenced the score
- **Assumptions:** What the score depends on
- **Risks:** What could change the score

---

## Scoring Tips

**When in doubt, score conservatively.** It's better to surface concerns early than to overstate readiness.

**Confidence affects scoring.** Low confidence in inputs should pull scores toward the middle (3) or flag the need for validation.

**Assumptions matter as much as scores.** A well-documented 3 is more useful than an undocumented 4.

**Scores are starting points, not verdicts.** The goal is informed conversation, not algorithmic decision-making.

---

*See [README](README.md) for folder overview.*