# Prompt Experiments

Structured experiments exploring prompt engineering as a risk-control discipline for regulated financial services workflows.

## Purpose

These experiments document the difference between prompts that "work" and prompts that are production-safe in compliance-sensitive environments. Each experiment follows a v1 → v2 refinement pattern, showing how vague instructions fail and how explicit constraints succeed.

The goal is not clever prompting — it's predictable, auditable, machine-readable model behavior.

## Experiments

| # | Experiment | Core Pattern | Key Insight |
|---|------------|--------------|-------------|
| 01 | Suitability Classification | Structured output + explicit definitions | Correct answers aren't enough; format and reasoning matter |
| 02 | Compliance Rewrite | Constraint-based editing | "Professional" ≠ "compliant" — models need explicit rules |
| 03 | Transcript Extraction | Schema-first design | "Extract key info" produces summaries; schemas produce data |
| 04 | Ambiguity Detection | Safety gating | Helpful is not always safe — pause before answering |
| 05 | Grounded Citation | Hallucination prevention | Models blend sources unless explicitly forbidden |

## Common Themes

Across all five experiments, the same principles emerged:

**1. Role assignment matters**
Generic roles ("helpful assistant") optimize for helpfulness. Compliance-specific roles ("compliance classifier for a regulated financial institution") change the model's defaults.

**2. Explicit constraints beat implicit expectations**
The model doesn't know your rules unless you state them. "Be professional" is not the same as "remove performance predictions."

**3. Structured output enables integration**
Free-form text requires parsing and breaks unpredictably. JSON with defined schemas integrates reliably with downstream systems.

**4. Refusal is a feature**
A model that refuses to answer unclear or out-of-scope questions is safer than one that always tries to help. Design for appropriate refusal.

**5. Audit trails require citation**
In regulated environments, knowing the answer isn't enough — you need to show where it came from.

## Connection to Toolkit

These patterns form the behavioral foundation for the Regulated AI Workflow Toolkit:

- **Market Intelligence Monitor:** Extraction patterns (Experiment 03) for parsing news and filings
- **ROI Decision Engine:** Classification patterns (Experiment 01) for categorizing inputs
- **Requirements Guardrails:** Ambiguity detection (Experiment 04) and safety gating
- **Compliance RAG Assistant:** Grounded citation (Experiment 05) and rewrite constraints (Experiment 02)

## Methodology

Each experiment follows the same structure:

1. **Goal** — What behavior are we testing?
2. **Prompt V1** — A naive or minimal prompt
3. **Output V1** — What the model actually produced
4. **Observation** — Why V1 fails or is risky
5. **Prompt V2** — Refined with explicit constraints
6. **Output V2** — Improved, production-safe output
7. **Takeaway** — The generalizable lesson

All experiments were run against GPT-3.5-turbo with temperature=0 for reproducibility.

## Files
```
/prompt-experiments
    PromptExperiments_01_Suitability_Classification.md
    PromptExperiments_02_Compliance_Rewrite.md
    PromptExperiments_03_Transcript_Extraction.md
    PromptExperiments_04_Ambiguity_Detection.md
    PromptExperiments_05_Grounded_Citation.md
    README.md
```

## About

These experiments were developed during Week 1 of a 17-week AI Product Manager transition program, with a focus on applying prompt engineering to regulated industry workflows in financial services.
