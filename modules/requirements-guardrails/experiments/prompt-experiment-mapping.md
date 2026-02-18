# Guardrail Prompt Experiments

**Module:** Requirements Guardrails  
**Purpose:** Document prompt engineering experiments that inform guardrail design.

---

## Overview

This folder maps prompt experiments from the `/prompt-experiments/` directory to Requirements Guardrails concepts. Each experiment demonstrates a pattern relevant to pre-invocation control.

---

## Experiment Mapping

| Experiment | Guardrail Concept | Routing Relevance |
|------------|-------------------|-------------------|
| **01: Suitability Classification** | Compliance trigger detection | Determines if query requires suitability review → ESCALATE |
| **02: Compliance Rewrite** | Output-layer guardrail | Post-generation control (adjacent to this module) |
| **03: Transcript Extraction** | Structured output enforcement | Ensures parseable outputs for audit trail |
| **04: Ambiguity Detection** | Ambiguity heuristics | Identifies unclear intent → CLARIFY |
| **05: Risk Disclosure** | Compliance language check | Detects missing risk language → ESCALATE |

---

## Experiment Details

### Experiment 01: Suitability Classification

**Location:** `/prompt-experiments/PromptExperiments_01_Suitability_Classification.md`

**Guardrail application:** Classifies incoming queries as suitability-relevant or not. Feeds into compliance trigger detection.

**Key learning:** V1 (vague prompt) produced inconsistent classifications. V2 (structured JSON output with explicit definitions) achieved reliable, parseable results.

**Pattern extracted:**
- Define classification labels explicitly in prompt
- Require structured output format (JSON)
- Include reasoning field for auditability

**Applied to guardrails:** Compliance trigger classifiers use this pattern for detecting suitability-relevant content.

---

### Experiment 02: Compliance Rewrite

**Location:** `/prompt-experiments/PromptExperiments_02_Compliance_Rewrite.md`

**Guardrail application:** Transforms advisor language to remove prohibited patterns (guarantees, predictions).

**Key learning:** The model can identify and rewrite non-compliant language when given explicit rules and examples.

**Pattern extracted:**
- Provide explicit list of prohibited patterns
- Show before/after examples
- Require explanation of changes made

**Applied to guardrails:** Informs `compliance-triggers.md` — the same patterns that trigger rewriting also trigger ESCALATE routing.

---

### Experiment 03: Transcript Extraction

**Location:** `/prompt-experiments/PromptExperiments_03_Transcript_Extraction.md`

**Guardrail application:** Extracts structured data from unstructured input.

**Key learning:** Strict schema definition prevents hallucination of missing fields. Empty string convention for absent data.

**Pattern extracted:**
- Define exact output schema in prompt
- Specify handling for missing information
- Prohibit inference beyond stated content

**Applied to guardrails:** Routing decision log schema uses this pattern for consistent, parseable output.

---

### Experiment 04: Ambiguity Detection

**Location:** `/prompt-experiments/PromptExperiments_04_Ambiguity_Detection.md`

**Guardrail application:** Identifies requests with unclear intent.

**Key learning:** Classifying ambiguity types (referential, scope, intent, temporal) enables targeted clarification prompts.

**Pattern extracted:**
- Categorize ambiguity rather than binary detection
- Map categories to specific clarification responses
- Preserve user intent during clarification

**Applied to guardrails:** Directly informs `ambiguity-heuristics.md` classification logic.

---

### Experiment 05: Risk Disclosure

**Location:** `/prompt-experiments/PromptExperiments_05_Grounded_Citation.md`

**Guardrail application:** Detects when investment content lacks required risk disclosures.

**Key learning:** FINRA 2210 requires balanced presentation. Model can detect one-sided benefit language.

**Pattern extracted:**
- Check for presence of risk language alongside benefit claims
- Flag omission as compliance issue
- Provide specific regulatory citation

**Applied to guardrails:** Feeds compliance trigger for "omission of material risk" pattern.

---

## V1 → V2 Refinement Patterns

Across experiments, consistent improvements emerged:

| V1 Problem | V2 Solution | Guardrail Application |
|------------|-------------|----------------------|
| Vague output format | Explicit JSON schema | Routing decision schema |
| Implicit definitions | Explicit label definitions | Rule documentation |
| Missing reasoning | Required rationale field | Audit trail design |
| Inconsistent handling of missing data | Empty string convention | Edge case handling |

---

## Experiment-to-Module Traceability

| Guardrail Artifact | Informed By Experiment |
|--------------------|------------------------|
| `ambiguity-heuristics.md` | Exp 04 (Ambiguity Detection) |
| `compliance-triggers.md` | Exp 01, 02, 05 (Suitability, Rewrite, Disclosure) |
| `routing-decision-log.md` | Exp 03 (Transcript Extraction schema pattern) |
| Output contract | All experiments (structured output pattern) |

---

## Related Documents

- [Full Prompt Experiments](../../prompt-experiments/) — Complete experiment files
- [Rules Directory](../rules/) — Classification logic derived from experiments
- [Outputs Directory](../outputs/) — Decision schema using experiment patterns
- [Sample Classifications](../evidence/sample-classifications.md) — Applied examples