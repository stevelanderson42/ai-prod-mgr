# ADR-005: v1 Scope and Deferred Categories

**Status:** Accepted
**Date:** May 2026
**Deciders:** Steve (AI PM)
**Module:** Requirements Guardrails

---

## Context

The Module 3 design specifies five guardrail categories: ambiguity detection, compliance triggers, suitability gaps, prohibited content, and human review triggers. Within prohibited content, the source design document prohibited-content.md specifies five sub-categories: illegal activity, harm to self or others, system exploitation, out-of-scope content, and abusive content.

A complete implementation would build all five guardrail categories and all five prohibited content sub-categories. The Module 3 v1 build, however, was scoped during Session 1 to a deliberate subset of these.

Some categories were excluded because their detection requires capabilities that exceed v1's deterministic-rules commitment (per ADR-001). Other categories were excluded because their detection without supporting response infrastructure would be a category error — the detection itself is the easy part; responsible handling of the detected case is the work that exceeds portfolio scope.

The scoping decisions are themselves architectural commitments. Future maintainers (and hiring managers reviewing the portfolio) need to understand both what is in v1 and why the excluded categories were excluded. Conflating "we didn't build this" with "we don't think this matters" would undersell the senior PM thinking that went into the decision.

---

## Decision

### 1. v1 Implementation Scope

The Module 3 v1 build implements three of five guardrail categories and three of five prohibited content sub-categories.

| Category | v1 Status | Rationale |
|----------|-----------|-----------|
| Compliance Triggers | Implemented | Deterministic rules effective for FINRA 2210, FINRA 2111, Reg BI patterns |
| Suitability & User Context Gaps | Implemented | Deterministic rules effective for Reg BI suitability context detection |
| Prohibited Content — Category 1 (Illegal Activity) | Implemented | Pattern detection sufficient; refusal response is unambiguous |
| Prohibited Content — Category 3 (System Exploitation) | Implemented | Pattern detection sufficient; refusal response is unambiguous |
| Prohibited Content — Category 4 (Out-of-Scope) | Implemented | Soft-redirect response well-defined; pattern detection via financial-domain absence |

### 2. Deferred Scope

| Category | Deferral Reason | Rationale |
|----------|-----------------|-----------|
| Ambiguity Detection | Engineering complexity | Subjective evaluation beyond deterministic rules; requires narrow validated classifiers |
| Human Review Triggers | Engineering complexity | Multi-domain reasoning beyond what rules express reliably |
| Prohibited Content — Category 2 (Harm to Self/Others) | Duty of care | Detection requires crisis response infrastructure that exceeds portfolio scope |
| Prohibited Content — Category 5 (Abusive Content) | Duty of care | Detection requires moderation policy and warning UX that exceeds portfolio scope |

### 3. Two Distinct Deferral Reasoning Paths

The deferrals are categorized into two distinct reasoning paths:

- **Engineering complexity** — where deterministic rules are insufficient for the task
- **Duty of care** — where detection without supporting infrastructure would be irresponsible

These are different arguments. Engineering complexity says "we can't build this well yet." Duty of care says "we should not build this without the supporting commitments."

---

## Rationale

### 1. Ambiguity Detection and Human Review Triggers (Engineering Complexity)

Both categories require subjective evaluation beyond what deterministic keyword and regex rules can reliably express.

**Ambiguity detection requires:**

- Resolving missing referents ("Is that a good idea?" — what is "that"?)
- Evaluating intent specificity ("Tell me about retirement" — what aspect?)
- Detecting pronouns without antecedents in absence of conversation history
- Distinguishing genuine ambiguity from acceptable shorthand

**Human review triggers require:**

- Multi-domain reasoning (compliance + suitability + account context simultaneously)
- Precedent-based escalation ("this account has been flagged recently AND this query touches a sensitive topic")
- Account-state-aware logic that depends on metadata not available to the v1 classifier

These categories are best implemented with narrow validated classifier components, which the v1 architectural commitment explicitly defers (per ADR-001). Building them with pure deterministic rules would either produce so many false positives that the classifier becomes user-hostile, or produce so many false negatives that the categories add no real safety value.

**The scope decision:** Implement the three categories where deterministic rules are genuinely effective. Document the other two with clear v2 rationale rather than ship them shallowly. False negatives in a portfolio classifier are tolerable for a demo. False positives that route legitimate queries to BLOCK or ESCALATE would be user-hostile and would weaken the credibility of the categories that do work.

### 2. Prohibited Content Categories 2 and 5 (Duty of Care)

These two categories are not deferred because they are harder to detect. They are deferred because detection without supporting infrastructure would be irresponsible.

**Category 2 (harm to self or others) requires more than pattern detection:**

- Validated crisis resources appropriate to the user's jurisdiction (988 Suicide and Crisis Lifeline in US; different resources internationally)
- Escalation paths to human-staffed crisis response, not just block-with-resource-link
- False-positive harm analysis — a false flag in this category has different consequences than a false flag in any other category
- Training data review for harm to users in distress; pattern lists must be tested against real crisis communication
- Ongoing monitoring of system behavior in real cases, including edge cases involving sarcasm, hypothetical framing, and culturally-specific expressions of distress

**Category 5 (abusive content) similarly requires more than pattern detection:**

- A moderation policy that defines what constitutes abuse in the financial services context
- User warning UX that escalates appropriately on repeated abuse rather than blocking on first instance
- Account-level flags for pattern detection across sessions
- Appeal mechanisms for false positives
- Cultural context awareness for terms that are abusive in some contexts and not others

A portfolio demo classifier cannot responsibly implement crisis detection or abuse moderation. The detection patterns are documented in prohibited-content.md for design reference. The implementation is deferred until the supporting infrastructure exists.

> **PM DECISION:** This is the most important reasoning in this ADR. Building detection without the response infrastructure would produce a system that appears to be handling crisis cases responsibly when it is not. A user in crisis whose message is intercepted by a "I can't help with that" response is potentially worse off than a user whose message proceeds normally. The duty-of-care argument is not "we couldn't build this in time" — it is "we should not build this without the supporting commitments." Recognizing the distinction is itself a senior PM signal.

### 3. Why the Implemented Categories Are Sufficient for v1

The implemented categories cover the substantive architectural patterns Module 3 is designed to demonstrate:

- Pre-invocation risk control with deterministic routing (per ADR-001)
- The PROCEED/CLARIFY/ESCALATE/BLOCK routing taxonomy (per ADR-002)
- The context-first override pattern (per ADR-003)
- The produce-intent upgrade mechanism (per ADR-004)
- Multi-category triggering with audit-completeness preservation

A reviewer of Module 3 can evaluate the architectural thinking from the implemented categories. The deferred categories would add detection breadth without changing what the architecture demonstrates.

---

## Alternatives Considered

### Alternative A: Implement All Five Guardrail Categories in v1

Build deterministic detection for ambiguity and human review triggers using whatever rules can be expressed.

**Rejected because:** The detection quality would be poor. Deterministic rules cannot reliably capture ambiguity or multi-domain triage. Shipping shallow detection in these categories would weaken the classifier's overall credibility. A reviewer testing the demo with an ambiguous query would receive a false-positive CLARIFY routing in cases where PROCEED was correct, or a false-negative PROCEED in cases where CLARIFY was correct. Either failure mode is worse than not shipping the category and documenting why.

### Alternative B: Implement Self-Harm and Abuse Detection Without Crisis-Response Infrastructure

Detect the patterns and route to BLOCK with a generic refusal.

**Rejected because:** This is the category error described in the rationale. Shipping detection without response infrastructure creates the appearance that the system is handling these cases responsibly when it is not. It potentially harms users in distress by intercepting their messages without providing real help. The right action is to defer detection until response infrastructure exists.

### Alternative C: Implement All Five Prohibited Content Sub-Categories Using Only Documented Patterns

Keep the implementation shallow and let the documentation note the limitations.

**Rejected because:** Documentation noting limitations is not a substitute for not shipping the feature. Self-harm and abuse detection are exactly the kinds of features where shipping shallow implementations is worse than not shipping at all. A hiring manager reviewing the portfolio would not give credit for "I built crisis detection but documented that it's incomplete" — they would either give credit for the duty-of-care reasoning that led to the deferral, or they would question the judgment behind shipping incomplete crisis handling.

### Alternative D: Defer All of Module 3 Until All Five Categories Can Be Implemented

Wait for production-level completeness before shipping anything.

**Rejected because:** This conflates portfolio demonstration with production deployment. The portfolio's job is to demonstrate the architectural thinking. The implemented categories demonstrate that thinking sufficiently. Waiting for production-level completeness before shipping anything would mean Module 3 stays at "design only" status indefinitely, which weakens the portfolio narrative.

---

## Consequences

### Positive

- **Tight, well-tested scope:** v1 ships a working, well-tested classifier on a focused scope rather than a sprawling, partially-functional one
- **Implementation quality:** The categories that are implemented are implemented well, with full test coverage and clear documentation
- **Duty-of-care reasoning:** The rationale for deferred prohibited content categories demonstrates senior PM judgment about which features require supporting infrastructure before they can responsibly ship
- **Explicit scope documentation:** The scope decision is documented in this ADR, in the YAML config descriptions, and (when updated) in the Module 3 README
- **Clear decision record:** Future maintainers have an explicit record explaining why deferred categories exist as documentation rather than implementation

### Negative

- **Incomplete coverage:** The classifier does not catch all input patterns described in the original Module 3 design. Self-harm language, abusive content, ambiguity, and complex multi-domain queries will route through the implemented categories or default to PROCEED rather than receiving category-specific handling
- **Demo gap:** A reviewer testing the demo with one of these query types would observe behavior that does not match the design documents' coverage
- **Documentation requirement:** The Module 3 README and YAML config descriptions must make the v1 scope explicit to prevent misinterpretation
- **Real future work:** The deferred categories represent real work. If Module 3 evolves toward production, the deferred categories need to be revisited with their duty-of-care and complexity requirements treated as in-scope

---

## Implementation Notes

### Documentation of v1 Scope

The v1 scope is documented in three places:

| Location | Role |
|----------|------|
| This ADR | Authoritative source for scope rationale |
| Module 3 README | User-facing scope summary (to be updated as Task 7 in the broader Module 3 work plan) |
| YAML config file descriptions | `src/config/compliance.yaml`, `suitability.yaml`, and `prohibited.yaml` (already in place from Session 1) |

### Test Coverage Reflects v1 Scope

The acceptance test suite in `tests/test_acceptance.py` uses 9 of 14 samples from `evidence/sample-classifications.md`. The 5 excluded samples (#4, #7, #11, #13, #14) depend on deferred categories (ambiguity, human review triggers). The Module 3 README should note this test coverage scope alongside the category scope.

### Restoration Path for Deferred Categories

If Module 3 evolves toward production or extends to v2, the deferred categories have clear restoration paths:

| Category | Prerequisites | Design Source |
|----------|---------------|---------------|
| Ambiguity Detection | Narrow validated classifier per ADR-001 Alternative C | `rules/ambiguity-heuristics.md` |
| Human Review Triggers | Module 4 (Compliance Retrieval Assistant) providing upstream context about account state and recent activity | Sample Classifications #7, #11, #14 |
| Prohibited Content — Category 2 (Harm to Self/Others) | Validated crisis resource registry, human-staffed escalation, false-positive monitoring, training data review | `rules/prohibited-content.md` |
| Prohibited Content — Category 5 (Abusive Content) | Written abuse policy, escalation thresholds, appeal mechanism, warning UX | `rules/prohibited-content.md` |

Each restoration path has prerequisites beyond just writing more code. The prerequisites are the actual work; the code is downstream of them.

---

## Related Documents

- [ADR-001: Deterministic Routing Logic](./ADR-001-routing-logic.md) — Establishes the rules-only commitment that justifies the engineering-complexity deferrals
- [ADR-002: Escalation Design](./ADR-002-escalation-design.md) — Defines the ESCALATE behavior referenced in the implemented categories
- [ADR-003: Context-First Override](./ADR-003-context-first-override.md) — Refines routing behavior across implemented categories
- [ADR-004: Produce-Intent Upgrade Mechanism](./ADR-004-produce-intent-upgrade.md) — Refines compliance trigger behavior within implemented categories
- [Compliance Triggers](../rules/compliance-triggers.md) — Design document for implemented compliance category
- [Prohibited Content](../rules/prohibited-content.md) — Design document including deferred categories 2 and 5
- [Ambiguity Heuristics](../rules/ambiguity-heuristics.md) — Design document for deferred ambiguity category
- [Sample Classifications](../evidence/sample-classifications.md) — 9 samples (in v1 scope) and 5 samples (testing deferred categories)
- [src/config/compliance.yaml](../src/config/compliance.yaml), [suitability.yaml](../src/config/suitability.yaml), [prohibited.yaml](../src/config/prohibited.yaml) — v1 implementations matching ADR-005 scope

---

## Decision Record

| Role | Name | Date |
|------|------|------|
| Author | Steve | May 2026 |
| Reviewer | — | — |
| Approver | — | — |
