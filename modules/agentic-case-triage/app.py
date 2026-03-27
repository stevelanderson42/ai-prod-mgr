import streamlit as st
from main import build_graph
from state import create_initial_state

# ── Page Config ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Case Triage Workflow",
    layout="wide",
)

st.title("AI Case Triage Workflow — Agentic Orchestration")

DEFAULT_CASE = (
    "Customer states their advisor recommended an unsuitable mutual fund product "
    "that did not align with their stated risk tolerance or investment objectives. "
    "Customer is requesting a full review of the recommendation and potential restitution."
)

# ── Two-Column Layout ──────────────────────────────────────
left, right = st.columns([0.4, 0.6])

with left:
    case_text = st.text_area(
        "Submit Operational Case",
        value=DEFAULT_CASE,
        height=220,
    )
    run = st.button("Run Triage", type="primary")

with right:
    if run and case_text.strip():
        with st.spinner("Running triage workflow..."):
            graph = build_graph()
            initial_state = create_initial_state(case_text.strip())
            result = graph.invoke(initial_state)

        # ── Error Banner ────────────────────────────
        if result.get("error"):
            st.error(result["error"])

        # ── Section 1: Classification ───────────────
        with st.expander("Classification", expanded=True):
            st.markdown(f"**Category:** {result.get('issue_category', '—')}")
            st.markdown(f"**Risk Level:** {result.get('risk_level', '—')}")
            st.markdown(f"**Regulatory Trigger:** {result.get('regulatory_trigger', '—')}")

        # ── Section 2: Entities ─────────────────────
        with st.expander("Entities", expanded=True):
            entities = result.get("entities") or {}
            if entities:
                for key, val in entities.items():
                    st.markdown(f"**{key}:** {val}")
            else:
                st.info("No entities extracted.")

        # ── Section 3: Policy References ────────────
        with st.expander("Policy References", expanded=True):
            snippets = result.get("policy_snippets") or []
            if snippets:
                for i, snippet in enumerate(snippets, 1):
                    display = f"{i}. {snippet[:300]}..." if len(snippet) > 300 else f"{i}. {snippet}"
                    st.caption(display)
            else:
                st.info("No policy snippets retrieved.")

        # ── Section 4: Priority ─────────────────────
        with st.expander("Priority", expanded=True):
            score = result.get("priority_score")
            rationale = result.get("priority_rationale", "—")
            st.markdown(f"**Score:** {score}/5" if score is not None else "**Score:** —")
            st.markdown(f"**Rationale:** {rationale}")

        # ── Section 5: Internal Note ────────────────
        with st.expander("Internal Note", expanded=True):
            st.markdown(result.get("internal_note") or "—")

        # ── Section 6: Routing Decision ─────────────
        with st.expander("Routing Decision", expanded=True):
            st.markdown(f"**Destination:** {result.get('routing_destination', '—')}")
            st.markdown(f"**Recommended Action:** {result.get('recommended_action', '—')}")

        # ── Execution Trace ─────────────────────────
        with st.expander("Execution Trace"):
            trace = result.get("trace") or []
            for i, entry in enumerate(trace, 1):
                st.markdown(f"**Node {i} — {entry['step']}**")
                st.markdown(f"- *Input:* {entry['input_summary']}")
                st.markdown(f"- *Output:* {entry['output_summary']}")
                if i < len(trace):
                    st.divider()

    elif run:
        st.warning("Please enter a case description before running triage.")
