# Test Case: Refusal — CONFLICTING_SOURCES

**Refusal Code:** `CONFLICTING_SOURCES`  
**Severity:** Escalate  
**Taxonomy Reference:** [config/refusal-taxonomy.yaml](../../config/refusal-taxonomy.yaml)

---

## Purpose

Validate that the CRA correctly refuses when authoritative sources in the corpus provide contradictory guidance. This is the most critical refusal code — the system must never arbitrarily choose between conflicting authorities without human review.

---

## Scenario

A user asks about a specific requirement. The retrieval stage finds relevant passages from multiple authoritative sources, but those sources contradict each other on a material point. The system should refuse, explain the conflict, and escalate for human resolution.

---

## Test Inputs

### Query
```
What is the required holding period for restricted securities before they can be sold?
```

### User Context
```yaml
user_role: analyst
session_id: test-session-005
```

### Corpus State
- Collections searched: regulatory-guidance, compliance-policies
- Conflicting passages found from different sources
- Corpus release: v2025.01.06

### Simulated Retrieved Passages
```yaml
passages:
  - passage_id: "sec-rule-144-chunk-8"
    source_id: "sec-rule-144-summary-2024"
    source_title: "SEC Rule 144 Summary"
    content: "The holding period for restricted securities is six months for reporting companies."
    collection: "regulatory-guidance"
    effective_date: "2024-03-15"
    similarity_score: 0.91
    
  - passage_id: "internal-policy-chunk-22"
    source_id: "restricted-securities-policy-v3"
    source_title: "Internal Restricted Securities Policy"
    content: "All restricted securities must be held for a minimum of twelve months before any sale is permitted."
    collection: "compliance-policies"
    effective_date: "2023-09-01"
    similarity_score: 0.88
```

---

## Expected Behavior

### Retrieval Stage
| Check | Expected |
|-------|----------|
| Collections searched | regulatory-guidance, compliance-policies |
| Passages retrieved | 2+ |
| Passages above threshold | 2 |
| Top passage score | ~0.91 |

### Grounding Stage
| Check | Expected |
|-------|----------|
| Conflict detection | TRUE |
| Conflict type | "contradictory_guidance" |
| Grounding status | REFUSED |
| Grounding coverage | N/A — conflict blocks grounding |

### Decision Stage
| Check | Expected |
|-------|----------|
| Outcome | REFUSE |
| Refusal code | CONFLICTING_SOURCES |
| Escalation triggered | **TRUE** |
| LLM invoked | No — refuse before generation |

---

## Expected Response

Per [response-contract.md](../../docs/response-contract.md):

```json
{
  "trace_id": "<generated>",
  "timestamp": "<generated>",
  "query": "What is the required holding period for restricted securities before they can be sold?",
  "grounding_status": "REFUSED",
  "answer": null,
  "citations": [],
  "refusal": {
    "code": "CONFLICTING_SOURCES",
    "reason": "I found conflicting information in authoritative sources and cannot provide a reliable answer.",
    "user_guidance": "The retrieved documents contain contradictory guidance on this topic. This has been flagged for review by a subject matter expert. Please consult directly with the Compliance team for authoritative guidance.",
    "next_steps": ["Consult Compliance team", "Await SME review", "Reference both sources with legal counsel"],
    "conflict_summary": {
      "sources_in_conflict": 2,
      "nature_of_conflict": "Different holding periods specified (6 months vs 12 months)",
      "escalation_id": "<generated>"
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
    "query": "What is the required holding period for restricted securities before they can be sold?",
    "user_role": "analyst"
  },
  "retrieval": {
    "collections_searched": ["regulatory-guidance", "compliance-policies"],
    "passages_retrieved": 2,
    "passages_above_threshold": 2,
    "top_passage_score": 0.91,
    "passage_ids": ["sec-rule-144-chunk-8", "internal-policy-chunk-22"]
  },
  "grounding": {
    "status": "REFUSED",
    "supporting_passages": 0,
    "grounding_coverage": 0.0,
    "conflict_detected": true,
    "conflict_details": {
      "conflict_type": "contradictory_guidance",
      "conflicting_passages": [
        {
          "passage_id": "sec-rule-144-chunk-8",
          "source_title": "SEC Rule 144 Summary",
          "position": "6-month holding period"
        },
        {
          "passage_id": "internal-policy-chunk-22",
          "source_title": "Internal Restricted Securities Policy",
          "position": "12-month holding period"
        }
      ]
    }
  },
  "decision": {
    "outcome": "REFUSE",
    "refusal_code": "CONFLICTING_SOURCES",
    "rationale_codes": ["CONFLICT_DETECTED", "AUTHORITATIVE_SOURCES_DISAGREE"],
    "escalation_triggered": true,
    "escalation_id": "<generated>"
  },
  "model": {
    "provider": null,
    "model_id": null,
    "prompt_tokens": 0,
    "completion_tokens": 0
  },
  "audit_metadata": {
    "retention_class": "permanent"
  }
}
```

---

## Expected Escalation

When CONFLICTING_SOURCES is detected, the system should create an escalation record:

```json
{
  "escalation_id": "<generated>",
  "trace_id": "<matches response>",
  "timestamp": "<generated>",
  "query": "What is the required holding period for restricted securities before they can be sold?",
  "conflict_summary": {
    "source_a": {
      "source_id": "sec-rule-144-summary-2024",
      "position": "6-month holding period",
      "effective_date": "2024-03-15"
    },
    "source_b": {
      "source_id": "restricted-securities-policy-v3",
      "position": "12-month holding period",
      "effective_date": "2023-09-01"
    }
  },
  "status": "pending_review",
  "assigned_to": null,
  "resolution": null
}
```

---

## Pass Criteria

| # | Criterion | Validation |
|---|-----------|------------|
| 1 | Refusal code is CONFLICTING_SOURCES | response.refusal.code == "CONFLICTING_SOURCES" |
| 2 | Grounding status is REFUSED | response.grounding_status == "REFUSED" |
| 3 | No answer provided | response.answer == null |
| 4 | Conflict detected in trace | trace.grounding.conflict_detected == true |
| 5 | Both sources logged | trace.grounding.conflict_details includes both passages |
| 6 | Escalation triggered | trace.decision.escalation_triggered == true |
| 7 | Escalation ID generated | response.refusal.conflict_summary.escalation_id exists |
| 8 | Permanent retention | trace.audit_metadata.retention_class == "permanent" |
| 9 | LLM not invoked | trace.model.provider == null |
| 10 | User directed to SME | response.refusal.user_guidance mentions Compliance team |

---

## Fail Conditions

| Condition | Why It's Wrong |
|-----------|----------------|
| System picks one source arbitrarily | **Critical failure** — could provide wrong guidance |
| System averages/synthesizes the answers | Fabrication — "9 months" is not in any source |
| System returns the newer source | Arbitrary rule — newer isn't always correct |
| System returns the regulatory source | Arbitrary rule — internal policy may be stricter for good reason |
| No escalation triggered | Conflicts must be reviewed by humans |
| Different refusal code | Misclassification — conflict is the issue |
| LLM invoked to "resolve" conflict | Model cannot authoritatively resolve source conflicts |

---

## Why This Matters

Conflicting sources are especially dangerous in regulated environments:

| If system chooses wrong... | Consequence |
|---------------------------|-------------|
| Uses 6-month period (SEC) but internal policy requires 12 | Employee violates company policy |
| Uses 12-month period (internal) but SEC allows 6 | Unnecessary restriction, potential business impact |
| Makes up a compromise | No authority for the answer — audit failure |

**The only safe response is to refuse and escalate.**

---

## Variations

### Variation A: Same source, different versions
```yaml
- source: "Wire Transfer Policy v2.1" says $10,000 limit
- source: "Wire Transfer Policy v3.0" says $25,000 limit
```
Should flag as conflict (corpus may have version control issues).

### Variation B: Regulatory vs. regulatory conflict
```yaml
- SEC guidance says X
- FINRA guidance says Y
```
Both are authoritative external sources — conflict must be escalated.

### Variation C: Ambiguous conflict (interpretation difference)
```yaml
- Source A: "generally within 6 months"
- Source B: "minimum of 6 months"
```
"Generally within" vs "minimum of" could be interpreted as conflict. Conservative approach: flag and escalate.

### Variation D: No conflict (complementary information)
```yaml
- Source A: "6-month holding period for reporting companies"
- Source B: "12-month holding period for non-reporting companies"
```
Not a conflict — different scopes. System should NOT refuse.

---

## Configuration Dependencies

From [refusal-taxonomy.yaml](../../config/refusal-taxonomy.yaml):

```yaml
CONFLICTING_SOURCES:
  severity: escalate
  resolution_guidance:
    - "Do not attempt to synthesize or average conflicting guidance"
    - "Present the conflict to a human reviewer"
    - "Log both positions for audit purposes"

escalation:
  always_escalate:
    - CONFLICTING_SOURCES
```

From [policy-constraints.yaml](../../config/policy-constraints.yaml):

```yaml
escalation:
  enabled: true  # Must be true for this test
  queue_endpoint: "<configured>"
  notify_user: true
```

---

## Related Artifacts

- [refusal-taxonomy.yaml](../../config/refusal-taxonomy.yaml) — Code definition, escalation rules
- [policy-constraints.yaml](../../config/policy-constraints.yaml) — Escalation configuration
- [response-contract.md](../../docs/response-contract.md) — Response structure
- [trace-schema.md](../../docs/trace-schema.md) — Audit structure, conflict_details
- [threat-model.md](../../docs/threat-model.md) — Conflicting Source Mishandling threat
- [ADR-001](../../architecture/decisions/ADR-001-grounding-status-over-confidence-scores.md) — Why we can't "confidence score" our way out of conflicts