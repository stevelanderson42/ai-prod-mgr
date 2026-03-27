import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from state import CaseState
from nodes.utils import parse_json_response

# Load .env from the repo root
load_dotenv(Path(__file__).resolve().parent.parent.parent.parent / ".env", override=True)

SYSTEM_PROMPT = (
    "You are a compliance triage assistant at a regulated financial services firm. "
    "Classify the incoming customer case and return a JSON object with exactly these fields:\n"
    "  issue_category: one of SUITABILITY_COMPLAINT, FRAUD, FEE_DISPUTE, COMMUNICATION_COMPLAINT, ACCOUNT_ACCESS\n"
    "  risk_level: one of HIGH, MEDIUM, LOW\n"
    "  regulatory_trigger: the most relevant regulation, e.g. Reg_BI, FINRA_2210, KYC_AML, SEC_17a4\n"
    "Return only valid JSON. No explanation, no markdown, no code fences."
)


def classify_issue(state: CaseState) -> CaseState:
    """Node 1: Classify the incoming case by issue type, risk level, and regulatory trigger.

    Uses GPT-4o via langchain-openai to produce a structured classification.
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=state["raw_input"]),
    ])

    # Parse the JSON response (strips markdown fences if present)
    result = parse_json_response(response.content)

    issue_category = result["issue_category"]
    risk_level = result["risk_level"]
    regulatory_trigger = result["regulatory_trigger"]

    state["issue_category"] = issue_category
    state["risk_level"] = risk_level
    state["regulatory_trigger"] = regulatory_trigger

    state["trace"].append({
        "step": "classify_issue",
        "input_summary": "Received raw case text for classification",
        "output_summary": f"Classified as {issue_category}, {risk_level} risk, {regulatory_trigger} trigger",
        "key_outputs": {
            "issue_category": issue_category,
            "risk_level": risk_level,
            "regulatory_trigger": regulatory_trigger,
        },
    })

    return state
