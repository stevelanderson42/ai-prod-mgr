# Evals

## Purpose

This evaluation framework is a **shared capability** used across multiple modules in the Regulated AI Workflow Toolkit.

It supports:
- the **ROI Decision Engine**, by providing structured inputs for comparing AI opportunities
- the **Compliance Retrieval Assistant**, by validating response quality, grounding, and refusal behavior

The goal is to ensure **decision traceability, repeatability, and output quality** across the system, rather than ad hoc or one-off evaluation.

The evaluation artifacts in this folder are intentionally structured to support both **automated scoring** and **human review**, reflecting how evaluation is performed in real, regulated environments.

---

## Folder Structure

This folder contains:

- `/datasets/`  
  Gold questions, reference answers, and labeled examples used for evaluation.

- `/schema/`  
  Metric definitions (JSON) and scoring rubrics that make evaluation criteria explicit and auditable.

- `/runs/`  
  Immutable run artifacts (CSV / JSONL) capturing evaluation outputs at specific points in time.

- `EVAL_LOG.md`  
  A human-readable index of evaluation runs, changes, and observed deltas over time.

Together, these components provide a durable record of how AI behavior was assessed and how decisions were informed.

