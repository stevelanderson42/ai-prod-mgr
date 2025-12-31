# ADR-001: Deterministic Routing Logic

**Status:** Accepted  
**Date:** December 2024  
**Module:** Requirements Guardrails (Module 3)

---

## Context

The Requirements Guardrails module must decide how to route incoming requests to one of four outcomes: PROCEED, CLARIFY, ESCALATE, or BLOCK. This routing decision is the core function of the module.

The fundamental question: **Should the routing decision be made by deterministic rules or by a machine learning model?**

This is not a trivial choice. The routing layer sits at a critical control point—between user input and model invocation. The design of this layer has significant implications for auditability, explainability, and regulatory compliance.

---

## Decision

**Use deterministic, rule-based logic for all routing decisions.**

No machine learning model, classifier, or LLM is invoked to make the routing decision itself. The routing logic consists of explicit, auditable rules that can be reviewed, validated, and approved by compliance teams.

---

## Rationale

### 1. Regulatory Explainability Requirements

Regulated industries require decisions to be explainable and auditable. SR 11-7 (Model Risk Management) mandates documentation of model behavior and decision rationale.

**Problem with ML routing:** When a classifier decides to block or escalate a request, the reasoning is opaque. "The model predicted 0.73 confidence for escalation" is not an acceptable explanation in a compliance review.

**Deterministic advantage:** Every routing decision can be traced to specific rules:
- "Blocked because: request contained guarantee language (Rule C-204)"
- "Escalated because: suitability context missing AND account flagged high-risk (Rules S-102, S-105)"

This is auditable. This is defensible.

### 2. No Recursive Model Risk

Using a model to decide whether to invoke a model creates recursive risk:
- What if the routing model hallucinates?
- What if the routing model is adversarially manipulated?
- What if the routing model drifts over time?

**Deterministic advantage:** The routing layer is a fixed control surface. It doesn't learn, drift, or hallucinate. It applies the same rules every time, which means:
- Behavior is predictable
- Testing is straightforward
- Validation is complete

> **PM DECISION:** The routing layer must be the most stable part of the system. Introducing ML here would undermine the entire governance architecture.

### 3. Compliance Team Reviewability

Rules can be reviewed and approved by non-technical stakeholders. Compliance officers, legal teams, and risk managers can:
- Read the rules
- Understand the logic
- Approve changes
- Audit decisions

**Problem with ML routing:** Compliance teams cannot meaningfully review a neural network. They can review accuracy metrics, but not the decision logic itself.

**Deterministic advantage:** The rule set becomes a reviewable artifact—similar to a policy document, but executable.

### 4. No Training Data Requirements

ML classifiers require labeled training data:
- "This request should be blocked"
- "This request should proceed"
- "This request needs clarification"

In regulated environments, acquiring and labeling this data is problematic:
- Historical data may contain compliance violations
- Labels require expert judgment
- Edge cases are underrepresented
- Data may be biased toward past (potentially flawed) decisions

**Deterministic advantage:** Rules are authored from first principles—based on regulatory requirements, not historical patterns.

### 5. No Model Drift at the Control Layer

ML models drift over time as:
- Input distributions change
- Underlying patterns shift
- Model behavior degrades

If the routing model drifts, the entire governance layer becomes unreliable.

**Deterministic advantage:** Rules don't drift. Rule C-204 blocks guarantee language today, tomorrow, and next year—unless explicitly changed through a governed change process.

### 6. Debugging and Incident Response

When something goes wrong:
- **ML routing:** "Why did this get blocked?" → Requires model interpretability tools, feature importance analysis, potentially inconclusive
- **Deterministic routing:** "Why did this get blocked?" → Rule C-204 triggered on token "guaranteed returns" at position 47

Incident response in regulated environments must be fast and precise. Deterministic routing enables this.

### 7. Performance and Latency

Deterministic rules execute in microseconds. ML inference adds latency:
- Model loading
- Feature extraction
- Inference computation
- Result interpretation

For a pre-invocation control layer that runs on every request, latency matters.

---

## Alternatives Considered

### Alternative A: ML Classifier for Routing

**Description:** Train a classifier (e.g., fine-tuned BERT, logistic regression on embeddings) to predict routing outcomes.

**Rejected because:**
- Opaque decision logic
- Requires labeled training data
- Subject to drift
- Cannot be reviewed by compliance teams
- Introduces model risk at the control layer

### Alternative B: LLM-Based Classification

**Description:** Use an LLM (e.g., GPT-4, Claude) to classify requests and determine routing.

**Rejected because:**
- Recursive risk (using a model to decide about model invocation)
- High latency for every request
- Non-deterministic outputs (same input may route differently)
- Expensive at scale
- Hallucination risk at the control layer

### Alternative C: Hybrid Approach (Rules + ML Fallback)

**Description:** Use deterministic rules for clear cases; fall back to ML for ambiguous cases.

**Considered but deferred because:**
- Adds complexity
- "Ambiguous" cases are exactly where explainability matters most
- Creates two systems to maintain and audit
- May be revisited in future if rule coverage proves insufficient

> **PM DECISION:** Start with pure deterministic routing. The hybrid approach remains an option if we encounter systematic gaps that rules cannot address—but that decision should be data-driven, not assumed.

---

## Consequences

### Positive

- **Full auditability:** Every decision traceable to specific rules
- **Compliance reviewable:** Non-technical stakeholders can validate logic
- **No drift:** Behavior is stable over time
- **Fast execution:** Microsecond latency
- **Simple testing:** Complete validation possible
- **Clear incident response:** Root cause identification is straightforward

### Negative

- **Rule maintenance burden:** Rules must be authored and maintained manually
- **Coverage gaps possible:** Novel inputs may not match existing rules
- **Less adaptive:** Cannot learn from new patterns automatically
- **Requires domain expertise:** Rule authors must understand regulatory requirements

### Mitigations for Negative Consequences

| Risk | Mitigation |
|------|------------|
| Rule maintenance burden | Structured rule format; version control; change review process |
| Coverage gaps | Default to ESCALATE for unmatched cases; monitor escalation patterns |
| Less adaptive | Quarterly rule review based on escalation analysis |
| Requires domain expertise | Involve compliance SMEs in rule authoring |

---

## Implementation Notes

### Rule Structure

Each rule should include:
- **Rule ID:** Unique identifier (e.g., C-204)
- **Category:** Which guardrail category it belongs to
- **Condition:** What triggers the rule
- **Action:** PROCEED / CLARIFY / ESCALATE / BLOCK
- **Rationale:** Why this rule exists
- **Regulatory reference:** If applicable (e.g., FINRA 2210)

### Rule Precedence

When multiple rules match:
1. BLOCK takes precedence over all others
2. ESCALATE takes precedence over CLARIFY and PROCEED
3. CLARIFY takes precedence over PROCEED
4. If no rules match → Default to ESCALATE (fail-safe)

### Change Management

Rule changes require:
- Documentation of change rationale
- Review by compliance stakeholder
- Testing against sample inputs
- Version control commit with clear message

---

## References

- SR 11-7: Guidance on Model Risk Management
- FINRA Rule 2210: Communications with the Public
- Module 3 README: Requirements Guardrails
- Context Diagram: Module 3 Internal Flow

---

## Decision Record

| Role | Name | Date |
|------|------|------|
| Author | Steve | December 2024 |
| Reviewer | — | — |
| Approver | — | — |