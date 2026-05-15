"""
Python heuristic functions for rules that require multi-signal
detection beyond keyword/regex matching.

Each function corresponds to a YAML rule with detection.type: heuristic,
or to a cross-cutting classification mechanism (produce-intent detection,
priority resolution).

All functions receive the query text and return a boolean (whether the
heuristic triggered) or a structured result. Implementation is deferred
to Session 2 — this file defines the interface contract only.
"""

from src.models import Classification, Category, TriggeredRule, GuardrailResult


# --- Produce-Intent Detection ---
#
# HIGHEST-RISK HEURISTIC in the inventory. This function determines
# whether compliance rules with produce_intent_upgrade are elevated
# to BLOCK. Edge-case behavior is most likely here.
#
# Session 2 must include explicit test coverage for:
#   - Produce-intent positives: samples #3, #8 (queries asking the
#     system to write/draft/generate violating content).
#   - False-positive avoidance: queries that contain but do not request
#     violating language, e.g., "My advisor said this is guaranteed,
#     should I be worried?" must NOT trigger produce-intent upgrade.


def detect_produce_intent(query: str) -> bool:
    """Determine whether the query asks the system to generate content.

    Returns True when the query asks the system to produce, write, draft,
    or create content (e.g., "Write me a message saying..."). Returns
    False when the query merely contains or references violating language
    (e.g., "My client said this is guaranteed, is that OK?").

    Used by the classifier to apply produce_intent_upgrade on eligible
    compliance rules.
    """
    ...


# --- Compliance Heuristics ---


def has_unbalanced_claims(query: str) -> bool:
    """Detect benefit language without corresponding risk disclosure.

    Returns True when benefit_signals are present AND risk_signals
    are absent. Signal lists are loaded from compliance.yaml
    (compliance.unbalanced_claims rule).
    """
    ...


# --- Suitability Heuristics ---


def is_recommendation_request(query: str) -> bool:
    """Detect whether the query is seeking a recommendation or advice.

    Gate function for all suitability.missing_* rules. If this returns
    False, no suitability context checks fire (a factual question
    doesn't require risk tolerance or time horizon).
    """
    ...


def has_risk_tolerance_context(query: str) -> bool:
    """Check whether risk tolerance is stated in the query.

    Returns True if any context_signals from
    suitability.missing_risk_tolerance are present.
    """
    ...


def has_time_horizon_context(query: str) -> bool:
    """Check whether time horizon is stated in the query.

    Returns True if any context_signals from
    suitability.missing_time_horizon are present.
    """
    ...


def has_jurisdiction_context(query: str) -> bool:
    """Check whether jurisdiction/state is stated in the query.

    Returns True if state names, abbreviations, or jurisdiction
    indicators are present.
    """
    ...


def has_account_type_context(query: str) -> bool:
    """Check whether account type is identifiable in the query.

    Returns True if any type_signals from
    suitability.missing_account_type are present.
    """
    ...


# --- Prohibited Heuristics ---


def is_out_of_scope(query: str) -> bool:
    """Detect queries entirely outside the financial services domain.

    Returns True when the query has no financial content signals.
    Heuristic approach: check for absence of financial domain
    keywords rather than presence of non-financial keywords
    (open-domain negative detection is unreliable via keywords alone).
    """
    ...


# --- Priority Resolution ---


def resolve_priority(
    triggered: list[tuple[Classification, Category, TriggeredRule]],
) -> tuple[Classification, Category]:
    """Resolve the final classification when multiple rules fire.

    Applies BLOCK > ESCALATE > CLARIFY > PROCEED priority ordering
    using Classification.priority. Returns the winning classification
    and the category of the highest-priority triggered rule.

    When multiple rules share the same classification level,
    category priority is: prohibited > compliance > suitability.
    Same-level multi-category triggering is rare in practice. The
    category field in GuardrailResult reports the highest-priority
    category that fired; the triggered_rules array carries the
    complete picture across all categories regardless of category
    tiebreaking.
    """
    ...
