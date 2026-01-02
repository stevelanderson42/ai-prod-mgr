# ADR-002: Escalation Design

**Status:** Accepted  
**Date:** 2025-01-02  
**Deciders:** Steve (AI PM)  
**Module:** Requirements Guardrails

---

## Context

The Requirements Guardrails module routes requests to one of four outcomes: PROCEED, CLARIFY, ESCALATE, or BLOCK. This ADR documents the design decisions around ESCALATE — specifically:

1. When should a request escalate vs. block?
2. How should escalation priority be determined?
3. What information must accompany an escalation?
4. How should escalation targets be selected?

These decisions directly impact user experience, compliance risk, and operational cost.

---

## Decision

### 1. Escalate vs. Block Threshold

**Principle:** BLOCK is reserved for requests with no legitimate interpretation. ESCALATE handles everything else that can't safely PROCEED.

| Scenario | Routing | Rationale |
|----------|---------|-----------|
| Explicit illegal intent | BLOCK | No human review needed; answer is always no |
| Compliance language violation | ESCALATE | User may not understand rules; coaching opportunity |
| Suitability red flags | ESCALATE | Context may reveal legitimate path |
| Manipulation-adjacent language | ESCALATE | Ambiguous; requires human judgment |
| System exploitation attempt | BLOCK | No legitimate interpretation |
| Complex multi-factor request | ESCALATE | Requires specialist knowledge |

**Key distinction:** BLOCK says "this is impermissible." ESCALATE says "this requires human judgment."

### 2. Escalation Priority Levels

Three priority levels determine response time expectations:

| Priority | SLA Target | Triggers |
|----------|------------|----------|
| **HIGH** | < 4 hours | Legal threats, regulatory mentions, fraud indicators, vulnerable user signals |
| **MEDIUM** | < 24 hours | Compliance language violations, suitability concerns, complex requests |
| **LOW** | < 72 hours | Borderline cases, proactive support opportunities, edge cases |

**Priority elevation rules:**
- Multiple triggers in single request → elevate one level
- Flagged account + any trigger → elevate one level
- Vulnerable user indicators (elderly, distressed language) → automatic HIGH

### 3. Escalation Payload Contract

Every escalation must include:

```json
{
  "escalation_id": "string",
  "timestamp": "ISO-8601",
  "priority": "HIGH | MEDIUM | LOW",
  "routing_target": "string",
  "user_context": {
    "user_id": "string (hashed)",
    "session_id": "string",
    "account_flags": ["array"],
    "relationship_tenure": "string"
  },
  "request_context": {
    "original_input": "string",
    "triggered_rules": ["array of rule IDs"],
    "confidence": "HIGH | MEDIUM | LOW",
    "rationale": "string"
  },
  "recommended_action": "string | null",
  "escalation_tags": ["array"],
  "preserve_session": "boolean"
}
```

**Required fields rationale:**
- `triggered_rules` — Human reviewer needs to know why this escalated
- `rationale` — Plain-language explanation, not just rule IDs
- `recommended_action` — System's suggestion (human can override)
- `preserve_session` — Whether to maintain conversation state for follow-up

### 4. Escalation Routing Targets

Requests route to specialized queues based on trigger category:

| Trigger Category | Routing Target | Typical Handlers |
|------------------|----------------|------------------|
| Suitability concerns | `suitability-review` | Licensed advisors |
| Compliance language | `compliance-review` | Compliance officers |
| Legal/regulatory threats | `compliance-legal` | Compliance + Legal |
| Tax questions | `tax-specialist` | Tax specialists |
| Estate/deceased | `estate-services` | Estate team |
| Fraud indicators | `fraud-ops` | Fraud operations |
| Vulnerable user | `client-relations` | Senior client relations |
| General complex | `supervisor-review` | Team supervisors |

**Multi-category routing:** When multiple categories apply, route to highest-risk queue. Include all relevant tags so secondary teams can be looped in.

### 5. Escalation-to-Resolution Workflow

```
ESCALATE Decision
       │
       ▼
┌─────────────────┐
│ Create Payload  │
│ Assign Priority │
│ Select Target   │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│ Queue Request   │
│ Notify Handler  │
│ Start SLA Clock │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│ Human Reviews   │
│ Takes Action    │
│ Documents Outcome│
└─────────────────┘
       │
       ▼
┌─────────────────┐
│ Close Escalation│
│ Update Metrics  │
│ Feed Back Loop  │
└─────────────────┘
```

**Feedback loop:** Resolution outcomes feed back into rule refinement. Patterns of "escalated but approved" suggest rules are too conservative. Patterns of "escalated and blocked" validate rule sensitivity.

---

## Alternatives Considered

### Alternative A: Binary PROCEED/BLOCK Only

**Rejected because:** Too many legitimate requests would be blocked. Users with reasonable but complex needs would be denied service. No path for human judgment on edge cases.

### Alternative B: Escalate Everything Uncertain

**Rejected because:** Would overwhelm human reviewers with low-risk requests. Operational cost would be unsustainable. Defeats purpose of automated guardrails.

### Alternative C: Single Escalation Queue

**Rejected because:** Different request types require different expertise. Suitability questions need licensed advisors; fraud indicators need fraud ops. Single queue creates bottlenecks and mismatched expertise.

### Alternative D: ML-Based Priority Scoring

**Rejected because:** Priority determination must be explainable for audit purposes. ML scoring creates "black box" that can't be justified to regulators. Rule-based priority is transparent and auditable.

---

## Consequences

### Positive

- **User experience preserved:** Complex requests get human help rather than rejection
- **Compliance risk managed:** Uncertain cases get expert review
- **Operational efficiency:** Priority levels prevent queue flooding
- **Audit trail:** Every escalation is documented with rationale
- **Continuous improvement:** Resolution outcomes inform rule refinement

### Negative

- **Operational cost:** Escalations require human time
- **Latency for users:** Escalated requests don't get immediate answers
- **Queue management:** Requires staffing to meet SLA targets
- **Training requirement:** Handlers need to understand escalation context

### Neutral

- **False positive tolerance:** System accepts some unnecessary escalations to avoid missing real issues
- **Conservative posture:** When uncertain, escalate rather than proceed

---

## Implementation Notes

### Metrics to Monitor

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Escalation rate (% of requests) | 3-7% | >10% |
| HIGH priority rate (% of escalations) | <20% | >30% |
| SLA compliance (% within target) | >95% | <90% |
| Resolution time (avg) | <8 hours | >24 hours |
| Escalate-to-approve rate | Track | Investigate if >80% |
| Escalate-to-block rate | Track | Investigate if <10% |

### Edge Case Handling

- **Duplicate escalations:** Same user, same topic within 24 hours → merge into single case
- **Abandoned sessions:** User disconnects after escalation → still process, attempt outreach
- **After-hours HIGH priority:** Route to on-call, notify management
- **Escalation loops:** If same request type escalates repeatedly → flag for rule review

### Integration Points

| System | Integration |
|--------|-------------|
| Compliance RAG Assistant | Receives PROCEED decisions only |
| Case Management | Receives escalation payloads |
| CRM | Updated with escalation history |
| Audit Log | All escalations logged with full context |
| Analytics | Aggregated metrics, no PII |

---

## Related Documents

- [ADR-001: Routing Logic](./ADR-001-routing-logic.md) — Overall routing architecture
- [Rules: Compliance Triggers](../rules/compliance-triggers.md) — What triggers ESCALATE
- [Rules: Prohibited Content](../rules/prohibited-content.md) — What triggers BLOCK
- [Sample Classifications](../evidence/sample-classifications.md) — ESCALATE examples (#7, #11, #14)
- [Edge Cases](../evidence/edge-cases.md) — Boundary decisions between ESCALATE and BLOCK