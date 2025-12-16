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

# Sample advisor message that needs compliance review
advisor_message = "I think this investment is definitely going to beat the market."

# ========== V1 PROMPT - too simple ==========
prompt_v1 = f"""
Rewrite this text professionally:

"{advisor_message}"
"""

print("=== V1 PROMPT ===")
print(prompt_v1)
print("\n=== V1 OUTPUT ===")
response_v1 = get_completion(prompt_v1)
print(response_v1)

# ========== V2 PROMPT - compliance-aware ==========
prompt_v2 = f"""
You are a compliance editor for a registered investment advisor.

Rewrite the following text to meet regulatory standards.

Rules:
- Remove any guarantees or predictions about performance
- Remove comparative claims ("beat the market", "outperform")
- Use neutral, factual language only
- Do not add claims not present in the original
- Keep it concise

Original text: "{advisor_message}"

Return only the rewritten text, nothing else.
"""

print("\n=== V2 PROMPT ===")
print(prompt_v2)
print("\n=== V2 OUTPUT ===")
response_v2 = get_completion(prompt_v2)
print(response_v2)


# === V1 PROMPT ===

# Rewrite this text professionally:

# "I think this investment is definitely going to beat the market."


# === V1 OUTPUT ===
# "I am confident that this investment will outperform the market."

# === V2 PROMPT ===

# You are a compliance editor for a registered investment advisor.

# Rewrite the following text to meet regulatory standards.        

# Rules:
# - Remove any guarantees or predictions about performance        
# - Remove comparative claims ("beat the market", "outperform")   
# - Use neutral, factual language only
# - Do not add claims not present in the original
# - Keep it concise

# Original text: "I think this investment is definitely going to beat the market."

# Return only the rewritten text, nothing else.


# === V2 OUTPUT ===
# This investment has the potential to perform well in the market.
# PS C:\Users\Steve\Documents\GitHub\ai-prod-mgr-sandbox> 