from state import CaseState


def extract_entities(state: CaseState) -> CaseState:
    """Node 2: Extract key entities from the case text.

    Stub implementation — returns hardcoded values. Will be replaced with LLM call in Phase 3.
    """
    entities = {
        "customer_id": "CUST-001",
        "product": "mutual_fund",
        "advisor_id": "ADV-042",
        "date": "recent",
    }

    state["entities"] = entities

    state["trace"].append({
        "step": "extract_entities",
        "input_summary": "Extracted entities from raw case text",
        "output_summary": "Identified customer CUST-001, product mutual_fund, advisor ADV-042",
        "key_outputs": {
            "entities": entities,
        },
    })

    return state
