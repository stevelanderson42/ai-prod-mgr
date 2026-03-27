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
    "You are a compliance risk officer. Based on the case "
    "classification and entities provided, score the priority "
    "and return a JSON object with:\n"
    "  priority_score: integer 1-5 (5=critical)\n"
    "  priority_rationale: one sentence explanation\n"
    "Return only valid JSON. No explanation, no markdown."
)


def score_priority(state: CaseState) -> CaseState:
    """Node 4: Score case priority based on classification and entities.

    Uses GPT-4o via langchain-openai to assess urgency.
    """
    try:
        llm = ChatOpenAI(model="gpt-4o", temperature=0)

        user_context = json.dumps({
            "raw_input": state["raw_input"],
            "issue_category": state.get("issue_category"),
            "risk_level": state.get("risk_level"),
            "regulatory_trigger": state.get("regulatory_trigger"),
            "entities": state.get("entities"),
        }, indent=2)

        response = llm.invoke([
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_context),
        ])

        result = parse_json_response(response.content)

        priority_score = result["priority_score"]
        priority_rationale = result["priority_rationale"]

        state["priority_score"] = priority_score
        state["priority_rationale"] = priority_rationale

        state["trace"].append({
            "step": "score_priority",
            "input_summary": f"Scored priority for {state.get('issue_category')} with risk level {state.get('risk_level')}",
            "output_summary": f"Priority score {priority_score}/5 — {priority_rationale}",
            "key_outputs": {
                "priority_score": priority_score,
                "priority_rationale": priority_rationale,
            },
        })

    except Exception as e:
        state["error"] = f"score_priority failed: {str(e)}"
        state["trace"].append({
            "step": "score_priority",
            "input_summary": f"Attempted priority scoring for {state.get('issue_category')}",
            "output_summary": f"ERROR: {str(e)}",
            "key_outputs": {},
        })

    return state
