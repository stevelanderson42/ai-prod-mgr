# Threat Model

**Failure Modes, Attack Vectors, and Mitigations for the Compliance Retrieval Assistant**

---

## Purpose

This document identifies what can go wrong with the Compliance Retrieval Assistant and how those risks are mitigated. It serves three audiences:

- **Security reviewers** evaluating the system's risk posture
- **Compliance teams** assessing regulatory exposure
- **Engineering teams** implementing defensive controls

> **PM DECISION:** A threat model is a governance artifact, not just a security exercise. In regulated environments, understanding failure modes is as important as building features.

---

## Threat Categories

### Overview

| Category | Primary Risk | Key Mitigation |
|----------|--------------|----------------|
| **Retrieval Failures** | Incorrect or missing information | Grounding validation, refusal taxonomy |
| **Grounding Failures** | Hallucinated or unsubstantiated claims | Citation requirements, grounding checker |
| **Policy Bypass** | Unauthorized access or behavior | RBAC, input validation, policy-as-data |
| **Audit Trail Compromise** | Inability to reconstruct decisions | Trace-before-respond, immutable logging |
| **Model Risks** | Unpredictable or changing behavior | Model-agnostic interface, evaluation |
| **Operational Failures** | Service disruption or degradation | Graceful degradation, monitoring |

---

## 1. Retrieval Failures

Risks related to the system's ability to find relevant, accurate information.

### 1.1 Irrelevant Passages Retrieved

| Attribute | Description |
|-----------|-------------|
| **Threat** | Vector search returns semantically similar but contextually irrelevant passages |
| **Impact** | Answers grounded in wrong content; user receives misleading information |
| **Likelihood** | Medium — common in RAG systems |
| **Detection** | Low grounding coverage scores; user feedback |

**Mitigations:**
- Hybrid search (vector + lexical) with term overlap requirements
- Similarity threshold filtering (policy-constraints.yaml)
- Grounding checker validates passage relevance
- Refusal when coverage is insufficient

---

### 1.2 Stale Corpus Content

| Attribute | Description |
|-----------|-------------|
| **Threat** | Corpus contains outdated policies or superseded regulations |
| **Impact** | Users receive guidance that is no longer accurate or compliant |
| **Likelihood** | Medium — regulatory content changes frequently |
| **Detection** | Corpus audit; user reports; regulatory monitoring |

**Mitigations:**
- Corpus versioning with release IDs (corpus-registry.yaml)
- Document metadata includes effective_date and supersedes fields
- Configurable cutoff_date to exclude old content
- Corpus refresh cadence defined per collection

---

### 1.3 Coverage Gaps

| Attribute | Description |
|-----------|-------------|
| **Threat** | Valid user questions fall outside corpus scope |
| **Impact** | System refuses legitimate requests; user frustration |
| **Likelihood** | High — no corpus covers everything |
| **Detection** | NO_ELIGIBLE_DOCS refusal rate monitoring |

**Mitigations:**
- Refusal with clear guidance (not silent failure)
- Refusal analytics to identify coverage gaps
- User guidance suggests alternatives (SME consultation)
- Corpus gap analysis as operational process

---

### 1.4 Retrieval Index Corruption

| Attribute | Description |
|-----------|-------------|
| **Threat** | Vector index becomes corrupted or inconsistent with source documents |
| **Impact** | Retrieval returns wrong passages or fails entirely |
| **Likelihood** | Low — but high impact |
| **Detection** | Index health checks; retrieval quality monitoring |

**Mitigations:**
- Index rebuild capability from source documents
- Corpus pipeline validation before publish
- Rollback to previous release if corruption detected
- Regular index integrity verification

---

## 2. Grounding Failures

Risks related to the system's ability to produce accurate, substantiated answers.

### 2.1 Hallucinated Content

| Attribute | Description |
|-----------|-------------|
| **Threat** | LLM generates content not present in retrieved passages |
| **Impact** | User receives fabricated information with false confidence |
| **Likelihood** | Medium — inherent LLM behavior |
| **Detection** | Citation validation; grounding checker; evaluation |

**Mitigations:**
- Strict citation requirements in prompt instructions
- Post-generation validation in Refusal Gate
- Grounding checker validates claims against passages
- Prohibited phrases list (no "guaranteed", "always")
- Partial grounding warnings when coverage incomplete

---

### 2.2 Citation Fabrication

| Attribute | Description |
|-----------|-------------|
| **Threat** | LLM creates citations to sources that weren't retrieved or don't exist |
| **Impact** | User cannot verify claims; audit trail is misleading |
| **Likelihood** | Low-Medium — depends on prompt engineering |
| **Detection** | Citation validation against retrieved passage list |

**Mitigations:**
- Response Assembler validates all citations reference actual passages
- Citation IDs are system-generated, not model-generated
- Passages are formatted with explicit citation markers in prompt
- Post-generation citation verification

---

### 2.3 Over-Extrapolation

| Attribute | Description |
|-----------|-------------|
| **Threat** | Model draws conclusions beyond what sources actually state |
| **Impact** | Users receive inferences presented as facts |
| **Likelihood** | Medium — common LLM behavior |
| **Detection** | Grounding coverage analysis; evaluation scorecard |

**Mitigations:**
- Prompt instructions prohibit extrapolation
- extrapolation_limit setting in policy-constraints.yaml
- Partial grounding status flags unsupported content
- Grounding checker evaluates claim-to-passage alignment

---

### 2.4 Conflicting Source Mishandling

| Attribute | Description |
|-----------|-------------|
| **Threat** | System arbitrarily chooses between contradictory authoritative sources |
| **Impact** | User receives one-sided guidance; compliance risk |
| **Likelihood** | Medium — regulatory content often has tensions |
| **Detection** | Conflict detection in Grounding Checker |

**Mitigations:**
- Explicit conflict detection logic
- CONFLICTING_SOURCES refusal code
- Automatic escalation when conflicts detected
- User guidance recommends human review
- Both conflicting sources logged in trace

---

## 3. Policy Bypass

Risks related to circumventing access controls or behavioral constraints.

### 3.1 Prompt Injection

| Attribute | Description |
|-----------|-------------|
| **Threat** | Malicious query manipulates LLM to ignore instructions |
| **Impact** | System produces ungrounded, inappropriate, or policy-violating output |
| **Likelihood** | Medium — well-known attack vector |
| **Detection** | Pattern matching in Preprocessor; output validation |

**Mitigations:**
- Query Preprocessor flags suspicious patterns
- Input sanitization and normalization
- Upstream Requirements Guardrails (Module 3)
- Post-generation validation in Refusal Gate
- Response validation against policy constraints

---

### 3.2 Role Spoofing

| Attribute | Description |
|-----------|-------------|
| **Threat** | User claims a role they don't have to access restricted content |
| **Impact** | Unauthorized access to sensitive corpus collections |
| **Likelihood** | Low — depends on upstream identity integration |
| **Detection** | Access audit logs; anomaly detection |

**Mitigations:**
- Role claims come from upstream identity system (not user input)
- CRA does not manage authentication
- All access decisions logged with user_role
- POLICY_BLOCKED refusal with generic message (no information leakage)
- Access denied logs for security review

---

### 3.3 Configuration Tampering

| Attribute | Description |
|-----------|-------------|
| **Threat** | Unauthorized modification of policy-constraints.yaml or other config |
| **Impact** | Policy controls bypassed; system behavior altered |
| **Likelihood** | Low — requires system access |
| **Detection** | Config change logging; version control |

**Mitigations:**
- Config files in version control with change tracking
- Config changes require governance approval
- Config snapshot included in evidence packages
- Runtime config hash for integrity verification

---

### 3.4 Collection Access Escalation

| Attribute | Description |
|-----------|-------------|
| **Threat** | User queries indirectly surface content from restricted collections |
| **Impact** | Information leakage from privileged content |
| **Likelihood** | Low — but high impact for sensitive content |
| **Detection** | Access pattern analysis; citation source tracking |

**Mitigations:**
- Collection filtering applied before retrieval
- Citations only from accessible collections
- Restricted collections excluded from search scope
- reveal_blocked_resource: false prevents information leakage

---

## 4. Audit Trail Compromise

Risks related to the integrity and completeness of audit records.

### 4.1 Missing Traces

| Attribute | Description |
|-----------|-------------|
| **Threat** | Interactions occur without corresponding audit records |
| **Impact** | Cannot demonstrate compliance; regulatory exposure |
| **Likelihood** | Low — but catastrophic impact |
| **Detection** | Trace count vs. response count reconciliation |

**Mitigations:**
- **Trace-before-respond guarantee** (non-negotiable)
- Trace commit is blocking; response waits for confirmation
- If trace fails, request fails (no silent degradation)
- Trace Writer operates throughout pipeline, not just at end

---

### 4.2 Trace Tampering

| Attribute | Description |
|-----------|-------------|
| **Threat** | Audit records modified after creation |
| **Impact** | Audit integrity compromised; cannot trust historical records |
| **Likelihood** | Low — requires privileged access |
| **Detection** | Hash verification; immutability checks |

**Mitigations:**
- Append-only trace storage
- Integrity hashes (query_hash, response_hash)
- Evidence package checksums in manifest
- Immutable object storage for evidence packages
- Retention policy prevents deletion

---

### 4.3 Incomplete Evidence

| Attribute | Description |
|-----------|-------------|
| **Threat** | Trace records lack sufficient detail to reconstruct decisions |
| **Impact** | Cannot explain why system behaved as it did |
| **Likelihood** | Medium — depends on schema completeness |
| **Detection** | Schema validation; audit dry runs |

**Mitigations:**
- Comprehensive trace schema with required fields
- Rationale codes provide machine-readable explanation
- Evidence packages preserve full context
- corpus_release_id enables point-in-time reconstruction
- Passage IDs enable retrieval reconstruction

---

### 4.4 Storage Failures

| Attribute | Description |
|-----------|-------------|
| **Threat** | Audit log store unavailable or loses data |
| **Impact** | Audit gap; potential regulatory violation |
| **Likelihood** | Low — depends on infrastructure |
| **Detection** | Storage health monitoring; write confirmations |

**Mitigations:**
- Trace commit confirmation required before response
- Storage redundancy and backup
- Incident alerting on storage failures
- Request fails if trace cannot be committed

---

## 5. Model Risks

Risks related to LLM behavior and lifecycle.

### 5.1 Model Drift

| Attribute | Description |
|-----------|-------------|
| **Threat** | Model behavior changes over time (updates, fine-tuning, or natural drift) |
| **Impact** | Previously acceptable responses become problematic |
| **Likelihood** | Medium — models are updated regularly |
| **Detection** | Evaluation scorecard; output quality monitoring |

**Mitigations:**
- Model version tracked in trace (model.model_id)
- Evaluation scorecard for ongoing quality assessment
- Re-evaluation triggered on model updates
- model_provider abstraction enables comparison testing

---

### 5.2 Vendor Lock-in

| Attribute | Description |
|-----------|-------------|
| **Threat** | Dependency on single LLM provider limits flexibility |
| **Impact** | Cannot respond to pricing changes, outages, or capability shifts |
| **Likelihood** | High — if not architected for flexibility |
| **Detection** | Vendor dependency analysis |

**Mitigations:**
- Model-agnostic LLM Provider Interface
- Standardized prompt format across providers
- Provider switching without code changes
- Multi-provider testing capability

---

### 5.3 Model Unavailability

| Attribute | Description |
|-----------|-------------|
| **Threat** | LLM provider experiences outage or rate limiting |
| **Impact** | Service disruption; users cannot get answers |
| **Likelihood** | Medium — external dependency |
| **Detection** | Health checks; error rate monitoring |

**Mitigations:**
- Retry logic with exponential backoff
- Graceful degradation (refuse rather than fail silently)
- Provider health check before request processing
- Monitoring and alerting on error rates

---

### 5.4 Adversarial Model Outputs

| Attribute | Description |
|-----------|-------------|
| **Threat** | Model produces harmful, biased, or inappropriate content |
| **Impact** | Reputational damage; compliance violation; user harm |
| **Likelihood** | Low — but high impact |
| **Detection** | Output validation; user reports |

**Mitigations:**
- Post-generation validation in Refusal Gate
- Prohibited phrases list
- Tone compliance checking
- Grounding requirement constrains output scope
- Upstream guardrails filter inappropriate requests

---

## 6. Operational Failures

Risks related to system availability and performance.

### 6.1 Service Degradation

| Attribute | Description |
|-----------|-------------|
| **Threat** | System becomes slow or partially unavailable |
| **Impact** | Poor user experience; potential data inconsistency |
| **Likelihood** | Medium — depends on infrastructure |
| **Detection** | Latency monitoring; error rate tracking |

**Mitigations:**
- Request timeout limits (policy-constraints.yaml)
- Rate limiting per user
- Performance metrics in trace
- Graceful degradation (refuse rather than hang)

---

### 6.2 Resource Exhaustion

| Attribute | Description |
|-----------|-------------|
| **Threat** | System runs out of memory, connections, or compute |
| **Impact** | Service outage or cascading failures |
| **Likelihood** | Low — with proper capacity planning |
| **Detection** | Resource monitoring; capacity alerts |

**Mitigations:**
- Rate limiting (rate_limit_rpm in policy)
- Max concurrent requests per user
- Token limits on prompts and responses
- Request queue management

---

## Risk Matrix

| Threat | Likelihood | Impact | Risk Level | Primary Mitigation |
|--------|------------|--------|------------|-------------------|
| Irrelevant passages | Medium | Medium | **Medium** | Hybrid search + grounding validation |
| Stale corpus | Medium | High | **High** | Corpus versioning + refresh cadence |
| Coverage gaps | High | Low | **Medium** | Refusal with guidance |
| Hallucinated content | Medium | High | **High** | Citation requirements + validation |
| Citation fabrication | Low | High | **Medium** | Citation verification |
| Over-extrapolation | Medium | Medium | **Medium** | Extrapolation limits + grounding |
| Conflicting sources | Medium | High | **High** | Conflict detection + escalation |
| Prompt injection | Medium | High | **High** | Input sanitization + output validation |
| Role spoofing | Low | High | **Medium** | Upstream identity + access logging |
| Missing traces | Low | Critical | **High** | Trace-before-respond guarantee |
| Trace tampering | Low | Critical | **Medium** | Immutable storage + hashing |
| Model drift | Medium | Medium | **Medium** | Version tracking + evaluation |
| Model unavailability | Medium | Medium | **Medium** | Retry logic + graceful degradation |

---

## Mitigations by Component

| Component | Threats Addressed |
|-----------|-------------------|
| **Query Preprocessor** | Prompt injection, input validation |
| **Retrieval Client** | Role spoofing, collection access escalation |
| **Grounding Checker** | Irrelevant passages, conflicting sources, coverage gaps |
| **Prompt Builder** | Over-extrapolation (via instructions) |
| **LLM Provider** | Vendor lock-in, model unavailability |
| **Refusal Gate** | Hallucination, citation fabrication, policy bypass |
| **Response Assembler** | Citation verification |
| **Trace Writer** | Missing traces, trace tampering, incomplete evidence |
| **config/*.yaml** | Configuration tampering (via version control) |

---

## Monitoring & Alerting

### Key Metrics to Monitor

| Metric | Alert Threshold | Threat Indicated |
|--------|-----------------|------------------|
| Refusal rate | >20% sustained | Coverage gaps or system issues |
| CONFLICTING_SOURCES rate | Any increase | Corpus consistency issues |
| Grounding coverage avg | <0.7 sustained | Retrieval quality degradation |
| Trace commit failures | Any | Audit integrity risk |
| LLM error rate | >5% | Provider issues |
| Latency P95 | >5s | Performance degradation |

### Incident Response

1. **Detection** — Monitoring alert or user report
2. **Assessment** — Determine threat category and scope
3. **Containment** — If necessary, restrict access or disable feature
4. **Investigation** — Use trace records to reconstruct events
5. **Remediation** — Address root cause
6. **Documentation** — Update threat model if new pattern identified

---

## Review Cadence

This threat model should be reviewed:

- **Quarterly** — Routine review against new threats
- **On model change** — When LLM provider or version changes
- **On corpus change** — When significant corpus updates occur
- **On incident** — After any security or compliance incident
- **On architecture change** — When components are modified

---

## Related Artifacts

- [component-design.md](../architecture/component-design.md) — Where mitigations are implemented
- [config/policy-constraints.yaml](../config/policy-constraints.yaml) — Configurable controls
- [config/refusal-taxonomy.yaml](../config/refusal-taxonomy.yaml) — Refusal handling
- [trace-schema.md](trace-schema.md) — Audit trail structure
- [evaluation/scorecard.md](../evaluation/scorecard.md) — Quality monitoring

---

*This threat model is a living document. It should evolve as the system matures and new threats are identified.*