# Prompt Experiments

This folder contains a small, intentional set of **prompt experiments** used to explore how large language models behave under different constraints in regulated environments.

These experiments are not “prompt hacks.”  
They are structured learning inputs that informed the design of downstream systems such as:

- Requirements Guardrails
- Evaluation workflows
- Compliance-aware response handling

---

## Purpose

The goal of these experiments was to answer practical product questions, such as:

- What kinds of ambiguity or risk can be reliably detected *before* model invocation?
- How do explicit structure and schemas affect consistency and auditability?
- Where do model behaviors require **pre-model guardrails** versus **post-model controls**?
- Which failure modes appear early and can be mitigated cheaply?

Each experiment started as a v1 hypothesis and was iterated to v2 based on observed failure modes.

---

## What’s Included

Each experiment document typically contains:

- the original prompt (v1)
- observed issues or inconsistencies
- revised prompt (v2)
- structured output examples (often JSON)
- a short summary of what changed and why it mattered

The emphasis is on **learning and traceability**, not optimization for a single demo response.

---

## How These Experiments Are Used

The experiments in this folder directly informed:

- **Input guardrails**  
  (e.g., suitability classification, ambiguity detection)

- **Output guardrails**  
  (e.g., compliance rewrites, grounding and citation enforcement)

- **Evaluation criteria**  
  (e.g., what “good” looks like for refusal behavior or structured extraction)

They serve as *evidence* for design decisions captured elsewhere in the repository.

---

## Relationship to Other Parts of the Repo

- The **narrative and system-level design** lives under:  
  → `modules/requirements-guardrails/`

- These prompt experiments provide the **raw empirical grounding** that supports that design.

Think of this folder as the lab notebook, not the finished product.

---

## Scope and Non-Goals

This folder intentionally does **not** include:

- production prompt orchestration
- agent frameworks
- runtime infrastructure

Those concerns are addressed at the module level, once the behavior is well understood.

---

## Status

Stable.

These experiments represent foundational learning and are not expected to grow significantly.  
Future work focuses on applying these insights within system workflows, not expanding the experiment set.
