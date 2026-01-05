# Test Case: Refusal — POLICY_BLOCKED

**Refusal Code:** `POLICY_BLOCKED`  
**Severity:** Warning  
**Taxonomy Reference:** [config/refusal-taxonomy.yaml](../../config/refusal-taxonomy.yaml)

---

## Purpose

Validate that the CRA correctly refuses when a user's role lacks permission to access the collections or topics needed to answer their query. This tests the access control layer and ensures no information leakage about restricted content.

---

## Scenario

A user with `analyst` role asks a question that requires access to the `internal-investigations` collection, which is restricted to `legal_counsel` and `compliance_officer` roles. The system should refuse without revealing which specific collection was blocked.

---

## Test Inputs

### Query
```
What were the findings from the Q3 internal investigation into the trading desk?
```

### User Context
```yaml
user_role: analyst
session_id: test-session-003
```

### Role Permissions
From [role-permissions.yaml](../../config/role-permissions.yaml):
```yaml
analyst:
  allowed_collections:
    - compliance-policies
    - regulatory-guidance
  restricted_collections: []
  
# internal-investigations requires legal_counsel or compliance_officer
```

### Corpus State
- Query would require: internal-investigations collection
- User has access to: compliance-policies, regulatory-guidance only
- Corpus release: v2025.01.06

---

## Expected Behavior

### Retrieval Stage
| Check | Expected |
|-------|----------|
| Permission check | FAIL — user lacks access |
| Collections searched | None (blocked before search) |
| Passages retrieved | 0 |

### Grounding Stage
| Check | Expected |
|-------|----------|
| Grounding status | REFUSED |
| Skipped | Yes — no retrieval occurred |

### Decision Stage
| Check | Expected |
|-------|----------|
| Outcome | REFUSE |
| Refusal code | POLICY_BLOCKED |
| Escalation triggered | false |
| LLM invoked | No |

---

## Expected Response

Per [response-contract.md](../../docs/response-contract.md):

```json
{
  "trace_id": "<generated>",
  "timestamp": "<generated>",
  "query": "What were the findings from the Q3 internal investigation into the trading desk?",
  "grounding_status": "REFUSED",
  "answer": null,
  "citations": [],
  "refusal": {
    "code": "POLICY_BLOCKED",
    "reason": "You don't have access to materials needed to answer this question.",
    "user_guidance": "Contact your administrator if you believe this is an error.",
    "next_steps": ["Contact your administrator", "Request elevated access if appropriate"],
    "retrieval_summary": null
  },
  "metadata": {
    "corpus_release_id": "v2025.01.06",
    "sources_consulted": 0,
    "model_provider": null,
    "processing_time_ms": "<generated>"
  }
}
```

### Critical: No Information Leakage

The response must **NOT** reveal:
- Which collection was blocked
- That `internal-investigations` collection exists
- What content might be in restricted collections
- Why specifically the query was blocked

---

## Expected Trace

Per [trace-schema.md](../../docs/trace-schema.md):

```json
{
  "trace_id": "<matches response>",
  "corpus_release_id": "v2025.01.06",
  "input": {
    "query": "What were the findings from the Q3 internal investigation into the trading desk?",
    "user_role": "analyst"
  },
  "retrieval": {
    "collections_searched": [],
    "passages_retrieved": 0,
    "passages_above_threshold": 0,
    "top_passage_score": null
  },
  "grounding": {
    "status": "REFUSED",
    "supporting_passages": 0,
    "grounding_coverage": 0.0,
    "conflict_detected": false
  },
  "decision": {
    "outcome": "REFUSE",
    "refusal_code": "POLICY_BLOCKED",
    "rationale_codes": ["ACCESS_DENIED", "COLLECTION_RESTRICTED", "ROLE_INSUFFICIENT"],
    "escalation_triggered": false
  },
  "model": {
    "provider": null,
    "model_id": null,
    "prompt_tokens": 0,
    "completion_tokens": 0
  }
}
```

### Note: Trace Contains More Detail

The trace **does** record the access denial reason (for audit purposes), but this detail is not exposed to the user.

---

## Pass Criteria

| # | Criterion | Validation |
|---|-----------|------------|
| 1 | Refusal code is POLICY_BLOCKED | response.refusal.code == "POLICY_BLOCKED" |
| 2 | Grounding status is REFUSED | response.grounding_status == "REFUSED" |
| 3 | No answer provided | response.answer == null |
| 4 | Generic user message | response.refusal.reason does NOT mention specific collection |
| 5 | No retrieval attempted | trace.retrieval.collections_searched == [] |
| 6 | LLM not invoked | trace.model.provider == null |
| 7 | Trace records denial reason | trace.decision.rationale_codes includes "ACCESS_DENIED" |
| 8 | Access attempt logged | trace exists for security audit |

---

## Fail Conditions

| Condition | Why It's Wrong |
|-----------|----------------|
| System reveals blocked collection | Information leakage — security violation |
| System searches then blocks | Inefficient — should block before search |
| Different refusal code | Misclassification — this is an access issue |
| System returns partial info from allowed collections | May mislead user about what's available |
| No trace record | Security events must always be logged |
| Message says "no information found" | Misleading — information exists, access is denied |

---

## Security Considerations

### Why Generic Messages Matter

Specific error messages can leak information:
- ❌ "You cannot access internal-investigations" → Reveals collection exists
- ❌ "Investigation findings are restricted" → Confirms investigations exist
- ✅ "You don't have access to materials needed" → Generic, safe

### Audit Trail Requirements

Even though user sees generic message, trace must capture:
- User role that was denied
- Collections that would have been needed
- Timestamp of attempt
- Full query text

This enables security review without user-facing leakage.

---

## Variations

### Variation A: Topic restriction (not collection)
```
What is the status of the whistleblower case?
```
User has access to collection, but `whistleblower` is a restricted topic per `global_topic_restrictions`. Should still return POLICY_BLOCKED with generic message.

### Variation B: Partial access
```
What are the wire transfer procedures and investigation findings?
```
Query spans allowed (wire procedures) and restricted (investigation) content. System should refuse entirely — partial answers risk information leakage about what's restricted.

### Variation C: Role just below threshold
User is `senior_analyst` (access to internal-procedures but not internal-investigations). Validates role hierarchy is enforced correctly.

---

## Configuration Dependencies

From [role-permissions.yaml](../../config/role-permissions.yaml):

```yaml
access_denied:
  refusal_code: POLICY_BLOCKED
  log_attempt: true
  include_in_audit: true
  reveal_blocked_resource: false  # Critical setting
```

---

## Related Artifacts

- [refusal-taxonomy.yaml](../../config/refusal-taxonomy.yaml) — Code definition
- [role-permissions.yaml](../../config/role-permissions.yaml) — Access control configuration
- [response-contract.md](../../docs/response-contract.md) — Response structure
- [trace-schema.md](../../docs/trace-schema.md) — Audit structure
- [threat-model.md](../../docs/threat-model.md) — Role spoofing, information leakage threats