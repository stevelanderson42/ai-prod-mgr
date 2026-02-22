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




# python code
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content

# Sample customer question
customer_question = "Should I move part of my 401(k) into bonds?"

# ========== V1 PROMPT - intentionally vague ==========
prompt_v1 = f"""
Classify this question as "general" or "suitability-related."

Question: {customer_question}
"""

print("=== V1 PROMPT ===")
print(prompt_v1)
print("\n=== V1 OUTPUT ===")
response_v1 = get_completion(prompt_v1)
print(response_v1)



# ========== V2 PROMPT - structured with definitions ==========
prompt_v2 = f"""
You are a compliance classifier for a regulated financial institution.

Classify the user's question using ONLY these two labels:

1. SUITABILITY_RELEVANT — if the question involves:
   - asset allocation
   - retirement decision-making
   - investment recommendation
   - risk-level change

2. GENERAL_INQUIRY — everything else

Return JSON only: {{"label": "...", "reason": "..."}}

Question: {customer_question}
"""

print("\n=== V2 PROMPT ===")
print(prompt_v2)
print("\n=== V2 OUTPUT ===")
response_v2 = get_completion(prompt_v2)
print(response_v2)


# ========== V1 OUTPUT (recorded 12/5/2025) ==========
# This question is suitability-related.

# ========== V2 OUTPUT (recorded 12/5/2025) ==========
# {
#     "label": "SUITABILITY_RELEVANT",
#     "reason": "The question involves asset allocation within a retirement account (401(k))"
# }
