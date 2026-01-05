# Test Case: Refusal — AMBIGUOUS_QUERY

**Refusal Code:** `AMBIGUOUS_QUERY`  
**Severity:** Info  
**Taxonomy Reference:** [config/refusal-taxonomy.yaml](../../config/refusal-taxonomy.yaml)

---

## Purpose

Validate that the CRA correctly identifies queries that lack sufficient specificity to retrieve meaningful results, and prompts the user for clarification rather than guessing or returning irrelevant information.

---

## Scenario

A user submits a vague or incomplete query that could match multiple unrelated topics in the corpus. Rather than guessing intent or returning a grab-bag of loosely related content, the system should ask for clarification.

---

## Test Inputs

### Query
```
What's the policy?
```

### User Context
```yaml
user_role: analyst
session_id: test-session-004
```

### Corpus State
- Corpus contains hundreds of policies across multiple topics
- Query provides no context to narrow scope
- Corpus release: v2025.01.06

---

## Expected Behavior

### Preprocessing Stage
| Check | Expected |
|-------|----------|
| Query normalized | "what's the policy" |
| Key terms extracted | ["policy"] — too generic |
| Intent classification | AMBIGUOUS |
| Ambiguity flags | ["no_specific_topic", "multiple_matches_likely"] |

### Retrieval Stage
| Check | Expected |
|-------|----------|
| Retrieval attempted | Optional — may skip or execute |
| If executed | Returns diverse, unrelated passages |
| Ambiguity detected | Yes — results too scattered |

### Decision Stage
| Check | Expected |
|-------|----------|
| Outcome | REFUSE |
| Refusal code | AMBIGUOUS_QUERY |
| Escalation triggered | false |
| LLM invoked | No |

---

## Expected Response

Per [response-contract.md](../../docs/response-contract.md):

```json
{
  "trace_id": "<generated>",
  "timestamp": "<generated>",
  "query": "What's the policy?",
  "grounding_status": "REFUSED",
  "answer": null,
  "citations": [],
  "refusal": {
    "code": "AMBIGUOUS_QUERY",
    "reason": "I need more detail to find the right information.",
    "user_guidance": "Your question could apply to many different policies. Could you specify which area you're asking about?",
    "next_steps": ["Specify the topic area", "Add context about your use case"],
    "clarification_prompts": [
      "Are you asking about a specific procedure (e.g., wire transfers, account opening)?",
      "Which business area does this relate to?",
      "Can you provide more context about what you're trying to accomplish?"
    ]
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
    "query": "What's the policy?",
    "user_role": "analyst"
  },
  "preprocessing": {
    "normalized_query": "what's the policy",
    "key_terms": ["policy"],
    "extracted_intent": "AMBIGUOUS",
    "ambiguity_flags": ["no_specific_topic", "multiple_matches_likely"]
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
    "refusal_code": "AMBIGUOUS_QUERY",
    "rationale_codes": ["QUERY_AMBIGUOUS", "INSUFFICIENT_SPECIFICITY"],
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
| 1 | Refusal code is AMBIGUOUS_QUERY | response.refusal.code == "AMBIGUOUS_QUERY" |
| 2 | Grounding status is REFUSED | response.grounding_status == "REFUSED" |
| 3 | No answer provided | response.answer == null |
| 4 | Clarification prompts provided | response.refusal.clarification_prompts is non-empty |
| 5 | Prompts are helpful | Prompts suggest specific ways to narrow query |
| 6 | Tone is helpful, not dismissive | Guidance doesn't blame user |
| 7 | LLM not invoked | trace.model.provider == null |
| 8 | Trace records ambiguity detection | trace.preprocessing.extracted_intent == "AMBIGUOUS" |

---

## Fail Conditions

| Condition | Why It's Wrong |
|-----------|----------------|
| System guesses and answers | Likely to return wrong policy; bad UX |
| System returns random policy | Misleading — user didn't ask for that |
| NO_ELIGIBLE_DOCS returned | Wrong code — docs exist, query is the problem |
| Generic "try again" message | Unhelpful — should guide user to better query |
| Condescending tone | "Your query is too vague" is dismissive |
| LLM invoked to "figure it out" | Wasted resources; ambiguity should be caught early |

---

## Ambiguity Detection Signals

The preprocessing stage should flag ambiguity when:

| Signal | Example |
|--------|---------|
| Very short query | "policy?" |
| Only generic terms | "what's the rule" |
| Missing topic specifier | "how does it work" |
| Pronouns without referent | "what about that" |
| High-cardinality term | "policy" matches 100+ documents |

---

## Variations

### Variation A: Pronouns without context
```
Can you explain it?
```
No referent for "it" — should request clarification.

### Variation B: Generic + specific (partial ambiguity)
```
What's the policy for wire transfers?
```
"Wire transfers" is specific enough — should NOT refuse as ambiguous. This validates that ambiguity detection doesn't over-trigger.

### Variation C: Multiple possible topics
```
What are the requirements?
```
Could be requirements for account opening, wire transfers, compliance training, etc. Should ask for clarification.

### Variation D: Ambiguous timeframe
```
What changed in the policy?
```
Which policy? When? Should prompt for specifics.

---

## Contrast with Other Refusal Codes

| Query | Correct Code | Why |
|-------|--------------|-----|
| "What's the policy?" | AMBIGUOUS_QUERY | Query is vague |
| "What's the cryptocurrency policy?" | NO_ELIGIBLE_DOCS | Query is specific, topic not in corpus |
| "What's the investigation policy?" | POLICY_BLOCKED | Query is specific, access denied |
| "What's the wire transfer policy?" | (No refusal) | Query is specific, should attempt answer |

---

## Configuration Dependencies

From [refusal-taxonomy.yaml](../../config/refusal-taxonomy.yaml):

```yaml
AMBIGUOUS_QUERY:
  clarification_prompts:
    - "Could you specify which policy area you're asking about?"
    - "What process or procedure does this relate to?"
    - "Can you provide more context about your question?"
```

---

## Related Artifacts

- [refusal-taxonomy.yaml](../../config/refusal-taxonomy.yaml) — Code definition with clarification prompts
- [response-contract.md](../../docs/response-contract.md) — Response structure
- [trace-schema.md](../../docs/trace-schema.md) — Audit structure
- [component-design.md](../../architecture/component-design.md) — Query Preprocessor component