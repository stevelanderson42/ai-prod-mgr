# Opportunity Packet: AI-Assisted Customer Routing

**Submitted By:** [Product Manager Name]  
**Date:** 2024-11-15  
**Business Unit:** Customer Service Operations  
**Sponsor:** VP, Customer Experience

---

## Opportunity Summary

**Problem Statement:**  
Customer service inquiries are currently routed based on simple queue rules (round-robin, skill group). This results in mismatches: complex inquiries go to junior reps (escalations, poor CX), simple inquiries go to senior reps (inefficient use of expertise). Average handle time is 12 minutes; escalation rate is 23%.

**Proposed Solution:**  
Implement AI-powered intent classification and routing that analyzes inquiry content and account context to match each customer with the optimal handling path: self-service resolution, junior rep, senior rep, or specialist queue.

**Target Outcome:**  
Reduce average handle time by 15%, reduce escalation rate to below 15%, improve first-contact resolution from 67% to 80%.

---

## Business Value Inputs

| Input | Declared Value |
|-------|----------------|
| Primary metric impacted | Average Handle Time (AHT) |
| Current baseline | 12.3 minutes AHT, 23% escalation rate |
| Target improvement | 15% AHT reduction, 8pt escalation reduction |
| Revenue/cost impact | $2.1M annual cost savings (labor efficiency) |
| Customer segment | All retail brokerage customers (1.2M accounts) |
| Strategic alignment | Supports "Digital First Service" initiative |

---

## Feasibility Inputs

| Input | Declared Value |
|-------|----------------|
| Data availability | CRM records, call transcripts (12 months), account data |
| Data quality | CRM: High quality; Transcripts: Medium (ASR errors) |
| System integration | CRM (Salesforce), telephony (Genesys), account system |
| Integration complexity | Medium — APIs exist but routing logic is legacy |
| Team capability | ML team has NLP experience; no prior routing models |
| Vendor/model options | Fine-tuned classifier vs. LLM-based intent detection |
| Timeline estimate | 4-6 months to pilot, 3 months to scale |

---

## Governance Inputs

| Input | Declared Value |
|-------|----------------|
| Data sensitivity | Contains PII (name, account number, inquiry content) |
| Applicable regulations | FINRA 3110 (supervision), state privacy laws |
| Explainability needs | Medium — reps need to understand why routing occurred |
| Fair treatment concerns | Must ensure no disparate impact by customer segment |
| Audit requirements | Routing decisions must be logged and reviewable |
| Prior precedent | No prior AI routing in production; chatbot pilot in 2023 |
| Compliance consulted | Initial conversation held; formal review pending |

---

## Stakeholder Alignment

| Stakeholder | Position | Concerns Raised |
|-------------|----------|-----------------|
| Customer Service VP | Sponsor, supportive | Wants pilot data before full commitment |
| Compliance | Cautiously supportive | Needs explainability and fair treatment analysis |
| IT/Engineering | Supportive | Concerned about legacy routing system integration |
| Finance | Neutral | Wants validated ROI before budget approval |

---

## Open Questions

1. Can we get clean intent labels from historical data, or do we need manual labeling?
2. What's the fallback if the model confidence is low?
3. How do we handle customers who explicitly request a human?
4. What's the regulatory precedent for AI-assisted (not AI-decided) routing?

---

## Attachments

- [Link to Customer Service metrics dashboard]
- [Link to preliminary data audit findings]
- [Link to "Digital First Service" strategy doc]

---

*Intake version: 1.0*  
*See [Intake README](../../intake/README.md) for intake process overview.*