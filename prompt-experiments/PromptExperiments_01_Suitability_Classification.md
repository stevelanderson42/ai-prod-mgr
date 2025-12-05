# Experiment 01: Suitability Classification

## Goal

Classify customer questions as either SUITABILITY_RELEVANT (requiring compliance handling) or GENERAL_INQUIRY in a regulated financial services context.

## Why This Matters

In broker-dealer and advisory environments, questions involving asset allocation, retirement accounts, or investment recommendations trigger different compliance requirements than general informational questions. An AI system must classify these consistently and provide auditable reasoning.

---

## Prompt V1
```
Classify this question as "general" or "suitability-related."

Question: Should I move part of my 401(k) into bonds?
```

## Output V1
```
This question is suitability-related.
```

## Observation

The model produced the correct classification, but the response has problems for production use:

- **Inconsistent format:** Asked for "general" or "suitability-related" but received a full sentence
- **No reasoning:** No explanation of why this classification was chosen
- **Not parseable:** Downstream systems can't reliably extract the label from free-form text
- **Not auditable:** Compliance teams need to see the decision logic

The model "got it right" but in a way that wouldn't survive a compliance review or integrate into an automated workflow.

---

## Prompt V2 (Refined)
```
You are a compliance classifier for a regulated financial institution.

Classify the user's question using ONLY these two labels:

1. SUITABILITY_RELEVANT — if the question involves:
   - asset allocation
   - retirement decision-making
   - investment recommendation
   - risk-level change

2. GENERAL_INQUIRY — everything else

Return JSON only: {"label": "...", "reason": "..."}

Question: Should I move part of my 401(k) into bonds?
```

## Output V2
```json
{
    "label": "SUITABILITY_RELEVANT",
    "reason": "The question involves asset allocation within a retirement account (401(k))"
}
```

## What Changed in V2

| Element | V1 | V2 |
|---------|----|----|
| Role assignment | None | Compliance classifier |
| Label definitions | Implied | Explicit criteria |
| Output format | Unspecified | JSON required |
| Reasoning | Not requested | Required in output |

---

## Takeaway

Correct answers aren't sufficient in regulated environments. The prompt must enforce:

1. **Structured output** — for reliable parsing and integration
2. **Explicit definitions** — so the model applies your rules, not its assumptions  
3. **Required reasoning** — for audit trails and compliance review

This pattern applies broadly: any classification task in financial services needs to produce consistent, explainable, machine-readable results.

---

## Connection to Toolkit

This classification pattern is foundational for the **Requirements Guardrails** module, where incoming user requests must be routed appropriately before the AI responds. It also informs the **Compliance RAG Assistant**, which needs to detect when a query requires sourced, compliant answers versus general information.