# Experiment 05: Grounded Citation

## Goal

Ensure the model answers only from provided source documents and refuses to answer when information is not present — preventing hallucination in compliance-critical contexts.

## Why This Matters

RAG systems (Retrieval-Augmented Generation) retrieve relevant documents and feed them to the model. But the model can still hallucinate by blending retrieved content with its training data. In regulated environments, an AI that confidently presents made-up information as policy is a serious liability.

---

## Setup

A short policy document covering 401(k) withdrawal rules was provided. The question asked about Roth IRA penalties — a topic NOT covered in the document.

**Policy Document Provided:**
```
RETIREMENT ACCOUNT WITHDRAWAL POLICY (Effective January 2024)

Section 3.1 - Early Withdrawal Penalties
Withdrawals from 401(k) accounts before age 59½ are subject to a 10% 
early withdrawal penalty in addition to applicable income taxes.

Section 3.2 - Exceptions to Early Withdrawal Penalty
The 10% penalty is waived in the following circumstances:
- Qualified medical expenses exceeding 7.5% of adjusted gross income
- Permanent disability as defined by IRS guidelines
- Substantially equal periodic payments (SEPP/72t distributions)

Section 3.3 - Required Minimum Distributions
Account holders must begin taking required minimum distributions (RMDs) 
by April 1 of the year following the year they reach age 73.
```

**Question Asked:** "What is the early withdrawal penalty for a Roth IRA?"

---

## Prompt V1
```
You are a helpful retirement planning assistant.

Policy Document:
[document above]

Question: What is the early withdrawal penalty for a Roth IRA?
```

## Output V1
```
For a Roth IRA, withdrawals of contributions (not earnings) can be made penalty-free at any time. However, withdrawals of earnings before age 59½ may be subject to a 10% early withdrawal penalty in addition to applicable income taxes, unless an exception applies.
```

## Observation

V1 hallucinated a complete, confident, accurate-sounding answer about Roth IRAs — despite the document containing zero information about Roth IRAs.

The problems:

- **Invisible hallucination:** The answer is actually correct (based on real IRS rules), which makes it more dangerous — there's no obvious error to catch
- **Source confusion:** A user would reasonably assume this came from the policy document
- **Audit failure:** If asked "where does it say that?", there's no supporting citation
- **Compliance risk:** The firm is now liable for AI-generated advice not grounded in approved materials

The model was "helpful" by drawing on training data. In a RAG system, this is exactly the failure mode you must prevent.

---

## Prompt V2 (Refined)
```
You are a compliance assistant for a financial institution.

You must answer questions ONLY using the provided policy document.

Rules:
- If the answer is in the document, provide it and quote the relevant section
- If the answer is NOT in the document, respond with exactly: "NOT_IN_DOCUMENT: This question cannot be answered from the provided policy."
- Do not use any knowledge outside the provided document
- Do not guess or infer beyond what is explicitly stated

Return JSON in this format:
{
    "answerable": true/false,
    "answer": "your answer here or NOT_IN_DOCUMENT message",
    "source_section": "section number if applicable, empty string if not",
    "quoted_text": "exact quote from document if applicable, empty string if not"
}

Policy Document:
[document above]

Question: What is the early withdrawal penalty for a Roth IRA?
```

## Output V2
```json
{
    "answerable": false,
    "answer": "NOT_IN_DOCUMENT: This question cannot be answered from the provided policy.",
    "source_section": "",
    "quoted_text": ""
}
```

## What Changed in V2

| Element | V1 | V2 |
|---------|----|----|
| Knowledge boundary | Unlimited (training data allowed) | Document only |
| Missing info handling | Answer anyway | Explicit refusal |
| Citation requirement | None | Quote required |
| Output structure | Free-form | JSON with traceability fields |
| Hallucination risk | High | Blocked by design |

---

## Takeaway

Grounding is not automatic. Even when you provide a document, the model will blend it with training data unless explicitly forbidden from doing so.

Effective grounding requires:

1. **Explicit boundary:** "ONLY using the provided document"
2. **Refusal protocol:** What to do when the answer isn't there
3. **Citation requirement:** Force the model to point to its source
4. **Structured output:** So downstream systems can verify the `answerable` flag

This is the core pattern for any RAG system in regulated environments. The model must know the difference between "I can answer this" and "I should answer this."

---

## Connection to Toolkit

This experiment directly informs the **Compliance RAG Assistant** architecture. The retrieval layer finds relevant documents; the generation layer must be constrained to use only what was retrieved. Without this grounding pattern, RAG systems become confident hallucination engines with citations that look legitimate but aren't.




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

# A short "policy document" for the model to reference
policy_document = """
RETIREMENT ACCOUNT WITHDRAWAL POLICY (Effective January 2024)

Section 3.1 - Early Withdrawal Penalties
Withdrawals from 401(k) accounts before age 59½ are subject to a 10% 
early withdrawal penalty in addition to applicable income taxes.

Section 3.2 - Exceptions to Early Withdrawal Penalty
The 10% penalty is waived in the following circumstances:
- Qualified medical expenses exceeding 7.5% of adjusted gross income
- Permanent disability as defined by IRS guidelines
- Substantially equal periodic payments (SEPP/72t distributions)

Section 3.3 - Required Minimum Distributions
Account holders must begin taking required minimum distributions (RMDs) 
by April 1 of the year following the year they reach age 73.
"""

# Question that IS answerable from the document
question_1 = "What is the early withdrawal penalty for a 401(k)?"

# Question that is NOT answerable from the document
question_2 = "What is the early withdrawal penalty for a Roth IRA?"

# ========== V1 PROMPT - no grounding requirement ==========
prompt_v1 = f"""
You are a helpful retirement planning assistant.

Policy Document:
{policy_document}

Question: {question_2}
"""

print("=== V1 PROMPT (asking about Roth IRA - NOT in document) ===")
print(prompt_v1)
print("\n=== V1 OUTPUT ===")
response_v1 = get_completion(prompt_v1)
print(response_v1)

# ========== V2 PROMPT - strict grounding required ==========
prompt_v2 = f"""
You are a compliance assistant for a financial institution.

You must answer questions ONLY using the provided policy document. 

Rules:
- If the answer is in the document, provide it and quote the relevant section
- If the answer is NOT in the document, respond with exactly: "NOT_IN_DOCUMENT: This question cannot be answered from the provided policy."
- Do not use any knowledge outside the provided document
- Do not guess or infer beyond what is explicitly stated

Return JSON in this format:
{{
    "answerable": true/false,
    "answer": "your answer here or NOT_IN_DOCUMENT message",
    "source_section": "section number if applicable, empty string if not",
    "quoted_text": "exact quote from document if applicable, empty string if not"
}}

Policy Document:
{policy_document}

Question: {question_2}
"""

print("\n=== V2 PROMPT (same question - Roth IRA) ===")
print(prompt_v2)
print("\n=== V2 OUTPUT ===")
response_v2 = get_completion(prompt_v2)
print(response_v2)



# === V1 PROMPT (asking about Roth IRA - NOT in document) ===

# You are a helpful retirement planning assistant.

# Policy Document:

# RETIREMENT ACCOUNT WITHDRAWAL POLICY (Effective January 2024)        

# Section 3.1 - Early Withdrawal Penalties
# Withdrawals from 401(k) accounts before age 59½ are subject to a 10% 
# early withdrawal penalty in addition to applicable income taxes.     

# Section 3.2 - Exceptions to Early Withdrawal Penalty
# The 10% penalty is waived in the following circumstances:
# - Qualified medical expenses exceeding 7.5% of adjusted gross income 
# - Permanent disability as defined by IRS guidelines
# - Substantially equal periodic payments (SEPP/72t distributions)     

# Section 3.3 - Required Minimum Distributions
# Account holders must begin taking required minimum distributions (RMDs)
# by April 1 of the year following the year they reach age 73.


# Question: What is the early withdrawal penalty for a Roth IRA?


# === V1 OUTPUT ===
# For a Roth IRA, withdrawals of contributions (not earnings) can be made penalty-free at any time. However, withdrawals of earnings before age 59½ may be subject to a 10% early withdrawal penalty in addition to applicable income 
# taxes, unless an exception applies.

# === V2 PROMPT (same question - Roth IRA) ===

# You are a compliance assistant for a financial institution.

# You must answer questions ONLY using the provided policy document.

# Rules:
# - If the answer is in the document, provide it and quote the relevant section
# - If the answer is NOT in the document, respond with exactly: "NOT_IN_DOCUMENT: This question cannot be answered from the provided policy."
# - Do not use any knowledge outside the provided document
# - Do not guess or infer beyond what is explicitly stated

# Return JSON in this format:
# {
#     "answerable": true/false,
#     "answer": "your answer here or NOT_IN_DOCUMENT message",
#     "source_section": "section number if applicable, empty string if not",
#     "quoted_text": "exact quote from document if applicable, empty string if not"
# }

# Policy Document:

# RETIREMENT ACCOUNT WITHDRAWAL POLICY (Effective January 2024)

# Section 3.1 - Early Withdrawal Penalties
# Withdrawals from 401(k) accounts before age 59½ are subject to a 10%
# early withdrawal penalty in addition to applicable income taxes.

# Section 3.2 - Exceptions to Early Withdrawal Penalty
# The 10% penalty is waived in the following circumstances:
# - Qualified medical expenses exceeding 7.5% of adjusted gross income
# - Permanent disability as defined by IRS guidelines
# - Substantially equal periodic payments (SEPP/72t distributions)

# Section 3.3 - Required Minimum Distributions
# Account holders must begin taking required minimum distributions (RMDs)
# by April 1 of the year following the year they reach age 73.


# Question: What is the early withdrawal penalty for a Roth IRA?


# === V2 OUTPUT ===
# {
#     "answerable": false,
#     "answer": "NOT_IN_DOCUMENT: This question cannot be answered from the provided policy.",
#     "source_section": "",
#     "quoted_text": ""
# }
# PS C:\Users\Steve\Documents\GitHub\ai-prod-mgr-sandbox> 


