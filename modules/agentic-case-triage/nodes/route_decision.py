from state import CaseState


def route_decision(state: CaseState) -> CaseState:
    """Node 6: Produce final routing decision and recommended action.

    Stub implementation — returns hardcoded values. Will be replaced with LLM call in Phase 3.
    """
    routing_destination = "COMPLIANCE_REVIEW"
    recommended_action = (
        "Assign to compliance officer within 24 hours. "
        "Preserve all communication records per SEC 17a-4."
    )

    state["routing_destination"] = routing_destination
    state["recommended_action"] = recommended_action

    state["trace"].append({
        "step": "route_decision",
        "input_summary": f"Determined routing for priority {state['priority_score']} {state['issue_category']}",
        "output_summary": f"Routed to {routing_destination} — {recommended_action}",
        "key_outputs": {
            "routing_destination": routing_destination,
            "recommended_action": recommended_action,
        },
    })

    return state
