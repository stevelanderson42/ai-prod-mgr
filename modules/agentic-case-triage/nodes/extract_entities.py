from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from state import CaseState
from nodes.utils import parse_json_response

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

SYSTEM_PROMPT = (
    "You are a compliance data extraction assistant. Extract key "
    "entities from this case and return a JSON object with:\n"
    "  customer_id: inferred identifier or 'UNKNOWN'\n"
    "  product: financial product mentioned\n"
    "  advisor_id: advisor identifier or 'UNKNOWN'\n"
    "  date: date referenced or 'UNSPECIFIED'\n"
    "  key_facts: one sentence summary of the core allegation\n"
    "Return only valid JSON. No explanation, no markdown."
)


def extract_entities(state: CaseState) -> CaseState:
    """Node 2: Extract key entities from the case text.

    Uses GPT-4o via langchain-openai to identify structured entities.
    """
    try:
        llm = ChatOpenAI(model="gpt-4o", temperature=0)

        response = llm.invoke([
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=state["raw_input"]),
        ])

        entities = parse_json_response(response.content)
        state["entities"] = entities

        state["trace"].append({
            "step": "extract_entities",
            "input_summary": "Extracted entities from raw case text",
            "output_summary": f"Identified customer {entities.get('customer_id')}, product {entities.get('product')}, advisor {entities.get('advisor_id')}",
            "key_outputs": {
                "entities": entities,
            },
        })

    except Exception as e:
        state["error"] = f"extract_entities failed: {str(e)}"
        state["trace"].append({
            "step": "extract_entities",
            "input_summary": "Attempted entity extraction from raw case text",
            "output_summary": f"ERROR: {str(e)}",
            "key_outputs": {},
        })

    return state
