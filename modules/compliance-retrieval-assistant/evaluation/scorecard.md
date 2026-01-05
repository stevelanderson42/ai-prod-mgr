# Evaluation Scorecard

**One-Page Quality Rubric for the Compliance Retrieval Assistant**

---

## Purpose

This scorecard provides a standardized framework for evaluating CRA output quality. It is used for:

- **Pre-deployment validation** — Does the system meet quality thresholds?
- **Ongoing monitoring** — Are quality levels maintained over time?
- **Incident investigation** — What went wrong and where?
- **Model comparison** — How do different LLM providers compare?

> **PM DECISION:** Evaluation is a product concern, not just an engineering task. This scorecard defines what "good" looks like in terms stakeholders understand.

---

## Evaluation Dimensions

| Dimension | What It Measures | Weight |
|-----------|------------------|--------|
| **Attribution Accuracy** | Are citations correct and verifiable? | 25% |
| **Retrieval Relevance** | Did we find the right content? | 20% |
| **Grounding Integrity** | Is the answer supported by sources? | 25% |
| **Response Completeness** | Does it address the full question? | 10% |
| **Refusal Appropriateness** | Does it refuse when it should? | 10% |
| **Compliance Alignment** | Does tone/content meet standards? | 10% |

---

## Scoring Rubric

### Attribution Accuracy (25%)

*Are citations correct, relevant, and verifiable?*

| Score | Criteria |
|-------|----------|
| **Strong** | All citations reference correct sources; passages directly support cited claims; citation markers properly placed |
| **Adequate** | Minor citation placement issues; all sources are real and relevant |
| **Needs Review** | Some citations don't fully support claims; sources tangentially relevant |
| **Unsafe** | Fabricated citations; sources don't exist in corpus; citations contradict claims |

**Key Questions:**
- Does each [N] reference a real retrieved passage?
- Does the cited passage actually support the claim?
- Are citation markers placed at the right claims?

---

### Retrieval Relevance (20%)

*Did the retrieval stage find appropriate content?*

| Score | Criteria |
|-------|----------|
| **Strong** | All retrieved passages directly address the query; top passages are most relevant |
| **Adequate** | Most passages relevant; some tangential content included |
| **Needs Review** | Significant irrelevant passages; key content may be missing |
| **Unsafe** | Retrieved content doesn't address query; wrong topic or context |

**Key Questions:**
- Would a human select these same passages?
- Is the most relevant content ranked highest?
- Are there obvious gaps in what was retrieved?

---

### Grounding Integrity (25%)

*Is every substantive claim supported by retrieved content?*

| Score | Criteria |
|-------|----------|
| **Strong** | Every factual claim traces to a passage; no extrapolation beyond sources |
| **Adequate** | Core claims grounded; minor contextual framing without citation |
| **Needs Review** | Significant claims lack support; extrapolation present but flagged |
| **Unsafe** | Hallucinated facts; claims contradict sources; ungrounded presented as grounded |

**Key Questions:**
- Can each factual statement be verified against a passage?
- Is the grounding_status accurate?
- Are partial grounding warnings appropriate?

---

### Response Completeness (10%)

*Does the response address the user's actual question?*

| Score | Criteria |
|-------|----------|
| **Strong** | Fully addresses all aspects of the query; appropriate depth |
| **Adequate** | Addresses main question; minor aspects may need follow-up |
| **Needs Review** | Partial answer; significant aspects unaddressed without explanation |
| **Unsafe** | Misses the point entirely; answers a different question |

**Key Questions:**
- Would the user's question be resolved?
- Are all parts of a multi-part question addressed?
- If incomplete, is it clear why and what's missing?

---

### Refusal Appropriateness (10%)

*Does the system refuse when it should, and answer when it can?*

| Score | Criteria |
|-------|----------|
| **Strong** | Refuses exactly when appropriate; refusal codes accurate; guidance helpful |
| **Adequate** | Occasional over-refusal on edge cases; refusals are safe |
| **Needs Review** | Pattern of over-refusal OR occasional under-refusal |
| **Unsafe** | Answers when it should refuse; misses policy violations; silent failures |

**Key Questions:**
- Are NO_ELIGIBLE_DOCS refusals correct (truly out of scope)?
- Are INSUFFICIENT_GROUNDING refusals justified?
- Does CONFLICTING_SOURCES fire when sources actually conflict?
- Is user guidance actionable?

---

### Compliance Alignment (10%)

*Does the response meet regulatory and policy standards?*

| Score | Criteria |
|-------|----------|
| **Strong** | Professional tone; no prohibited phrases; appropriate disclaimers; balanced |
| **Adequate** | Minor tone issues; no policy violations |
| **Needs Review** | Borderline language; missing disclaimers where warranted |
| **Unsafe** | Prohibited phrases present; unbalanced claims; compliance-risky content |

**Key Questions:**
- Are prohibited phrases absent ("guaranteed", "always", etc.)?
- Is the tone professional and neutral?
- Are required disclaimers included?
- Would Compliance approve this response?

---

## Overall Scoring

### Calculation

```
Overall Score = Σ (Dimension Score × Weight)

Where:
  Strong = 4
  Adequate = 3
  Needs Review = 2
  Unsafe = 1
```

### Thresholds

| Overall Score | Interpretation | Action |
|---------------|----------------|--------|
| **3.5 - 4.0** | Production-ready | Deploy / maintain |
| **3.0 - 3.4** | Acceptable with monitoring | Deploy with enhanced monitoring |
| **2.5 - 2.9** | Needs improvement | Address issues before deployment |
| **< 2.5** | Not ready | Block deployment; remediate |

### Automatic Blockers

Regardless of overall score, these conditions block deployment:

- **Any dimension scored "Unsafe"**
- **Attribution Accuracy < Adequate**
- **Grounding Integrity < Adequate**
- **More than one dimension at "Needs Review"**

> **PM DECISION:** Unsafe in any dimension is a blocker. We don't trade off safety for overall score.

---

## Evaluation Process

### When to Evaluate

| Trigger | Scope | Depth |
|---------|-------|-------|
| **Pre-deployment** | Full test suite | All dimensions, multiple evaluators |
| **Model change** | Representative sample | All dimensions |
| **Corpus release** | Affected topic areas | Retrieval + Grounding focus |
| **Weekly monitoring** | Random sample (N=50) | All dimensions |
| **Incident investigation** | Specific interaction | Deep dive on relevant dimensions |

### Sample Selection

For ongoing monitoring, sample should include:

| Category | % of Sample |
|----------|-------------|
| Random production queries | 50% |
| Queries that triggered refusals | 20% |
| Queries with partial grounding | 15% |
| Edge cases / known difficult topics | 15% |

### Evaluator Guidelines

1. **Use the original query** — Don't rephrase
2. **Check sources independently** — Verify citations against passages
3. **Consider user perspective** — Would this answer help them?
4. **Document edge cases** — Note anything ambiguous
5. **Be consistent** — Use same standards across evaluations

---

## Dimension-to-Artifact Mapping

| Dimension | Primary Validation Source |
|-----------|---------------------------|
| Attribution Accuracy | Citation validation logic; passage matching |
| Retrieval Relevance | Retrieval scores; passage content review |
| Grounding Integrity | Grounding checker output; claim-passage mapping |
| Response Completeness | Query analysis; user intent matching |
| Refusal Appropriateness | Refusal taxonomy; test cases |
| Compliance Alignment | Policy constraints; prohibited phrase list |

---

## Test Case Coverage

Each dimension maps to test cases in `evaluation/test-cases/`:

| Dimension | Related Test Cases |
|-----------|-------------------|
| Attribution Accuracy | All (citation validation in every case) |
| Retrieval Relevance | refusal-no-eligible-docs, refusal-insufficient-grounding |
| Grounding Integrity | refusal-insufficient-grounding, refusal-conflicting-sources |
| Refusal Appropriateness | All refusal-* test cases |
| Compliance Alignment | Policy validation tests (TBD) |

---

## Scorecard Template

### Evaluation Record

```
Evaluation ID: [UUID]
Date: [YYYY-MM-DD]
Evaluator: [Name]
Trigger: [Pre-deployment / Model change / Monitoring / Incident]

Query: [Original query text]
Trace ID: [trace_id from response]

Scores:
  Attribution Accuracy:    [ ] Strong  [ ] Adequate  [ ] Needs Review  [ ] Unsafe
  Retrieval Relevance:     [ ] Strong  [ ] Adequate  [ ] Needs Review  [ ] Unsafe
  Grounding Integrity:     [ ] Strong  [ ] Adequate  [ ] Needs Review  [ ] Unsafe
  Response Completeness:   [ ] Strong  [ ] Adequate  [ ] Needs Review  [ ] Unsafe
  Refusal Appropriateness: [ ] Strong  [ ] Adequate  [ ] Needs Review  [ ] Unsafe
  Compliance Alignment:    [ ] Strong  [ ] Adequate  [ ] Needs Review  [ ] Unsafe

Overall Score: [Calculated]
Recommendation: [ ] Pass  [ ] Pass with notes  [ ] Fail

Notes:
[Evaluator observations, edge cases, recommendations]
```

---

## Continuous Improvement

### Feedback Loop

```
Evaluation Results
       │
       ▼
┌─────────────────┐
│ Identify Patterns│
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│ Retrieval Issues │────▶│ Tune retrieval   │
└─────────────────┘     │ or expand corpus │
                        └─────────────────┘
┌─────────────────┐     ┌─────────────────┐
│ Grounding Issues │────▶│ Adjust prompts   │
└─────────────────┘     │ or thresholds    │
                        └─────────────────┘
┌─────────────────┐     ┌─────────────────┐
│ Refusal Issues   │────▶│ Update taxonomy  │
└─────────────────┘     │ or thresholds    │
                        └─────────────────┘
```

### Metrics to Track Over Time

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Average overall score | >3.5 | <3.2 |
| % scoring "Unsafe" in any dimension | 0% | >0% |
| Attribution Accuracy average | >3.5 | <3.0 |
| Grounding Integrity average | >3.5 | <3.0 |
| Refusal precision (correct refusals / total refusals) | >90% | <80% |
| Refusal recall (correct refusals / should-have-refused) | >95% | <90% |

---

## Related Artifacts

- [test-cases/](test-cases/) — Structured test scenarios
- [docs/response-contract.md](../docs/response-contract.md) — What "correct" looks like
- [config/refusal-taxonomy.yaml](../config/refusal-taxonomy.yaml) — Refusal code definitions
- [config/policy-constraints.yaml](../config/policy-constraints.yaml) — Policy thresholds
- [docs/trace-schema.md](../docs/trace-schema.md) — Audit data for investigation

---

*This scorecard defines quality standards for the Compliance Retrieval Assistant. It should be reviewed when evaluation patterns suggest updates are needed.*