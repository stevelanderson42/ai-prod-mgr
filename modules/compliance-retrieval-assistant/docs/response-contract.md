# Response Contract

**User-Facing Contract for the Compliance Retrieval Assistant**

---

## Purpose

This document defines the structure and guarantees of responses returned to users by the Compliance Retrieval Assistant. It is the **user-facing contract** — what end users see and can rely upon.

> **PM DECISION:** Users and auditors have different needs. This contract serves users; the [trace-schema.md](trace-schema.md) serves auditors. Separating these concerns enables clarity for both audiences.

---

## Response Shape

Every response from the CRA conforms to this structure:

```json
{
  "trace_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2025-01-06T14:30:00Z",
  "query": "What is the required holding period for restricted securities?",
  
  "grounding_status": "FULLY_GROUNDED",
  
  "answer": "Under SEC Rule 144, the holding period for restricted securities is six months for reporting companies and one year for non-reporting companies. [1] The holding period begins when the securities are fully paid for. [1]",
  
  "citations": [
    {
      "citation_id": 1,
      "source_id": "sec-rule-144-summary-2024",
      "source_title": "SEC Rule 144 Summary",
      "effective_date": "2024-03-15",
      "passage": "The holding period is six months if the issuer is a reporting company, or one year if the issuer is not a reporting company.",
      "collection": "regulatory-guidance"
    }
  ],
  
  "refusal": null,
  
  "metadata": {
    "corpus_release_id": "v2025.01.04",
    "sources_consulted": 3,
    "model_provider": "anthropic"
  }
}
```

---

## Field Definitions

### Core Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `trace_id` | UUID | Always | Unique identifier for audit lookup |
| `timestamp` | ISO-8601 | Always | When the response was generated |
| `query` | String | Always | Original user query (echoed back) |
| `grounding_status` | Enum | Always | How well the answer is supported |
| `answer` | String | Conditional | Response text (null if refused) |
| `citations` | Array | Conditional | Sources supporting the answer |
| `refusal` | Object | Conditional | Refusal details (null if answered) |
| `metadata` | Object | Always | Response context and provenance |

### Grounding Status Enum

| Status | Meaning | User Experience |
|--------|---------|-----------------|
| `FULLY_GROUNDED` | All substantive claims supported by retrieved passages | Answer displayed with citations |
| `PARTIALLY_GROUNDED` | Some claims supported; others are contextual framing | Answer displayed with grounding warning |
| `REFUSED` | Cannot produce a grounded answer | Refusal message with guidance |

> **PM DECISION:** Grounding status is categorical, not numeric. "87% confident" invites "why not 100%?" in audits. Categorical status is defensible and legible to compliance reviewers.

---

## Citation Object

When `grounding_status` is `FULLY_GROUNDED` or `PARTIALLY_GROUNDED`, the `citations` array contains:

```json
{
  "citation_id": 1,
  "source_id": "document-identifier",
  "source_title": "Human-Readable Document Title",
  "effective_date": "2024-03-15",
  "passage": "Relevant excerpt from the source document...",
  "collection": "regulatory-guidance"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `citation_id` | Integer | Always | Reference number used in answer text [1] |
| `source_id` | String | Always | Unique document identifier |
| `source_title` | String | Always | Human-readable title |
| `effective_date` | Date | Always | When the source became effective |
| `passage` | String | Always | Supporting excerpt (max 150 chars) |
| `collection` | String | Always | Corpus collection containing this source |

### Citation Rules

1. **Every substantive claim maps to a citation** — No uncited factual statements
2. **Citations use bracketed references** — Format: `[1]`, `[2]`, etc.
3. **Maximum 5 distinct sources per response** — Prevents citation proliferation
4. **Passages are excerpts, not full documents** — Users see relevant snippets

---

## Refusal Object

When `grounding_status` is `REFUSED`, the `refusal` object contains:

```json
{
  "code": "INSUFFICIENT_GROUNDING",
  "reason": "Found related content but cannot fully substantiate an answer",
  "user_guidance": "Found related content but cannot fully answer your question. The following partial information may help: [context]",
  "next_steps": [
    "Narrow your question to a specific regulation or policy",
    "Consult a compliance specialist for complex interpretations"
  ],
  "retrieval_summary": {
    "passages_found": 3,
    "passages_above_threshold": 0,
    "closest_topic": "Securities holding periods (tangential)"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `code` | Enum | Always | Refusal code from taxonomy |
| `reason` | String | Always | Brief explanation of why refusal occurred |
| `user_guidance` | String | Always | Helpful message for the user |
| `next_steps` | Array | Optional | Actionable suggestions |
| `retrieval_summary` | Object | Optional | What was found (helps user understand) |

### Refusal Codes

| Code | When It Applies |
|------|-----------------|
| `NO_ELIGIBLE_DOCS` | Query outside corpus scope |
| `INSUFFICIENT_GROUNDING` | Retrieved but can't substantiate |
| `POLICY_BLOCKED` | Role/permission restriction |
| `AMBIGUOUS_QUERY` | Insufficient specificity |
| `CONFLICTING_SOURCES` | Authoritative sources disagree |

Full definitions: [config/refusal-taxonomy.yaml](../config/refusal-taxonomy.yaml)

---

## Metadata Object

Every response includes metadata for context and provenance:

```json
{
  "corpus_release_id": "v2025.01.04",
  "sources_consulted": 3,
  "model_provider": "anthropic",
  "processing_time_ms": 1250
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `corpus_release_id` | String | Always | Version of corpus used for retrieval |
| `sources_consulted` | Integer | Always | Number of passages evaluated |
| `model_provider` | String | Always | LLM provider used (model-agnostic signal) |
| `processing_time_ms` | Integer | Optional | Response generation time |

> **PM DECISION:** `corpus_release_id` is always present. This enables point-in-time reconstruction: "What did the system know when it answered this question?"

---

## Guarantees

The CRA makes these guarantees for every response:

### What Users Can Rely On

| Guarantee | Description |
|-----------|-------------|
| **No uncited substantive claims** | Every factual statement maps to a citation |
| **Trace ID always present** | Every response can be audited |
| **Corpus version always present** | Point-in-time reconstruction is possible |
| **Refusal is explicit** | System never silently fails or guesses |
| **Grounding status is honest** | Partial grounding is flagged, not hidden |

### What Users Do NOT See

| Hidden Element | Rationale |
|----------------|-----------|
| Retrieval similarity scores | Numeric scores invite misinterpretation |
| Model confidence / logprobs | "87% confident" is not defensible |
| Internal rationale codes | These go to audit log, not users |
| Raw retrieved passages | Users see curated excerpts |
| Policy constraint details | Implementation detail, not user concern |

> **PM DECISION:** Transparency doesn't mean exposing everything. Users see what helps them trust the answer. Auditors see what helps them reconstruct the decision.

---

## Response Examples

### Fully Grounded Response

```json
{
  "trace_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2025-01-06T14:30:00Z",
  "query": "What are the communication standards for retail investors?",
  "grounding_status": "FULLY_GROUNDED",
  "answer": "Communications with retail investors must be fair, balanced, and not misleading. [1] All material facts must be disclosed, and claims about benefits must be balanced with risks. [1] Performance data must include standardized disclosures. [2]",
  "citations": [
    {
      "citation_id": 1,
      "source_id": "finra-2210-summary",
      "source_title": "FINRA Rule 2210 Communications Standards",
      "effective_date": "2023-06-01",
      "passage": "Communications must be fair and balanced, providing a sound basis for evaluating the facts.",
      "collection": "regulatory-guidance"
    },
    {
      "citation_id": 2,
      "source_id": "performance-disclosure-policy",
      "source_title": "Performance Advertising Disclosure Requirements",
      "effective_date": "2024-01-15",
      "passage": "All performance presentations must include standardized 1, 5, and 10-year returns.",
      "collection": "compliance-policies"
    }
  ],
  "refusal": null,
  "metadata": {
    "corpus_release_id": "v2025.01.04",
    "sources_consulted": 5,
    "model_provider": "anthropic"
  }
}
```

### Partially Grounded Response

```json
{
  "trace_id": "660e8400-e29b-41d4-a716-446655440001",
  "timestamp": "2025-01-06T14:35:00Z",
  "query": "How do suitability requirements apply to robo-advisors?",
  "grounding_status": "PARTIALLY_GROUNDED",
  "answer": "Suitability requirements under Reg BI apply to recommendations made through digital platforms. [1] **Note: The following context is informational framing and not directly cited:** Implementation details for algorithmic recommendations may vary by platform and are subject to evolving SEC guidance.",
  "citations": [
    {
      "citation_id": 1,
      "source_id": "reg-bi-digital-guidance",
      "source_title": "Regulation Best Interest: Digital Advice Platforms",
      "effective_date": "2024-02-01",
      "passage": "The suitability obligation applies regardless of whether a recommendation is made by a human or algorithm.",
      "collection": "regulatory-guidance"
    }
  ],
  "refusal": null,
  "metadata": {
    "corpus_release_id": "v2025.01.04",
    "sources_consulted": 4,
    "model_provider": "anthropic",
    "grounding_warning": "Some contextual framing is not directly supported by retrieved sources"
  }
}
```

### Refusal Response

```json
{
  "trace_id": "770e8400-e29b-41d4-a716-446655440002",
  "timestamp": "2025-01-06T14:40:00Z",
  "query": "What is the required holding period for restricted securities?",
  "grounding_status": "REFUSED",
  "answer": null,
  "citations": [],
  "refusal": {
    "code": "CONFLICTING_SOURCES",
    "reason": "Multiple authoritative sources provide contradictory guidance",
    "user_guidance": "Approved sources contain conflicting information on this topic. Human review is recommended before proceeding.",
    "next_steps": [
      "Consult with a compliance specialist",
      "Reference both SEC Rule 144 and internal policy memo for comparison"
    ],
    "retrieval_summary": {
      "passages_found": 4,
      "passages_above_threshold": 2,
      "conflict_description": "SEC guidance specifies 6 months; internal policy specifies 12 months"
    }
  },
  "metadata": {
    "corpus_release_id": "v2025.01.04",
    "sources_consulted": 4,
    "model_provider": "anthropic",
    "escalation_triggered": true
  }
}
```

---

## Integration Notes

### For UI Developers

- Always display `grounding_status` prominently
- Render citations as clickable references when possible
- Display `refusal.user_guidance` as the primary message on refusal
- Include `trace_id` in support/feedback flows for audit lookup

### For Downstream Systems

- Key on `grounding_status` for routing decisions
- Use `trace_id` for correlation with audit logs
- Check `refusal.code` for automated handling of specific refusal types

---

## Related Artifacts

- [trace-schema.md](trace-schema.md) — Audit-facing contract (what auditors see)
- [config/refusal-taxonomy.yaml](../config/refusal-taxonomy.yaml) — Refusal code definitions
- [config/policy-constraints.yaml](../config/policy-constraints.yaml) — Citation and response configuration
- [evaluation/scorecard.md](../evaluation/scorecard.md) — How response quality is assessed

---

*This contract defines the interface between the Compliance Retrieval Assistant and its users. Changes require governance review.*