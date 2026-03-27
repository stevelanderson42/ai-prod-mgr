import streamlit as st
from main import build_graph
from state import create_initial_state

# ── Page Config ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Case Triage Workflow",
    layout="wide",
)

st.title("AI Case Triage Workflow — Agentic Orchestration")

SCENARIOS = {
    "1. Suitability Complaint (Reg BI)": (
        "Customer states their advisor recommended an unsuitable mutual fund product "
        "that did not align with their stated risk tolerance or investment objectives. "
        "Customer is requesting a full review of the recommendation and potential restitution."
    ),
    "2. Unauthorized Transaction (Fraud)": (
        "Customer reports three unauthorized transactions totaling $4,200 on their "
        "brokerage account over the past week. Customer states they did not authorize "
        "these trades and believes their account credentials may have been compromised. "
        "Requesting immediate account freeze and investigation."
    ),
    "3. Communication Complaint (FINRA 2210)": (
        "Customer received a promotional communication from their advisor that included "
        "projected returns and performance guarantees without adequate risk disclosures. "
        "Customer states the communication was misleading and influenced their investment "
        "decision."
    ),
    "4. Account Access / Fraud Report": (
        "Customer is unable to access their online brokerage account and suspects "
        "unauthorized access. Customer reports receiving password reset emails they did "
        "not initiate and notices an unrecognized device in their account activity log."
    ),
    "5. Fee Dispute with Escalation": (
        "Customer is disputing $340 in advisory fees charged over the past quarter, "
        "stating the fees were not disclosed in their client agreement. Customer is "
        "requesting a full fee breakdown and refund, and is threatening to escalate to "
        "FINRA if not resolved within 5 business days."
    ),
}

# ── Two-Column Layout ──────────────────────────────────────
left, right = st.columns([0.4, 0.6])

with left:
    st.markdown("### What This Demo Shows")
    st.markdown("""
This demo simulates how an AI-orchestrated triage system
processes operational cases in a regulated financial services
environment. Submit a case in plain text — or select one of
five pre-loaded scenarios — and watch a six-step agentic
workflow classify the issue, extract key entities, retrieve
relevant compliance policy, score priority, draft an internal
routing note, and produce a final routing decision. Every step
is logged in a visible execution trace.
""")

    st.markdown("### Select a Scenario to Get Started")
    st.markdown("""
Each scenario represents a real complaint or incident category
that regulated firms handle daily — designed to exercise
different regulatory triggers and produce different
classification, policy retrieval, and routing outcomes.
Select one to pre-populate the case text, or write your own below.
""")

    scenario = st.selectbox("Select Demo Scenario", list(SCENARIOS.keys()))
    case_text = st.text_area(
        "Submit Operational Case",
        value=SCENARIOS[scenario],
        height=220,
    )
    run = st.button("Run Triage", type="primary")

    st.markdown("---")
    st.markdown("### Understanding Your Results")
    st.markdown("""
Results appear in the right panel. Each section reflects
one stage of the workflow:
""")
    st.markdown("""
- **Classification** — identifies the issue type, risk level,
  and regulatory trigger
- **Entities** — extracts structured facts from the case text
- **Policy References** — shows compliance content retrieved
  live from the knowledge corpus
- **Priority** — scores urgency on a 1–5 scale with rationale
- **Internal Note** — drafts a structured summary for the
  routing team
- **Routing Decision** — produces the final destination and
  recommended action
- **Execution Trace** — logs every node's input and output
  in sequence
""")

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
                for i, snippet in enumerate(snippets):
                    lines = [l for l in snippet.split('\n')
                             if not l.strip().startswith('#') and l.strip()]
                    clean = ' '.join(lines)[:250]
                    st.info(f"[{i+1}] {clean}...")
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
