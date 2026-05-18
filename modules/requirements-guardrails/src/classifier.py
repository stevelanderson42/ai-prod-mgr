"""
Classifier orchestrator for the Requirements Guardrails module.

Main entry point: classify(query) -> GuardrailResult

Evaluates a query against all rule categories (compliance, suitability,
prohibited), resolves heuristic rules via Python functions, applies
produce-intent upgrades and context-first override logic, and returns
a fully-populated GuardrailResult.
"""

from src.models import (
    Classification,
    Category,
    TriggeredRule,
    GuardrailResult,
)
from src.rules.yaml_evaluator import evaluate_category, get_rule_config, RuleMatch
from src.rules.heuristics import (
    detect_produce_intent,
    has_unbalanced_claims,
    is_recommendation_request,
    has_risk_tolerance_context,
    has_time_horizon_context,
    has_jurisdiction_context,
    has_account_type_context,
    is_out_of_scope,
    resolve_priority,
)


# ── Heuristic Dispatch ───────────────────────────────────────────


def _has_gate_signals(query: str, rule_id: str, signal_key: str) -> bool:
    """Check whether a rule's gate signals are present in the query.

    Reads the specified signal list from the rule's YAML detection
    config and performs case-insensitive substring matching.
    """
    config = get_rule_config(rule_id)
    signals = config["detection"][signal_key]
    query_lower = query.lower()
    return any(s.lower() in query_lower for s in signals)


def _evaluate_heuristic(rule_id: str, query: str) -> bool:
    """Dispatch a heuristic rule to its Python implementation.

    Each heuristic rule has custom logic. Suitability rules use
    per-rule gate signals from YAML — is_recommendation_request
    gates risk_tolerance and time_horizon, while jurisdiction and
    account_type use their own YAML-defined gate signals.
    """
    if rule_id == "compliance.unbalanced_claims":
        return has_unbalanced_claims(query)

    if rule_id == "prohibited.out_of_scope":
        return is_out_of_scope(query)

    # Suitability rules: gate signal + context absence
    if rule_id == "suitability.missing_risk_tolerance":
        return (is_recommendation_request(query)
                and not has_risk_tolerance_context(query))

    if rule_id == "suitability.missing_time_horizon":
        return (is_recommendation_request(query)
                and not has_time_horizon_context(query))

    if rule_id == "suitability.missing_jurisdiction":
        return (_has_gate_signals(query, rule_id, "tax_signals")
                and not has_jurisdiction_context(query))

    if rule_id == "suitability.missing_account_type":
        return (_has_gate_signals(query, rule_id, "account_signals")
                and not has_account_type_context(query))

    return False


# ── Context-First Override ───────────────────────────────────────
#
# DESIGN DECISION: When suitability rules fire at CLARIFY (indicating
# missing context required for proper evaluation), compliance rules
# at ESCALATE are suppressed from priority resolution.
#
# Rationale: Escalating to a human reviewer without the required
# suitability context (risk tolerance, time horizon, jurisdiction)
# wastes the reviewer's time — they would need to request the same
# missing context before they could evaluate the compliance concern.
# CLARIFY first, then re-evaluate on the next request.
#
# Constraints:
#   - BLOCK rules are NEVER suppressed. A BLOCK from any category
#     always wins, regardless of suitability gaps.
#   - Suppressed compliance rules still appear in
#     GuardrailResult.triggered_rules for audit completeness.
#   - Only compliance ESCALATE rules are suppressed. Compliance
#     BLOCK rules (e.g., from produce-intent upgrade or
#     market_manipulation) are not affected.
#
# Assumption: produce-intent upgrade always transforms ESCALATE → BLOCK.
# The override checks for ESCALATE specifically, so upgraded rules
# (now at BLOCK) are never suppressed. If a future upgrade target
# other than BLOCK is introduced, this logic must be revisited.


def _apply_context_first_override(
    confirmed_matches: list[RuleMatch],
) -> list[tuple[Classification, Category, TriggeredRule]]:
    """Build the priority resolution input, applying context-first override.

    Returns a filtered list of (Classification, Category, TriggeredRule)
    tuples for resolve_priority. When suitability CLARIFY rules are
    present, compliance ESCALATE rules are excluded from this list
    (but remain in confirmed_matches for audit purposes).
    """
    has_suitability_clarify = any(
        m.category == Category.SUITABILITY
        and m.classification == Classification.CLARIFY
        for m in confirmed_matches
    )

    priority_input = []
    for m in confirmed_matches:
        # Suppress compliance ESCALATE when suitability CLARIFY fires
        if (has_suitability_clarify
                and m.category == Category.COMPLIANCE
                and m.classification == Classification.ESCALATE):
            continue
        priority_input.append((
            m.classification,
            m.category,
            TriggeredRule(rule_id=m.rule_id, description=m.description),
        ))

    return priority_input


# ── Result Construction ──────────────────────────────────────────


def _build_decision_reason(
    final_cls: Classification,
    confirmed_matches: list[RuleMatch],
    missing_context: list[str],
) -> str:
    """Generate a human-readable decision reason."""
    if final_cls == Classification.PROCEED:
        return "No guardrails triggered."

    if final_cls == Classification.CLARIFY:
        fields = ", ".join(missing_context)
        return f"Missing required context: {fields}."

    # For BLOCK, check for out-of-scope specifically
    if final_cls == Classification.BLOCK:
        if any(m.rule_id == "prohibited.out_of_scope"
               for m in confirmed_matches
               if m.classification == Classification.BLOCK):
            return "Request is outside the financial services domain."

    # For ESCALATE and BLOCK, use the first matching rule's description
    for m in confirmed_matches:
        if m.classification == final_cls:
            return m.description

    return "Classification determined by rule evaluation."


def _build_next_action(
    final_cls: Classification,
    confirmed_matches: list[RuleMatch],
    missing_context: list[str],
) -> str:
    """Generate a human-readable next action."""
    if final_cls == Classification.PROCEED:
        return "Forward to model for response generation."

    if final_cls == Classification.CLARIFY:
        fields = ", ".join(missing_context)
        return (f"Request additional context from user "
                f"before proceeding: {fields}.")

    if final_cls == Classification.ESCALATE:
        return "Route to human review with full context."

    # BLOCK — soft redirect for out-of-scope, hard block otherwise
    if any(m.rule_id == "prohibited.out_of_scope"
           for m in confirmed_matches
           if m.classification == Classification.BLOCK):
        return (
            "This system is designed for financial services questions. "
            "I can help with investment, account, and financial planning "
            "topics instead."
        )

    return "Request blocked. Inform user with explanation."


# ── Main Entry Point ─────────────────────────────────────────────


def classify(query: str) -> GuardrailResult:
    """Classify a query against all guardrail rules.

    Steps:
        1. Evaluate all three rule categories (keyword/regex + heuristic
           candidates) via the YAML evaluator.
        2. Resolve heuristic rules via Python functions.
        3. Apply produce-intent upgrade to eligible compliance rules.
        4. Apply context-first override (suitability CLARIFY suppresses
           compliance ESCALATE from priority resolution).
        5. Resolve priority routing to determine final classification.
        6. Determine reporting category via tiebreaking.
        7. Construct and return a fully-populated GuardrailResult.

    Args:
        query: The user's input text.

    Returns:
        A GuardrailResult with classification, category, triggered_rules,
        missing_context, decision_reason, and next_action populated.
    """
    # Step 1: Evaluate all categories
    all_matches: list[RuleMatch] = []
    for category in [Category.COMPLIANCE, Category.SUITABILITY, Category.PROHIBITED]:
        all_matches.extend(evaluate_category(query, category))

    # Step 2: Resolve heuristic rules — keep only confirmed matches
    confirmed_matches: list[RuleMatch] = []
    for match in all_matches:
        if match.is_heuristic:
            if _evaluate_heuristic(match.rule_id, query):
                confirmed_matches.append(match)
        else:
            # Already confirmed by keyword/regex matching
            confirmed_matches.append(match)

    # Step 3: Apply produce-intent upgrade
    # Mutates RuleMatch.classification in place. Assumes upgrade target
    # is BLOCK (see context-first override comment for implications).
    if detect_produce_intent(query):
        for match in confirmed_matches:
            if match.produce_intent_upgrade is not None:
                match.classification = match.produce_intent_upgrade

    # Step 4: Build triggered_rules for audit (ALL confirmed rules,
    # including those that will be suppressed by context-first override)
    triggered_rules = [
        TriggeredRule(rule_id=m.rule_id, description=m.description)
        for m in confirmed_matches
    ]

    # Step 5: Apply context-first override and resolve priority
    priority_input = _apply_context_first_override(confirmed_matches)
    final_cls, final_cat = resolve_priority(priority_input)

    # Step 6: Collect missing_context from suitability CLARIFY rules
    missing_context: list[str] = []
    if final_cls == Classification.CLARIFY:
        for m in confirmed_matches:
            if (m.category == Category.SUITABILITY
                    and m.classification == Classification.CLARIFY):
                for ctx in m.missing_context:
                    if ctx not in missing_context:
                        missing_context.append(ctx)

    # Step 7: Build human-readable fields
    decision_reason = _build_decision_reason(
        final_cls, confirmed_matches, missing_context,
    )
    next_action = _build_next_action(
        final_cls, confirmed_matches, missing_context,
    )

    # Step 8: Construct result
    return GuardrailResult(
        classification=final_cls,
        category=final_cat,
        decision_reason=decision_reason,
        next_action=next_action,
        triggered_rules=triggered_rules,
        missing_context=missing_context,
    )
