# Routing Decision Log

**Module:** Requirements Guardrails  
**Purpose:** Sample audit trail demonstrating the structured output format for routing decisions.

---

## Overview

Every request processed by the Requirements Guardrails module produces a structured decision record. This log demonstrates the output format and provides examples of actual routing decisions for audit and compliance review.

**Key principle:** Decisions are explainable. Every routing outcome traces to specific rules and evidence.

---

## Output Schema

```json
{
  "request_id": "string",
  "timestamp": "ISO-8601",
  "user_id": "string (hashed)",
  "session_id": "string",
  "input_text": "string",
  "routing_decision": "PROCEED | CLARIFY | ESCALATE | BLOCK",
  "triggered_rules": ["array of rule IDs"],
  "confidence": "HIGH | MEDIUM | LOW",
  "rationale": "string",
  "downstream_target": "string | null",
  "metadata": {
    "processing_time_ms": "number",
    "classifier_versions": {},
    "flags": []
  }
}
```

---

## Sample Decision Records

### Record 1: PROCEED

```json
{
  "request_id": "req-2025-001-0847",
  "timestamp": "2025-01-02T14:23:17Z",
  "user_id": "usr_hash_7f3a2b",
  "session_id": "sess_9c4d1e",
  "input_text": "What is the current expense ratio for VTSAX?",
  "routing_decision": "PROCEED",
  "triggered_rules": [],
  "confidence": "HIGH",
  "rationale": "Clear informational query about specific fund attribute. No ambiguity, compliance triggers, or prohibited content detected.",
  "downstream_target": "compliance-rag-assistant",
  "metadata": {
    "processing_time_ms": 47,
    "classifier_versions": {
      "ambiguity": "1.2.0",
      "compliance": "1.1.3",
      "prohibited": "1.0.1"
    },
    "flags": []
  }
}
```

---

### Record 2: CLARIFY

```json
{
  "request_id": "req-2025-001-0848",
  "timestamp": "2025-01-02T14:25:42Z",
  "user_id": "usr_hash_3b8c9d",
  "session_id": "sess_2a5f7g",
  "input_text": "Show me my balance",
  "routing_decision": "CLARIFY",
  "triggered_rules": ["AMB-REF-001"],
  "confidence": "HIGH",
  "rationale": "Referential ambiguity: user has multiple accounts (brokerage, IRA, 401k). Account identifier required.",
  "downstream_target": null,
  "clarification_prompt": "I can show you balances for your accounts. Which would you like to see: Brokerage, Traditional IRA, Roth IRA, or all accounts?",
  "metadata": {
    "processing_time_ms": 52,
    "classifier_versions": {
      "ambiguity": "1.2.0",
      "compliance": "1.1.3",
      "prohibited": "1.0.1"
    },
    "flags": ["multi_account_user"],
    "accounts_on_file": 4
  }
}
```

---

### Record 3: ESCALATE (Suitability)

```json
{
  "request_id": "req-2025-001-0849",
  "timestamp": "2025-01-02T14:31:08Z",
  "user_id": "usr_hash_5d2e4f",
  "session_id": "sess_8h3j2k",
  "input_text": "I'm 68 and retiring next month. Should I put my entire 401k into crypto?",
  "routing_decision": "ESCALATE",
  "triggered_rules": ["SUIT-RISK-001", "SUIT-CONC-001", "SUIT-TIME-001"],
  "confidence": "HIGH",
  "rationale": "Multiple suitability red flags: (1) age/timeline indicates low risk tolerance appropriate, (2) crypto is high-volatility asset, (3) 'entire' signals concentration risk, (4) imminent retirement reduces recovery time.",
  "downstream_target": "compliance-review-queue",
  "escalation_priority": "HIGH",
  "escalation_tags": ["suitability", "concentration", "retirement"],
  "metadata": {
    "processing_time_ms": 89,
    "classifier_versions": {
      "ambiguity": "1.2.0",
      "compliance": "1.1.3",
      "prohibited": "1.0.1",
      "suitability": "1.0.4"
    },
    "flags": ["near_retirement", "high_risk_product", "concentration_language"],
    "user_profile": {
      "age": 68,
      "stated_risk_tolerance": "moderate",
      "retirement_date": "2025-02"
    }
  }
}
```

---

### Record 4: ESCALATE (Compliance Language)

```json
{
  "request_id": "req-2025-001-0850",
  "timestamp": "2025-01-02T14:45:22Z",
  "user_id": "usr_hash_9a7b3c",
  "session_id": "sess_4m6n8p",
  "input_text": "Draft a message to my clients telling them this fund will definitely outperform the market",
  "routing_decision": "ESCALATE",
  "triggered_rules": ["COMP-GUAR-001", "COMP-PRED-001"],
  "confidence": "HIGH",
  "rationale": "Prohibited language patterns detected: (1) 'definitely' implies guarantee, (2) 'outperform the market' is forward-looking performance claim. Violates FINRA 2210(d)(1)(A) and 2210(d)(1)(F).",
  "downstream_target": "compliance-review-queue",
  "escalation_priority": "MEDIUM",
  "escalation_tags": ["finra-2210", "performance-guarantee", "client-communication"],
  "metadata": {
    "processing_time_ms": 71,
    "classifier_versions": {
      "ambiguity": "1.2.0",
      "compliance": "1.1.3",
      "prohibited": "1.0.1"
    },
    "flags": ["advisor_communication", "guarantee_language"],
    "detected_patterns": ["definitely", "will outperform"]
  }
}
```

---

### Record 5: BLOCK

```json
{
  "request_id": "req-2025-001-0851",
  "timestamp": "2025-01-02T15:02:55Z",
  "user_id": "usr_hash_2c4d6e",
  "session_id": "sess_1q3r5s",
  "input_text": "[REDACTED - prohibited content]",
  "routing_decision": "BLOCK",
  "triggered_rules": ["PROH-EXPL-002"],
  "confidence": "HIGH",
  "rationale": "System exploitation attempt detected. Request contained instruction override pattern.",
  "downstream_target": null,
  "block_response": "I can't process that request. How can I help with your account or investment questions?",
  "metadata": {
    "processing_time_ms": 23,
    "classifier_versions": {
      "ambiguity": "1.2.0",
      "compliance": "1.1.3",
      "prohibited": "1.0.1"
    },
    "flags": ["prompt_injection_attempt"],
    "content_logged": false
  }
}
```

**Note:** Prohibited content is not logged in full to avoid creating records of harmful content. Only the category and rule ID are retained.

---

## Log Aggregation Metrics

For compliance reporting and system health monitoring:

### Daily Summary (Sample)

| Metric | Value |
|--------|-------|
| Total requests processed | 12,847 |
| PROCEED | 11,203 (87.2%) |
| CLARIFY | 1,024 (8.0%) |
| ESCALATE | 583 (4.5%) |
| BLOCK | 37 (0.3%) |
| Avg processing time | 54ms |
| P99 processing time | 142ms |

### Escalation Breakdown

| Category | Count | % of Escalations |
|----------|-------|------------------|
| Suitability flags | 287 | 49.2% |
| Compliance language | 198 | 34.0% |
| Regulatory boundary | 71 | 12.2% |
| Tax/legal advice | 27 | 4.6% |

### Clarification Efficiency

| Metric | Value |
|--------|-------|
| Single-round resolution | 847 (82.7%) |
| Two-round resolution | 142 (13.9%) |
| Abandoned after clarify | 35 (3.4%) |

---

## Audit Query Examples

Common queries compliance teams run against this log:

```sql
-- All escalations for a specific user in date range
SELECT * FROM routing_decisions 
WHERE user_id = 'usr_hash_xxx' 
  AND routing_decision = 'ESCALATE'
  AND timestamp BETWEEN '2025-01-01' AND '2025-01-31';

-- Suitability escalations for retirement-age users
SELECT * FROM routing_decisions 
WHERE 'suitability' = ANY(escalation_tags)
  AND metadata->>'user_profile'->>'age' >= 65;

-- Block rate trend by week
SELECT DATE_TRUNC('week', timestamp), 
       COUNT(*) FILTER (WHERE routing_decision = 'BLOCK') as blocks,
       COUNT(*) as total
FROM routing_decisions
GROUP BY 1 ORDER BY 1;
```

---

## Retention Policy

| Record Type | Retention Period | Rationale |
|-------------|------------------|-----------|
| PROCEED | 90 days | Operational monitoring |
| CLARIFY | 1 year | UX pattern analysis |
| ESCALATE | 7 years | Regulatory requirement |
| BLOCK | 7 years | Compliance/legal requirement |

---

## Related Documents

- [Rules: Ambiguity Heuristics](../rules/ambiguity-heuristics.md) — CLARIFY trigger definitions
- [Rules: Compliance Triggers](../rules/compliance-triggers.md) — ESCALATE trigger definitions
- [Rules: Prohibited Content](../rules/prohibited-content.md) — BLOCK trigger definitions
- [ADR-001: Routing Logic](../architecture/ADR-001-routing-logic.md) — Why this structure