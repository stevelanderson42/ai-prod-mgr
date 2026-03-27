# Regulated AI Workflow Toolkit

This repository presents a **six-module AI system for building and operating LLM applications in regulated environments** — from strategic prioritization through governed retrieval and agentic orchestration.

Rather than showcasing isolated AI demos, this toolkit demonstrates how AI can be operated as a **governed product capability** that earns trust from Legal, Risk, Compliance, Engineering, and Executive stakeholders.

---

## What This Is

This is not a collection of AI demos.

It is a system-level portfolio demonstrating how LLM-based products are designed, governed, and operated across the full lifecycle:

- Strategic prioritization
- Pre-invocation risk control
- Governed retrieval
- Evaluation and measurement
- Agentic workflow orchestration

Each module represents a capability. Together, they form a production-oriented AI system.

---

## Why This Exists

In real organizations, AI initiatives must answer:

- How do we prioritize AI opportunities responsibly?
- How do we prevent unsafe or non-compliant usage before it happens?
- How do we ensure outputs are auditable and defensible?
- How do we orchestrate multi-step workflows without losing control or traceability?

This toolkit was created to show how those questions can be addressed **by design**, not retroactively.

---

## What This Demonstrates About My Approach

- **Systems over features** — AI as an end-to-end workflow, not a chatbot
- **Policy before models** — guardrails and governance first, generation second
- **Deterministic controls before probabilistic reasoning**
- **Auditability as a first-class requirement**
- **Explicit tradeoffs**, not hidden assumptions
- **Cross-module architecture** — modules that consume each other as tools, not standalone demos

The goal is not clever prompting.
The goal is **reliable, repeatable, defensible AI behavior inside real organizations**.

---

## The Six Modules

Together, these six modules represent the core capabilities required for responsible AI enablement in regulated environments — from strategic prioritization through agentic orchestration.

### 1. Market Intelligence Monitor
Tracks competitor AI releases, regulatory signals, and industry trends to inform **strategic prioritization** and opportunity discovery.

---

### 2. ROI Decision Engine
A structured, risk-aware scoring framework used to prioritize AI initiatives based on **business value, feasibility, and regulatory complexity**.

---

### 3. Requirements Guardrails
Identifies ambiguity, suitability risk, and compliance concerns in user requests **before model invocation**, enabling safe routing, escalation, and policy enforcement.

---

### 4. Compliance Retrieval Assistant
A retrieval-augmented generation (RAG) assistant designed for high-risk workflows requiring **citation, traceability, grounding, and audit-ready responses**.

---

### 5. RAG Knowledge Pilot | *Live: rag-knowledge-pilot.streamlit.app*
A production-deployed RAG system achieving **90.9% grounded answer rate** and **100% refusal correctness** across 15 domain-realistic test queries. Incorporates an agentic reflection loop, structured refusal logic, grounding validation, and audit logging designed to meet SEC 17a-4 traceability requirements.

**Value to organizations:**
Demonstrates how retrieval-augmented AI can be evaluated, measured, and governed in compliance-sensitive environments. Consumed as a retrieval tool by Module 6.

---

### 6. AI Case Triage Workflow (Agentic Orchestration) | *Live: ai-case-triage-workflow.streamlit.app*
A LangGraph-orchestrated six-node agentic workflow that classifies operational cases, extracts entities, retrieves live compliance policy from the Module 5 RAG corpus, scores priority, drafts internal routing notes, and drives structured routing decisions — all with a full execution trace.

**Value to organizations:**
Demonstrates how bounded agentic workflows can operate safely in regulated environments — with deterministic control logic, live policy retrieval, and auditability at every step.

---

## How the Modules Work Together

Individually, each module delivers standalone value.
Together, they form a **governance-aligned AI delivery system**:

**Market Intelligence** identifies opportunities →
**ROI Decision Engine** prioritizes responsibly →
**Requirements Guardrails** ensures safe execution →
**Compliance Retrieval Assistant** delivers auditable outputs →
**RAG Knowledge Pilot** provides the governed retrieval layer →
**AI Case Triage Workflow** orchestrates the full pipeline agentically

Modules 5 and 6 have a direct architectural dependency: Module 6 consumes Module 5's retrieval layer as a live tool within the orchestration workflow.

This creates a true system — not a collection of demos.

---

## How to Navigate This Repository

- Start with this README for the system-level narrative
- Each module folder contains a README describing its purpose, scope, and artifacts
- Implementation artifacts (prompts, schemas, code, live demos) are included to support design decisions

---

## Current Status

| Module | Status |
|---|---|
| Market Intelligence Monitor | Design complete |
| ROI Decision Engine | Design complete |
| Requirements Guardrails | Implemented |
| Compliance Retrieval Assistant | Implemented |
| RAG Knowledge Pilot | **Live deployed** — rag-knowledge-pilot.streamlit.app |
| AI Case Triage Workflow | **Live deployed** — ai-case-triage-workflow.streamlit.app |

---

## How This Is Intended to Be Used

This repository is designed to support:
- Portfolio review conversations
- Interview walkthroughs
- Architecture and product design discussions
- Cross-functional alignment scenarios

It reflects how I think about building AI products that can survive contact with **real users, real regulators, and real organizations**.