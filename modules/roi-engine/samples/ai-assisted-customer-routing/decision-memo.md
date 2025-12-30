# Decision Memo: AI-Assisted Customer Routing

**Opportunity:** AI-Assisted Customer Routing  
**Date:** 2024-11-18  
**Prepared By:** [Product Manager Name]  
**Status:** Ready for Review

---

## Executive Summary

AI-assisted customer routing offers meaningful operational efficiency gains ($2.1M projected annually) with manageable regulatory complexity. The opportunity scores well on business value and feasibility, with regulatory considerations that are addressable through standard governance processes. **Recommendation: Proceed to discovery phase** with focused validation on data quality, fair treatment analysis, and timeline refinement.

---

## Opportunity Overview

**Problem Statement:**  
Current rule-based routing creates mismatches between inquiry complexity and rep expertise, driving a 23% escalation rate and 12.3-minute average handle time.

**Proposed Solution:**  
AI-powered intent classification to route inquiries to optimal handling path (self-service, junior rep, senior rep, specialist).

**Target Outcome:**  
15% AHT reduction, escalation rate below 15%, first-contact resolution improvement to 80%.

**Stakeholders:**  
Customer Service VP (sponsor), Compliance, IT/Engineering, Finance

---

## Composite Score

| Dimension | Score (1-5) | Weight | Weighted |
|-----------|-------------|--------|----------|
| Business Value | 4 | 40% | 1.60 |
| Feasibility | 3 | 35% | 1.05 |
| Regulatory Complexity | 3 | 25% | 0.75 |
| **Composite** | | | **3.40** |

*Note: Regulatory Complexity inverted (6 - 3 = 3) for composite calculation.*

**Interpretation:** Score of 3.40 indicates a **solid opportunity with manageable risks**. Not a slam-dunk, but worth investment in discovery to validate assumptions.

---

## Dimension Scores & Rationale

### Business Value: 4/5

**Key Drivers:**
- Clear, measurable target metrics (AHT, escalation rate)
- Credible cost savings estimate with Finance validation
- Direct alignment to stated strategic priority
- Large customer base creates meaningful impact at scale

**Why not a 5:**
- ROI depends on achieving 15% improvement target (industry range is 10-20%)
- No direct revenue impact; cost savings only

**Supporting Evidence:**
- CS Operations Dashboard (Oct 2024)
- Finance ROI model v2.1
- "Digital First Service" strategy doc

**Assumptions:**
- 15% AHT improvement is achievable (industry midpoint)
- No significant customer satisfaction degradation

---

### Feasibility: 3/5

**Key Drivers:**
- Core data assets exist (CRM, transcripts, account data)
- ML team has relevant NLP experience
- APIs available for key system integrations

**Why not higher:**
- Transcript data quality concerns (15% ASR error rate)
- Legacy routing system integration is uncertain
- Timeline estimate is low-confidence (no comparable project baseline)
- Intent labeling approach not yet determined

**Supporting Evidence:**
- Data catalog audit (Oct 2024)
- Engineering SME interview (Nov 2024)
- Team skills matrix (Q3 2024)

**Assumptions:**
- Transcript quality sufficient for intent classification (needs validation)
- 4-6 month pilot timeline is realistic (low confidence)

---

### Regulatory Complexity: 3/5

**Key Drivers:**
- Standard PII handling (established controls exist)
- FINRA 3110 supervision requirements are understood
- Audit logging requirements are clear and achievable
- AI-assisted (not AI-decided) framing reduces explainability burden

**Why not lower (less complex):**
- Fair treatment analysis not yet completed
- No direct precedent for AI routing in this context
- Compliance has indicated formal review required

**Why not higher (more complex):**
- Not a high-risk decision (routing, not advice or trading)
- Explainability requirement is "medium" not "high"
- Early compliance engagement signals partnership

**Supporting Evidence:**
- Compliance SME interview (Nov 2024)
- Data classification policy (2024)
- Supervision policy (2024)

**Assumptions:**
- Fair treatment analysis will not surface blocking issues
- "AI-assisted" framing will be accepted by compliance

---

## Risk Summary

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Transcript data quality insufficient | Medium | High | Expanded sample review before pilot; fallback to CRM-only features |
| Fair treatment analysis surfaces issues | Low | High | Early legal engagement; design for auditability from start |
| Timeline slippage | Medium | Medium | Phase pilot scope; identify minimum viable routing rules |
| Model accuracy below threshold | Medium | Medium | Define accuracy threshold upfront; A/B test against current routing |
| Customer satisfaction decrease | Low | High | Include CSAT in pilot metrics; rapid rollback capability |

---

## Assumptions Requiring Validation

| Assumption | Validation Method | Owner | Timeline |
|------------|-------------------|-------|----------|
| Transcript quality sufficient | Expanded sample review (500+ transcripts) | Data Science | 2 weeks |
| No fair treatment concerns | Legal/Compliance review | Compliance | 3 weeks |
| 4-6 month pilot feasible | Engineering spike + comparable analysis | Engineering | 2 weeks |
| Intent labels derivable from history | Labeling feasibility study | Data Science | 2 weeks |

---

## Recommendation

**Recommendation:** Proceed to Discovery Phase

**Rationale:**  
The opportunity shows strong business value alignment and manageable complexity. Key uncertainties (data quality, fair treatment, timeline) are all validatable within a bounded discovery phase. No blocking issues identified; risks are addressable through standard governance processes.

**Conditions for Pilot Approval:**
- Transcript data quality validated as sufficient
- Fair treatment analysis completed with no blocking findings
- Refined timeline estimate with engineering confidence
- Compliance sign-off on "AI-assisted" framing

**Suggested Next Steps:**
1. **Week 1-2:** Data quality validation (transcript sample review, intent labeling feasibility)
2. **Week 2-3:** Fair treatment analysis with Legal/Compliance
3. **Week 2-3:** Engineering spike on routing integration + timeline refinement
4. **Week 4:** Discovery readout and pilot go/no-go decision

---

## Appendix

**Evidence References:** [input-evidence-references.md](input-evidence-references.md)

**Opportunity Packet:** [opportunity-packet.md](opportunity-packet.md)

**Related Documents:**
- CS Operations Dashboard
- Finance ROI Model v2.1
- "Digital First Service" Strategy Doc
- FINRA Rule 3110 Reference

---

*Memo version: 1.0*  
*See [Outputs README](../../outputs/README.md) for decision memo overview.*