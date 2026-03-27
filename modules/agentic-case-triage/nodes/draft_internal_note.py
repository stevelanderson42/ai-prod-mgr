import json
from pathlib import Path


from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from state import CaseState
from nodes.utils import parse_json_response

# Load .env from the repo root
load_dotenv(Path(__file__).resolve().parent.parent.parent.parent / ".env", override=True)

SYSTEM_PROMPT = (
    "You are a compliance operations writer. Draft a concise "
    "internal routing note for this case. Return a JSON object with:\n"
    "  internal_note: 2-3 sentence structured summary including "
    "issue type, priority, regulatory trigger, and recommended next step\n"
    "Return only valid JSON. No explanation, no markdown."
)


def draft_internal_note(state: CaseState) -> CaseState:
    """Node 5: Draft a structured internal routing note.

    Uses GPT-4o via langchain-openai to generate a concise summary.
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
        }, indent=2)

        response = llm.invoke([
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_context),
        ])

        result = parse_json_response(response.content)
        internal_note = result["internal_note"]

        state["internal_note"] = internal_note

        state["trace"].append({
            "step": "draft_internal_note",
            "input_summary": f"Drafted internal note for {state.get('issue_category')} (priority {state.get('priority_score')})",
            "output_summary": "Generated structured routing summary for compliance team",
            "key_outputs": {
                "internal_note": internal_note,
            },
        })

    except Exception as e:
        state["error"] = f"draft_internal_note failed: {str(e)}"
        state["trace"].append({
            "step": "draft_internal_note",
            "input_summary": f"Attempted drafting internal note for {state.get('issue_category')}",
            "output_summary": f"ERROR: {str(e)}",
            "key_outputs": {},
        })

    return state
