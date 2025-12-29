# Intake — Input Handling

## Purpose

This folder contains the input structures and templates for capturing opportunity data. All inputs are treated as **declared assumptions** — explicit statements that can be validated, challenged, and refined.

## Input Categories

The ROI Decision Engine accepts inputs in three categories, each mapping to a scoring dimension:

### 1. Business Value Inputs

**Source:** PM / Business Sponsor, Domain / Operations SME

| Input | Description |
|-------|-------------|
| Opportunity description | What the AI initiative does |
| Problem statement | What problem it solves |
| Target KPIs | Metrics expected to improve |
| Value type | Cost reduction, CX improvement, risk reduction, etc. |
| Impact estimate | Expected magnitude (range acceptable) |
| Impact confidence | Low / Medium / High |

### 2. Feasibility Inputs

**Source:** Engineering / Architecture, Domain / Operations SME

| Input | Description |
|-------|-------------|
| Systems touched | Integration points |
| Data required | What data the model needs |
| Data availability | Available / Partial / Not available |
| Delivery effort | Small / Medium / Large |
| Timeline estimate | Expected duration |
| Key dependencies | Blockers or prerequisites |

### 3. Governance Inputs

**Source:** Legal / Compliance / Risk

| Input | Description |
|-------|-------------|
| Customer-facing impact | Does it affect customers directly? |
| Model role | Advisory vs. automated |
| Data sensitivity | PII, financial, health, none |
| Decision impact | Low / Medium / High stakes |
| Explainability requirement | Low / Medium / High |
| Known constraints | Regulatory requirements |
| Open questions | Unknowns for compliance to resolve |

## Files in This Folder

| File | Purpose |
|------|---------|
| `opportunity-packet-schema.md` | Formal schema definition for opportunity packets |
| `/templates/opportunity-intake-form.md` | Blank template for capturing all inputs |
| `/templates/governance-intake-questions.md` | Focused template for governance inputs |

## Design Principles

1. **Declared assumptions, not answers** — Inputs represent current understanding, subject to validation
2. **Source attribution** — Each input category has identified providers
3. **Governance as partner** — Compliance inputs captured alongside business/technical, not after

---

*See main [README](../README.md) for module overview.*