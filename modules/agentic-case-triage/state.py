from typing import TypedDict, Optional


class CaseState(TypedDict):
    """Shared state object that flows through every node in the triage graph."""

    # ── Input ──────────────────────────────────
    raw_input: str

    # ── Node 1: classify_issue ─────────────────
    issue_category: Optional[str]
    risk_level: Optional[str]
    regulatory_trigger: Optional[str]

    # ── Node 2: extract_entities ───────────────
    entities: Optional[dict]

    # ── Node 3: retrieve_policy ────────────────
    policy_snippets: Optional[list]

    # ── Node 4: score_priority ─────────────────
    priority_score: Optional[int]
    priority_rationale: Optional[str]

    # ── Node 5: draft_internal_note ────────────
    internal_note: Optional[str]

    # ── Node 6: route_decision ─────────────────
    routing_destination: Optional[str]
    recommended_action: Optional[str]

    # ── Execution Trace ────────────────────────
    trace: list
    error: Optional[str]


def create_initial_state(raw_input: str) -> CaseState:
    """Create a fresh CaseState with defaults for a new case submission."""
    return CaseState(
        raw_input=raw_input,
        issue_category=None,
        risk_level=None,
        regulatory_trigger=None,
        entities=None,
        policy_snippets=None,
        priority_score=None,
        priority_rationale=None,
        internal_note=None,
        routing_destination=None,
        recommended_action=None,
        trace=[],
        error=None,
    )
