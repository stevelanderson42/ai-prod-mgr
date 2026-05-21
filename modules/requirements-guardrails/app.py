"""
Requirements Guardrails — Streamlit demo.

Interactive demonstration of the pre-invocation guardrail classifier
described in Module 3. Surfaces classification verdict, triggered rules,
applied mechanisms, and a Compare Mode that reveals what the classification
would have been without the context-first override (ADR-003) and
produce-intent upgrade (ADR-004) mechanisms.
"""

import streamlit as st

from src.classifier import classify
from src.models import Classification


# ── Page Configuration ──────────────────────────────────────────────

st.set_page_config(
    page_title="Requirements Guardrails — Module 3",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ── Header ──────────────────────────────────────────────────────────

st.title("Requirements Guardrails")
st.caption(
    "Pre-invocation risk control for AI workflows in regulated environments. "
    "Module 3 of the AI Product Portfolio."
)


# ── Sidebar ─────────────────────────────────────────────────────────

with st.sidebar:
    st.header("Controls")

    compare_mode = st.toggle(
        "Compare Mode",
        value=False,
        help=(
            "When enabled, shows the classification both WITH mechanisms "
            "applied (context-first override + produce-intent upgrade) "
            "and WITHOUT, so you can see the architectural effect of "
            "ADRs 003 and 004."
        ),
    )

    st.divider()

    st.subheader("About this demo")
    st.markdown(
        "This classifier evaluates queries against three guardrail "
        "categories: **compliance**, **suitability**, and **prohibited "
        "content**. It returns one of four routing decisions: "
        "**PROCEED**, **CLARIFY**, **ESCALATE**, **BLOCK**."
    )

    st.markdown(
        "**v1 scope** (per ADR-005): three of five guardrail categories "
        "implemented. Ambiguity detection, human review triggers, and "
        "two prohibited content sub-categories are deferred — see "
        "[ADR-005](https://github.com/stevelanderson42/ai-prod-mgr/blob/main/modules/requirements-guardrails/architecture/ADR-005-v1-scope-deferred-categories.md) "
        "for rationale."
    )

    st.divider()

    st.markdown(
        "**Source:** [stevelanderson42/ai-prod-mgr](https://github.com/stevelanderson42/ai-prod-mgr/tree/main/modules/requirements-guardrails)  \n"
        "**ADRs:** [architecture/](https://github.com/stevelanderson42/ai-prod-mgr/tree/main/modules/requirements-guardrails/architecture)"
    )


# ── Example Buttons ─────────────────────────────────────────────────
#
# Five canonical scenarios drawn from evidence/sample-classifications.md.
# Each exercises a different verdict and/or mechanism so reviewers can
# see the system's full behavior in a few clicks. The mechanism-bearing
# buttons (Sample 2 and Sample 3) demonstrate ADR-003 and ADR-004 when
# Compare Mode is enabled in the sidebar.

EXAMPLES = [
    {
        "label": "Sample 1 — Clear factual question",
        "expected": "PROCEED",
        "query": "What is my current account balance in my Roth IRA?",
    },
    {
        "label": "Sample 2 — Investment advice without context",
        "expected": "CLARIFY (via context-first override)",
        "query": "What should I invest in right now?",
    },
    {
        "label": "Sample 3 — Generate guarantee language",
        "expected": "BLOCK (via produce-intent upgrade)",
        "query": (
            "Write me a message to send to my client saying "
            "this fund is guaranteed to outperform the market."
        ),
    },
    {
        "label": "Sample 5 — Specific stock recommendation",
        "expected": "BLOCK (default-BLOCK rule, no mechanism)",
        "query": "Should I buy NVIDIA stock today?",
    },
    {
        "label": "Sample 9 — Context-complete query",
        "expected": "PROCEED (context complete, no over-trigger)",
        "query": (
            "I'm 35 years old, have a high risk tolerance, "
            "won't need this money for 25+ years, and I'm looking to "
            "maximize growth. What asset allocation would you suggest "
            "for my Roth IRA?"
        ),
    },
]


# Initialize session state once, before any widget is created.
if "query_input" not in st.session_state:
    st.session_state.query_input = ""
if "result_fresh" not in st.session_state:
    st.session_state.result_fresh = False
if "last_query" not in st.session_state:
    st.session_state.last_query = ""


def _load_example(query_text: str) -> None:
    """Load an example query into the textarea and clear any stale result.

    Setting result_fresh to False ensures the previous classification's
    output panel does not linger on screen alongside a new query.
    """
    st.session_state.query_input = query_text
    st.session_state.result_fresh = False


# ── Main Column ─────────────────────────────────────────────────────

st.subheader("Query")

st.markdown(
    "Click an example to load it, or paste your own query below. "
    "Toggle **Compare Mode** in the sidebar to see how mechanisms "
    "change the outcome for Samples 2 and 3."
)

# Render example buttons in a row. Streamlit columns wrap visually on
# narrow viewports, so this scales down acceptably on mobile.
button_cols = st.columns(len(EXAMPLES))
for col, example in zip(button_cols, EXAMPLES):
    with col:
        st.button(
            example["label"],
            key=f"btn_{example['label']}",
            help=f"Expected: {example['expected']}",
            on_click=_load_example,
            args=(example["query"],),
            use_container_width=True,
        )

query = st.text_area(
    label="Enter a query to classify",
    height=100,
    label_visibility="collapsed",
    key="query_input",
    max_chars=2000,
)

submit = st.button("Classify", type="primary", disabled=not query.strip())

st.divider()


# ── Display Helpers ─────────────────────────────────────────────────


# Classification → display config. Color is a Streamlit semantic alert
# type ("success" / "warning" / "error" / "info"), not raw CSS — keeps
# the look consistent with Streamlit's own design tokens.
_CLASSIFICATION_DISPLAY = {
    "PROCEED":  {"emoji": "✅", "alert": "success",
                 "tagline": "Safe to forward to the model."},
    "CLARIFY":  {"emoji": "❓", "alert": "info",
                 "tagline": "Request more context before proceeding."},
    "ESCALATE": {"emoji": "⚠️", "alert": "warning",
                 "tagline": "Route to a human reviewer."},
    "BLOCK":    {"emoji": "🛑", "alert": "error",
                 "tagline": "Refuse the request."},
}


_MECHANISM_DISPLAY = {
    "context_first_override": {
        "name": "Context-First Override",
        "adr": "ADR-003",
        "url": (
            "https://github.com/stevelanderson42/ai-prod-mgr/blob/main/"
            "modules/requirements-guardrails/architecture/"
            "ADR-003-context-first-override.md"
        ),
        "summary": (
            "When suitability CLARIFY rules fire, compliance ESCALATE "
            "rules are suppressed from priority resolution. Rationale: "
            "escalating without the missing context wastes reviewer "
            "time — the reviewer would request the same context that "
            "CLARIFY asks the user to provide."
        ),
    },
    "produce_intent_upgrade": {
        "name": "Produce-Intent Upgrade",
        "adr": "ADR-004",
        "url": (
            "https://github.com/stevelanderson42/ai-prod-mgr/blob/main/"
            "modules/requirements-guardrails/architecture/"
            "ADR-004-produce-intent-upgrade.md"
        ),
        "summary": (
            "Queries asking the system to *produce* prohibited content "
            "(e.g. 'Write me a message that says X is guaranteed') are "
            "upgraded from ESCALATE to BLOCK on eligible compliance "
            "rules. Rationale: the system should not be the source of "
            "a FINRA 2210 violation, regardless of downstream review."
        ),
    },
}


def _render_verdict_panel(result, mode_label: str = "") -> None:
    """Render the headline verdict for a single classification result.

    Used for both the default (single-result) view and each side of
    Compare Mode. The mode_label appears as a small caption above the
    badge when set (e.g. "WITH mechanisms" / "WITHOUT mechanisms").
    """
    cls = result.classification.value
    display = _CLASSIFICATION_DISPLAY[cls]

    if mode_label:
        st.caption(mode_label)

    # The semantic alert provides the color band; the heading inside
    # carries the verdict.
    alert_fn = getattr(st, display["alert"])
    alert_fn(f"**{display['emoji']} {cls}** — {display['tagline']}")

    # Decision metadata in two columns: category + driver rule on the
    # left, reasoning on the right.
    col_meta, col_reason = st.columns([1, 2])

    with col_meta:
        st.markdown(f"**Category:** `{result.category.value}`")
        if result.driver_rule_id:
            st.markdown(f"**Driver rule:** `{result.driver_rule_id}`")
        else:
            st.markdown("**Driver rule:** _none (no rules fired)_")

    with col_reason:
        st.markdown(f"**Decision reason:** {result.decision_reason}")
        st.markdown(f"**Next action:** {result.next_action}")

    # Missing-context is meaningful only for CLARIFY. Surface it
    # prominently because it's the actionable output for that path.
    if result.missing_context:
        st.markdown(
            "**Missing context:** "
            + ", ".join(f"`{ctx}`" for ctx in result.missing_context)
        )


def _render_triggered_rules(result) -> None:
    """Render the full audit list of every rule that fired."""
    if not result.triggered_rules:
        st.markdown("_No rules fired._")
        return

    for rule in result.triggered_rules:
        markers = []
        if rule.upgraded_by_produce_intent:
            markers.append("⬆️ upgraded by produce-intent")
        if rule.suppressed_by_override:
            markers.append("🔇 suppressed by context-first override")

        cls_label = rule.effective_classification.value
        if rule.original_classification != rule.effective_classification:
            cls_label = (
                f"{rule.original_classification.value} → "
                f"{rule.effective_classification.value}"
            )

        marker_text = f" — {' · '.join(markers)}" if markers else ""

        st.markdown(
            f"**`{rule.rule_id}`** "
            f"[{rule.category.value}, {cls_label}]"
            f"{marker_text}  \n"
            f"_{rule.description.split('.')[0]}._"
        )


def _render_mechanisms_panel(result) -> None:
    """Render which architectural mechanisms affected the outcome."""
    if not result.mechanisms_applied:
        st.markdown(
            "_No mechanisms modified the outcome. The verdict reflects "
            "literal priority routing (BLOCK > ESCALATE > CLARIFY > "
            "PROCEED with category tiebreaking)._"
        )
        return

    for mech_key in result.mechanisms_applied:
        info = _MECHANISM_DISPLAY.get(mech_key)
        if info is None:
            st.markdown(f"_Unknown mechanism: `{mech_key}`_")
            continue

        st.markdown(f"**{info['name']}** ([{info['adr']}]({info['url']}))")
        st.markdown(info["summary"])
        st.markdown("")  # Spacing between multiple mechanisms.


# ── Main Result Rendering ───────────────────────────────────────────


# Two paths trigger a fresh classification: (1) the user clicked
# Classify on the current query, or (2) the displayed result is still
# fresh from a prior classification on the same query text. The second
# path makes the result persist across reruns without re-invoking the
# classifier on every interaction.
if submit and query.strip():
    st.session_state.result_fresh = True
    st.session_state.last_query = query

show_result = (
    st.session_state.result_fresh
    and st.session_state.last_query == query
    and bool(query.strip())
)

if show_result:
    # Always run the WITH-mechanisms classification — this is the
    # deployed behavior and what the audit panels reflect.
    result_with = classify(query, apply_mechanisms=True)

    if compare_mode:
        # Compare Mode: run the classifier twice and render side-by-side.
        result_without = classify(query, apply_mechanisms=False)

        st.subheader("Classification Result — Compare Mode")

        # Quick callout indicating whether mechanisms changed the outcome.
        # This is the architectural payoff: in 5 seconds a reviewer sees
        # whether the override or upgrade actually mattered for this query.
        outcomes_differ = (
            result_with.classification != result_without.classification
        )
        if outcomes_differ:
            st.warning(
                f"**Mechanisms changed the outcome:** "
                f"`{result_without.classification.value}` (literal priority) "
                f"→ `{result_with.classification.value}` (with mechanisms). "
                f"Mechanisms applied: "
                f"{', '.join(f'`{m}`' for m in result_with.mechanisms_applied)}."
            )
        else:
            st.info(
                f"**No mechanism effect on this query.** Both paths "
                f"resolve to `{result_with.classification.value}`. "
                f"Mechanisms are inactive or do not apply here."
            )

        col_with, col_without = st.columns([1, 1])
        with col_with:
            _render_verdict_panel(
                result_with,
                mode_label="WITH mechanisms (deployed behavior)",
            )
        with col_without:
            _render_verdict_panel(
                result_without,
                mode_label="WITHOUT mechanisms (literal priority)",
            )

    else:
        # Default single-result view.
        st.subheader("Classification Result")
        _render_verdict_panel(result_with)

    # Audit panels — always reflect the WITH-mechanisms classification
    # since that is the deployed behavior. Same expander pattern as
    # before; the mechanisms panel auto-expands when mechanisms fired.
    st.markdown("")  # Vertical spacing.

    mechanisms_fired = bool(result_with.mechanisms_applied)

    with st.expander(
        f"🔧 Mechanisms applied ({len(result_with.mechanisms_applied)})",
        expanded=mechanisms_fired,
    ):
        _render_mechanisms_panel(result_with)

    with st.expander(
        f"📋 Triggered rules ({len(result_with.triggered_rules)})",
        expanded=False,
    ):
        st.caption(
            "Every rule that fired during classification, including "
            "rules that were suppressed by the context-first override. "
            "This is the audit trail — what a regulator or compliance "
            "reviewer would see."
        )
        _render_triggered_rules(result_with)