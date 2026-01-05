# Test Case: Refusal — NO_ELIGIBLE_DOCS

**Refusal Code:** `NO_ELIGIBLE_DOCS`  
**Severity:** Info  
**Taxonomy Reference:** [config/refusal-taxonomy.yaml](../../config/refusal-taxonomy.yaml)

---

## Purpose

Validate that the CRA correctly refuses when a query falls entirely outside the scope of the approved corpus. This is not a failure — it's the system correctly recognizing its boundaries.

---

## Scenario

A user asks a question on a topic that has no coverage in any approved collection. The retrieval stage finds no passages above the similarity threshold.

---

## Test Inputs

### Query
```
What are the tax implications of cryptocurrency staking rewards?
```

### User Context
```yaml
user_role: analyst
session_id: test-session-001
```

### Corpus State
- Collections searched: compliance-policies, regulatory-guidance
- No documents about cryptocurrency taxation in corpus
- Corpus release: v2025.01.06

---

## Expected Behavior

### Retrieval Stage
| Check | Expected |
|-------|----------|
| Collections searched | compliance-policies, regulatory-guidance |
| Passages retrieved | 0 (or all below threshold) |
| Passages above threshold | 0 |

### Grounding Stage
| Check | Expected |
|-------|----------|
| Grounding status | REFUSED |
| Grounding coverage | 0.0 |
| Conflict detected | false |

### Decision Stage
| Check | Expected |
|-------|----------|
| Outcome | REFUSE |
| Refusal code | NO_ELIGIBLE_DOCS |
| Escalation triggered | false |
| LLM invoked | No — skip LLM when no eligible docs |

---

## Expected Response

Per [response-contract.md](../../docs/response-contract.md):

```json
{
  "trace_id": "<generated>",
  "timestamp": "<generated>",
  "query": "What are the tax implications of cryptocurrency staking rewards?",
  "grounding_status": "REFUSED",
  "answer": null,
  "citations": [],
  "refusal": {
    "code": "NO_ELIGIBLE_DOCS",
    "reason": "Your question falls outside the topics covered by the compliance knowledge base.",
    "user_guidance": "This system covers internal compliance policies, regulatory guidance, and operational procedures. For tax-related questions, please consult the Tax Advisory team or refer to IRS guidance.",
    "next_steps": ["Contact Tax Advisory", "Consult external resources"],
    "retrieval_summary": {
      "collections_searched": ["compliance-policies", "regulatory-guidance"],
      "passages_found": 0
    }
  },
  "metadata": {
    "corpus_release_id": "v2025.01.06",
    "sources_consulted": 0,
    "model_provider": null,
    "processing_time_ms": "<generated>"
  }
}
```

---

## Expected Trace

Per [trace-schema.md](../../docs/trace-schema.md):

```json
{
  "trace_id": "<matches response>",
  "corpus_release_id": "v2025.01.06",
  "input": {
    "query": "What are the tax implications of cryptocurrency staking rewards?",
    "user_role": "analyst"
  },
  "retrieval": {
    "collections_searched": ["compliance-policies", "regulatory-guidance"],
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
    "refusal_code": "NO_ELIGIBLE_DOCS",
    "rationale_codes": ["NO_RELEVANT_PASSAGES"],
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

---

## Pass Criteria

| # | Criterion | Validation |
|---|-----------|------------|
| 1 | Refusal code is NO_ELIGIBLE_DOCS | response.refusal.code == "NO_ELIGIBLE_DOCS" |
| 2 | Grounding status is REFUSED | response.grounding_status == "REFUSED" |
| 3 | No answer provided | response.answer == null |
| 4 | No citations | response.citations == [] |
| 5 | User guidance is helpful | response.refusal.user_guidance contains actionable alternatives |
| 6 | LLM not invoked | trace.model.provider == null |
| 7 | Trace committed | trace exists and is complete |
| 8 | Collections searched logged | trace.retrieval.collections_searched is populated |

---

## Fail Conditions

| Condition | Why It's Wrong |
|-----------|----------------|
| System returns an answer | Hallucination — no grounding exists |
| Different refusal code | Misclassification of the failure mode |
| LLM was invoked | Wasted resources; should short-circuit |
| No trace record | Audit integrity violation |
| Generic/unhelpful guidance | Poor user experience |

---

## Variations

### Variation A: Partial topic match
Query mentions a term that appears in corpus but in unrelated context.
```
What is the policy on employee cryptocurrency holdings?
```
May return low-relevance passages. Should still refuse if below grounding threshold.

### Variation B: Adjacent topic
Query is close to corpus scope but not covered.
```
What are the GDPR requirements for customer data?
```
If corpus doesn't include GDPR content, should refuse with NO_ELIGIBLE_DOCS.

---

## Related Artifacts

- [refusal-taxonomy.yaml](../../config/refusal-taxonomy.yaml) — Code definition
- [response-contract.md](../../docs/response-contract.md) — Response structure
- [trace-schema.md](../../docs/trace-schema.md) — Audit structure
- [scorecard.md](../scorecard.md) — Refusal Appropriateness dimension