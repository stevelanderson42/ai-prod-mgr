from langgraph.graph import StateGraph, END
from state import CaseState, create_initial_state
from nodes.classify_issue import classify_issue
from nodes.extract_entities import extract_entities
from nodes.retrieve_policy import retrieve_policy
from nodes.score_priority import score_priority
from nodes.draft_internal_note import draft_internal_note
from nodes.route_decision import route_decision


def build_graph() -> StateGraph:
    """Build the full six-node triage workflow graph."""
    graph = StateGraph(CaseState)

    graph.add_node("classify_issue", classify_issue)
    graph.add_node("extract_entities", extract_entities)
    graph.add_node("retrieve_policy", retrieve_policy)
    graph.add_node("score_priority", score_priority)
    graph.add_node("draft_internal_note", draft_internal_note)
    graph.add_node("route_decision", route_decision)

    graph.set_entry_point("classify_issue")
    graph.add_edge("classify_issue", "extract_entities")
    graph.add_edge("extract_entities", "retrieve_policy")
    graph.add_edge("retrieve_policy", "score_priority")
    graph.add_edge("score_priority", "draft_internal_note")
    graph.add_edge("draft_internal_note", "route_decision")
    graph.add_edge("route_decision", END)

    return graph.compile()


if __name__ == "__main__":
    app = build_graph()

    test_input = (
        "Customer states their advisor recommended an unsuitable mutual fund product "
        "that did not align with their stated risk tolerance or investment objectives. "
        "Customer is requesting a full review of the recommendation and potential restitution."
    )

    initial_state = create_initial_state(test_input)
    result = app.invoke(initial_state)

    print("=" * 60)
    print("  AI CASE TRIAGE — FULL WORKFLOW RESULT")
    print("=" * 60)

    print("\n--- Classification ---")
    print(f"  Category:          {result['issue_category']}")
    print(f"  Risk Level:        {result['risk_level']}")
    print(f"  Reg Trigger:       {result['regulatory_trigger']}")

    print("\n--- Entities ---")
    if result["entities"]:
        for key, val in result["entities"].items():
            print(f"  {key}: {val}")

    print("\n--- Policy Snippets ---")
    if result["policy_snippets"]:
        for i, snippet in enumerate(result["policy_snippets"], 1):
            print(f"  [{i}] {snippet}")

    print("\n--- Priority ---")
    print(f"  Score:             {result['priority_score']}/5")
    print(f"  Rationale:         {result['priority_rationale']}")

    print("\n--- Internal Note ---")
    print(f"  {result['internal_note']}")

    print("\n--- Routing Decision ---")
    print(f"  Destination:       {result['routing_destination']}")
    print(f"  Recommended Action:{result['recommended_action']}")

    print("\n" + "=" * 60)
    print("  EXECUTION TRACE")
    print("=" * 60)
    for i, entry in enumerate(result["trace"], 1):
        print(f"\n  Node {i} — {entry['step']}")
        print(f"    Input:  {entry['input_summary']}")
        print(f"    Output: {entry['output_summary']}")
