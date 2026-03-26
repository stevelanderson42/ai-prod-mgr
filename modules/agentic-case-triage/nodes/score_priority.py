from state import CaseState


def score_priority(state: CaseState) -> CaseState:
    """Node 4: Score case priority based on classification and entities.

    Stub implementation — returns hardcoded values. Will be replaced with LLM call in Phase 3.
    """
    priority_score = 4
    priority_rationale = "High-risk suitability complaint with Reg BI trigger warrants urgent compliance review"

    state["priority_score"] = priority_score
    state["priority_rationale"] = priority_rationale

    state["trace"].append({
        "step": "score_priority",
        "input_summary": f"Scored priority for {state['issue_category']} with risk level {state['risk_level']}",
        "output_summary": f"Priority score {priority_score}/5 — {priority_rationale}",
        "key_outputs": {
            "priority_score": priority_score,
            "priority_rationale": priority_rationale,
        },
    })

    return state
