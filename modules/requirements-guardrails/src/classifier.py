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
    """Check whether a rule's gate signals are present in the query."""
    config = get_rule_config(rule_id)
    signals = config["detection"][signal_key]
    query_lower = query.lower()
    return any(s.lower() in query_lower for s in signals)


def _evaluate_heuristic(rule_id: str, query: str) -> bool:
    """Dispatch a heuristic rule to its Python implementation."""
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


# ── Mechanism Application (Pure, Non-Mutating) ───────────────────


def _compute_effective_classifications(
    confirmed_matches: list[RuleMatch],
    produce_intent: bool,
) -> dict[str, Classification]:
    """Compute each rule's effective classification after produce-intent upgrade.

    Returns a dict mapping rule_id -> effective_classification. Does NOT
    mutate the input matches. When produce_intent is False, effective
    equals original for every rule.
    """
    effective: dict[str, Classification] = {}
    for m in confirmed_matches:
        if produce_intent and m.produce_intent_upgrade is not None:
            effective[m.rule_id] = m.produce_intent_upgrade
        else:
            effective[m.rule_id] = m.classification
    return effective


def _apply_context_first_override(
    confirmed_matches: list[RuleMatch],
    effective: dict[str, Classification],
) -> tuple[list[tuple[Classification, Category, TriggeredRule]], set[str]]:
    """Build priority resolution input, applying context-first override.

    When suitability CLARIFY rules are present in the effective
    classification map, compliance ESCALATE rules are excluded from
    the priority resolution input. Returns:
        - The filtered list for resolve_priority
        - A set of rule_ids that were suppressed by the override

    BLOCK rules are never suppressed. Upgraded rules (now at BLOCK
    via produce_intent) are also never suppressed because the
    suppression check tests for ESCALATE specifically.
    """
    has_suitability_clarify = any(
        m.category == Category.SUITABILITY
        and effective[m.rule_id] == Classification.CLARIFY
        for m in confirmed_matches
    )

    priority_input = []
    suppressed_ids: set[str] = set()

    for m in confirmed_matches:
        eff_cls = effective[m.rule_id]
        if (has_suitability_clarify
                and m.category == Category.COMPLIANCE
                and eff_cls == Classification.ESCALATE):
            suppressed_ids.add(m.rule_id)
            continue
        priority_input.append((
            eff_cls,
            m.category,
            TriggeredRule(
                rule_id=m.rule_id,
                description=m.description,
                category=m.category,
                original_classification=m.classification,
                effective_classification=eff_cls,
            ),
        ))

    return priority_input, suppressed_ids


# ── Result Helpers ───────────────────────────────────────────────


def _build_decision_reason(
    final_cls: Classification,
    confirmed_matches: list[RuleMatch],
    effective: dict[str, Classification],
    missing_context: list[str],
) -> str:
    """Generate a human-readable decision reason."""
    if final_cls == Classification.PROCEED:
        return "No guardrails triggered."

    if final_cls == Classification.CLARIFY:
        fields = ", ".join(missing_context)
        return f"Missing required context: {fields}."

    if final_cls == Classification.BLOCK:
        if any(m.rule_id == "prohibited.out_of_scope"
               for m in confirmed_matches
               if effective[m.rule_id] == Classification.BLOCK):
            return "Request is outside the financial services domain."

    for m in confirmed_matches:
        if effective[m.rule_id] == final_cls:
            return m.description

    return "Classification determined by rule evaluation."


def _build_next_action(
    final_cls: Classification,
    confirmed_matches: list[RuleMatch],
    effective: dict[str, Classification],
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

    if any(m.rule_id == "prohibited.out_of_scope"
           for m in confirmed_matches
           if effective[m.rule_id] == Classification.BLOCK):
        return (
            "This system is designed for financial services questions. "
            "I can help with investment, account, and financial planning "
            "topics instead."
        )

    return "Request blocked. Inform user with explanation."


# ── Main Entry Point ─────────────────────────────────────────────


def classify(query: str, apply_mechanisms: bool = True) -> GuardrailResult:
    """Classify a query against all guardrail rules.

    Args:
        query: The user's input text.
        apply_mechanisms: When True (default), applies produce-intent
            upgrade and context-first override. When False, returns the
            literal priority-routing outcome with no mechanism modifications.
            Used by Compare Mode in the Streamlit UI to demonstrate the
            architectural effect of mechanisms (ADR-003, ADR-004). All
            existing acceptance tests use the default (True) and behave
            identically to the pre-Compare-Mode implementation.

    Returns:
        A GuardrailResult with classification, category, triggered_rules,
        missing_context, decision_reason, next_action, driver_rule_id,
        and mechanisms_applied populated.
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
            confirmed_matches.append(match)

    # Step 3: Compute effective classifications (produce-intent upgrade)
    # No mutation — effective is a separate dict.
    produce_intent_detected = detect_produce_intent(query) and apply_mechanisms
    effective = _compute_effective_classifications(
        confirmed_matches, produce_intent_detected
    )

    # Step 4: Apply context-first override (or skip when mechanisms disabled)
    if apply_mechanisms:
        priority_input, suppressed_ids = _apply_context_first_override(
            confirmed_matches, effective
        )
    else:
        # No override: every confirmed rule goes to priority resolution.
        priority_input = [
            (
                effective[m.rule_id],
                m.category,
                TriggeredRule(
                    rule_id=m.rule_id,
                    description=m.description,
                    category=m.category,
                    original_classification=m.classification,
                    effective_classification=effective[m.rule_id],
                ),
            )
            for m in confirmed_matches
        ]
        suppressed_ids = set()

    # Step 5: Resolve priority — now also returns the driver rule
    final_cls, final_cat, driver_rule = resolve_priority(priority_input)

    # Step 6: Build the full triggered_rules audit list.
    # Includes suppressed rules with the suppression flag set.
    # Includes upgrade flags for rules whose effective != original.
    triggered_rules = []
    for m in confirmed_matches:
        eff_cls = effective[m.rule_id]
        was_upgraded = (
            apply_mechanisms
            and m.produce_intent_upgrade is not None
            and produce_intent_detected
        )
        triggered_rules.append(TriggeredRule(
            rule_id=m.rule_id,
            description=m.description,
            category=m.category,
            original_classification=m.classification,
            effective_classification=eff_cls,
            suppressed_by_override=(m.rule_id in suppressed_ids),
            upgraded_by_produce_intent=was_upgraded,
        ))

    # Step 7: Determine which mechanisms actually fired (and affected outcome).
    mechanisms_applied: list[str] = []
    if apply_mechanisms:
        if any(r.upgraded_by_produce_intent for r in triggered_rules):
            mechanisms_applied.append("produce_intent_upgrade")
        if suppressed_ids:
            mechanisms_applied.append("context_first_override")

    # Step 8: Collect missing_context from suitability CLARIFY rules
    missing_context: list[str] = []
    if final_cls == Classification.CLARIFY:
        for m in confirmed_matches:
            if (m.category == Category.SUITABILITY
                    and effective[m.rule_id] == Classification.CLARIFY):
                for ctx in m.missing_context:
                    if ctx not in missing_context:
                        missing_context.append(ctx)

    # Step 9: Build human-readable fields
    decision_reason = _build_decision_reason(
        final_cls, confirmed_matches, effective, missing_context,
    )
    next_action = _build_next_action(
        final_cls, confirmed_matches, effective, missing_context,
    )

    # Step 10: Construct result
    return GuardrailResult(
        classification=final_cls,
        category=final_cat,
        decision_reason=decision_reason,
        next_action=next_action,
        triggered_rules=triggered_rules,
        missing_context=missing_context,
        driver_rule_id=driver_rule.rule_id if driver_rule else None,
        mechanisms_applied=mechanisms_applied,
    )