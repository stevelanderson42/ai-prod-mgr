# Case Study #2: Output Governance for Regulated AI — From Generation to Supervisory Approval

**Module:** Output Governance (Post-Generation Controls)  
**Focus:** Supervisory review, compliance validation, audit-ready delivery

---

> **TL;DR**
> - **What this is:** Decision memo for post-generation governance controls before AI outputs reach customers
> - **Core thesis:** In regulated environments, "safe output" isn't just toxicity filtering — it's supervisory controls, evidence, retention, and reviewability before anything becomes a regulated communication
> - **What I designed:** Output policy enforcement + citation verification + supervisory review workflows + immutable logging + incident response paths
> - **Why it matters:** FINRA 2210 requires that communications be "fair and balanced" and reviewed by a principal before distribution — AI outputs are no exception
> - **Validation:** Aligns with existing broker-dealer supervisory requirements and SEC books-and-records obligations

---

## Problem

A financial services firm has deployed an AI assistant that passes pre-invocation governance ([Case Study #1](./Case%20Study%201%20-%20Pre-Invocation%20Governance%20as%20a%20Product%20Control.md)) and retrieves grounded content from a controlled corpus ([Case Study #3](./Case%20Study%203%20-%20Retrieval%20Architecture%20for%20Audit-Ready%20Compliance%20Workflows.md)). The model generates a response.

Now what?

The response exists. It has been generated. But it has not yet been delivered to the user. This is the last decision point before the firm creates a regulated communication.

The question isn't *"Is this response toxic?"*

It's *"Can we demonstrate that this response meets our supervisory obligations before it reaches the customer?"*

This distinction matters because:

- **AI outputs are regulated communications.** Under FINRA Rule 2210, any communication with the public — including AI-generated content — must be fair, balanced, not misleading, and supervised by a registered principal.
- **"We filtered it" is not supervision.** Toxicity filters catch egregious content. They don't verify that disclosures are present, that claims are substantiated, or that the response is appropriate for the customer's situation.
- **Post-hoc review doesn't scale.** If every AI response requires human review before delivery, you've built an expensive chatbot. But if no responses are reviewed, you've built a compliance violation.
- **The audit question is "show me the evidence."** When examiners review AI-generated communications, they don't ask "did you have good intentions?" They ask "where is the documentation showing this was supervised?"

The core failure mode is not hallucination (addressed upstream). It is **unsupervised delivery** — releasing AI-generated content to customers without the controls, evidence, and oversight that would apply to any other regulated communication.

Real-world context:

- **FINRA sweep letters (2024):** Regulators asked firms to document their supervisory procedures for AI-generated content, including how they ensure compliance with Rule 2210.
- **SEC marketing rule updates:** Emphasis on substantiation of claims and retention of supporting documentation — including for AI-assisted communications.

---

## Constraints

| Constraint | Impact on Design |
|------------|------------------|
| **FINRA 2210 supervision requirements** | All customer communications must be reviewed and approved according to firm procedures |
| **Proportional review** | Not every output needs full human review — but the decision about what gets reviewed must be defensible |
| **Real-time expectations** | Users expect conversational response times; full supervisory review adds latency |
| **Retention obligations (SEC 17a-4)** | All communications must be retained in immutable, searchable format |
| **Substantiation requirements** | Claims must be supportable; "the AI said it" is not substantiation |
| **No promissory language** | AI cannot make guarantees, promises, or forward-looking statements on behalf of the firm |
| **Disclosure completeness** | Required disclosures must be present when relevant topics arise |
| **Suitability boundaries** | AI should not provide personalized recommendations without suitability context |
| **Incident response readiness** | When something goes wrong, the firm needs a kill switch, not a committee meeting |

---

## Decision Criteria

What mattered most in this context — explicitly ranked:

| Priority | Criterion | Rationale |
|----------|-----------|-----------|
| **1** | Supervisory defensibility | If we can't demonstrate appropriate oversight, we fail the exam |
| **2** | Evidence completeness | Every delivery decision must have a documented trail |
| **3** | Proportional automation | Human review for edge cases, not every message |
| **4** | Disclosure compliance | Required disclosures must be present, verifiable, and logged |
| **5** | Incident containment | Problems must be stoppable within minutes, not days |
| **6** | Response latency | Important, but never at the expense of criteria 1–5 |

> *Supervisory defensibility means: when an examiner asks "how did you supervise this AI-generated communication?", we have a documented answer that maps to our written supervisory procedures.*

This ranking drove every downstream decision. When tradeoffs arose, we optimized up the stack.

---

## Options Considered

### Option A: Human Review of All Outputs

**Approach:**
- Queue every AI response for principal review before delivery
- Reviewer approves, edits, or rejects
- Approved responses released to customer

**Why it was rejected:**

| Failure Mode | Consequence |
|--------------|-------------|
| Doesn't scale | Human reviewers become bottleneck at any meaningful volume |
| Latency destroys UX | Users expect conversational response times, not next-day delivery |
| Reviewer fatigue | 99% of responses are routine; attention degrades |
| Cost prohibitive | Fully-supervised AI costs more than just hiring humans |

Full human review is appropriate for outbound marketing and high-risk advice. It is not viable for conversational AI at scale.

### Option B: Toxicity Filtering Only

**Approach:**
- Apply standard content safety filters (toxicity, profanity, PII)
- Pass everything else through to the customer
- Log for post-hoc audit

**Why it was rejected:**

| Failure Mode | Consequence |
|--------------|-------------|
| Filters ≠ supervision | Regulators expect supervisory procedures, not just word filters |
| No substantiation check | Claims may be unsubstantiated or misleading without being "toxic" |
| No disclosure verification | Required disclosures may be missing |
| No evidence of review | Audit shows what was blocked, not what was approved or why |

Toxicity filtering is necessary but not sufficient. It addresses safety, not supervision.

### Option C: Risk-Stratified Output Governance (Selected)

**Approach:**
Implement a multi-layer output governance system that applies proportional controls based on output characteristics:

**Key characteristics:**
- Policy-based output validation (disclosures, prohibited patterns, tone)
- Citation verification (no citation = no claim)
- Risk stratification (routine vs. elevated vs. high-risk)
- Automated approval for routine outputs with full logging
- Human review queue for elevated-risk outputs
- Structured delivery modes (approved, draft-only, refused)
- Immutable retention of all outputs and governance decisions
- Real-time monitoring and incident response triggers

**Why it won:**

| Capability | Value |
|------------|-------|
| Proportional supervision | Human attention focused where it matters |
| Documented evidence | Every output has a governance decision record |
| Policy-driven automation | Rules can be updated without code changes |
| Scales with volume | Automated approval for routine outputs |
| Incident-ready | Kill switch and rollback built into architecture |

This approach mirrors how broker-dealers already supervise communications: risk-based procedures with sampling, escalation, and documentation.

---

## Key Decisions

### Decision 1: Output Validation as a Compliance Gate

**The choice:** Treat every generated response as a candidate communication that must pass validation before delivery — not as approved content that might get filtered.

**Why this matters:** This reframes the question from:

- *"Is there anything wrong with this response?"*

to:

- *"Has this response met the conditions for supervised release?"*

The validation layer checks:

| Check | What It Validates |
|-------|-------------------|
| **Disclosure presence** | Required disclosures present when relevant topics detected |
| **Prohibited pattern scan** | No promissory language, guarantees, or forward-looking statements |
| **Citation verification** | All factual claims have supporting citations from approved sources |
| **Tone compliance** | Language is professional, balanced, not misleading |
| **Scope boundaries** | Response stays within authorized topics; no personalized advice without suitability |

**Regulatory connection:** FINRA Rule 2210 requires that communications be "fair and balanced" and include required disclosures. This validation layer operationalizes those requirements.

### Decision 2: Citation Verification as Hard Requirement

**The choice:** Any response containing a factual claim must include a citation to an approved source. No citation = claim removed or response refused.

**Implementation:**

```yaml
# output-policy.yaml
citation_requirements:
  factual_claims:
    rule: "CITATION_REQUIRED"
    action_if_missing: "REMOVE_CLAIM"
    fallback: "REFUSE_WITH_GUIDANCE"
    
  statistics:
    rule: "CITATION_REQUIRED"
    source_whitelist: ["regulatory_filings", "firm_disclosures", "approved_research"]
    action_if_missing: "REFUSE"
    
  product_information:
    rule: "CITATION_REQUIRED"
    source_whitelist: ["product_documents", "approved_marketing"]
    action_if_missing: "REFUSE"
```

**Why this matters:** 

- Substantiation is a regulatory requirement, not a nice-to-have
- "The AI said it" is not a defense in an enforcement action
- Citations create an audit trail back to approved source material
- Missing citations surface grounding failures that should be fixed upstream

**Regulatory connection:** SEC marketing rules require substantiation of material claims. Citation verification creates the documentation trail examiners expect.

### Decision 3: Risk-Stratified Review Paths

**The choice:** Not all outputs carry the same risk. Apply proportional review based on output characteristics.

| Risk Level | Characteristics | Review Path |
|------------|-----------------|-------------|
| **Routine** | General information, well-grounded, no advice, disclosures present | Automated approval with logging |
| **Elevated** | Opinion language, complex topics, near-boundary content | Supervisory sampling queue |
| **High-Risk** | Advice-adjacent, suitability-relevant, customer-specific | Human review required |
| **Prohibited** | Policy violations, missing citations, disclosure failures | Refused with structured feedback |

**Why this matters:**

- Concentrates human attention on outputs that need it
- Creates defensible sampling procedures aligned with FINRA expectations
- Automated approval is appropriate when validation checks pass
- High-risk routing prevents "advice" from slipping through without review

**Regulatory connection:** FINRA's supervision requirements allow for risk-based procedures with sampling. This stratification maps directly to that framework.

### Decision 4: Structured Delivery Modes

**The choice:** Not every output should be delivered the same way. Define explicit delivery modes:

| Mode | What Happens | When It's Used |
|------|--------------|----------------|
| `APPROVED` | Full response delivered, logged as supervised | Routine outputs passing all checks |
| `APPROVED_WITH_DISCLOSURE` | Response delivered with appended disclosure | Topics requiring specific disclosures |
| `DRAFT_ONLY` | Response shown as "draft" requiring human review | Elevated-risk content |
| `ESCALATE` | Queued for supervisory review before any delivery | High-risk or edge cases |
| `REFUSE` | Structured refusal with guidance | Policy violations or substantiation failures |

**Why this matters:** 

- "Draft only" mode lets AI assist without creating unsupervised communications
- Explicit modes are logged and auditable
- Different modes can have different retention and review requirements
- Users understand what they're getting (approved guidance vs. draft for review)

**Regulatory connection:** This mirrors how firms handle different communication types — some require pre-approval, some post-review, some sampling.

### Decision 5: Immutable Output Logging

**The choice:** Every output and governance decision is logged to an immutable store with full context:

| Field | Purpose |
|-------|---------|
| `output_id` | Unique identifier for the generated response |
| `request_id` | Link to pre-invocation decision (Case Study #1) |
| `retrieval_id` | Link to retrieval results (Case Study #3) |
| `timestamp` | When output was generated |
| `policy_version` | Which output policies were in effect |
| `validation_results` | Results of each validation check |
| `risk_classification` | How the output was stratified |
| `delivery_mode` | How the output was delivered |
| `reviewer_id` | If human reviewed, who and when |
| `customer_context` | Relevant context (anonymized as needed) |
| `full_output` | Complete generated response |
| `citations_used` | Sources cited in the response |

**Why this matters:**

- SEC 17a-4 requires retention of communications
- Immutability prevents after-the-fact modification
- Full context enables reconstruction during exams
- Links to upstream decisions (pre-invocation, retrieval) create complete audit chain

**Regulatory connection:** Books and records requirements demand that firms maintain complete, unalterable records of communications. This logging structure meets that standard.

### Decision 6: Incident Response Architecture

**The choice:** Build incident response into the system architecture, not as an afterthought:

| Capability | Implementation |
|------------|----------------|
| **Kill switch** | Immediate halt of AI responses to customers; switch to "service unavailable" |
| **Rollback** | Revert to previous policy version if new rules cause problems |
| **Quarantine** | Flag specific output patterns for review without full shutdown |
| **Notification triggers** | Automatic alerts when error rates or refusal rates spike |
| **Examiner mode** | Read-only access for regulators to review logs without production access |

**Why this matters:**

- Incidents will happen; response speed determines impact
- "We'll figure it out when it happens" is not a supervisory procedure
- Regulators expect documented incident response plans
- Kill switch is a compliance control, not just an engineering feature

**Regulatory connection:** FINRA expects firms to have supervisory procedures that include how problems are identified and addressed. Incident response is part of supervision.

---

## Architecture

### Output Governance Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                     OUTPUT GOVERNANCE LAYER                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐           │
│  │  Generated   │───▶│   Policy     │───▶│    Risk      │           │
│  │   Output     │    │  Validation  │    │ Stratification│          │
│  └──────────────┘    └──────────────┘    └──────────────┘           │
│         │                   │                   │                    │
│         │                   ▼                   ▼                    │
│         │           ┌──────────────┐    ┌──────────────┐            │
│         │           │   Output     │    │  Governance  │            │
│         │           │   Policy     │    │   Logger     │            │
│         │           │   Store      │    │              │            │
│         │           └──────────────┘    └──────────────┘            │
│         │                                      │                     │
│         ▼                                      ▼                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                     DELIVERY DECISION                        │    │
│  │  ┌─────────┐ ┌───────────┐ ┌─────────┐ ┌────────┐ ┌───────┐ │    │
│  │  │APPROVED │ │  W/DISC   │ │  DRAFT  │ │ESCALATE│ │REFUSE │ │    │
│  │  └────┬────┘ └─────┬─────┘ └────┬────┘ └───┬────┘ └───┬───┘ │    │
│  └───────┼────────────┼────────────┼──────────┼──────────┼─────┘    │
│          │            │            │          │          │          │
└──────────┼────────────┼────────────┼──────────┼──────────┼──────────┘
           │            │            │          │          │
           ▼            ▼            ▼          ▼          ▼
    ┌──────────┐  ┌──────────┐  ┌─────────┐ ┌───────┐ ┌─────────┐
    │  Direct  │  │  With    │  │  Draft  │ │ Review│ │Structured│
    │ Delivery │  │Disclosure │  │  Mode   │ │ Queue │ │ Refusal │
    └──────────┘  └──────────┘  └─────────┘ └───────┘ └─────────┘
```

### Validation Pipeline

```
                    ┌─────────────────┐
                    │Generated Output │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Disclosure    │──────▶ ADD DISCLOSURE (if missing)
                    │     Check       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Prohibited    │──────▶ REFUSE (if detected)
                    │ Pattern Scan    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Citation     │──────▶ REMOVE CLAIM or REFUSE
                    │  Verification   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     Tone &      │──────▶ FLAG FOR REVIEW
                    │ Balance Check   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     Scope       │──────▶ REFUSE (if exceeded)
                    │   Boundaries    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │      Risk       │
                    │ Classification  │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        ┌──────────┐  ┌───────────┐  ┌───────────┐
        │ ROUTINE  │  │ ELEVATED  │  │ HIGH-RISK │
        │(Auto-App)│  │(Sampling) │  │(Mandatory)│
        └──────────┘  └───────────┘  └───────────┘
```

### End-to-End Governance Chain

This case study completes the governance arc:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Case Study    │     │   Case Study    │     │   Case Study    │
│       #1        │────▶│       #3        │────▶│       #2        │
│ Pre-Invocation  │     │   Retrieval     │     │Output Governance│
│   Governance    │     │  Architecture   │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
  "Should model          "What sources           "Can we deliver
   respond at all?"      inform response?"       this response?"
```

---

## Tradeoffs Acknowledged

| We Gained | We Gave Up |
|-----------|------------|
| Supervisory defensibility for AI outputs | Added latency for validation checks |
| Documented evidence for every delivery | Storage costs for comprehensive logging |
| Proportional human review | Some outputs that "would have been fine" go to review |
| Citation-backed substantiation | Responses without sources are refused |
| Incident response capability | Engineering complexity for kill switch, rollback |
| Regulatory alignment | More conservative than pure toxicity filtering |

**The hardest tradeoff:** Risk stratification requires judgment calls about what's "routine" vs. "elevated." Set thresholds too low, and humans are overwhelmed. Set them too high, and risky outputs slip through.

This is intentional. In regulated environments:

- Calibration is ongoing, not one-time
- Sampling results inform threshold adjustment
- Conservative initial settings are appropriate
- "We're tuning based on production data" is a defensible answer

**Important assumption:** This design assumes the firm has written supervisory procedures (WSPs) that define review requirements for AI-generated content. The system implements those procedures — it doesn't replace the obligation to have them.

---

## Outcome & Validation Signals

This is portfolio work, not a production deployment. However, the design enables specific validation:

| Signal | How We'd Measure |
|--------|------------------|
| **Disclosure compliance** | % of relevant outputs with required disclosures present |
| **Citation coverage** | % of factual claims with valid citations |
| **Risk stratification accuracy** | % of elevated/high-risk outputs that actually needed review |
| **False positive rate** | % of routine outputs incorrectly escalated |
| **Review queue latency** | Time from escalation to reviewer decision |
| **Incident response time** | Time from trigger to kill switch activation |
| **Audit reconstructability** | Can any output be traced with full context? |

**Evaluation approach:** The key metric isn't "how many responses were delivered" — it's "how many deliveries can we demonstrate were appropriately supervised."

---

## Enterprise Scaling Considerations

What changes when this isn't a portfolio project but a production system at a Fortune 500 financial institution?

| Dimension | Portfolio Version | Enterprise Version |
|-----------|-------------------|-------------------|
| **Output volume** | Sample responses | Millions of daily outputs across channels |
| **Review staffing** | Conceptual queues | Dedicated supervisory teams with SLAs |
| **Policy complexity** | Single rule set | Multiple policies by business line, product, customer type |
| **Disclosure library** | Sample disclosures | Hundreds of approved disclosures by topic |
| **Integration** | Standalone | Connected to firm's compliance surveillance systems |
| **Retention** | Local logs | Enterprise archive with 7+ year retention |
| **Examiner access** | Documentation | Real-time regulatory access portals |
| **Incident response** | Documented procedure | 24/7 on-call, regulatory notification workflows |

**Key insight:** The architecture decisions (policy-driven validation, risk stratification, immutable logging) scale cleanly. What changes at enterprise scale is the operational infrastructure around the architecture.

**Ownership model:**
- **Product** owns the output governance framework and delivery modes
- **Engineering** owns system reliability, latency, and integration
- **Compliance** owns policy definitions, disclosure content, review procedures
- **Supervision** owns review queues, sampling rates, escalation decisions
- **Legal** owns regulatory interpretation and examiner response
- **Audit** owns retention requirements and evidence completeness

---

## Open Questions

Decisions I'd want to revisit with more data or stakeholder input:

1. **Risk stratification thresholds** — Where exactly is the line between routine and elevated? This requires production data and ongoing calibration based on sampling results.

2. **Sampling rates** — What percentage of "routine" outputs should be sampled for post-hoc review? FINRA expects risk-based sampling but doesn't prescribe rates.

3. **Draft mode UX** — How do we present "draft" outputs so users understand they're not approved communications? UX design matters for compliance.

4. **Reviewer tooling** — What does the supervisory review interface look like? How do we make review efficient without cutting corners?

5. **Cross-channel consistency** — If the same AI powers chat, email, and voice, how do we ensure consistent output governance across channels?

6. **Customer notification** — Should customers know when they're interacting with AI? Disclosure requirements are evolving.

---

## References

### Regulatory Guidance

- [FINRA Rule 2210: Communications with the Public](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2210) — Requirements for supervision, content standards, and approval
- [SEC Rule 17a-4: Books and Records](https://www.sec.gov/rules/final/34-38245.txt) — Retention requirements for communications
- [SR 11-7: Guidance on Model Risk Management](https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm) — Applicable to AI/ML models in financial services
- [SEC Marketing Rule (206(4)-1)](https://www.sec.gov/rules/final/2020/ia-5653.pdf) — Substantiation and retention requirements

### Industry Frameworks

- [OWASP Top 10 for LLM Applications (2025)](../regulatory-governance/ai-governance/owasp-llm-top-10.md) — LLM05: Improper Output Handling
- [NIST AI Risk Management Framework](../regulatory-governance/ai-governance/nist-ai-rmf.md) — Output validation and human oversight

### Vendor Documentation

- [Microsoft Azure Content Safety](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/) — Output filtering capabilities
- [AWS Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) — Output policy configuration

---

## Related Artifacts

- [Case Study #1: Pre-Invocation Governance](./Case%20Study%201%20-%20Pre-Invocation%20Governance%20as%20a%20Product%20Control.md)
- [Case Study #3: Retrieval Architecture](./Case%20Study%203%20-%20Retrieval%20Architecture%20for%20Audit-Ready%20Compliance%20Workflows.md)
- [Regulatory Reference: FINRA 2210](../regulatory-governance/finserv/finra-2210-communications.md)
- [Regulatory Reference: SEC 17a-4](../regulatory-governance/finserv/sec-17a-4-books-records.md)
- [Regulatory Reference: OWASP Top 10](../regulatory-governance/ai-governance/owasp-llm-top-10.md)

---

*This case study documents design decisions for a portfolio project demonstrating AI product thinking in regulated environments. It reflects governance patterns and architectural choices, not production deployment outcomes.*

---

## Why This Belongs in the Portfolio

Because in regulated AI, **generation is not delivery.**

The moment an LLM produces a response, a compliance boundary has been approached — but not yet crossed. The output governance layer is the last checkpoint before the firm creates a regulated communication.

This case study demonstrates:

- How to frame output governance as supervisory procedure, not just content filtering
- Why "safe output" in regulated environments means evidence, not just absence of toxicity
- How to design proportional review that scales without abandoning oversight
- The specific tradeoffs a senior PM navigates when supervision and latency conflict

The question that matters in exams is not *"Did you filter bad content?"*

It is *"Show me how this communication was supervised."*

This architecture provides a defensible answer.