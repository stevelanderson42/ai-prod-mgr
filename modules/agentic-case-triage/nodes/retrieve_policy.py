from state import CaseState


def retrieve_policy(state: CaseState) -> CaseState:
    """Node 3: Retrieve relevant policy snippets based on issue classification.

    Stub implementation — returns hardcoded values. Will be replaced with Module 5 RAG layer in Phase 3.
    """
    policy_snippets = [
        "FINRA Rule 2111: suitability obligations require advisors to have reasonable basis...",
        "Reg BI: broker-dealers must act in best interest of retail customer...",
    ]

    state["policy_snippets"] = policy_snippets

    state["trace"].append({
        "step": "retrieve_policy",
        "input_summary": f"Retrieved policy for category {state['issue_category']}",
        "output_summary": f"Found {len(policy_snippets)} relevant policy snippets",
        "key_outputs": {
            "policy_snippets": policy_snippets,
        },
    })

    return state
