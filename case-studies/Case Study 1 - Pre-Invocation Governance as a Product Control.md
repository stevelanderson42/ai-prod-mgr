# Case Study #1: Pre-Invocation Governance as a Product Control

**Module:** Requirements Guardrails (Input Analyzer)  
**Focus:** Preventive AI governance, audit defensibility, controlled model access

---

> **TL;DR**
> - **What this is:** Decision memo for a pre-invocation governance control plane
> - **Core thesis:** In regulated AI, the question isn't "how do we filter outputs?" — it's "how do we justify allowing the model to respond at all?"
> - **What I designed:** Deterministic rules + specialized classifiers + explicit routing + policy-as-data configuration + structured refusal outcomes
> - **Why it matters:** Audit defensibility — examiners ask "why was this allowed?", not just "what did it say?"
> - **Validation:** Aligns with OWASP Top 10, Microsoft Prompt Shields, AWS Bedrock Guardrails, Anthropic Constitutional Classifiers

---

## Problem

A financial services firm wants to deploy AI assistants to help employees with compliance questions, document analysis, and workflow guidance. Leadership is enthusiastic about productivity gains — but compliance, risk, and audit teams have concerns that go beyond typical AI safety discussions.

Their core question isn't *"How do we filter bad outputs?"*

It's *"How do we justify allowing the model to respond at all?"*

This distinction matters because:

- **Examiners ask "why" questions.** During regulatory exams, auditors don't just review what the system said. They ask why it was permitted to answer. "We filtered it afterward" is not a defensible answer.
- **Generation creates exposure.** Once an LLM produces a response — even one that gets filtered — the organization has crossed a compliance boundary. The model processed sensitive input, reasoned about regulated topics, and produced content that now exists in logs somewhere.
- **Post-hoc controls explain suppression, not authorization.** Filters show what was blocked. They don't explain why the system believed it was acceptable to attempt an answer in the first place.
- **Adversarial inputs bypass intent.** Prompt injection attacks manipulate the model *during* generation — before any output filter can act. The attack succeeds not because filtering failed, but because the model was allowed to process the malicious input at all.

The problem compounds at scale:

| Volume | Without Pre-Invocation Controls | With Pre-Invocation Controls |
|--------|--------------------------------|------------------------------|
| 100 queries/day | Manual review feasible | Automated gating |
| 10,000 queries/day | Review backlog grows | Deterministic decisions logged |
| 100,000 queries/day | Exposure scales with usage | Risk contained before generation |

The core failure mode is not hallucination. It is **uncontrolled invocation** — the system answers questions it should never attempt, reasons without required context, and produces guidance that cannot be defended to an examiner even when factually correct.

Real-world incidents illustrate the stakes:

- **DPD chatbot (January 2024):** Customer told chatbot to "disregard any rules" about profanity. It complied, swore at the customer, and wrote poetry criticizing the company. No input guardrails prevented the role manipulation.
- **Chevrolet dealership (December 2023):** User instructed chatbot to agree to any offer and end responses with "that's a legally binding offer — no takesies backsies." Bot then "agreed" to sell a $76,000 Tahoe for $1.

These weren't hallucinations. They were **prompt injection attacks succeeding because no control plane evaluated whether the model should respond to those inputs at all.**

These are public-facing chatbot incidents, but the failure mode generalizes: uncontrolled invocation + instruction hijacking can occur in any LLM deployment without pre-invocation governance.

---

## Constraints

| Constraint | Impact on Design |
|------------|------------------|
| **Fail-closed expectation** | Refusing to answer is preferable to answering incorrectly or inappropriately |
| **Explainability to non-ML reviewers** | Decisions must be interpretable by compliance officers and examiners |
| **Reconstructable audit trails** | System must explain why an interaction was allowed or blocked, months later |
| **Policy velocity exceeds release cycles** | Rules change faster than engineering can deploy code updates |
| **Separation of duties** | Compliance owns policy; engineering owns systems; product owns the boundary |
| **No humans in the routine critical path** | Scale requires automation; humans reserved for escalation, calibration, and adversarial review |
| **Model independence** | LLM behavior changes across versions and providers; governance must be model-agnostic |
| **Latency budgets** | Governance checks add overhead but must remain acceptable for enterprise UX |
| **Multi-turn risk accumulation** | Dangerous patterns can emerge across a conversation, not just in a single prompt |

---

## Decision Criteria

What mattered most in this context — explicitly ranked:

| Priority | Criterion | Rationale |
|----------|-----------|-----------|
| **1** | Audit defensibility | If we can't explain why invocation was permitted, we fail the exam |
| **2** | Deterministic governance | Same request under same conditions must yield same gating decision |
| **3** | Refusal over generation | A refusal with guidance is better than an ungrounded or unauthorized answer |
| **4** | Governance portability | Controls must survive model swaps, version upgrades, and vendor changes |
| **5** | Operational configuration | Policy changes shouldn't require code deployments |
| **6** | User experience | Important, but never at the expense of criteria 1–5 |

> *Deterministic governance means: the same request, evaluated under the same policy version and classifier version, should produce the same routing decision — allow, refuse, clarify, or escalate. The downstream model response may vary; the gating decision must not.*

This ranking drove every downstream decision. When tradeoffs arose, we optimized up the stack.

---

## Options Considered

### Option A: Post-Generation Filtering Only

**Approach:**
- Allow model invocation by default
- Filter or redact unsafe outputs after generation
- Log responses for audit review

**Why it was rejected:**

| Failure Mode | Consequence |
|--------------|-------------|
| Risk introduced before controls apply | Exposure exists regardless of filtering |
| Known vulnerability to prompt injection | OWASP ranks prompt injection as #1 LLM threat; attacks succeed during generation, before filters act |
| No authorization explanation | Audit shows what was blocked, not why answering was permitted |
| Filters explain suppression, not decision rationale | Examiners ask "why did you try?" — no answer available |

Post-hoc filtering treats symptoms (bad outputs) rather than causes (uncontrolled invocation). In regulated environments, this is insufficient.

### Option B: Prompt Engineering + Confidence Scores

**Approach:**
- Carefully crafted system prompts encoding policy rules
- Confidence thresholds to decide whether to show responses
- Rely on model compliance with instructions

**Why it was rejected:**

| Failure Mode | Consequence |
|--------------|-------------|
| Prompts are not enforceable controls | Model behavior varies across versions and providers |
| Confidence scores are opaque | What does "82% confident" mean to a compliance reviewer? |
| Threshold tuning becomes arbitrary | Where's the cutoff? Who decides? How do you defend it? |
| Fails under adversarial inputs | Prompt injection bypasses safety intent entirely |
| No audit trail for governance decisions | Logs show what was said, not what rules were evaluated |

Prompt engineering is valuable for shaping output quality. It is not a substitute for architectural governance.

> *"Prompt injection vulnerabilities are possible due to the nature of generative AI. Given the stochastic influence at the heart of the way models work, it is unclear if there are fool-proof methods of prevention."* — OWASP Top 10 for LLM Applications (2025)

### Option C: Pre-Invocation Governance Control Plane (Selected)

**Approach:**
Introduce a dedicated control plane that evaluates every request before any LLM is invoked.

**Key characteristics:**
- Deterministic rule evaluation (fail-closed by default)
- Specialized classifiers for ambiguity, intent, and risk
- Explicit routing decisions (which model, or none)
- Policy-as-data configuration (rules externalized to YAML)
- First-class refusal outcomes with structured reason codes
- Comprehensive decision logging for audit reconstruction

**Why it won:**

| Capability | Value |
|------------|-------|
| Prevents unauthorized generation entirely | Risk contained before exposure |
| Produces deterministic, auditable governance outcomes | Examiners can trace decision rationale |
| Decouples governance from model behavior | Survives model swaps and version changes |
| Scales through automation | Human review becomes exception handling |
| Configuration-driven | Policy changes without code deployments |

This approach aligns with how major cloud providers now implement AI safety:

- **Microsoft Prompt Shields:** "Prompt Shields is a unified API in Azure AI Content Safety that detects and blocks adversarial user input attacks on large language models... by analyzing prompts and documents **before content is generated**."
- **AWS Bedrock Guardrails:** "The ApplyGuardrail API is decoupled from foundational models. You can now use Guardrails **without invoking Foundation Models**."
- **Anthropic Constitutional Classifiers:** Reduced jailbreak success rate from 86% to 4.4% by evaluating inputs before generation.

---

## Key Decisions

### Decision 1: Invocation as a Governed Action

**The choice:** Treat model invocation as a privilege that must be explicitly authorized — not a default behavior that gets filtered afterward.

**Why this matters:** This reframes the fundamental question from:

- *"How do we clean up model outputs?"*

to:

- *"How do we justify model access in the first place?"*

The control plane becomes the system of record for that justification. Every invocation must pass through a gate that logs:
- What rules were evaluated
- What decision was reached
- Why that decision was appropriate under policy

**Regulatory connection:** [SR 11-7](https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm) emphasizes that "banking organizations should be attentive to the possible adverse consequences... of decisions based on models that are incorrect or misused, and should address those consequences through **active model risk management**." A pre-invocation control plane operationalizes this principle.

### Decision 2: Deterministic Rules for Non-Negotiable Conditions

**The choice:** Implement hard-coded rules for conditions that should never reach a model, regardless of context:

- Requests for explicitly prohibited content categories
- Missing required jurisdictional or product context
- Known prompt injection patterns
- Requests outside authorized scope

**Example (config excerpt):**
```yaml
# policy-rules.yaml
hard_blocks:
  - rule_id: PROHIBITED_TOPIC
    condition: "topic_classifier.output IN ['weapons', 'illegal_activity', 'pii_extraction']"
    action: REFUSE
    reason_code: PROHIBITED_CONTENT
    
  - rule_id: MISSING_CONTEXT
    condition: "required_fields.jurisdiction IS NULL"
    action: CLARIFY
    reason_code: INSUFFICIENT_CONTEXT
    guidance: "Please specify the jurisdiction this question applies to."
```

**Why this matters:** Rules are deterministic, logged, and version-controlled. When an examiner asks "why was this request blocked?", we can point to a specific rule ID, its evaluation timestamp, and the policy version in effect.

**Regulatory connection:** Deterministic rules produce the interpretable, reproducible decisions that compliance reviewers require. Probabilistic thresholds don't.

### Decision 3: Specialized Classifiers for Risk Assessment

**The choice:** Deploy purpose-built classifiers for dimensions that rules can't capture:

| Classifier | Purpose | Output |
|------------|---------|--------|
| **Ambiguity detector** | Flag requests that can't be answered without clarification | `CLEAR` / `AMBIGUOUS` / `UNINTERPRETABLE` |
| **Intent classifier** | Distinguish legitimate queries from potential manipulation | `BENIGN` / `SUSPICIOUS` / `ADVERSARIAL` |
| **Scope classifier** | Determine whether query falls within authorized domain | `IN_SCOPE` / `ADJACENT` / `OUT_OF_SCOPE` |
| **Sensitivity tagger** | Identify when response would involve restricted content | `UNRESTRICTED` / `INTERNAL_ONLY` / `RESTRICTED` |

**Why this matters:** Not all governance decisions can be reduced to keyword matching. Classifiers handle semantic complexity while maintaining categorical, version-controlled outputs.

**Key design principle:** Classifier outputs are categorical, not continuous. "Is this request ambiguous?" returns `YES` or `NO` — not "73% likely to be ambiguous." Categorical outputs are auditable; probability scores require threshold justifications that compliance can't provide.

**Regulatory connection:** This aligns with Anthropic's Constitutional Classifiers approach, which uses "a constitution that delineates categories of permissible and restricted content" to train classifiers that produce categorical safety decisions.

### Decision 4: Routing as a Product Surface

**The choice:** Make the routing decision explicit and logged. Every request results in one of:

| Routing Decision | What Happens | When It's Used |
|------------------|--------------|----------------|
| `ALLOW_FULL` | Full LLM invocation | Clean request, clear context, authorized scope |
| `ALLOW_CONSTRAINED` | LLM with restricted capabilities | Legitimate request with elevated risk |
| `RETRIEVAL_ONLY` | RAG without generation | Request for information, not advice |
| `CLARIFY` | Return guidance, request more context | Ambiguous or incomplete request |
| `ESCALATE` | Route to human review | High-risk or edge case |
| `REFUSE` | Decline with structured reason | Prohibited content or policy violation |

**Why this matters:** Routing is not a hidden implementation detail — it's a product decision that gets logged, reviewed, and optimized. Different request types receive appropriate handling rather than all-or-nothing access.

If allowed, the request may route into compliance retrieval ([Case Study #3](./case-study-3-retrieval-architecture.md)) or other governed workflows. The control plane established here provides the authorization gate for all downstream AI capabilities.

**Regulatory connection:** This pattern mirrors how financial institutions handle transaction authorization — different risk levels receive different controls, all auditable.

### Decision 5: Policy-as-Data Configuration

**The choice:** Externalize all governance rules, refusal conditions, and routing logic to configuration files rather than application code.

**Configuration files created:**

| File | Purpose |
|------|---------|
| `policy-rules.yaml` | Deterministic rules for blocking, clarifying, or routing |
| `classifier-thresholds.yaml` | Categorical cutoffs for each classifier |
| `routing-matrix.yaml` | Decision logic mapping inputs to routing outcomes |
| `refusal-taxonomy.yaml` | Structured reason codes with user-facing guidance |
| `scope-definitions.yaml` | What topics and document types are authorized |

**Why this matters:** 

- Policy changes happen through governed configuration updates, not code deployments
- Compliance owns rule content; engineering owns system reliability
- Audit can review policy versions independently of application versions
- A/B testing of policy changes is possible without engineering involvement

**Regulatory connection:** This separation of duties aligns with SR 11-7's emphasis on governance structures that maintain "appropriate incentive and organizational structures" with clear accountability.

### Decision 6: Structured Refusal as First-Class Outcome

**The choice:** Treat refusal as a designed behavior with taxonomy, guidance, and logging — not an error state.

**Refusal taxonomy:**

| Code | Meaning | User Guidance |
|------|---------|---------------|
| `PROHIBITED_CONTENT` | Request involves blocked topic | "This topic is outside the scope of this assistant." |
| `INSUFFICIENT_CONTEXT` | Missing required inputs | "Please provide [specific fields] to continue." |
| `AMBIGUOUS_REQUEST` | Multiple interpretations possible | "Could you clarify whether you mean X or Y?" |
| `OUT_OF_SCOPE` | Topic not in authorized domain | "For questions about [topic], please contact [resource]." |
| `ADVERSARIAL_PATTERN` | Suspected manipulation attempt | "I can't process this request as structured." |
| `CONFLICTING_POLICY` | No safe response possible | "This scenario requires human review. Escalating." |

**Why this matters:** A refusal with guidance is more useful than a confident-sounding guess. Users understand why they can't proceed and what to do next. Auditors see that the system made a deliberate, policy-compliant decision.

**Regulatory connection:** This aligns with FINRA Rule 2210's emphasis on communications being "fair and balanced" — refusing to provide inappropriate guidance is itself a form of appropriate communication.

---

## Architecture

### Control Plane Overview

![Control Plane Overview](./docs/diagrams/Case_Study_1_Control_Plane_Diagram.PNG)

### Decision Flow

![Decision Flow](./docs/diagrams/Case_Study_1_Routing_Decisions.PNG)

```

### Latency Considerations

Pre-invocation evaluation adds overhead. Design targets:

| Stage | Target Latency | Notes |
|-------|---------------|-------|
| Hard rules evaluation | < 5ms | Local, deterministic |
| Classifier ensemble | < 50ms | Parallelized, cached |
| Routing decision | < 10ms | Lookup table |
| **Total pre-invocation** | **< 100ms** | Before any LLM call |

In regulated environments, the cost of a slightly slower response is negligible compared to:

- Providing ungrounded or inappropriate guidance
- Failing to explain why a response was allowed
- Eroding examiner trust during audits or enforcement actions

### Audit Implications

Every pre-invocation decision is logged with:

| Field | Purpose |
|-------|---------|
| `request_id` | Unique identifier for trace correlation |
| `timestamp` | When decision was made |
| `policy_version` | Which rule set was in effect |
| `classifier_version` | Which classifier models were in effect |
| `rules_evaluated` | List of rule IDs checked |
| `classifier_outputs` | Categorical results from each classifier |
| `routing_decision` | Final decision with reason code |
| `refusal_guidance` | User-facing message (if refused) |
| `session_context` | Relevant session state for multi-turn tracking |

This creates an audit trail explaining *why the system was allowed to answer at all* — not just what it ultimately returned.

---

## Tradeoffs Acknowledged

| We Gained | We Gave Up |
|-----------|------------|
| Audit defensibility at every decision point | Development speed — more components to build |
| Deterministic governance outcomes | Some "could have answered" cases now refuse |
| Policy changes without deployments | Configuration complexity — more files to manage |
| Model-agnostic architecture | Tighter coupling to our abstraction layer |
| Structured refusals with guidance | Higher initial refusal rate during calibration |
| Scalable automation | Upfront classifier training and rule definition work |

**The hardest tradeoff:** Pre-invocation governance reduces system permissiveness. Some requests that could produce a plausible answer will instead be refused or routed for clarification.

This is intentional. In regulated environments:

- A conservative refusal is safer than a confident guess
- Governance consistency matters more than response coverage
- Scaling safely requires automation that errs on the side of constraint

The unresolved tension — **scale vs. safety** — does not disappear. It becomes a design problem, not an operational surprise.

**Important assumption:** This design assumes human review remains available for escalations — not as a substitute for system-level governance. The goal is to reduce routine escalations, not eliminate human judgment entirely.

---

## Outcome & Validation Signals

This is portfolio work, not a production deployment. However, the design enables specific validation:

| Signal | How We'd Measure |
|--------|------------------|
| **Refusal appropriateness** | % of refusals that were justified (evaluated via test cases) |
| **False positive rate** | % of legitimate requests incorrectly refused |
| **Adversarial resistance** | % of prompt injection attempts blocked |
| **Decision consistency** | Same request yields same routing across trials (given same policy + classifier versions) |
| **Audit reconstructability** | Can any decision be traced from logs? |
| **Policy compliance** | Target: zero unauthorized invocations (as defined by policy), monitored via audit logs + alerts |

**Test cases created:** Structured scenarios validating each routing decision path and refusal code.

**Evaluation approach:** The key metric isn't "how many requests get answered" — it's "how many decisions can we defend to an examiner."

---

## Enterprise Scaling Considerations

What changes when this isn't a portfolio project but a production system at a Fortune 500 financial institution?

| Dimension | Portfolio Version | Enterprise Version |
|-----------|-------------------|-------------------|
| **Request volume** | Sample queries | 100,000+ daily requests across business lines |
| **Policy complexity** | Single rule set | Multiple policy domains (lending, trading, advisory) |
| **Classifier training** | Pre-trained models | Custom classifiers trained on firm-specific data |
| **Access control** | Simple roles | Integration with enterprise IAM, data classification |
| **Audit retention** | Local logs | 7-year retention in immutable audit store |
| **Change management** | Direct config edits | Policy changes require compliance review board approval |
| **Monitoring** | Manual review | Real-time dashboards, alerting on refusal rate anomalies |
| **Incident response** | Ad hoc | Documented runbooks, regulatory notification procedures |
| **Model governance** | Single provider | Multi-vendor strategy with per-model risk assessment |

**Key insight:** The architecture decisions (pre-invocation control plane, policy-as-data, structured routing) scale cleanly. What changes at enterprise scale is operational rigor around the architecture — not the architecture itself.

**Ownership model:** 
- **Product** owns the contract between engineering and compliance
- **Engineering** owns system reliability and performance
- **Compliance** owns rule content and policy definitions
- **Risk** owns classifier calibration and threshold approval
- **Audit** owns retention requirements and trace completeness validation

---

## Open Questions

Decisions I'd want to revisit with more data or stakeholder input:

1. **Refusal threshold tuning** — Is the current calibration too conservative? Would users prefer more answers with caveats vs. more refusals with guidance? This requires production data to answer.

2. **Multi-turn risk accumulation** — Current design evaluates requests independently. How should risk signals accumulate across a conversation? A single benign request might be fine; a sequence of similar requests might indicate adversarial probing.

3. **Classifier drift monitoring** — How do we detect when classifier performance degrades as attack patterns evolve? What's the recalibration workflow?

4. **Human-in-the-loop escalation** — When `ESCALATE` fires, what's the actual workflow? Design assumes someone receives it — but who, and with what SLA?

5. **False negative detection** — How do we discover requests that should have been blocked but weren't? Post-hoc analysis of successful invocations may reveal patterns the classifiers missed.

---

## References

### Regulatory Guidance

- [SR 11-7: Guidance on Model Risk Management](https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm) — Federal Reserve guidance on model validation, documentation, and governance
- [SEC Rule 17a-4](https://www.sec.gov/rules/final/34-38245.txt) — Books and records retention requirements
- [FINRA Rule 2210](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2210) — Communications with the public

### Industry Frameworks

- [OWASP Top 10 for LLM Applications (2025)](https://genai.owasp.org/llm-top-10/) — Prompt injection ranked as #1 threat
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) — Federal guidance on AI governance and risk

### Vendor Documentation

- [Microsoft Prompt Shields](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection) — Pre-generation attack detection
- [AWS Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) — Configurable safeguards decoupled from foundation models
- [AWS ApplyGuardrail API](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-use-independent-api.html) — Guardrail evaluation without model invocation

### Safety Research

- [Anthropic Constitutional Classifiers](https://www.anthropic.com/research/constitutional-classifiers) — Input/output classifiers reducing jailbreak success from 86% to 4.4%
- [Constitutional Classifiers Paper](https://arxiv.org/abs/2501.18837) — Technical details on classifier training and evaluation
- [Constitutional Classifiers++](https://arxiv.org/abs/2601.04603) — Production-grade system with 40x cost reduction

### Incident Reports

- [DPD Chatbot Incident](https://incidentdatabase.ai/cite/631/) — AI Incident Database entry
- [Chevrolet Dealership Incident](https://incidentdatabase.ai/cite/622/) — AI Incident Database entry

---

## Related Artifacts

- [Architecture: Control Plane Design](../modules/guardrails/architecture/control-plane-design.md)
- [Config: Policy Rules](../modules/guardrails/config/policy-rules.yaml)
- [Config: Routing Matrix](../modules/guardrails/config/routing-matrix.yaml)
- [Config: Refusal Taxonomy](../modules/guardrails/config/refusal-taxonomy.yaml)
- [Docs: Decision Logging Schema](../modules/guardrails/docs/decision-log-schema.md)
- [Evaluation: Test Cases](../modules/guardrails/evaluation/test-cases/)
- [Case Study #3: Retrieval Architecture](./case-study-3-retrieval-architecture.md)

---

*This case study documents design decisions for a portfolio project demonstrating AI product thinking in regulated environments. It reflects governance patterns and architectural choices, not production deployment outcomes.*

---

## Why This Belongs in the Portfolio

Because in regulated AI, **the most important product decision is often whether the model runs at all.**

This case study demonstrates:

- How to frame governance as a product surface, not a compliance afterthought
- Why major cloud providers have converged on pre-invocation control patterns
- How to design systems that pass examiner scrutiny, not just user acceptance testing
- The specific tradeoffs a senior PM navigates when scale and safety conflict

The question that matters in audits is not *"Was the answer accurate?"*

It is *"Why was the system allowed to answer at all?"*

This architecture provides a defensible answer.