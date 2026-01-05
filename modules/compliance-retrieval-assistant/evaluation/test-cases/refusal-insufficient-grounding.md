# Test Case: Refusal — INSUFFICIENT_GROUNDING

**Refusal Code:** `INSUFFICIENT_GROUNDING`  
**Severity:** Warning  
**Taxonomy Reference:** [config/refusal-taxonomy.yaml](../../config/refusal-taxonomy.yaml)

---

## Purpose

Validate that the CRA correctly refuses when passages are retrieved but they cannot adequately substantiate an answer. This tests the grounding checker's ability to distinguish "found something" from "found enough."

---

## Scenario

A user asks a specific question. The retrieval stage finds relevant passages, but they don't contain sufficient information to fully answer the question. The grounding coverage falls below the configured threshold.

---

## Test Inputs

### Query
```
What is the maximum dollar amount for expedited wire transfers without additional approval?
```

### User Context
```yaml
user_role: analyst
session_id: test-session-002
```

### Corpus State
- Collections searched: compliance-policies, internal-procedures
- Retrieved passages discuss wire transfer procedures generally
- No passage specifies the exact dollar threshold
- Corpus release: v2025.01.06

### Simulated Retrieved Passages
```yaml
passages:
  - passage_id: "wire-procedures-chunk-12"
    content: "Wire transfers require dual approval from authorized personnel. Expedited processing is available for time-sensitive transactions."
    similarity_score: 0.82
    
  - passage_id: "wire-procedures-chunk-15"
    content: "All wire transfers must be logged in the transaction management system with full audit trail."
    similarity_score: 0.76
```

---

## Expected Behavior

### Retrieval Stage
| Check | Expected |
|-------|----------|
| Collections searched | compliance-policies, internal-procedures |
| Passages retrieved | 2+ |
| Passages above threshold | 2 |
| Top passage score | ~0.82 |

### Grounding Stage
| Check | Expected |
|-------|----------|
| Grounding status | REFUSED |
| Grounding coverage | < policy threshold (e.g., 0.3) |
| Supporting passages | 0 (none adequately answer the question) |
| Conflict detected | false |

### Decision Stage
| Check | Expected |
|-------|----------|
| Outcome | REFUSE |
| Refusal code | INSUFFICIENT_GROUNDING |
| Escalation triggered | false (configurable) |
| LLM invoked | No — refuse before generation |

---

## Expected Response

Per [response-contract.md](../../docs/response-contract.md):

```json
{
  "trace_id": "<generated>",
  "timestamp": "<generated>",
  "query": "What is the maximum dollar amount for expedited wire transfers without additional approval?",
  "grounding_status": "REFUSED",
  "answer": null,
  "citations": [],
  "refusal": {
    "code": "INSUFFICIENT_GROUNDING",
    "reason": "I found some related information, but not enough to fully answer your question.",
    "user_guidance": "The retrieved documents discuss wire transfer procedures but don't specify the dollar threshold you're asking about. Consider refining your question or consulting the Wire Operations team directly.",
    "next_steps": ["Refine your question", "Contact Wire Operations", "Review wire transfer policy manual"],
    "retrieval_summary": {
      "collections_searched": ["compliance-policies", "internal-procedures"],
      "passages_found": 2,
      "relevance_note": "Related content found but insufficient for specific answer"
    }
  },
  "metadata": {
    "corpus_release_id": "v2025.01.06",
    "sources_consulted": 2,
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
    "query": "What is the maximum dollar amount for expedited wire transfers without additional approval?",
    "user_role": "analyst"
  },
  "retrieval": {
    "collections_searched": ["compliance-policies", "internal-procedures"],
    "passages_retrieved": 2,
    "passages_above_threshold": 2,
    "top_passage_score": 0.82,
    "passage_ids": ["wire-procedures-chunk-12", "wire-procedures-chunk-15"]
  },
  "grounding": {
    "status": "REFUSED",
    "supporting_passages": 0,
    "grounding_coverage": 0.3,
    "conflict_detected": false
  },
  "decision": {
    "outcome": "REFUSE",
    "refusal_code": "INSUFFICIENT_GROUNDING",
    "rationale_codes": ["BELOW_GROUNDING_THRESHOLD", "SPECIFIC_INFO_NOT_FOUND"],
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
| 1 | Refusal code is INSUFFICIENT_GROUNDING | response.refusal.code == "INSUFFICIENT_GROUNDING" |
| 2 | Grounding status is REFUSED | response.grounding_status == "REFUSED" |
| 3 | No answer provided | response.answer == null |
| 4 | Passages were found | trace.retrieval.passages_retrieved > 0 |
| 5 | Coverage below threshold | trace.grounding.grounding_coverage < threshold |
| 6 | User guidance acknowledges partial info | Guidance mentions "found some related information" |
| 7 | LLM not invoked | trace.model.provider == null |
| 8 | Trace committed | trace exists and is complete |

---

## Fail Conditions

| Condition | Why It's Wrong |
|-----------|----------------|
| System fabricates an answer | Hallucination — inventing the dollar amount |
| NO_ELIGIBLE_DOCS returned | Wrong code — docs were found, just insufficient |
| System returns partial answer without warning | Must flag grounding gaps explicitly |
| LLM was invoked | Should refuse before generation |
| Guidance says "no information found" | Inaccurate — info was found, just not enough |

---

## Boundary Cases

### Case A: Just below threshold
Grounding coverage is 0.58, threshold is 0.60.
- Should refuse with INSUFFICIENT_GROUNDING
- Tests threshold boundary behavior

### Case B: Just above threshold (should NOT refuse)
Grounding coverage is 0.62, threshold is 0.60.
- Should proceed with PARTIALLY_GROUNDED
- This case validates the threshold is working correctly

### Case C: High retrieval score, low grounding
Passages are semantically similar (high retrieval score) but don't answer the question.
- Retrieval score: 0.88
- Grounding coverage: 0.25
- Should refuse — retrieval score ≠ grounding adequacy

---

## Configuration Dependencies

From [policy-constraints.yaml](../../config/policy-constraints.yaml):

```yaml
grounding:
  min_supporting_passages: 1
  partial_grounding_allowed: true
  partial_threshold: 0.6
```

This test assumes grounding coverage falls below `partial_threshold`.

---

## Related Artifacts

- [refusal-taxonomy.yaml](../../config/refusal-taxonomy.yaml) — Code definition
- [policy-constraints.yaml](../../config/policy-constraints.yaml) — Grounding thresholds
- [response-contract.md](../../docs/response-contract.md) — Response structure
- [trace-schema.md](../../docs/trace-schema.md) — Audit structure
- [component-design.md](../../architecture/component-design.md) — Grounding Checker component