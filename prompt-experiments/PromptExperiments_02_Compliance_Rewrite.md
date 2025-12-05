# Experiment 02: Compliance Rewrite

## Goal

Rewrite advisor communications to meet regulatory standards by removing performance predictions, guarantees, and comparative claims.

## Why This Matters

FINRA and SEC regulations prohibit investment advisors from making promissory statements or predicting performance. Marketing and client communications must be reviewed for compliance. An AI assistant that "professionalizes" text without understanding compliance rules creates legal risk.

---

## Prompt V1
```
Rewrite this text professionally:

"I think this investment is definitely going to beat the market."
```

## Output V1
```
"I am confident that this investment will outperform the market."
```

## Observation

V1 made the compliance problem worse:

- **Strengthened the claim:** Changed "I think" to "I am confident"
- **Kept prohibited language:** "outperform the market" is a comparative performance claim
- **More violative than original:** A compliance officer would flag this immediately

"Professional" doesn't mean "compliant." Without explicit rules, the model optimizes for confidence and polish — exactly the wrong direction for regulated communications.

---

## Prompt V2 (Refined)
```
You are a compliance editor for a registered investment advisor.

Rewrite the following text to meet regulatory standards.

Rules:
- Remove any guarantees or predictions about performance
- Remove comparative claims ("beat the market", "outperform")
- Use neutral, factual language only
- Do not add claims not present in the original
- Keep it concise

Original text: "I think this investment is definitely going to beat the market."

Return only the rewritten text, nothing else.
```

## Output V2
```
This investment has the potential to perform well in the market.
```

## What Changed in V2

| Element | V1 | V2 |
|---------|----|----|
| Role assignment | None | Compliance editor for RIA |
| Performance language | Allowed | Explicitly prohibited |
| Comparative claims | Allowed | Explicitly prohibited |
| Guidance | "Professional" | Specific compliance rules |

---

## Takeaway

Generic instructions like "rewrite professionally" can make compliance problems worse. The model optimizes for whatever goal you give it — and "professional" suggests confidence, not caution.

In regulated environments, prompts must include explicit constraints that mirror actual compliance rules. The AI needs to know what it *cannot* say, not just what tone to use.

---

## Connection to Toolkit

This pattern directly supports the **Requirements Guardrails** module, where AI-generated or AI-edited content must pass compliance checks before reaching customers. It also informs how the **Compliance RAG Assistant** should frame responses — always with appropriate hedging and without forward-looking statements.