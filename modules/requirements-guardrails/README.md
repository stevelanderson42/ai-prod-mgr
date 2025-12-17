# Requirements Guardrails

## What This Module Is

The Requirements Guardrails module represents the **pre-execution control layer** of a regulated AI product system.

Its purpose is to analyze user requests *before* any model invocation occurs and determine whether they are **clear, appropriate, compliant, and eligible** to proceed.

This module exists to answer a question that many AI systems fail to ask early enough:

> *“Should this request be handled by AI at all — and if so, under what constraints?”*

---

## Why This Matters in Regulated Environments

In regulated industries, many AI failures occur **before** a model generates a response:

- unclear or underspecified requests lead to incorrect assumptions
- suitability-sensitive questions trigger unintentional advice
- out-of-scope or compliance-sensitive queries are answered too confidently
- risk is discovered *after* execution, when remediation is costly

Relying solely on prompt instructions or post-response filtering is insufficient.

This module enforces **deterministic, auditable controls upstream**, ensuring that unsafe or inappropriate requests are intercepted *before* execution paths are chosen.

---

## Key Decisions This Module Enables

This module supports decisions such as:

- Whether a request is sufficiently clear to proceed
- Whether a request triggers suitability or compliance concerns
- Which execution path or agent (if any) is permitted
- When to escalate to human review or require clarification
- When to block or redirect requests entirely

These decisions are typically owned by **Product**, **Risk**, and **Compliance**, and must be explainable to auditors and governance stakeholders.

---

## How This Module Fits Into the Overall System

The Requirements Guardrails module sits **between prioritization and execution**.

- It operates after an initiative has been approved by the **ROI Decision Engine**
- It runs *before* any LLM, tool, or data access occurs
- Its outputs directly control routing into downstream execution paths, including the **Compliance Retrieval Assistant**

By design, this module ensures that **policy enforcement precedes intelligence**.

---

## Guardrail Categories Enforced

This module applies multiple categories of guardrails at request time, including:

- **Ambiguity detection**  
  Identifies unclear or underspecified requests that require clarification before execution.

- **Suitability and advice risk detection**  
  Flags requests that may constitute personalized or regulated advice.

- **Compliance and scope checks**  
  Identifies prohibited claims, guarantees, or out-of-scope topics.

- **Routing and eligibility decisions**  
  Determines whether a request may proceed, must be redirected, escalated, clarified, or blocked.

Each guardrail produces **explicit, structured outputs** that can be logged, audited, and reasoned about downstream.

---

## Entry Artifacts (Curated)

The following artifacts represent the primary entry points for this module:

- **Guardrails Overview**  
  Defines the role of guardrails in the overall AI system and how they are enforced.  
  → `../../guardrails/Guardrails.md`

- **Heuristics & Routing Rules (v0.1)**  
  Documents the deterministic logic used for topic classification, risk detection, and action selection.  
  → `../../guardrails/heuristics_v0.1.md`

- **Responsible AI & Guardrails Connection**  
  Maps internal guardrails to external responsible AI principles.  
  → `../../guardrails/Responsible_AI_&_Guardrails_Connection.md`

- **Privacy, Security, and Data Boundaries**  
  Defines what data is intentionally excluded at this stage.  
  → `../../guardrails/Privacy_and_Security.md`

These artifacts emphasize **explainability and control**, not model cleverness.

---

## Where to Go Deeper

For additional detail and supporting material:

- `../../guardrails/` — full guardrail documentation and rationale
- Prompt Experiments — empirical exploration of guardrail patterns and failure modes
- FinServ AI Query Lifecycle — sequence diagrams showing guardrail placement
- Public Notion Portfolio — architectural context and design decisions

---

## Status

Active development and refinement.

This module is central to the system and is intentionally iterated as new failure modes and regulatory considerations are identified.
