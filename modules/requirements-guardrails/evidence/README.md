# Evidence — Requirements Guardrails

This folder contains documented examples demonstrating how the guardrail logic evaluates real-world inputs.

---

## Contents

| File | Description |
|------|-------------|
| [sample-classifications.md](./sample-classifications.md) | 14 annotated examples covering all routing outcomes |

---

## Purpose

Evidence artifacts serve three functions:

1. **Validation** — Test cases for verifying rule logic behaves as intended
2. **Communication** — Concrete examples for stakeholders reviewing the module
3. **Portfolio signal** — Demonstrates PM reasoning to hiring managers

---

## What Belongs Here

- Sample inputs with full classification analysis
- Edge cases with documented PM rationale
- False positive / false negative analysis
- Coverage gap identification

---

## What Does NOT Belong Here

- Rule definitions → `/rules/`
- Architecture decisions → `/architecture/`
- Prompt experiments → `/experiments/`
- Output logs and audit trails → `/outputs/`