from state import CaseState


def draft_internal_note(state: CaseState) -> CaseState:
    """Node 5: Draft a structured internal routing note.

    Stub implementation — returns hardcoded values. Will be replaced with LLM call in Phase 3.
    """
    internal_note = (
        "SUITABILITY COMPLAINT — Priority 4/5. "
        "Customer alleges unsuitable product recommendation. Reg BI "
        "trigger identified. Recommend immediate compliance review."
    )

    state["internal_note"] = internal_note

    state["trace"].append({
        "step": "draft_internal_note",
        "input_summary": f"Drafted internal note for {state['issue_category']} (priority {state['priority_score']})",
        "output_summary": "Generated structured routing summary for compliance team",
        "key_outputs": {
            "internal_note": internal_note,
        },
    })

    return state
