# ADR-0001: Choose Verification-First Repo Scaffold
**Date:** 2025-10-23
**Status:** Accepted 

## Context
I needed a consistent structure across all AI PM project repos to show verification artifacts
(decision logs, evals, prompts, risk docs).  
Goal: make verification easy and reproducible for reviewers and hiring managers.

## Options Considered
A) Keep ad-hoc Notion notes and screenshots  
B) Use a README-only style with mixed content   
C) Adopt a verification-first scaffold with `/decisions`, `/evals`, `/prompts`, `/risk`

## Decision
Chose **Option C**, adopting a verification-first scaffold with ADRs and EVAL_LOGs as core evidence.

## Consequences
- ✅ Easier for hiring managers to audit reasoning and trace changes  
- ✅ Enables repeatable eval tracking and process storytelling  
- ⚠️ Slightly higher upfront maintenance overhead (must log ADRs and evals regularly)

## Links
- Commit: [`f2f5e50 - add verification - first scaffold ](https://github.com/stevelanderson42/ai-prod-mgr/commit/f2f5e50299461b60d64a12885b54915224ff88c7)
- Eval run:  [2025-10-23 baseline .csv](../evals/runs/2025-10-23_baseline.csv)
- Think‑aloud: <link>
