# Evidence Folder

## Purpose

This folder contains **evidence traceability artifacts** that connect ROI Engine inputs and scores to their supporting sources.

In regulated environments, decision rationale must be auditable. This folder ensures every declared assumption in an Opportunity Packet can be traced back to its origin—whether that's a market report, internal metric, SME interview, or regulatory guidance.

---

## Why Evidence Traceability Matters

ROI scores are only as credible as the inputs they're based on. Without evidence linkage:

- Stakeholders can't validate assumptions
- Compliance can't audit decision rationale
- Future reviewers can't understand why scores were assigned
- "Garbage in, garbage out" goes undetected

Evidence traceability transforms the ROI Engine from a scoring calculator into a **defensible decision framework**.

---

## What Goes Here

| Artifact | Description |
|----------|-------------|
| `input-evidence-references.md` | Per-opportunity table linking each declared input to its source |

Templates for these artifacts live in `/templates`.

---

## Relationship to ADR-0003

This folder implements the [Evidence Traceability Standard](../../../architecture/decisions/ADR-0003%20-%20Evidence%20Traceability%20Standard.md) established at the toolkit level.

Key principles applied:
- Every processed artifact includes evidence pointers to upstream sources
- Chain must be traceable: output → score → input → source
- Timestamps enable temporal debugging and audit trails

---

## MVP Scope

**MVP:** Manual evidence table created alongside each Opportunity Packet

**Strong MVP:** Evidence validation checklist (are sources current? authoritative? conflicting?)

**Backlog:** Automated evidence linking from structured intake forms

---

*See [ROI Engine README](../README.md) for module overview.*