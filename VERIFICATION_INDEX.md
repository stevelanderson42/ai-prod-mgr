# Verification Index
---
## 🧩 Verification Decision Index

This section links to Architecture Decision Records (ADRs) and Commits - ADRs define key reasoning and workflow choices, while Commits are just the usual record of Commits.

| ADR | Title | Date | Status | Purpose |
|-----|-------|------|--------|---------|
| [ADR-0001](decisions/ADR-0001-first-decision.md) | Choose Verification-First Repo Scaffold | 2025-10-23 | ✅ Accepted | Establish structure for verifiable artifacts (`/decisions` \| `/evals` \| `/prompts` \| `/risk`) |
| [ADR-0002](decisions/ADR-0002-Define%20Evaluation%20Workflow%20for%20Prompts%20and%20Evals.md) | Define Evaluation Workflow for Prompts & Evals | 2025-10-23 | ✅ Accepted | Formalize how prompts & evals are logged, measured, and cross-linked |
| [COMMIT-c69cbd4] (https://github.com/stevelanderson42/ai-prod-mgr/commit/c69cbd46176eb13d920c320fd0ca28b8f4cae441) | 2025-11-27 |  ✅ Complete | test for verification index



---

### 🔄 Update cadence
- Add a new row for each accepted ADR.  
- Link directly to its Markdown file.  
- Keep **Status** updated (Accepted / Superseded / Draft).  

---

### 📘 Related directories
| Folder | Purpose |
|---------|----------|
| `/decisions` | Stores ADRs – verifiable reasoning artifacts |
| `/evals` | Stores structured results of evaluation runs |
| `/prompts` | Holds system/prompt versions used in evals |
| `/risk` | Captures assumptions, guardrails, and ethical checks |

This page is the **single place** for a hiring manager to verify your work without digging.

## Latest Evidence
- **Eval run (latest):** `/evals/runs/2025-10-23_baseline.csv`
- **Eval log summary:** `/evals/EVAL_LOG.md`
- **Most recent decision (ADR):** `/decisions/ADR-0001.md`
- **Think‑aloud video:** (paste Loom/Drive link)
- **Guardrails & risk summary:** `/risk/Guardrails.md`

## Repo Evidence Map
| Capability | Proof Artifacts |
|---|---|
| Evaluation & QA | `/evals/*`, `EVAL_LOG.md`, metric screenshots |
| Product sense under uncertainty | `/decisions/*.md` with trade‑offs |
| Risk/Governance | `/risk/Guardrails.md`, `/risk/Data_Provenance_and_Licenses.md` |
| Tech→Biz translation | `docs/requirements/*.md`, AC examples |

## Changelog
See `/CHANGELOG.md`.
