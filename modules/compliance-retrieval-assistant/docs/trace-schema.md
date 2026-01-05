# Trace Schema

**Audit-Facing Contract for the Compliance Retrieval Assistant**

---

## Purpose

This document defines the audit trail structure for every Compliance Retrieval Assistant interaction. It is the **audit-facing contract** — what compliance reviewers, regulators, and internal audit teams see.

> **PM DECISION:** Users and auditors have different needs. The [response-contract.md](response-contract.md) serves users; this schema serves auditors. Auditors need to reconstruct decisions; users need to trust answers.

---

## Core Principle: Trace Before Respond

A trace record is committed before any user-visible response is returned.

This ordering guarantee ensures:
- No response exists without an audit record
- System failures don't create gaps in the audit trail
- Regulatory inquiries can always be answered

> **PM DECISION:** This is non-negotiable. "We don't have a record of that interaction" is not an acceptable answer to a regulator.

---

## Trace Record Shape

Every CRA interaction generates a trace record with this structure:

```json
{
  "trace_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2025-01-06T14:30:00.000Z",
  "corpus_release_id": "v2025.01.06",
  
  "input": {
    "query": "What is the required holding period for restricted securities?",
    "query_hash": "sha256:a1b2c3d4...",
    "user_role": "analyst",
    "user_id_hash": "sha256:e5f6g7h8...",
    "session_id": "sess_abc123",
    "source_system": "compliance-portal"
  },
  
  "retrieval": {
    "collections_searched": ["compliance-policies", "regulatory-guidance"],
    "passages_retrieved": 10,
    "passages_above_threshold": 4,
    "top_passage_score": 0.89,
    "lowest_included_score": 0.76,
    "retrieval_time_ms": 145,
    "passage_ids": ["doc-123-chunk-4", "doc-456-chunk-2", "doc-789-chunk-1"]
  },
  
  "grounding": {
    "status": "FULLY_GROUNDED",
    "supporting_passages": 2,
    "grounding_coverage": 1.0,
    "unsupported_claims": 0,
    "conflict_detected": false
  },
  
  "decision": {
    "outcome": "ANSWER",
    "refusal_code": null,
    "rationale_codes": ["GROUNDED_BY_PASSAGE_1", "GROUNDED_BY_PASSAGE_3"],
    "escalation_triggered": false,
    "policy_constraints_applied": ["citation_required", "max_sources_5"]
  },
  
  "output": {
    "response_length_chars": 342,
    "response_hash": "sha256:i9j0k1l2...",
    "citation_count": 2,
    "sources_cited": ["sec-rule-144-summary-2024", "holding-period-policy-v2"]
  },
  
  "model": {
    "provider": "anthropic",
    "model_id": "claude-3-sonnet",
    "prompt_tokens": 1847,
    "completion_tokens": 156,
    "total_tokens": 2003,
    "generation_time_ms": 892
  },
  
  "performance": {
    "total_time_ms": 1250,
    "retrieval_time_ms": 145,
    "grounding_time_ms": 78,
    "generation_time_ms": 892,
    "logging_time_ms": 35
  },
  
  "audit_metadata": {
    "trace_version": "1.0",
    "cra_version": "0.1.0",
    "environment": "production",
    "retention_class": "standard"
  }
}
```

---

## Field Definitions

### Identification Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `trace_id` | UUID | Always | Unique identifier for this interaction |
| `timestamp` | ISO-8601 | Always | When the trace was created (millisecond precision) |
| `corpus_release_id` | String | Always | Version of corpus used — enables point-in-time reconstruction |

### Input Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `input.query` | String | Always | Original user query |
| `input.query_hash` | String | Always | SHA-256 hash (for integrity verification) |
| `input.user_role` | String | Always | Role used for access control |
| `input.user_id_hash` | String | Always | Hashed user identifier (PII protection) |
| `input.session_id` | String | Optional | Session correlation identifier |
| `input.source_system` | String | Optional | Originating system or interface |

### Retrieval Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `retrieval.collections_searched` | Array | Always | Which collections were queried |
| `retrieval.passages_retrieved` | Integer | Always | Total passages returned by retrieval |
| `retrieval.passages_above_threshold` | Integer | Always | Passages meeting similarity threshold |
| `retrieval.top_passage_score` | Float | Always | Highest similarity score |
| `retrieval.lowest_included_score` | Float | Always | Lowest score of included passages |
| `retrieval.retrieval_time_ms` | Integer | Always | Retrieval latency |
| `retrieval.passage_ids` | Array | Always | Identifiers of retrieved passages |

### Grounding Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `grounding.status` | Enum | Always | FULLY_GROUNDED, PARTIALLY_GROUNDED, or REFUSED |
| `grounding.supporting_passages` | Integer | Always | Passages used to ground the answer |
| `grounding.grounding_coverage` | Float | Always | Proportion of claims grounded (0.0-1.0) |
| `grounding.unsupported_claims` | Integer | Always | Claims without passage support |
| `grounding.conflict_detected` | Boolean | Always | Whether conflicting sources were found |

### Decision Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `decision.outcome` | Enum | Always | ANSWER, PARTIAL_ANSWER, REFUSE, ESCALATE |
| `decision.refusal_code` | String | Conditional | Code from refusal taxonomy (if refused) |
| `decision.rationale_codes` | Array | Always | Machine-readable decision rationale |
| `decision.escalation_triggered` | Boolean | Always | Whether escalation queue was invoked |
| `decision.policy_constraints_applied` | Array | Always | Which policy rules affected this response |

### Output Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `output.response_length_chars` | Integer | Always | Length of response text |
| `output.response_hash` | String | Always | SHA-256 hash of response (integrity) |
| `output.citation_count` | Integer | Always | Number of citations in response |
| `output.sources_cited` | Array | Always | Document IDs of cited sources |

### Model Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `model.provider` | String | Always | LLM provider (anthropic, openai, azure) |
| `model.model_id` | String | Always | Specific model identifier |
| `model.prompt_tokens` | Integer | Always | Tokens in prompt |
| `model.completion_tokens` | Integer | Always | Tokens in completion |
| `model.total_tokens` | Integer | Always | Total token usage |
| `model.generation_time_ms` | Integer | Always | Model inference latency |

### Performance Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `performance.total_time_ms` | Integer | Always | End-to-end latency |
| `performance.retrieval_time_ms` | Integer | Always | Retrieval stage latency |
| `performance.grounding_time_ms` | Integer | Always | Grounding check latency |
| `performance.generation_time_ms` | Integer | Always | Model generation latency |
| `performance.logging_time_ms` | Integer | Always | Trace write latency |

### Audit Metadata Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `audit_metadata.trace_version` | String | Always | Schema version for this trace |
| `audit_metadata.cra_version` | String | Always | CRA software version |
| `audit_metadata.environment` | String | Always | production, staging, development |
| `audit_metadata.retention_class` | String | Always | Retention policy applied |

---

## Rationale Codes

The `decision.rationale_codes` array provides machine-readable explanations for the decision. These enable automated audit analysis.

### Answer Rationale Codes

| Code | Meaning |
|------|---------|
| `GROUNDED_BY_PASSAGE_N` | Claim supported by passage N |
| `FULL_COVERAGE` | All claims have passage support |
| `PARTIAL_COVERAGE` | Some claims grounded, others contextual |
| `WITHIN_POLICY_BOUNDS` | Response meets all policy constraints |

### Refusal Rationale Codes

| Code | Meaning |
|------|---------|
| `NO_RELEVANT_PASSAGES` | Retrieval returned no qualifying passages |
| `BELOW_GROUNDING_THRESHOLD` | Insufficient passage support |
| `CONFLICT_DETECTED` | Authoritative sources disagree |
| `ACCESS_DENIED` | User role lacks permission |
| `QUERY_AMBIGUOUS` | Cannot determine intent |
| `PROHIBITED_CONTENT` | Request matches block pattern |

---

## Retention Requirements

Trace records are retained according to regulatory requirements and internal policy.

| Retention Class | Duration | Applies To |
|-----------------|----------|------------|
| `standard` | 7 years | Normal interactions |
| `extended` | 10 years | Interactions involving enforcement content |
| `permanent` | Indefinite | Escalations, refusals, audit-flagged |

### SEC 17a-4 Alignment

This trace schema is designed for conceptual alignment with books-and-records requirements:

| 17a-4 Requirement | How Addressed |
|-------------------|---------------|
| **Immutability** | Traces are append-only; no modification after write |
| **Completeness** | Every interaction generates a trace (trace-before-respond) |
| **Retrievability** | Indexed by trace_id, timestamp, user_role, corpus_release_id |
| **Accuracy** | Hashes enable integrity verification |
| **Accessibility** | Standard JSON format; exportable for regulatory review |

> **PM DECISION:** We don't claim legal compliance — that's for Legal and Compliance to determine. We provide the technical foundation that makes compliance achievable.

---

## Evidence Packages

For detailed audit review, traces can be expanded into full **Evidence Packages**. These are created:
- Always for refusals and escalations
- Always when conflicts are detected
- On a 10% random sample of normal interactions
- On demand for regulatory inquiries

### Evidence Package Structure

```
evidence-package-{trace_id}/
├── trace.json              # Complete trace record
├── query.txt               # Original user query (plain text)
├── response.json           # Full response as delivered to user
├── retrieved/              # All retrieved passages
│   ├── passage-001.json    # Passage content + metadata
│   ├── passage-002.json
│   └── ...
├── config-snapshot/        # Policy config at query time
│   ├── policy-constraints.yaml
│   ├── role-permissions.yaml
│   └── corpus-registry.yaml
└── manifest.json           # Package metadata and checksums
```

### Evidence Package Manifest

```json
{
  "trace_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2025-01-06T14:30:01.000Z",
  "package_version": "1.0",
  "trigger": "refusal",
  "files": [
    {"name": "trace.json", "sha256": "..."},
    {"name": "query.txt", "sha256": "..."},
    {"name": "response.json", "sha256": "..."}
  ],
  "total_size_bytes": 15234,
  "retention_class": "permanent"
}
```

---

## Trace Examples

### Successful Answer Trace

```json
{
  "trace_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2025-01-06T14:30:00.000Z",
  "corpus_release_id": "v2025.01.06",
  "input": {
    "query": "What are the FINRA 2210 requirements for retail communications?",
    "user_role": "analyst"
  },
  "retrieval": {
    "collections_searched": ["regulatory-guidance"],
    "passages_retrieved": 8,
    "passages_above_threshold": 3,
    "top_passage_score": 0.92
  },
  "grounding": {
    "status": "FULLY_GROUNDED",
    "supporting_passages": 2,
    "grounding_coverage": 1.0,
    "conflict_detected": false
  },
  "decision": {
    "outcome": "ANSWER",
    "refusal_code": null,
    "rationale_codes": ["GROUNDED_BY_PASSAGE_1", "GROUNDED_BY_PASSAGE_2", "FULL_COVERAGE"],
    "escalation_triggered": false
  },
  "output": {
    "response_length_chars": 428,
    "citation_count": 2
  }
}
```

### Refusal Trace (Conflicting Sources)

```json
{
  "trace_id": "660e8400-e29b-41d4-a716-446655440001",
  "timestamp": "2025-01-06T14:35:00.000Z",
  "corpus_release_id": "v2025.01.06",
  "input": {
    "query": "What is the required holding period for restricted securities?",
    "user_role": "analyst"
  },
  "retrieval": {
    "collections_searched": ["regulatory-guidance", "compliance-policies"],
    "passages_retrieved": 6,
    "passages_above_threshold": 4,
    "top_passage_score": 0.88
  },
  "grounding": {
    "status": "REFUSED",
    "supporting_passages": 0,
    "grounding_coverage": 0.0,
    "conflict_detected": true
  },
  "decision": {
    "outcome": "REFUSE",
    "refusal_code": "CONFLICTING_SOURCES",
    "rationale_codes": ["CONFLICT_DETECTED", "SEC_VS_INTERNAL_POLICY"],
    "escalation_triggered": true
  },
  "output": {
    "response_length_chars": 215,
    "citation_count": 0
  },
  "audit_metadata": {
    "retention_class": "permanent"
  }
}
```

### Access Denied Trace

```json
{
  "trace_id": "770e8400-e29b-41d4-a716-446655440002",
  "timestamp": "2025-01-06T14:40:00.000Z",
  "corpus_release_id": "v2025.01.06",
  "input": {
    "query": "What were the findings from the 2024 internal investigation?",
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
  "output": {
    "response_length_chars": 142,
    "citation_count": 0
  }
}
```

---

## Query Capabilities

Auditors can query the trace store using these indexed fields:

| Query Type | Indexed Fields |
|------------|----------------|
| **By interaction** | trace_id |
| **By time range** | timestamp |
| **By user** | input.user_id_hash, input.user_role |
| **By corpus version** | corpus_release_id |
| **By outcome** | decision.outcome, decision.refusal_code |
| **By escalation** | decision.escalation_triggered |
| **By source** | output.sources_cited |

### Example Audit Queries

- "Show all refusals in the past 30 days"
- "Find all interactions using corpus release v2025.01.06"
- "List escalations triggered by CONFLICTING_SOURCES"
- "Show all queries from external_auditor role"

---

## Integration Notes

### For Audit Systems

- Ingest traces via streaming API or batch export
- Index on trace_id (primary), timestamp (range), decision.outcome (filter)
- Store evidence packages in immutable object storage
- Implement integrity verification using hashes

### For Monitoring Systems

- Alert on escalation_triggered = true
- Track refusal rates by refusal_code
- Monitor retrieval.passages_above_threshold trends
- Dashboard grounding.grounding_coverage distribution

---

## Related Artifacts

- [response-contract.md](response-contract.md) — User-facing contract (what users see)
- [config/refusal-taxonomy.yaml](../config/refusal-taxonomy.yaml) — Refusal code definitions
- [config/policy-constraints.yaml](../config/policy-constraints.yaml) — Logging configuration
- [evidence/README.md](../evidence/README.md) — Evidence package storage

---

*This schema defines the audit interface for the Compliance Retrieval Assistant. Changes require governance review and may require audit system updates.*