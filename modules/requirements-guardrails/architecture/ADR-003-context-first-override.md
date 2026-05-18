# ADR-003: Context-First Override for Suitability CLARIFY Routing

**Status:** Accepted
**Date:** May 2026
**Deciders:** Steve (AI PM)
**Module:** Requirements Guardrails

---

## Context

The Requirements Guardrails classifier applies priority routing across multiple guardrail categories. The locked priority ordering established in ADR-001 is BLOCK > ESCALATE > CLARIFY > PROCEED, with category tiebreaking (prohibited > compliance > suitability) when multiple rules fire at the same classification level.

During implementation of the v1 classifier, two acceptance test cases surfaced a conflict between the literal priority ordering and the expected routing outcome:

| Sample | Query | Compliance Rule (ESCALATE) | Suitability Rule (CLARIFY) | Standard Priority Result | Expected Result |
|--------|-------|---------------------------|---------------------------|--------------------------|-----------------|
| #2 | "What should I invest in right now?" | `compliance.investment_advice` | `suitability.missing_risk_tolerance`, `suitability.missing_time_horizon` | ESCALATE | CLARIFY |
| #10 | "What are the tax implications if I convert my traditional IRA to a Roth?" | `compliance.tax_advice` | `suitability.missing_jurisdiction` | ESCALATE | CLARIFY |

The sample classifications document specifies CLARIFY for both cases. This is not a documentation bug. The conflict is genuine: a query may legitimately raise compliance concerns while also lacking the user context required to evaluate those concerns properly.

---

## Decision

**The classifier applies a context-first override before priority resolution.** When suitability rules at CLARIFY are present in the triggered rule set, compliance rules at ESCALATE are excluded from priority resolution. The excluded compliance rules remain in the `triggered_rules` array for audit completeness. The override affects only which rule drives the user-facing routing decision, not which rules are recorded.

### Constraints on the Override

| Constraint | Detail |
|------------|--------|
| BLOCK rules never suppressed | A BLOCK from any category always wins, regardless of suitability gaps |
| Only compliance ESCALATE suppressed | Compliance BLOCK rules (produce-intent upgrades, market manipulation) are unaffected |
| Implementation boundary | Override lives in the classifier orchestrator, not in the priority resolution function, preserving `resolve_priority` as a clean mechanical function |
| Audit completeness | Suppressed rules appear in `triggered_rules` — only their influence on the user-facing routing decision is removed |

---

## Rationale

### 1. Escalation Without Context Wastes Reviewer Time

Escalating to a human reviewer without the context required to evaluate the request produces a predictable outcome: the reviewer's first action is to request the same missing context that CLARIFY directly asks the user to provide. The user-facing flow that respects this logic:

1. User submits incomplete query
2. System asks for missing context (CLARIFY)
3. User provides context
4. System re-evaluates the now-complete query
5. If compliance concerns persist after context is provided, the second-pass evaluation can still escalate

### 2. Severity vs. Sequencing

The standard priority ordering (BLOCK > ESCALATE > CLARIFY > PROCEED) describes **severity**. The override captures a different dimension: **sequencing**. CLARIFY is an earlier step in the request lifecycle than ESCALATE, even though it has lower severity in the standard ordering. You must know what the user is asking before you can determine whether it needs human review.

### 3. Audit Completeness Is Preserved

A regulator or auditor reviewing a classification decision can see that the compliance rule fired even though it was not the driver of the user-facing routing. The `triggered_rules` array carries the complete picture; the `classification` field reflects the actionable routing.

> **PM DECISION:** This override is not in the original ADR-001 priority routing spec. It emerged during implementation when the conflict surfaced. The decision to add it — rather than accept literal priority routing — reflects a product judgment that user experience and operational efficiency outweigh literal architectural elegance in this specific case. The override is bounded, documented, and testable. If it causes problems, it can be removed without structural changes.

---

## Alternatives Considered

### Alternative A: Accept ESCALATE as the Routing Outcome

Update test expectations to match standard priority routing. Argue that compliance concerns always take precedence over suitability gaps.

**Rejected because:** This produces a worse user experience. Escalating without context wastes reviewer time and creates a round-trip the user did not expect. The compliance reviewer would just ask for the same missing context.

### Alternative B: Refine Compliance Rules to Not Fire on These Queries

Make `compliance.investment_advice` more selective so it doesn't fire on vague recommendation queries.

**Rejected because:** The compliance rules are correctly designed. A vague recommendation request IS a compliance concern. Tightening the rule to exclude these queries would weaken its ability to catch real compliance issues when full context is present.

### Alternative C: Encode the Override as a YAML-Level Concept

Add a `suppression_rules` section to the YAML configs, allowing rules to declare which other rules they can suppress.

**Rejected because:** This is a single, well-bounded override. Adding a generalized suppression framework to YAML would be over-engineering for a single use case. If additional suppression patterns emerge in v2, the framework can be generalized then.

---

## Consequences

### Positive

- **Better user experience:** Users with incomplete queries are asked for context rather than routed to compliance reviewers
- **Reviewer time preserved:** Compliance reviewers handle cases where context is actually present and a real compliance judgment is needed
- **Audit completeness maintained:** Suppressed rules remain visible in `triggered_rules`
- **Product logic documented:** The override is documented in code (`classifier.py`), in this ADR, and noted for the Module 3 README update

### Negative

- **Reduced predictability:** A reader of the priority routing rules in ADR-001 would not anticipate the override without reading this ADR
- **Adversarial preemption risk:** A user could construct queries that trigger both compliance and suitability rules to delay compliance escalation. Mitigation: the user must still provide context in the follow-up, and the second-pass evaluation will apply compliance rules with full context
- **Additional complexity:** One additional code path beyond the literal priority routing spec

---

## Implementation Notes

### Code Location

The override logic lives in `_apply_context_first_override()` in `src/classifier.py`. The function is called before `resolve_priority()` in the orchestration sequence (step 5 of the `classify()` function).

### Test Coverage

The acceptance test suite explicitly verifies both dimensions:
- **Routing outcome:** `test_sample_02` and `test_sample_10` assert `Classification.CLARIFY`
- **Audit completeness:** Both tests assert that the suppressed compliance rule (`compliance.investment_advice`, `compliance.tax_advice`) appears in `triggered_rules`

### Monitoring Recommendation

If this module evolves toward production, track the rate at which compliance ESCALATE rules are suppressed by the override. A high suppression rate could indicate that compliance rules are firing too aggressively on incomplete queries and may warrant rule refinement rather than systematic suppression.

---

## Related Documents

- [ADR-001: Deterministic Routing Logic](./ADR-001-routing-logic.md) — Establishes the literal priority routing that this ADR amends
- [ADR-002: Escalation Design](./ADR-002-escalation-design.md) — Defines the ESCALATE behavior that this override modifies
- [src/classifier.py](../src/classifier.py) — Implementation of the override
- [tests/test_acceptance.py](../tests/test_acceptance.py) — `test_sample_02` and `test_sample_10` verify the override
- [Sample Classifications](../evidence/sample-classifications.md) — Samples #2 and #10 define the expected behavior

---

## Decision Record

| Role | Name | Date |
|------|------|------|
| Author | Steve | May 2026 |
| Reviewer | — | — |
| Approver | — | — |
