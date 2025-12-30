# Sample: AI-Assisted Customer Routing

## What This Sample Demonstrates

This folder contains a **complete artifact chain** for a single AI opportunity evaluation:

    opportunity-packet.md (intake)
            ↓
    input-evidence-references.md (evidence)
            ↓
    decision-memo.md (output)

The sample illustrates how the ROI Engine transforms a proposed AI initiative into an auditable, stakeholder-ready decision recommendation.

---

## The Scenario

**Opportunity:** Use AI to route incoming customer service inquiries to the optimal handling path (self-service, junior rep, senior rep, specialist) based on intent classification and account context.

**Why This Example:**
- Realistic regulated financial services use case
- Touches multiple compliance considerations (fair treatment, data privacy, explainability)
- Demonstrates balanced scoring (not a slam-dunk or obvious reject)
- Shows how assumptions and risks surface through the process

---

## Declared Assumptions

The following assumptions were declared during intake and would require validation in discovery:

| Assumption | Validation Needed |
|------------|-------------------|
| 70% of inquiries have clear routing signals | Analysis of 6-month inquiry sample |
| Existing CRM data sufficient for context | Data quality audit |
| No fair lending implications in routing logic | Compliance legal review |
| Customer satisfaction won't decrease | A/B test design |

---

## What Strong MVP Would Add

- Side-by-side comparison with 1-2 alternative opportunities
- Quantified confidence intervals on ROI estimates
- Formal sign-off workflow tracking

---

## Files in This Sample

| File | Description |
|------|-------------|
| opportunity-packet.md | Completed intake form with all declared inputs |
| input-evidence-references.md | Evidence table mapping inputs to sources |
| decision-memo.md | Final recommendation document |

---

*See [ROI Engine README](../../README.md) for module overview.*