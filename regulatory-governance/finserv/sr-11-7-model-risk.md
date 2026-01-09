# SR 11-7 — Model Risk Management

**Regulatory Citation:** Federal Reserve SR 11-7 / OCC 2011-12  
**Issued:** April 4, 2011  
**Regulator:** Federal Reserve Board & Office of the Comptroller of the Currency (OCC)  
**Type:** Supervisory Guidance (not statute, but examiner-enforced)

---

## Summary

SR 11-7 is the foundational guidance for **model risk management** in U.S. financial institutions. It establishes expectations for how financial institutions develop, validate, document, and govern models — including AI/ML systems.

The core premise: **models are useful but dangerous**. They simplify reality, embed assumptions, and can fail in ways that aren't immediately visible. Organizations must manage this risk through robust documentation, independent validation, and ongoing monitoring.

For AI products, SR 11-7 means: if you can't explain how it works, document its limitations, and validate its behavior — it doesn't ship.

> *This document interprets SR 11-7 from a product and architecture perspective, not as a legal or compliance directive.*

---

## Key Regulatory Language

### On Documentation

> "Model documentation should be sufficiently detailed to allow parties unfamiliar with a model to understand how the model operates, as well as its limitations and key assumptions."
>
> — *SR 11-7, Attachment: Guidance on Model Risk Management*

### On Governance

> "Banks should have a sound governance framework for model risk management that includes policies and procedures, controls, compliance, and accountability structures."
>
> — *SR 11-7, Attachment*

### On the Scope of "Model"

> "The definition of model... refers to a quantitative method, system, or approach that applies statistical, economic, financial, or mathematical theories, techniques, and assumptions to process input data into quantitative estimates."
>
> — *SR 11-7, Attachment*

This definition is broad enough to include AI/ML systems, retrieval-augmented generation, and scoring engines — all components of the Regulated AI Workflow Toolkit.

### On Validation

> "Effective validation helps ensure that models are sound and functioning as intended... Validation should be performed by staff with appropriate incentives, competence, and influence — generally independent of model development."
>
> — *SR 11-7, Attachment*

---

## Core Expectations

From an examiner's perspective, SR 11-7 requires:

### Documentation
- **Purpose and intended use** clearly stated
- **Assumptions and limitations** explicitly documented
- **Input data sources** and quality requirements defined
- **Output interpretation guidance** for downstream users
- **Version history** maintained with change rationale

### Governance
- **Policies and procedures** for model development, approval, and use
- **Roles and responsibilities** clearly assigned
- **Escalation paths** for model issues
- **Board and senior management oversight** demonstrated

### Validation
- **Independent review** of model logic and performance
- **Outcomes analysis** comparing predictions to actuals
- **Sensitivity testing** to understand behavior under stress
- **Ongoing monitoring** for drift and degradation

### Controls
- **Access controls** limiting who can modify models
- **Change management** processes for updates
- **Audit trails** for model changes, approvals, and production deployments
- **Incident response** procedures for model failures

---

## Product & Architecture Implications

For AI products in regulated environments, SR 11-7 creates concrete design requirements:

| Expectation | What It Means for AI Systems |
|-------------|------------------------------|
| **"Sufficiently detailed" documentation** | README files, ADRs, and architecture docs aren't optional — they're regulatory artifacts |
| **Limitations must be explicit** | Every module must document what it does NOT do and where it will fail |
| **Independent validation** | Evaluation frameworks must exist; self-assessment isn't sufficient |
| **Assumptions documented** | Prompt design choices, retrieval thresholds, refusal logic — all must be explained |
| **Version control required** | Corpus versions, model versions, config versions — all must be traceable |
| **Ongoing monitoring** | Systems must detect drift; "deploy and forget" is non-compliant |

### The Documentation Standard

SR 11-7's "parties unfamiliar with a model" standard is the bar:

> Could someone who didn't build this system understand how it works, what it assumes, and where it might fail — from the documentation alone?

If the answer is no, the documentation is insufficient.

---

## Where This Shows Up in the Portfolio

| Artifact | How SR 11-7 Informed It |
|----------|-------------------------|
| **All Module READMEs** | "What This Module Does NOT Do" section — explicit limitations |
| **Architecture Decision Records (ADRs)** | Document assumptions and rationale for key design choices |
| **Compliance Retrieval Assistant** | `corpus_release_id` versioning enables "what did the system know when?" reconstruction |
| **Evaluation Scorecard** | Independent validation framework for RAG output quality |
| **Trace Schema** | Audit trail preserving inputs, outputs, and decision rationale |
| **Requirements Guardrails** | Deterministic routing logic is documentable and explainable |
| **ROI Decision Engine** | Decision Memo artifact creates auditable prioritization rationale |

### Specific Design Decisions Driven by SR 11-7

| Decision | SR 11-7 Driver |
|----------|----------------|
| No opaque inference at control layer | "Parties unfamiliar" must understand routing logic |
| Grounding status over confidence scores | Categorical status is explainable; numeric confidence is not |
| Refusal taxonomy as config | Refusal logic must be documentable and auditable |
| Corpus versioning with release IDs | Enables reconstruction of "what the system knew when" |
| Dual response contracts (user + audit) | Different audiences need different documentation |

---

## Common Examiner Questions (Applied Lens)

Based on SR 11-7, examiners may ask:

1. **"Walk me through how this model works."**  
   → Your documentation should enable this without the developer present.

2. **"What are the key assumptions?"**  
   → ADRs and README files should list these explicitly.

3. **"How do you know it's working correctly?"**  
   → Evaluation scorecard and ongoing monitoring should answer this.

4. **"What happens when it fails?"**  
   → Refusal taxonomy and escalation paths should be documented.

5. **"Show me the change history."**  
   → Version control, ADRs, and corpus release IDs should provide this.

---

## Key Distinction: Guidance vs. Rule

SR 11-7 is **supervisory guidance**, not a statute or regulation. It doesn't sit in the Code of Federal Regulations.

However:
- Examiners use it as the standard for evaluating model risk management
- Findings of "inadequate model risk management" can result in enforcement actions
- Most large financial institutions treat it as de facto mandatory

For portfolio purposes, treat SR 11-7 as: **the documentation and governance bar your AI systems must clear to be taken seriously in regulated environments.**

---

## References

- [SR 11-7 Letter (Federal Reserve)](https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm)
- [SR 11-7 Attachment: Guidance on Model Risk Management (PDF)](https://www.federalreserve.gov/supervisionreg/srletters/sr1107a1.pdf)
- [OCC 2011-12 (Companion Guidance)](https://www.occ.gov/news-issuances/bulletins/2011/bulletin-2011-12.html)

---

*Part of the [Regulatory Governance Context](../README.md) — documenting the external constraints that shape AI product design.*