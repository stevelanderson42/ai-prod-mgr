"""
Python heuristic functions for rules that require multi-signal
detection beyond keyword/regex matching.

Each function corresponds to a YAML rule with detection.type: heuristic,
or to a cross-cutting classification mechanism (produce-intent detection,
priority resolution).

All functions receive the query text and return a boolean (whether the
heuristic triggered) or a structured result.
"""

import re

from src.models import Classification, Category, TriggeredRule
from src.rules.yaml_evaluator import get_rule_config


# ── Produce-Intent Detection ─────────────────────────────────────
#
# HIGHEST-RISK HEURISTIC in the inventory. This function determines
# whether compliance rules with produce_intent_upgrade are elevated
# to BLOCK. Edge-case behavior is most likely here.
#
# Test coverage:
#   - Produce-intent positives: samples #3, #8 (queries asking the
#     system to write/draft/generate violating content).
#   - False-positive avoidance: queries that contain but do not request
#     violating language, e.g., "My advisor said this is guaranteed,
#     should I be worried?" must NOT trigger produce-intent upgrade.

_PRODUCE_SIGNALS = [
    "write me ",
    "write a ",
    "write an ",
    "help me write",
    "draft a ",
    "draft an ",
    "draft me ",
    "help me draft",
    "create a ",
    "create an ",
    "help me create",
    "generate a ",
    "generate an ",
    "compose a ",
    "compose an ",
]


def detect_produce_intent(query: str) -> bool:
    """Determine whether the query asks the system to generate content.

    Returns True when the query asks the system to produce, write, draft,
    or create content (e.g., "Write me a message saying..."). Returns
    False when the query merely contains or references violating language
    (e.g., "My client said this is guaranteed, is that OK?").

    Uses substring matching against multi-word produce signals.
    Trailing spaces in signals provide basic word-boundary behavior
    (e.g., "write a " won't match "write about").

    Used by the classifier to apply produce_intent_upgrade on eligible
    compliance rules.
    """
    query_lower = query.lower()
    return any(signal in query_lower for signal in _PRODUCE_SIGNALS)


# ── Compliance Heuristics ─────────────────────────────────────────


def has_unbalanced_claims(query: str) -> bool:
    """Detect benefit language without corresponding risk disclosure.

    Returns True when benefit_signals are present AND risk_signals
    are absent. Signal lists are loaded from compliance.yaml
    (compliance.unbalanced_claims rule).
    """
    config = get_rule_config("compliance.unbalanced_claims")
    detection = config["detection"]
    benefit_signals = detection["benefit_signals"]
    risk_signals = detection["risk_signals"]

    query_lower = query.lower()
    has_benefits = any(s.lower() in query_lower for s in benefit_signals)
    has_risks = any(s.lower() in query_lower for s in risk_signals)

    return has_benefits and not has_risks


# ── Suitability Heuristics ────────────────────────────────────────


def is_recommendation_request(query: str) -> bool:
    """Detect whether the query is seeking a recommendation or advice.

    Gate function for suitability.missing_risk_tolerance and
    suitability.missing_time_horizon. Other suitability rules
    (missing_jurisdiction, missing_account_type) use their own
    gate signals defined in YAML — the orchestrator handles dispatch.

    Signal list loaded from suitability.missing_risk_tolerance
    (recommendation_signals shared across recommendation-gated rules).
    """
    config = get_rule_config("suitability.missing_risk_tolerance")
    signals = config["detection"]["recommendation_signals"]
    query_lower = query.lower()
    return any(s.lower() in query_lower for s in signals)


def has_risk_tolerance_context(query: str) -> bool:
    """Check whether risk tolerance is stated in the query.

    Returns True if any context_signals from
    suitability.missing_risk_tolerance are present.
    """
    config = get_rule_config("suitability.missing_risk_tolerance")
    signals = config["detection"]["context_signals"]
    query_lower = query.lower()
    return any(s.lower() in query_lower for s in signals)


def has_time_horizon_context(query: str) -> bool:
    """Check whether time horizon is stated in the query.

    Returns True if any context_signals from
    suitability.missing_time_horizon are present.
    """
    config = get_rule_config("suitability.missing_time_horizon")
    signals = config["detection"]["context_signals"]
    query_lower = query.lower()
    return any(s.lower() in query_lower for s in signals)


_US_STATE_NAMES = [
    "alabama", "alaska", "arizona", "arkansas", "california",
    "colorado", "connecticut", "delaware", "florida", "georgia",
    "hawaii", "idaho", "illinois", "indiana", "iowa", "kansas",
    "kentucky", "louisiana", "maine", "maryland", "massachusetts",
    "michigan", "minnesota", "mississippi", "missouri", "montana",
    "nebraska", "nevada", "new hampshire", "new jersey",
    "new mexico", "new york", "north carolina", "north dakota",
    "ohio", "oklahoma", "oregon", "pennsylvania", "rhode island",
    "south carolina", "south dakota", "tennessee", "texas", "utah",
    "vermont", "virginia", "washington", "west virginia",
    "wisconsin", "wyoming", "district of columbia",
]

# All 50 states + DC. Case-sensitive word-boundary matching reduces
# false positives from common English words (in, or, me, oh, ok, hi).
_US_STATE_ABBREVS = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
    "DC",
]


def has_jurisdiction_context(query: str) -> bool:
    """Check whether jurisdiction/state is stated in the query.

    Returns True if US state names (case-insensitive substring match)
    or state abbreviations (case-sensitive word-boundary match) are
    present.

    v1 limitation: Case-sensitive abbreviation matching may miss
    all-caps queries where common words like "IN" appear as
    standalone tokens. Full state names are the reliable path.
    """
    query_lower = query.lower()
    if any(state in query_lower for state in _US_STATE_NAMES):
        return True
    for abbrev in _US_STATE_ABBREVS:
        if re.search(rf"\b{abbrev}\b", query):
            return True
    return False


def has_account_type_context(query: str) -> bool:
    """Check whether account type is identifiable in the query.

    Returns True if any type_signals from
    suitability.missing_account_type are present.
    """
    config = get_rule_config("suitability.missing_account_type")
    signals = config["detection"]["type_signals"]
    query_lower = query.lower()
    return any(s.lower() in query_lower for s in signals)


# ── Prohibited Heuristics ─────────────────────────────────────────

# Financial domain signals for out-of-scope detection.
# is_out_of_scope returns True when NONE of these are present.
# Partial stems (e.g., "securit", "diversif") match inflected forms.
_FINANCIAL_DOMAIN_SIGNALS = [
    "invest", "fund", "stock", "bond", "ira", "401k", "roth",
    "portfolio", "return", "market", "trade", "financial", "bank",
    "savings", "retirement", "tax", "asset", "allocation", "expense",
    "ratio", "dividend", "interest", "mortgage", "loan", "credit",
    "wealth", "capital", "equity", "etf", "index", "brokerage",
    "deposit", "withdrawal", "contribution", "beneficiary", "trust",
    "estate", "annuity", "insurance", "pension", "dollar-cost",
    "compound", "diversif", "hedge", "option", "futures", "commodity",
    "yield", "balance", "account", "fee", "premium", "securit",
    "money", "income", "profit", "loss", "risk", "growth",
    "inflation", "debt", "budget", "fiduciary", "advisor",
]


def is_out_of_scope(query: str) -> bool:
    """Detect queries entirely outside the financial services domain.

    Returns True when the query has no financial content signals.
    Heuristic approach: check for absence of financial domain
    keywords rather than presence of non-financial keywords
    (open-domain negative detection is unreliable via keywords alone).

    Matching is substring-based — signals like "risk" will match
    within "risk-free", "loss" within "losses", "securit" within
    "securities", etc. This is intentional: substring matching
    with stem fragments provides lightweight inflection coverage.

    v1 design: conservative — only blocks queries with zero financial
    relevance. A non-financial query containing a financial term
    incidentally (e.g., "what's the balance of power") would pass
    through, which is an acceptable false negative for v1.
    """
    query_lower = query.lower()
    return not any(signal in query_lower for signal in _FINANCIAL_DOMAIN_SIGNALS)


# ── Priority Resolution ──────────────────────────────────────────

# Category tiebreaking when multiple rules fire at the same
# classification level. Higher value = higher priority.
_CATEGORY_PRIORITY: dict[Category, int] = {
    Category.PROHIBITED: 2,
    Category.COMPLIANCE: 1,
    Category.SUITABILITY: 0,
}


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

    Note: The classifier orchestrator applies a context-first override
    BEFORE calling this function — when suitability CLARIFY rules fire,
    compliance ESCALATE rules are removed from the input list. See
    classifier.py for the override rationale. This function implements
    only the mechanical priority ordering.
    """
    if not triggered:
        return (Classification.PROCEED, Category.NONE)

    # Find highest classification level
    max_priority = max(t[0].priority for t in triggered)

    # Filter to rules at that classification level
    at_max = [t for t in triggered if t[0].priority == max_priority]

    # Tiebreak by category priority: prohibited > compliance > suitability
    winner = max(at_max, key=lambda t: _CATEGORY_PRIORITY.get(t[1], -1))

    return (winner[0], winner[1])
