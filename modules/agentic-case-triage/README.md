# Module 6 — AI Case Triage Workflow (Agentic Orchestration)

> **10-Second Summary:**
> Module 6 orchestrates multi-step AI triage workflows — classifying, enriching,
> retrieving policy, and routing decisions with a full execution trace — demonstrating
> how governed agentic systems operate in regulated environments.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-case-triage-workflow.streamlit.app)

---

## What This Module Does

This module simulates how a regulated financial services company triages operational
cases (complaints, disputes, incidents) using a bounded, auditable AI workflow.

A user submits a case in plain text. The system runs it through a six-node LangGraph
state machine — classifying the issue, extracting key entities, retrieving relevant
policy, scoring priority, drafting an internal routing note, and producing a final
routing decision.

Every step is logged. Every decision is traceable. Nothing is a black box.

---

## Why This Matters (Portfolio Context)

Most AI demos show a chatbot that answers questions.

This module shows something different:

- A **multi-step AI workflow** with explicit state management
- **Tool-using orchestration** via LangGraph nodes
- **Policy retrieval** consumed from the Module 5 RAG layer as a workflow tool
- **Execution trace** exposing every node's input, output, and rationale
- **Routing logic** that produces a structured, actionable output

> Module 6 consumes Module 5's retrieval layer as a tool within an orchestrated
> workflow. This is not a standalone demo — it is an architecture.

---

## Regulatory Anchors

Case scenarios are designed around real FinServ operational triggers:

| Trigger | Regulatory Reference |
|---|---|
| Suitability complaint | Reg BI / FINRA Rule 2111 |
| Communication dispute | FINRA Rule 2210 |
| Unauthorized transaction | KYC / AML workflow |
| Disclosure failure | SEC / Reg BI |
| Escalation threshold | SR 11-7 model risk alignment |

---

## System Architecture

```
User Input (plain text case)
        ↓
┌─────────────────────────────┐
│   LangGraph State Machine   │
│                             │
│  Node 1: classify_issue     │  → issue type, risk category
│  Node 2: extract_entities   │  → customer, product, dates, facts
│  Node 3: retrieve_policy    │  → policy snippets (Module 5 RAG layer)
│  Node 4: score_priority     │  → urgency score + rationale
│  Node 5: draft_internal_note│  → structured routing summary
│  Node 6: route_decision     │  → final routing + recommended action
└─────────────────────────────┘
        ↓
Structured Output + Full Execution Trace
```

**Shared state flows through every node.** Each node reads what it needs,
adds what it produces. Nothing is lost between steps.

---

## Execution Trace (Audit by Design)

Every node appends to a running trace log:

```
Node 1 — classify_issue
  Input:  "Customer states advisor recommended unsuitable product..."
  Output: category=SUITABILITY_COMPLAINT, risk_level=HIGH, reg_trigger=Reg_BI

Node 2 — extract_entities
  Input:  [raw case text]
  Output: customer_id=implied, product=mutual_fund, advisor_id=implied, date=recent

Node 3 — retrieve_policy
  Input:  category=SUITABILITY_COMPLAINT
  Output: FINRA Rule 2111 snippet, Reg BI obligation summary

...and so on through Node 6.
```

This trace is displayed in the Streamlit UI alongside the final output.
It proves the system is transparent, auditable, and governable — not just functional.

---

## Demo Scenarios (Synthetic)

Five representative cases designed to exercise different triage paths:

| # | Scenario | Expected Path |
|---|---|---|
| 1 | Unauthorized transaction dispute | fraud → escalation |
| 2 | Suitability complaint on product recommendation | Reg BI → compliance review |
| 3 | Communication/disclosure complaint | FINRA 2210 → documentation review |
| 4 | Account access / fraud report | security → immediate escalation |
| 5 | Fee dispute with escalation flag | ops → supervisor review |

---

## Tech Stack

| Component | Technology |
|---|---|
| Orchestration | LangGraph |
| LLM | OpenAI GPT-4o (via LangChain) |
| Policy Retrieval | Module 5 RAG layer (ChromaDB) |
| UI | Streamlit |
| State Management | LangGraph TypedDict state |
| Audit Logging | Execution trace (per-node JSON) |

---

## Portfolio Connection

| Module | Role in System |
|---|---|
| Module 3 — Requirements Guardrails | Pre-invocation risk control |
| Module 4 — Compliance RAG | Governed execution layer |
| Module 5 — RAG Knowledge Pilot | Retrieval layer consumed by Module 6 |
| **Module 6 — AI Case Triage Workflow (Agentic Orchestration)** | **Agentic orchestration + runtime trace** |

---

## Status

✅ Live Demo: https://ai-case-triage-workflow.streamlit.app

---

---
---

# State Schema (Python)
# File: state.py

```python
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END


# ─────────────────────────────────────────────
# SHARED STATE OBJECT
# Flows through every node in the graph.
# Each node reads what it needs, adds what it produces.
# ─────────────────────────────────────────────

class CaseState(TypedDict):

    # ── Input ──────────────────────────────────
    raw_input: str                    # Original plain-text case submission

    # ── Node 1: classify_issue ─────────────────
    issue_category: Optional[str]     # e.g. SUITABILITY_COMPLAINT, FRAUD, FEE_DISPUTE
    risk_level: Optional[str]         # HIGH / MEDIUM / LOW
    regulatory_trigger: Optional[str] # e.g. Reg_BI, FINRA_2210, KYC_AML

    # ── Node 2: extract_entities ───────────────
    entities: Optional[dict]          # customer_id, product, advisor, date, key_facts

    # ── Node 3: retrieve_policy ────────────────
    policy_snippets: Optional[list]   # Retrieved chunks from Module 5 RAG layer

    # ── Node 4: score_priority ─────────────────
    priority_score: Optional[int]     # 1 (low) → 5 (critical)
    priority_rationale: Optional[str] # Plain-language explanation of score

    # ── Node 5: draft_internal_note ────────────
    internal_note: Optional[str]      # Structured summary for routing team

    # ── Node 6: route_decision ─────────────────
    routing_destination: Optional[str]    # e.g. COMPLIANCE_REVIEW, FRAUD_OPS, SUPERVISOR
    recommended_action: Optional[str]     # What the receiving team should do first

    # ── Execution Trace (built throughout) ─────
    trace: list                        # Per-node log: step / input_summary / output_summary
    error: Optional[str]               # Surface any node failure without crashing graph
```

---

## Trace Entry Pattern (use in every node)

```python
# At the end of each node function, append to trace:

state["trace"].append({
    "step": "classify_issue",           # node name
    "input_summary": "...",             # 1-sentence description of what came in
    "output_summary": "...",            # 1-sentence description of what was produced
    "key_outputs": {                    # the actual values generated
        "issue_category": state["issue_category"],
        "risk_level": state["risk_level"],
        "regulatory_trigger": state["regulatory_trigger"]
    }
})
```

This pattern is identical across all six nodes — only `step` and `key_outputs` change.

---

## Initialization Pattern

```python
# How to initialize state before running the graph:

initial_state: CaseState = {
    "raw_input": "Customer complaint text goes here...",
    "issue_category": None,
    "risk_level": None,
    "regulatory_trigger": None,
    "entities": None,
    "policy_snippets": None,
    "priority_score": None,
    "priority_rationale": None,
    "internal_note": None,
    "routing_destination": None,
    "recommended_action": None,
    "trace": [],        # starts empty, grows with each node
    "error": None
}
```

---

## What Comes Next (Phase 1 → 2)

Phase 1: Install LangGraph, create state.py, run a single stub node
         that classifies "hello world" and appends to trace. Prove graph executes.

Phase 2: Wire all 6 nodes as stubs. Prove state flows correctly node-to-node
         with trace entries at each step. No LLM yet.

Phase 3: Replace stubs with real LLM calls, one node at a time.

Phase 4: Add Streamlit UI. Display final output + full execution trace side by side.

Phase 5: Polish scenarios, README, resume bullets.

