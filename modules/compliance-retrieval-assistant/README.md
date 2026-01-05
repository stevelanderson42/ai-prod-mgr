# Compliance Retrieval Assistant

**Governance-First Retrieval for Regulated AI Workflows**

**Status:** 🟡 In Progress — Context architecture and governance scaffolding complete  
**Module:** 4 of 4 in the Regulated AI Workflow Toolkit

---

## Purpose

This module acts as the **execution layer** for AI-assisted responses in regulated environments. It delivers retrieval-augmented generation (RAG) with strict requirements for **grounding, citation, traceability, and auditability**.

> **Core insight:** In regulated industries, the question isn't "Can the model answer?" — it's "Can we defend the answer?"

---

## The Problem This Solves

Most RAG implementations fail in regulated environments not because of weak retrieval, but because of missing governance:

- **Models hallucinate confidently.** They'll cite sources that don't exist or extrapolate beyond retrieved content.
- **Audit trails are afterthoughts.** When regulators ask "Why did you say this?", there's no reconstructible answer.
- **Refusal isn't designed in.** Systems answer when they shouldn't, rather than declining gracefully.
- **Corpus versioning is ignored.** "What did the system know when?" becomes unanswerable.

Without governance at the execution layer, organizations either:
1. Deploy AI that creates compliance risk, or
2. Block AI from the workflows where it could add the most value

This module provides a **third path**: constrained execution that enables AI assistance in high-risk contexts without sacrificing trust or accountability.

> **PM DECISION:** In regulated environments, a well-reasoned refusal is more valuable than a confident but ungrounded answer. This module treats refusal as a feature, not a failure.

---

## Where It Sits in the Workflow

```
Market Intelligence    →    ROI Engine    →    Guardrails    →    [RAG Assistant]
 (surfaces opportunities)   (prioritizes)      (validates input)   (executes safely)
```

**Upstream:** Requirements Guardrails determines *whether* a request can safely proceed  
**This module:** Executes the request with grounding, citation, and audit guarantees  
**Downstream:** Users receive answers; auditors receive traces

Inputs arrive only after passing upstream controls. Outputs are either:
- **Grounded response** — Answer with citations and trace ID
- **Partial response** — Answer with grounding warning
- **Refusal** — Decline with explanation and guidance
- **Escalation** — Route to human review queue (when enabled)

A partial response indicates that some claims are grounded while others cannot be fully substantiated; unsupported portions are explicitly marked.

> **PM DECISION:** This module does not override upstream decisions. If Guardrails says proceed, we execute. If execution can't meet grounding standards, we refuse — we don't silently degrade.

---

## Architecture Overview

### Context Diagram (System-in-the-World)

![Context Diagram](./docs/diagrams/Compliance-Retrieval-Assistant%20Context%20Diagram.PNG)

The context diagram shows the CRA's position within the broader enterprise environment: upstream systems that feed it (Requirements Guardrails, Policy Store, Corpus Pipeline), downstream systems it serves (Users, Audit Log, Handoff Queue), and the governance boundaries it operates within.

---

### Component Diagram (Internal Structure)

![Component Diagram](./docs/diagrams/Compliance-Retrieval-Assistant%20Component%20Diagram.PNG)

The CRA consists of 8 internal components organized as a pipeline:

| Component | Responsibility |
|-----------|----------------|
| **Query Preprocessor** | Normalize input, extract terms, detect injection patterns |
| **Retrieval Client** | Hybrid search (vector + lexical), access control filtering |
| **Grounding Checker** | Assess coverage, detect conflicts, determine grounding status |
| **Prompt Builder** | Assemble instructions + context + retrieved passages |
| **LLM Provider** | Model-agnostic interface (Anthropic, OpenAI, Azure) |
| **Refusal Gate** | Final decision logic, post-generation validation |
| **Response Assembler** | Package response per contract, build citations |
| **Trace Writer** | Continuous audit logging throughout pipeline |

See [architecture/component-design.md](./architecture/component-design.md) for detailed specifications.

---

### Sequence Diagram (Request Lifecycle)

![Sequence Diagram](./docs/diagrams/Compliance-Retrieval-Assistant%20Sequence%20Diagram.PNG)

The sequence diagram shows how a query flows through the system:

1. **Preprocess & validate** — Normalize query, check for injection patterns
2. **Retrieve passages** — Fetch top-K from approved corpus
3. **Check grounding** — Can retrieved content support an answer?
4. **Generate (if grounded)** — LLM constrained by prompt + sources
5. **Validate & assemble** — Verify citations, check policy compliance
6. **Commit trace** — Write to audit log (blocking)
7. **Return response** — Answer + citations OR Refusal + guidance

> **Key pattern:** Trace is committed and confirmed *before* any response is returned to the user. This ensures audit integrity — no interaction exists without a record.

---

## Core Execution Principles

These principles are non-negotiable constraints, not aspirational values:

| Principle | Rationale |
|-----------|-----------|
| **Retrieval before generation** | Responses are grounded in pre-approved sources, not model knowledge |
| **Citation by default** | Every substantive claim must be traceable to a source |
| **Refusal over speculation** | If adequate grounding is unavailable, decline to answer |
| **Grounding status over confidence scores** | Numeric confidence is hard to defend; categorical status is legible |
| **Corpus versioning** | Every trace includes corpus_release_id for point-in-time reconstruction |
| **Policy as data** | Behavior changes via config files, not code deployment |
| **Trace before respond** | A trace record is committed before any user-visible response is returned |

> **PM DECISION:** These constraints exist because responses may be reviewed by regulators, auditors, or legal teams. "The model said so" is not a defensible answer.

---

## Refusal Taxonomy

The system knows when it *cannot* answer safely and communicates why. Refusal is a governed capability, not an error state.

| Code | Trigger | User Guidance |
|------|---------|---------------|
| `NO_ELIGIBLE_DOCS` | Query outside corpus scope | "This topic isn't covered in approved sources" |
| `INSUFFICIENT_GROUNDING` | Retrieved but can't substantiate | "Found related content but can't fully answer" |
| `POLICY_BLOCKED` | Role/permission restriction | "You don't have access to these materials" |
| `AMBIGUOUS_QUERY` | Insufficient specificity | "Please clarify: [specific ask]" |
| `CONFLICTING_SOURCES` | Authoritative sources disagree | "Sources conflict; human review recommended" |

Full taxonomy with escalation triggers: [config/refusal-taxonomy.yaml](./config/refusal-taxonomy.yaml)

> **PM DECISION:** Each refusal code has defined user guidance. Users should never see a generic "I can't help with that" — they should understand *why* and *what to do next*.

---

## Output Contracts

This module maintains two contracts: one for users, one for auditors.

### User-Facing Response ([docs/response-contract.md](./docs/response-contract.md))

```json
{
  "trace_id": "uuid",
  "query": "original user query",
  "grounding_status": "FULLY_GROUNDED | PARTIALLY_GROUNDED | REFUSED",
  "answer": "response text (null if refused)",
  "citations": [
    {
      "source_id": "doc-identifier",
      "source_title": "Document Title",
      "passage": "relevant excerpt"
    }
  ],
  "refusal": {
    "code": "REFUSAL_CODE",
    "user_guidance": "explanation for user"
  }
}
```

### Audit-Facing Trace ([docs/trace-schema.md](./docs/trace-schema.md))

```json
{
  "trace_id": "uuid",
  "timestamp": "ISO-8601",
  "corpus_release_id": "v2025.01.04",
  "retrieval": {
    "passages_retrieved": 5,
    "passages_above_threshold": 3,
    "collections_searched": ["compliance-policies"]
  },
  "decision": {
    "grounding_status": "FULLY_GROUNDED",
    "refusal_code": null,
    "rationale_codes": ["GROUNDED_BY_PASSAGE_1"]
  }
}
```

> **PM DECISION:** Users see what they need to trust the answer. Auditors see what they need to reconstruct the decision. These are different audiences with different needs.

---

## Regulatory Alignment

This module explicitly addresses requirements from key regulatory frameworks:

| Regulation | How It's Addressed |
|------------|-------------------|
| **FINRA 2210** | Citation requirements ensure claims are grounded; no unbalanced statements |
| **Reg BI** | Grounding checks prevent unsuitable extrapolation beyond source content |
| **SR 11-7** | Trace schema provides model risk documentation; corpus versioning enables validation |
| **17a-4** | Immutable trace logs; corpus_release_id enables point-in-time reconstruction |

*These references are conceptual anchors for product design, not legal interpretations or compliance advice.*

---

## What This Module Does NOT Do

Scope discipline is a senior PM signal. This module has clear boundaries:

- ❌ **Does not validate input risk** — That's Module 3 (Requirements Guardrails)
- ❌ **Does not prioritize opportunities** — That's Module 2 (ROI Engine)
- ❌ **Does not ingest corpus in real-time** — Corpus releases are batch-approved
- ❌ **Does not maintain conversation state** — Each request is independent
- ❌ **Does not authenticate users** — Assumes upstream RBAC
- ❌ **Does not guarantee model correctness** — It guarantees grounding and traceability
- ❌ **Does not expose confidence scores** — Grounding status is categorical, not numeric

> **PM DECISION:** Knowing what NOT to build is as important as knowing what to build. Every exclusion here is deliberate.

---

## Relationship to Other Modules

| Module | Relationship |
|--------|--------------|
| **Market Intelligence** (Module 1) | No direct dependency; different timescales |
| **ROI Decision Engine** (Module 2) | Determines which workflows justify RAG investment |
| **Requirements Guardrails** (Module 3) | Validates input before this module executes |
| **Governance Infrastructure** | Receives all trace logs; owns evidence retention |

---

## Repository Map

| Artifact / Path | Purpose |
|-----------------|---------|
| 🟦 **config/** | Policy as data — externalized, auditable, versionable |
| config/policy-constraints.yaml | Runtime constraints (citation rules, thresholds, escalation on/off) |
| config/role-permissions.yaml | Access control: who can query which corpora |
| config/corpus-registry.yaml | Approved releases, `current_release_id`, point-in-time state |
| config/refusal-taxonomy.yaml | Refusal codes, meanings, and user guidance |
| 🟦 **docs/** | Human-readable specifications and governance design |
| docs/diagrams/ | Visual architecture artifacts |
| docs/diagrams/Compliance-Retrieval-Assistant Context Diagram.PNG | System-in-the-world view — external actors and boundaries |
| docs/diagrams/Compliance-Retrieval-Assistant Component Diagram.PNG | Internal decomposition — pipeline stages and data flow *(planned)* |
| docs/response-contract.md | **User-facing contract** — grounding_status, citations, refusal shape |
| docs/trace-schema.md | **Audit-facing contract** — trace fields, retention requirements |
| docs/threat-model.md | Failure modes, attack vectors, mitigations |
| 🟦 **architecture/** | Technical design and internal structure |
| architecture/README.md | Architecture overview and ADR links |
| architecture/component-design.md | Internal decomposition — 8 components with responsibilities |
| 🟦 **corpus/** | Sample content for development and evaluation |
| corpus/sample-documents/ | Representative compliance documents |
| 🟦 **evaluation/** | Quality validation framework |
| evaluation/scorecard.md | One-page rubric: attribution, relevance, hallucination risk |
| evaluation/test-cases/ | Structured scenarios for refusal and grounding behavior |
| 🟦 **evidence/** | Audit trail artifacts and samples |
| evidence/samples/ | Example trace packages for portfolio demonstration |
| 🟦 **outputs/** | User-facing response examples |
| outputs/examples/ | Sample responses showing grounding, citations, refusals |
| 🟦 **src/** | Implementation scaffolding |
| src/preprocess/ | Query normalization, intent extraction |
| src/retrieval/ | Index client, hybrid vector + lexical search |
| src/grounding/ | Passage support validation |
| src/prompt/ | Prompt assembly with retrieved context |
| src/llm/ | Model-agnostic provider interface |
| src/decision/ | Refusal gate, grounding status selection |
| src/response/ | Response assembly per contract |
| src/logging/ | Trace writer for audit log |

---

## Success Criteria

This module is complete when:

- [x] Context diagram reflecting governance boundaries
- [x] Folder structure with clear artifact purposes
- [x] Refusal taxonomy with 5 codes and user guidance
- [x] Response contract (user-facing) defined
- [x] Trace schema (audit-facing) defined
- [ ] Threat model with mitigations
- [ ] Component design with interface contracts
- [ ] Sample corpus documents for testing
- [ ] Evaluation scorecard applied to test cases
- [ ] At least 5 sample outputs (grounded + refusals)
- [ ] Evidence package examples
- [ ] Integration contract with Requirements Guardrails

---

## Key PM Decisions Documented

| Decision | Rationale |
|----------|-----------|
| **Grounding status over confidence** | Numeric confidence invites "why not higher?" — categorical status is defensible |
| **Corpus versioning with release IDs** | Enables "what did the system know when?" for audit reconstruction |
| **Refusal taxonomy as config** | Refusal logic is policy, not code — externalized for governance |
| **Model-agnostic provider interface** | Prevents vendor lock-in; supports re-certification when models change |
| **Dual contracts (response + trace)** | Users and auditors have different needs; serve both explicitly |
| **Trace before respond** | Audit integrity requires log completion before delivery |

---

## Related Artifacts

- [Requirements Guardrails](../requirements-guardrails/) — Upstream input validation
- [ROI Decision Engine](../roi-engine/) — Upstream prioritization
- [Market Intelligence](../market-intel/) — Strategic context
- [Architecture Decisions](../../architecture/) — System-level ADRs

---

*Part of the [Regulated AI Workflow Toolkit](../../README.md) — demonstrating governance-first AI product design for financial services and other regulated industries.*