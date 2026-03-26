import json
from pathlib import Path


from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from state import CaseState
from nodes.utils import parse_json_response

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

SYSTEM_PROMPT = (
    "You are a compliance routing officer. Based on the full "
    "case analysis, produce a final routing decision. Return "
    "a JSON object with:\n"
    "  routing_destination: one of COMPLIANCE_REVIEW, FRAUD_OPS, "
    "SUPERVISOR_REVIEW, DOCUMENTATION_REVIEW, IMMEDIATE_ESCALATION\n"
    "  recommended_action: one sentence describing the first "
    "action the receiving team should take\n"
    "Return only valid JSON. No explanation, no markdown."
)


def route_decision(state: CaseState) -> CaseState:
    """Node 6: Produce final routing decision and recommended action.

    Uses GPT-4o via langchain-openai to determine routing.
    """
    try:
        llm = ChatOpenAI(model="gpt-4o", temperature=0)

        user_context = json.dumps({
            "raw_input": state["raw_input"],
            "issue_category": state.get("issue_category"),
            "risk_level": state.get("risk_level"),
            "regulatory_trigger": state.get("regulatory_trigger"),
            "entities": state.get("entities"),
            "policy_snippets": state.get("policy_snippets"),
            "priority_score": state.get("priority_score"),
            "priority_rationale": state.get("priority_rationale"),
            "internal_note": state.get("internal_note"),
        }, indent=2)

        response = llm.invoke([
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_context),
        ])

        result = parse_json_response(response.content)

        routing_destination = result["routing_destination"]
        recommended_action = result["recommended_action"]

        state["routing_destination"] = routing_destination
        state["recommended_action"] = recommended_action

        state["trace"].append({
            "step": "route_decision",
            "input_summary": f"Determined routing for priority {state.get('priority_score')} {state.get('issue_category')}",
            "output_summary": f"Routed to {routing_destination} — {recommended_action}",
            "key_outputs": {
                "routing_destination": routing_destination,
                "recommended_action": recommended_action,
            },
        })

    except Exception as e:
        state["error"] = f"route_decision failed: {str(e)}"
        state["trace"].append({
            "step": "route_decision",
            "input_summary": f"Attempted routing for {state.get('issue_category')}",
            "output_summary": f"ERROR: {str(e)}",
            "key_outputs": {},
        })

    return state
