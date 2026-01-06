# Evaluation

**Quality assurance framework for the Compliance Retrieval Assistant**

---

## Purpose

This folder contains the evaluation framework for measuring CRA output quality. Evaluation is a **product concern**, not just an engineering task — it defines what "good" means in terms stakeholders understand.

> **PM DECISION:** We evaluate the system, not just the model. Retrieval quality, grounding integrity, refusal appropriateness, and compliance alignment all matter — not just "did the LLM generate a good response?"

---

## Contents

```
evaluation/
├── README.md              # This file
├── scorecard.md           # 6-dimension quality rubric
└── test-cases/
    ├── refusal-no-eligible-docs.md
    ├── refusal-insufficient-grounding.md
    ├── refusal-policy-blocked.md
    ├── refusal-ambiguous-query.md
    └── refusal-conflicting-sources.md
```

---

## Scorecard

**[scorecard.md](scorecard.md)** — The one-page quality rubric for evaluating CRA responses.

### Six Evaluation Dimensions

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| Attribution Accuracy | 25% | Are citations correct and verifiable? |
| Retrieval Relevance | 20% | Did we find the right content? |
| Grounding Integrity | 25% | Is the answer supported by sources? |
| Response Completeness | 10% | Does it address the full question? |
| Refusal Appropriateness | 10% | Does it refuse when it should? |
| Compliance Alignment | 10% | Does tone/content meet standards? |

### Scoring Scale

| Score | Meaning |
|-------|---------|
| **Strong** | Meets all criteria |
| **Adequate** | Minor issues, acceptable |
| **Needs Review** | Significant gaps |
| **Unsafe** | Fails criteria — blocks deployment |

### Deployment Thresholds

- **≥ 3.5** — Production-ready
- **3.0 - 3.4** — Deploy with enhanced monitoring
- **< 3.0** — Block deployment, remediate
- **Any "Unsafe"** — Automatic blocker regardless of score

---

## Test Cases

The `test-cases/` folder contains structured scenarios for validating refusal behavior. Each test case maps to a code in the [refusal taxonomy](../config/refusal-taxonomy.yaml).

### Refusal Test Coverage

| Test Case | Refusal Code | Severity | Key Validation |
|-----------|--------------|----------|----------------|
| [refusal-no-eligible-docs.md](test-cases/refusal-no-eligible-docs.md) | `NO_ELIGIBLE_DOCS` | Info | Query outside corpus scope; LLM skipped |
| [refusal-insufficient-grounding.md](test-cases/refusal-insufficient-grounding.md) | `INSUFFICIENT_GROUNDING` | Warning | Passages found but inadequate for answer |
| [refusal-policy-blocked.md](test-cases/refusal-policy-blocked.md) | `POLICY_BLOCKED` | Warning | Access denied; no information leakage |
| [refusal-ambiguous-query.md](test-cases/refusal-ambiguous-query.md) | `AMBIGUOUS_QUERY` | Info | Vague query; clarification prompts provided |
| [refusal-conflicting-sources.md](test-cases/refusal-conflicting-sources.md) | `CONFLICTING_SOURCES` | Escalate | Sources disagree; escalation triggered |

### Test Case Structure

Each test case follows a consistent format:

1. **Purpose** — What this test validates
2. **Scenario** — The situation being tested
3. **Test Inputs** — Query, user context, corpus state
4. **Expected Behavior** — By pipeline stage
5. **Expected Response** — Full JSON per response contract
6. **Expected Trace** — Full JSON per trace schema
7. **Pass Criteria** — Specific validations that must succeed
8. **Fail Conditions** — What would indicate a bug
9. **Variations** — Edge cases and boundary conditions

---

## How to Use This Framework

### Pre-Deployment Validation

Before any deployment:

1. Run all 5 refusal test cases
2. Evaluate a sample of responses using the scorecard
3. Verify no dimension scores "Unsafe"
4. Check that overall score ≥ 3.0

### Ongoing Monitoring

After deployment:

1. Weekly sample evaluation (N=50 recommended)
2. Track refusal rates by code
3. Monitor grounding coverage trends
4. Alert on any "Unsafe" scores

### Model Change Validation

When switching LLM providers or versions:

1. Re-run all test cases
2. Compare scorecard results before/after
3. Pay special attention to:
   - Grounding Integrity (model behavior changes)
   - Compliance Alignment (tone may shift)
   - Refusal Appropriateness (thresholds may need tuning)

### Incident Investigation

When investigating a problematic response:

1. Retrieve the trace using trace_id
2. Walk through each pipeline stage
3. Identify where behavior diverged from expected
4. Score the response on all 6 dimensions
5. Document findings for pattern analysis

---

## Evaluation vs. Testing

| Evaluation | Testing |
|------------|---------|
| "Is this response good?" | "Does this code work?" |
| Human judgment required | Automated pass/fail |
| Uses scorecard dimensions | Uses test case criteria |
| Ongoing, sampled | Pre-deployment, exhaustive |
| Measures quality trends | Catches regressions |

Both are necessary. Test cases catch regressions; scorecard evaluation measures quality.

---

## Planned Additions

As the CRA matures, this folder will expand:

- [ ] Automated test runner for refusal scenarios
- [ ] Golden dataset of query/response pairs
- [ ] Evaluation result logs with timestamps
- [ ] Comparative analysis across model versions
- [ ] Inter-rater reliability guidelines for scorecard

---

## Related Artifacts

- [config/refusal-taxonomy.yaml](../config/refusal-taxonomy.yaml) — Refusal code definitions
- [config/policy-constraints.yaml](../config/policy-constraints.yaml) — Thresholds that affect evaluation
- [docs/response-contract.md](../docs/response-contract.md) — What "correct" responses look like
- [docs/trace-schema.md](../docs/trace-schema.md) — Audit data for investigation
- [docs/threat-model.md](../docs/threat-model.md) — Failure modes evaluation should catch

---

*This framework defines quality standards for the Compliance Retrieval Assistant. It should evolve as the system matures and operational patterns emerge.*