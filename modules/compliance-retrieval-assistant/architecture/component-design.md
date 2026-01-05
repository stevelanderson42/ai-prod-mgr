# Component Design

**Internal Architecture of the Compliance Retrieval Assistant**

---

## Purpose

This document describes the internal decomposition of the Compliance Retrieval Assistant into discrete components. Each component has clear responsibilities, defined interfaces, and explicit failure modes.

> **PM DECISION:** Components are designed for auditability and testability. Each stage can be evaluated independently, and the pipeline can be traced step-by-step for any interaction.

---

## Architecture Principles

| Principle | Rationale |
|-----------|-----------|
| **Pipeline architecture** | Linear flow enables clear tracing and debugging |
| **Single responsibility** | Each component does one thing well |
| **Explicit interfaces** | Contracts between components are documented |
| **Fail-fast** | Problems surface early, not at response time |
| **Trace everything** | Every component contributes to the audit trail |
| **No hidden state** | All context is explicit in the pipeline data |

---

## Component Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Compliance Retrieval Assistant                          │
│                                                                              │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐       │
│  │   Query    │    │ Retrieval  │    │  Grounding │    │   Prompt   │       │
│  │Preprocessor│ ─▶ │   Client   │ ─▶ │  Checker   │ ─▶ │  Builder   │       │
│  └────────────┘    └────────────┘    └────────────┘    └────────────┘       │
│        │                 │                 │                 │              │
│        ▼                 ▼                 ▼                 ▼              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        Trace Writer (continuous)                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│        │                 │                 │                 │              │
│        ▼                 ▼                 ▼                 ▼              │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐       │
│  │    LLM     │    │  Refusal   │    │  Response  │    │   Output   │       │
│  │  Provider  │ ─▶ │    Gate    │ ─▶ │ Assembler  │ ─▶ │            │       │
│  └────────────┘    └────────────┘    └────────────┘    └────────────┘       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Pipeline Flow

```
Query ─▶ Preprocess ─▶ Retrieve ─▶ Ground ─▶ Build Prompt ─▶ Generate ─▶ Decide ─▶ Assemble ─▶ Respond
                                                                │
                                                     [Trace Writer throughout]
```

---

## Components

### 1. Query Preprocessor

**Location:** `src/preprocess/`

**Responsibility:** Normalize and analyze incoming queries before retrieval.

#### Inputs

| Field | Type | Source |
|-------|------|--------|
| `raw_query` | String | User input |
| `user_role` | String | Upstream identity system |
| `session_context` | Object | Optional session metadata |

#### Outputs

| Field | Type | Description |
|-------|------|-------------|
| `normalized_query` | String | Cleaned, normalized query text |
| `query_hash` | String | SHA-256 for integrity verification |
| `extracted_intent` | String | Detected query type (lookup, comparison, procedure) |
| `key_terms` | Array | Extracted terminology for lexical matching |
| `preprocessing_flags` | Array | Warnings or annotations |

#### Operations

1. **Normalize text** — Whitespace, encoding, case handling
2. **Extract key terms** — Identify regulated terminology, entity names
3. **Detect intent** — Classify query type for retrieval optimization
4. **Check for injection patterns** — Flag suspicious input structures
5. **Hash query** — Generate integrity hash for audit

#### Failure Modes

| Failure | Detection | Response |
|---------|-----------|----------|
| Query too long | Length check | Truncate with warning |
| Encoding errors | Validation | Reject with error |
| Injection pattern detected | Pattern matching | Flag for review, proceed cautiously |
| Empty query | Null check | Return AMBIGUOUS_QUERY refusal |

> **PM DECISION:** Preprocessing does NOT invoke any ML models. It uses deterministic rules and heuristics to ensure explainability at the input layer.

---

### 2. Retrieval Client

**Location:** `src/retrieval/`

**Responsibility:** Fetch relevant passages from the approved corpus using hybrid search.

#### Inputs

| Field | Type | Source |
|-------|------|--------|
| `normalized_query` | String | Query Preprocessor |
| `key_terms` | Array | Query Preprocessor |
| `user_role` | String | Pipeline context |
| `policy_constraints` | Object | config/policy-constraints.yaml |

#### Outputs

| Field | Type | Description |
|-------|------|-------------|
| `passages` | Array | Retrieved passages with metadata |
| `retrieval_metadata` | Object | Search statistics and timing |

#### Passage Object

```json
{
  "passage_id": "doc-123-chunk-4",
  "content": "The holding period for restricted securities...",
  "source_id": "sec-rule-144-summary-2024",
  "source_title": "SEC Rule 144 Summary",
  "collection": "regulatory-guidance",
  "effective_date": "2024-03-15",
  "similarity_score": 0.89,
  "term_overlap_score": 0.45
}
```

#### Operations

1. **Check access permissions** — Filter collections by user_role
2. **Execute vector search** — Semantic similarity via embeddings
3. **Execute lexical search** — BM25 or similar for term matching
4. **Merge and rank** — Combine results using hybrid_weight
5. **Apply threshold** — Filter by similarity_threshold
6. **Enforce limits** — Cap at top_k passages

#### Failure Modes

| Failure | Detection | Response |
|---------|-----------|----------|
| No passages found | Empty result | Proceed to Refusal Gate (NO_ELIGIBLE_DOCS) |
| All passages below threshold | Score check | Proceed to Refusal Gate (INSUFFICIENT_GROUNDING) |
| Index unavailable | Connection error | Return service error, log incident |
| Access denied to all collections | Permission check | Return POLICY_BLOCKED |

> **PM DECISION:** Retrieval uses hybrid search (vector + lexical) because compliance contexts require both semantic understanding and precise terminology matching. Pure vector search misses exact regulatory terms.

---

### 3. Grounding Checker

**Location:** `src/grounding/`

**Responsibility:** Validate that retrieved passages can support a complete, accurate answer.

#### Inputs

| Field | Type | Source |
|-------|------|--------|
| `passages` | Array | Retrieval Client |
| `normalized_query` | String | Query Preprocessor |
| `extracted_intent` | String | Query Preprocessor |
| `policy_constraints` | Object | config/policy-constraints.yaml |

#### Outputs

| Field | Type | Description |
|-------|------|-------------|
| `grounding_status` | Enum | FULLY_GROUNDED, PARTIALLY_GROUNDED, or REFUSED |
| `supporting_passages` | Array | Passages that support an answer |
| `grounding_coverage` | Float | Proportion of query addressable (0.0-1.0) |
| `conflict_detected` | Boolean | Whether sources contradict |
| `conflict_details` | Object | Details if conflict detected |

#### Operations

1. **Assess coverage** — Can retrieved passages address the query?
2. **Check for conflicts** — Do authoritative sources disagree?
3. **Evaluate sufficiency** — Enough support for min_supporting_passages?
4. **Determine grounding status** — Apply thresholds from policy
5. **Select supporting passages** — Identify which passages to use

#### Conflict Detection

```json
{
  "conflict_detected": true,
  "conflict_type": "contradictory_guidance",
  "conflicting_passages": [
    {"passage_id": "doc-123-chunk-4", "position": "6-month holding period"},
    {"passage_id": "doc-456-chunk-2", "position": "12-month holding period"}
  ],
  "resolution": "ESCALATE"
}
```

#### Failure Modes

| Failure | Detection | Response |
|---------|-----------|----------|
| Insufficient coverage | Coverage < threshold | Set PARTIALLY_GROUNDED or REFUSED |
| Conflicting sources | Contradiction detection | Set REFUSED with CONFLICTING_SOURCES |
| No supporting passages | Empty support set | Set REFUSED with INSUFFICIENT_GROUNDING |

> **PM DECISION:** Conflict detection is conservative. When authoritative sources disagree, we refuse and escalate rather than arbitrarily choosing one. This is the right behavior in regulated environments.

---

### 4. Prompt Builder

**Location:** `src/prompt/`

**Responsibility:** Assemble the prompt for the LLM, including instructions, context, and retrieved passages.

#### Inputs

| Field | Type | Source |
|-------|------|--------|
| `normalized_query` | String | Query Preprocessor |
| `supporting_passages` | Array | Grounding Checker |
| `grounding_status` | Enum | Grounding Checker |
| `policy_constraints` | Object | config/policy-constraints.yaml |

#### Outputs

| Field | Type | Description |
|-------|------|-------------|
| `prompt` | String | Complete prompt for LLM |
| `prompt_metadata` | Object | Token counts, structure info |

#### Prompt Structure

```
[System Instructions]
- You are a compliance assistant for regulated financial services
- Answer ONLY based on the provided sources
- Cite every factual claim using [1], [2], etc.
- If you cannot fully answer from the sources, say so explicitly
- Do not speculate or extrapolate beyond the sources
- Use professional, neutral tone
- Avoid: "I think", "probably", "might be", "guaranteed", "always", "never"

[Retrieved Context]
Source [1]: {source_title} (Effective: {effective_date})
{passage_content}

Source [2]: {source_title} (Effective: {effective_date})
{passage_content}

[User Query]
{normalized_query}

[Response Instructions]
Provide a grounded answer with inline citations. Every factual claim must reference a source.
```

#### Operations

1. **Select system instructions** — Based on query type and policy
2. **Format passages** — Structure retrieved content with citations
3. **Apply token limits** — Ensure prompt fits context window
4. **Add response instructions** — Citation requirements, tone guidance
5. **Calculate token counts** — For logging and cost tracking

#### Failure Modes

| Failure | Detection | Response |
|---------|-----------|----------|
| Prompt exceeds context window | Token count | Truncate passages, log warning |
| No passages to include | Empty array | Should not reach this stage (caught by Grounding) |

> **PM DECISION:** The prompt explicitly prohibits extrapolation. The model is constrained to retrieved content. This is enforced through instructions, then verified by the Refusal Gate.

---

### 5. LLM Provider Interface

**Location:** `src/llm/`

**Responsibility:** Abstract LLM API calls, enabling model-agnostic operation.

#### Inputs

| Field | Type | Source |
|-------|------|--------|
| `prompt` | String | Prompt Builder |
| `model_config` | Object | Runtime configuration |

#### Outputs

| Field | Type | Description |
|-------|------|-------------|
| `raw_response` | String | Model-generated text |
| `model_metadata` | Object | Provider, model ID, token usage, latency |

#### Supported Providers

| Provider | Models | Configuration Key |
|----------|--------|-------------------|
| Anthropic | Claude 3 family | `anthropic` |
| OpenAI | GPT-4 family | `openai` |
| Azure OpenAI | GPT-4 via Azure | `azure` |

#### Provider Interface

```python
class LLMProvider:
    def generate(self, prompt: str, config: dict) -> LLMResponse:
        """Generate completion from prompt."""
        pass
    
    def health_check(self) -> bool:
        """Verify provider availability."""
        pass
    
    def get_token_count(self, text: str) -> int:
        """Count tokens for the provider's tokenizer."""
        pass
```

#### Operations

1. **Select provider** — Based on configuration
2. **Execute API call** — With retry logic and timeout
3. **Capture metadata** — Token usage, latency, model version
4. **Handle errors** — Rate limits, timeouts, API failures

#### Failure Modes

| Failure | Detection | Response |
|---------|-----------|----------|
| Rate limit exceeded | API response code | Retry with backoff, or fail gracefully |
| Timeout | Request timeout | Return error, log incident |
| Provider unavailable | Connection failure | Fail with service error |
| Invalid response | Response validation | Retry once, then fail |

> **PM DECISION:** The LLM is swappable. Controls and grounding matter more than which model generates the response. This prevents vendor lock-in and supports re-certification when models change.

---

### 6. Refusal Gate

**Location:** `src/decision/`

**Responsibility:** Make the final decision on whether to return an answer, partial answer, or refusal.

#### Inputs

| Field | Type | Source |
|-------|------|--------|
| `grounding_status` | Enum | Grounding Checker |
| `raw_response` | String | LLM Provider |
| `supporting_passages` | Array | Grounding Checker |
| `conflict_detected` | Boolean | Grounding Checker |
| `policy_constraints` | Object | config/policy-constraints.yaml |
| `refusal_taxonomy` | Object | config/refusal-taxonomy.yaml |

#### Outputs

| Field | Type | Description |
|-------|------|-------------|
| `decision` | Enum | ANSWER, PARTIAL_ANSWER, REFUSE, ESCALATE |
| `refusal_code` | String | Code from taxonomy (if refusing) |
| `rationale_codes` | Array | Machine-readable decision rationale |
| `escalation_triggered` | Boolean | Whether to invoke escalation queue |
| `validated_response` | String | Response text (if answering) |

#### Decision Logic

```
IF grounding_status == REFUSED:
    IF conflict_detected:
        RETURN REFUSE with CONFLICTING_SOURCES
    ELSE IF no_passages:
        RETURN REFUSE with NO_ELIGIBLE_DOCS
    ELSE:
        RETURN REFUSE with INSUFFICIENT_GROUNDING

ELSE IF grounding_status == PARTIALLY_GROUNDED:
    IF policy.partial_grounding_allowed:
        RETURN PARTIAL_ANSWER with warnings
    ELSE:
        RETURN REFUSE with INSUFFICIENT_GROUNDING

ELSE IF grounding_status == FULLY_GROUNDED:
    Validate response against policy constraints
    IF response_valid:
        RETURN ANSWER
    ELSE:
        RETURN REFUSE with policy violation reason
```

#### Post-Generation Validation

Even with FULLY_GROUNDED status, the Refusal Gate validates:

| Check | Purpose |
|-------|---------|
| Citation presence | Every claim has a citation |
| Prohibited phrases | No "guaranteed", "always", etc. |
| Response length | Within max_response_tokens |
| Tone compliance | Professional, neutral |

#### Failure Modes

| Failure | Detection | Response |
|---------|-----------|----------|
| Response fails validation | Policy checks | Attempt regeneration once, then refuse |
| Unexpected grounding status | Enum validation | Log error, refuse conservatively |

> **PM DECISION:** The Refusal Gate is the last line of defense. Even if grounding passes, the response must meet policy constraints. When in doubt, refuse.

---

### 7. Response Assembler

**Location:** `src/response/`

**Responsibility:** Package the final response according to the response contract.

#### Inputs

| Field | Type | Source |
|-------|------|--------|
| `decision` | Enum | Refusal Gate |
| `validated_response` | String | Refusal Gate |
| `supporting_passages` | Array | Grounding Checker |
| `refusal_code` | String | Refusal Gate |
| `trace_id` | UUID | Trace Writer |
| `corpus_release_id` | String | config/corpus-registry.yaml |

#### Outputs

| Field | Type | Description |
|-------|------|-------------|
| `response` | Object | Complete response per response-contract.md |

#### Operations

1. **Build citations** — Format supporting passages as citations
2. **Assemble answer** — Response text with inline citation markers
3. **Build refusal object** — If refusing, include code and guidance
4. **Attach metadata** — trace_id, corpus_release_id, timestamps
5. **Validate contract** — Ensure response matches schema

#### Response Assembly by Decision

| Decision | Answer | Citations | Refusal |
|----------|--------|-----------|---------|
| ANSWER | Full text | Populated | null |
| PARTIAL_ANSWER | Full text + warning | Populated | null |
| REFUSE | null | Empty | Populated |
| ESCALATE | null | Empty | Populated + escalation flag |

> **PM DECISION:** The Response Assembler never modifies content — it only packages. Content decisions are made upstream by the Refusal Gate.

---

### 8. Trace Writer

**Location:** `src/logging/`

**Responsibility:** Generate and persist audit trail records throughout the pipeline.

#### Design Pattern: Continuous Tracing

Unlike other components that execute once, the Trace Writer operates **throughout** the pipeline:

```
Preprocess ──┬──▶ Retrieval ──┬──▶ Grounding ──┬──▶ ... ──┬──▶ Response
             │                │                │          │
             ▼                ▼                ▼          ▼
         [Write]          [Write]          [Write]    [Finalize]
             │                │                │          │
             └────────────────┴────────────────┴──────────┘
                                    │
                                    ▼
                            Trace Record (committed)
```

#### Operations

1. **Initialize trace** — Generate trace_id, start timestamp
2. **Accumulate events** — Collect data from each pipeline stage
3. **Finalize trace** — Complete record before response delivery
4. **Commit trace** — Write to audit log store (blocking)
5. **Generate evidence package** — If sampling criteria met

#### Trace Lifecycle

| Stage | Event | Data Captured |
|-------|-------|---------------|
| Initialize | Pipeline start | trace_id, timestamp, input fields |
| Preprocess | Query normalized | query_hash, extracted_intent, flags |
| Retrieve | Passages fetched | retrieval stats, passage_ids |
| Ground | Grounding assessed | grounding_status, coverage, conflicts |
| Generate | LLM called | model metadata, token counts |
| Decide | Decision made | outcome, refusal_code, rationale |
| Assemble | Response built | response_hash, citation_count |
| Finalize | Pipeline complete | total_time, all accumulated data |

#### Critical Guarantee: Trace Before Respond

```python
def execute_pipeline(query):
    trace = TraceWriter.initialize()
    
    try:
        # ... pipeline stages ...
        response = assemble_response(...)
        
        # CRITICAL: Commit trace BEFORE returning response
        trace.finalize()
        trace.commit()  # Blocking write
        
        return response
        
    except Exception as e:
        trace.record_error(e)
        trace.commit()  # Still commit trace on error
        raise
```

#### Failure Modes

| Failure | Detection | Response |
|---------|-----------|----------|
| Trace commit fails | Write error | Retry, then fail entire request |
| Storage unavailable | Connection error | Fail request (no silent degradation) |

> **PM DECISION:** If we cannot write the audit trail, we do not return a response. Audit integrity is non-negotiable. This may cause user-visible failures, but that's preferable to unaudited interactions.

---

## Inter-Component Contracts

### Pipeline Context Object

A shared context object flows through the pipeline, accumulating data:

```json
{
  "trace_id": "uuid",
  "timestamp": "ISO-8601",
  "corpus_release_id": "v2025.01.06",
  
  "input": { },
  "preprocessing": { },
  "retrieval": { },
  "grounding": { },
  "prompt": { },
  "generation": { },
  "decision": { },
  "response": { }
}
```

Each component:
1. Reads from upstream sections
2. Writes to its own section
3. Never modifies upstream sections

### Error Propagation

Errors are captured in the context and propagated to the Refusal Gate:

```json
{
  "errors": [
    {
      "component": "retrieval",
      "error_type": "NO_PASSAGES_FOUND",
      "message": "No passages above threshold",
      "timestamp": "ISO-8601"
    }
  ]
}
```

The Refusal Gate interprets errors and determines the appropriate refusal code.

---

## Testing Strategy

### Unit Testing (Per Component)

| Component | Test Focus |
|-----------|------------|
| Preprocessor | Normalization, term extraction, injection detection |
| Retrieval | Score merging, threshold filtering, access control |
| Grounding | Coverage calculation, conflict detection |
| Prompt Builder | Token limits, instruction formatting |
| LLM Provider | Mock responses, error handling |
| Refusal Gate | Decision logic, policy validation |
| Response Assembler | Contract compliance, schema validation |
| Trace Writer | Event accumulation, commit ordering |

### Integration Testing

- End-to-end pipeline with mock LLM
- Refusal scenarios (all 5 codes)
- Escalation triggering
- Evidence package generation

### Contract Testing

- Response matches response-contract.md schema
- Trace matches trace-schema.md schema
- Refusal codes match refusal-taxonomy.yaml

---

## Related Artifacts

- [Context Diagram](../docs/diagrams/Compliance-Retrieval-Assistant%20Context%20Diagram.PNG) — System-in-the-world view
- [Component Diagram](../docs/diagrams/Compliance-Retrieval-Assistant%20Component%20Diagram.PNG) — Visual representation of this design
- [response-contract.md](../docs/response-contract.md) — Output contract
- [trace-schema.md](../docs/trace-schema.md) — Audit contract
- [config/policy-constraints.yaml](../config/policy-constraints.yaml) — Runtime configuration

---

*This design defines the internal architecture of the Compliance Retrieval Assistant. Changes require architecture review and may impact multiple components.*