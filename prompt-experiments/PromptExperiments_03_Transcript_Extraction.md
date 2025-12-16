# Experiment 03: Transcript Extraction

## Goal

Extract structured data from customer call transcripts for compliance logging, CRM updates, and audit trails.

## Why This Matters

Financial services firms must maintain records of customer interactions, especially those involving investment decisions or account changes. Extracting this data manually is expensive and inconsistent. An AI extractor must produce reliable, structured output that integrates with existing systems.

---

## Prompt V1
```
Extract the key information from this transcript:

On October 12th I spoke with Maria Chen about her rollover IRA. 
She's concerned about market volatility and mentioned she's 
considering moving approximately $50,000 into a target-date fund. 
She wants to discuss this with her husband before making any decisions.
```

## Output V1
```
- Date of conversation: October 12th
- Person spoken with: Maria Chen
- Topic: Rollover IRA
- Concerns: Market volatility
- Consideration: Moving $50,000 into a target-date fund
- Decision-making process: Wants to discuss with her husband
```

## Observation

V1 captured the correct information, but the output is problematic for production use:

- **Inconsistent field names:** "Person spoken with" vs "customer_name" — every run could use different labels
- **Not machine-readable:** Bullet points require parsing; downstream systems can't reliably extract values
- **Schema drift:** Process 100 transcripts and you'll get 100 slightly different structures
- **No handling for missing data:** What happens when information isn't present?

The model summarized rather than extracted. Good for a human reader, unusable for a data pipeline.

---

## Prompt V2 (Refined)
```
You are a compliance data extractor for a financial services firm.

Extract information from the transcript below into this exact JSON structure:

{
    "customer_name": "",
    "date": "",
    "account_type": "",
    "concerns": "",
    "potential_action": "",
    "amount": "",
    "next_steps": ""
}

Rules:
- Use empty string "" if information is not present
- Do not infer or add information not explicitly stated
- Return only valid JSON, no other text

Transcript:
On October 12th I spoke with Maria Chen about her rollover IRA. 
She's concerned about market volatility and mentioned she's 
considering moving approximately $50,000 into a target-date fund. 
She wants to discuss this with her husband before making any decisions.
```

## Output V2
```json
{
    "customer_name": "Maria Chen",
    "date": "October 12th",
    "account_type": "rollover IRA",
    "concerns": "market volatility",
    "potential_action": "moving approximately $50,000 into a target-date fund",
    "amount": "$50,000",
    "next_steps": "discuss with her husband before making any decisions"
}
```

## What Changed in V2

| Element | V1 | V2 |
|---------|----|----|
| Role assignment | None | Compliance data extractor |
| Output format | Unspecified | Exact JSON schema provided |
| Field names | Model's choice | Predefined and consistent |
| Missing data handling | Not addressed | Empty string rule |
| Inference rules | Not addressed | Explicitly prohibited |

---

## Takeaway

"Extract key information" produces summaries. "Extract into this exact schema" produces data.

The difference matters when you need to:
- Store results in a database
- Feed output to downstream systems
- Compare across thousands of records
- Audit what was captured vs. what was missed

Schema-first prompting turns an LLM into a reliable data extraction tool. Without a schema, you get prose that looks helpful but can't be operationalized.

---

## Connection to Toolkit

This extraction pattern is core to the **Compliance RAG Assistant**, which must pull structured information from policy documents, customer records, and regulatory filings. It also supports the **Market Intelligence Monitor**, where news and filings need to be parsed into consistent data structures for analysis.




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

# Sample transcript snippet from a customer call
transcript = """
On October 12th I spoke with Maria Chen about her rollover IRA. 
She's concerned about market volatility and mentioned she's 
considering moving approximately $50,000 into a target-date fund. 
She wants to discuss this with her husband before making any decisions.
"""

# ========== V1 PROMPT - vague instruction ==========
prompt_v1 = f"""
Extract the key information from this transcript:

{transcript}
"""

print("=== V1 PROMPT ===")
print(prompt_v1)
print("\n=== V1 OUTPUT ===")
response_v1 = get_completion(prompt_v1)
print(response_v1)

# ========== V2 PROMPT - structured schema ==========
prompt_v2 = f"""
You are a compliance data extractor for a financial services firm.

Extract information from the transcript below into this exact JSON structure:

{{
    "customer_name": "",
    "date": "",
    "account_type": "",
    "concerns": "",
    "potential_action": "",
    "amount": "",
    "next_steps": ""
}}

Rules:
- Use empty string "" if information is not present
- Do not infer or add information not explicitly stated
- Return only valid JSON, no other text

Transcript:
{transcript}
"""

print("\n=== V2 PROMPT ===")
print(prompt_v2)
print("\n=== V2 OUTPUT ===")
response_v2 = get_completion(prompt_v2)
print(response_v2)


# === V1 PROMPT ===

# Extract the key information from this transcript:


# On October 12th I spoke with Maria Chen about her rollover IRA.
# She's concerned about market volatility and mentioned she's
# considering moving approximately $50,000 into a target-date fund.
# She wants to discuss this with her husband before making any decisions.



# === V1 OUTPUT ===
# - Date of conversation: October 12th
# - Person spoken with: Maria Chen
# - Topic: Rollover IRA
# - Concerns: Market volatility
# - Consideration: Moving $50,000 into a target-date fund     
# - Decision-making process: Wants to discuss with her husband

# === V2 PROMPT ===

# You are a compliance data extractor for a financial services firm.

# Extract information from the transcript below into this exact JSON structure:

# {
#     "customer_name": "",
#     "date": "",
#     "account_type": "",
#     "concerns": "",
#     "potential_action": "",
#     "amount": "",
#     "next_steps": ""
# }

# Rules:
# - Use empty string "" if information is not present
# - Do not infer or add information not explicitly stated
# - Return only valid JSON, no other text

# Transcript:

# On October 12th I spoke with Maria Chen about her rollover IRA.
# She's concerned about market volatility and mentioned she's
# considering moving approximately $50,000 into a target-date fund.
# She wants to discuss this with her husband before making any decisions.



# === V2 OUTPUT ===
# {
#     "customer_name": "Maria Chen",
#     "date": "October 12th",
#     "account_type": "rollover IRA",
#     "concerns": "market volatility",
#     "potential_action": "moving approximately $50,000 into a target-date fund",
#     "amount": "$50,000",
#     "next_steps": "discuss with her husband before making any decisions"
# }
# PS C:\Users\Steve\Documents\GitHub\ai-prod-mgr-sandbox> 