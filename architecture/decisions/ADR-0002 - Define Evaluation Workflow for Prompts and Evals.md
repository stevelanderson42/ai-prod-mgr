# ADR-0002: Define Evaluation Workflow for Prompts and Evals  
**Date:** 2025-10-23  
**Status:** Accepted  

## Context
The project now has a verification-first scaffold, but no defined method to evaluate prompts, iterations, or outcomes.
To make progress verifiable, every prompt change must produce measurable results logged under `/evals/`.

The goal:  
Create a lightweight evaluation workflow that captures **inputs**, **outputs**, **metrics**, and **interpretation** in a repeatable way.

## Options Considered
A) Manual free-form notes after each experiment  
B) Structured JSON/CSV logs (one file per run) with metadata  
C) Use a hybrid model — JSON schema + human commentary file linked from ADRs  

## Decision
Adopt **Option C**, using:
- `/evals/runs/` for machine-readable output (`YYYY-MM-DD_baseline.csv` or `.jsonl`)
- `/evals/schema/metrics.json` for metric definitions  
- `/evals/EVAL_LOG.md` for human summaries of what changed, why, and what was learned  
- Each eval run links back to its originating `/prompts/system-v0.x.md`

This approach enables both automation and human reasoning to coexist — a key requirement for AI PM verification.

## Consequences
✅ Provides traceable evidence of iteration quality  
✅ Makes it possible to visualize improvement over time  
⚠️ Requires discipline in logging after each iteration  

## Links
- Related ADR: [ADR-0001 – Verification-First Scaffold](ADR-0001%20-%20first%20decision.md)  
- Example schema: [`../evals/schema/metrics.json`](../evals/schema/metrics.json)  
- Eval log: [`../evals/EVAL_LOG.md`](../evals/EVAL_LOG.md)  

