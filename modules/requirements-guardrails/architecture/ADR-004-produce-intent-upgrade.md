# ADR-004: Produce-Intent Upgrade Mechanism

**Status:** Accepted
**Date:** May 2026
**Deciders:** Steve (AI PM)
**Module:** Requirements Guardrails

---

## Context

Two compliance trigger patterns appeared in source documents with apparently inconsistent routing:

The compliance-triggers.md document specifies that performance guarantee language (e.g., "guaranteed returns") routes to ESCALATE for compliance review. The sample-classifications.md document, however, specifies that a query asking the system to *generate* a message containing guarantee language (Sample 3: "Write me a message to send to my client saying this fund is guaranteed to outperform the market") routes to BLOCK.

The same divergence appears in Sample 8 (unbalanced claims), where a query asking the system to draft a one-sided marketing message routes to BLOCK rather than the default ESCALATE for unbalanced claim language.

On inspection, this is not a documentation inconsistency. It reflects a real architectural distinction:

| Case | User Intent | Correct Routing | Reasoning |
|------|-------------|-----------------|-----------|
| Query **contains** prohibited language | User has encountered, witnessed, or is asking about the language | ESCALATE | Compliance review can determine whether the underlying communication is acceptable in its original context |
| Query asks system to **produce** prohibited language | User wants the system itself to generate the violating content | BLOCK | The system becoming a source of a FINRA 2210 violation is unambiguously prohibited regardless of downstream interpretation |

The classifier must distinguish between these two cases for compliance rules where the produce-vs-contain distinction is material.

---

## Decision

### 1. Per-Rule Upgrade Eligibility

Specific compliance rules are marked in YAML configuration with a `produce_intent_upgrade: BLOCK` field. When the classifier detects that a query asks the system to produce content (via the `detect_produce_intent()` heuristic), it upgrades any triggered rule with this field from its default classification (ESCALATE) to the upgrade target (BLOCK).

Eligibility is decided per-rule:

| Rule | Default | Upgrade-Eligible | Reasoning |
|------|---------|------------------|-----------|
| `compliance.guarantee_language` | ESCALATE | Yes → BLOCK | System should not produce guarantee language |
| `compliance.predictions_projections` | ESCALATE | Yes → BLOCK | System should not produce factual-tone predictions |
| `compliance.unbalanced_claims` | ESCALATE | Yes → BLOCK | System should not produce one-sided marketing |
| `compliance.investment_advice` | ESCALATE | No | Boundary requires human review whether or not user requests generation |
| `compliance.tax_advice` | ESCALATE | No | Same logic as investment_advice |
| `compliance.legal_advice` | ESCALATE | No | Same logic as investment_advice |
| `compliance.suspicious_activity` | ESCALATE | No | Pattern detection requires review regardless of intent framing |
| `compliance.market_manipulation` | BLOCK | N/A | Already BLOCK by default — produce-intent does not change behavior |

### 2. Produce-Intent Detection

The produce-intent detection is performed by a deterministic heuristic. The function uses substring matching against a fixed list of multi-word produce signals: `"write me "`, `"write a "`, `"write an "`, `"help me write"`, `"draft a "`, `"draft an "`, `"create a "`, `"generate a "`, `"compose a "`, and similar variants. Trailing spaces in signal patterns provide basic word-boundary behavior (e.g., `"write a "` does not match `"write about"`).

### 3. Upgrade Application

The upgrade is applied in the classifier orchestrator after heuristic resolution and before priority resolution. Triggered `RuleMatch` objects with a `produce_intent_upgrade` field have their `classification` field updated in place to the upgrade target.

---

## Rationale

### 1. Contains vs. Produces Is an Architectural Distinction

The system can refuse to be the *source* of a violation even when the system would not necessarily refuse to *discuss* the violation.

A user asking "Is it OK that my advisor said this is guaranteed?" is asking about an interaction with a third party. That interaction deserves compliance review. ESCALATE is correct. A user asking the system itself to produce the guarantee language receives an immediate refusal — there is no legitimate downstream interpretation that makes the request acceptable. BLOCK is correct.

### 2. Policy as Data

The mechanism is implemented as a YAML field rather than hardcoded in the classifier for three reasons:

1. It documents which rules are upgrade-eligible in configuration that auditors and compliance reviewers can read without inspecting Python
2. New compliance rules can specify their upgrade behavior at definition time without requiring classifier code changes
3. The "policy as data" principle established for Module 4 is preserved here

### 3. Highest-Risk Heuristic

The `detect_produce_intent()` function is the highest-risk heuristic in the Module 3 v1 build. False positives would incorrectly elevate ESCALATE cases to BLOCK; false negatives would fail to catch genuine produce-intent requests. Test coverage explicitly verifies both directions:

| Test | Query | Expected Behavior |
|------|-------|-------------------|
| `test_sample_03` | "Write me a message...guaranteed to outperform..." | Produce-intent detected → upgrade to BLOCK |
| `test_sample_08` | "Help me write an email...high returns..." | Produce-intent detected → upgrade to BLOCK |
| `test_contains_guarantee_not_produce` | "My advisor said this is guaranteed, should I be worried?" | Produce-intent NOT detected → stays ESCALATE |

The third test is the critical false-positive-avoidance check. Without it, the upgrade mechanism could silently over-classify and the failure would not surface.

> **PM DECISION:** The produce-intent distinction could have been captured by adding new compliance rules (e.g., `compliance.guarantee_language_produce` as a separate BLOCK rule alongside `compliance.guarantee_language` at ESCALATE). The upgrade mechanism was chosen instead because it keeps the rule set smaller, makes the conditional relationship explicit in YAML, and avoids duplication of pattern definitions. The upgrade is one architectural mechanism that handles three rules; rule duplication would have produced six rules with overlapping definitions.

---

## Alternatives Considered

### Alternative A: Hardcode the Upgrade Behavior in the Classifier

A switch statement that lists the three eligible rules and applies BLOCK when produce-intent is detected.

**Rejected because:** This puts policy in code. Adding or removing eligible rules would require code changes rather than YAML edits. Auditors would need to read Python to understand upgrade behavior, breaking the policy-as-data principle.

### Alternative B: Make All Compliance Rules Eligible for Upgrade by Default

Simpler logic — no per-rule field needed.

**Rejected because:** Several compliance rules (`investment_advice`, `tax_advice`, `legal_advice`) require human review whether or not the user asks the system to produce content. Blanket upgrade would incorrectly route legitimate compliance review cases to BLOCK.

### Alternative C: Detect Produce-Intent via a Narrow Validated LLM Classifier

Use a single-purpose model instead of deterministic substring matching.

**Rejected because:** The v1 architectural commitment is to deterministic rules with no LLM in the classifier path (per ADR-001). A narrow validated classifier for produce-intent is a reasonable v2 enhancement once the deterministic version is in production and edge cases have been catalogued.

### Alternative D: Create Separate Compliance Rules for Each Produce-Intent Case

E.g., `compliance.guarantee_language_produce` alongside `compliance.guarantee_language`.

**Rejected because:** This doubles the rule count for the affected categories. The conditional relationship — "this rule routes to BLOCK when intent is to produce, otherwise ESCALATE" — is more clearly expressed as one rule with an upgrade field than as two separate rules with overlapping definitions.

---

## Consequences

### Positive

- **Correct routing:** The classifier correctly distinguishes "contains" from "produces" cases, matching the routing intended in the sample classifications
- **Auditable via YAML:** Any rule's upgrade behavior is visible in the config file without reading Python
- **Generalizable:** Future compliance rules can opt into upgrade behavior by adding the `produce_intent_upgrade` field
- **Documented across layers:** The mechanism is documented in code, in YAML descriptions, in tests, and in this ADR

### Negative

- **Fixed signal list:** The `detect_produce_intent()` heuristic relies on substring matching. Edge cases — particularly indirect produce requests like "Could you possibly help me with writing..." or "I need you to put together..." — may not be detected. These represent false negatives that would route to ESCALATE instead of BLOCK
- **In-place mutation:** The upgrade introduces a mutation step in the classifier orchestrator: triggered `RuleMatch` objects have their `classification` field updated in place before priority resolution. This is documented in the orchestrator code as a v2 cleanup opportunity (compute `effective_classification` rather than mutating)
- **Binary upgrade only:** The mechanism is binary (upgrade to BLOCK or no upgrade). It does not support nuanced upgrades (e.g., from one ESCALATE category to a different ESCALATE category). v2 could generalize if such nuance becomes necessary

---

## Implementation Notes

### Code Location

The produce-intent detection lives in `detect_produce_intent()` in `src/rules/heuristics.py`. The signal list `_PRODUCE_SIGNALS` is module-level and immutable. The upgrade application happens in step 3 of the `classify()` function in `src/classifier.py`, where the orchestrator iterates over `confirmed_matches` and applies the upgrade to any `RuleMatch` with a `produce_intent_upgrade` field set.

### YAML Configuration

The three eligible rules in `src/config/compliance.yaml` carry the field:

```yaml
- id: compliance.guarantee_language
  classification: ESCALATE
  produce_intent_upgrade: BLOCK
  ...
```

Rules without this field are not upgrade-eligible regardless of produce-intent detection.

### Test Coverage

The acceptance test suite includes:

- **`test_sample_03_guarantee_language_produce`:** Verifies Sample 3 triggers upgrade to BLOCK
- **`test_sample_08_unbalanced_claims_produce`:** Verifies Sample 8 triggers upgrade to BLOCK
- **`test_contains_guarantee_not_produce`:** Verifies "My advisor said this is guaranteed, should I be worried?" does NOT trigger upgrade and remains ESCALATE

The third test is the critical false-positive-avoidance check.

### Monitoring Recommendation

If this module evolves toward production, track two metrics:

| Metric | Purpose |
|--------|---------|
| Produce-intent upgrade rate | Percentage of compliance rule triggers that get upgraded — establishes baseline |
| Reported false positives | Queries upgraded to BLOCK when ESCALATE would have been correct — signals list refinement needed |

A high upgrade rate combined with high false-positive reports would indicate the signal list needs refinement.

---

## Related Documents

- [ADR-001: Deterministic Routing Logic](./ADR-001-routing-logic.md) — Establishes the rules-only commitment that justifies deterministic upgrade logic
- [ADR-002: Escalation Design](./ADR-002-escalation-design.md) — Defines the ESCALATE behavior that the upgrade modifies
- [src/rules/heuristics.py](../src/rules/heuristics.py) — Implementation of `detect_produce_intent()`
- [src/classifier.py](../src/classifier.py) — Orchestrator that applies the upgrade
- [src/config/compliance.yaml](../src/config/compliance.yaml) — YAML rules with `produce_intent_upgrade` fields
- [tests/test_acceptance.py](../tests/test_acceptance.py) — Sample 3, Sample 8, and false-positive test
- [Sample Classifications](../evidence/sample-classifications.md) — Samples #3 and #8 define expected behavior

---

## Decision Record

| Role | Name | Date |
|------|------|------|
| Author | Steve | May 2026 |
| Reviewer | — | — |
| Approver | — | — |
