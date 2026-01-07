# Case Study #3: Retrieval Architecture for Audit-Ready Compliance Workflows

**Module:** Compliance Retrieval Assistant  
**Focus:** Governance-first design, auditability, regulated AI deployment

---

## Problem

A financial services compliance team needs to answer policy questions quickly and accurately. They currently rely on manual document searches, institutional knowledge, and escalation to senior staff — a process that's slow, inconsistent, and doesn't scale.

An AI-powered retrieval assistant could help, but the environment creates unique challenges:

- **Answers must be defensible.** When a compliance officer cites a policy in a regulatory exam, they need to know exactly where that answer came from.
- **Wrong answers have consequences.** Unlike a customer service chatbot, incorrect compliance guidance can lead to regulatory violations, fines, or enforcement actions.
- **Auditors will ask questions.** Any AI system touching compliance workflows will eventually face questions from internal audit, external examiners, or regulators.

The core question wasn't *"Can we build a RAG system?"* — it was *"Can we build one that compliance and audit will trust when it matters — during an exam or enforcement review?"*

---

## Constraints

| Constraint | Impact on Design |
|------------|------------------|
| **Regulatory scrutiny** | Every answer must be traceable to approved source documents |
| **No tolerance for hallucination** | System must refuse rather than guess |
| **Multiple stakeholders** | End users want answers; auditors want evidence trails |
| **Policy changes frequently** | Corpus must be versioned; stale content must be excluded |
| **Role-based access** | Not all users can see all content (sensitivity tiers) |
| **Model uncertainty** | Underlying LLM will change; design must survive model swaps |

---

## Decision Criteria

What mattered most in this context — explicitly ranked:

| Priority | Criterion | Rationale |
|----------|-----------|-----------|
| **1** | Audit defensibility | If we can't explain a decision to an examiner, it doesn't ship |
| **2** | Deterministic behavior | Reviewers need consistent interpretation across interactions |

> *Deterministic behavior means: the same question, asked under the same conditions, should produce the same grounding status and refusal outcome — even if the generated text varies slightly.*
| **3** | Refusal over guessing | A "no answer" is better than a wrong answer in compliance contexts |
| **4** | Operational governance | Rules must be changeable without code deployments |
| **5** | User experience | Important, but not at the expense of criteria 1-4 |

This ranking drove every downstream decision. When tradeoffs arose, we optimized up the stack.

---

## Options Considered

### Option A: Standard RAG Implementation
- Retrieve chunks, pass to LLM, return response
- Confidence scores on outputs
- Minimal guardrails

**Rejected because:** No audit trail. Confidence scores are meaningless to compliance reviewers. No mechanism to refuse when grounding is insufficient.

### Option B: RAG + Post-Hoc Filtering
- Standard RAG pipeline
- Add output filters for prohibited content
- Log responses for audit

**Rejected because:** Filtering happens after generation — the model still produces problematic content, we just hide it. Doesn't address grounding quality. Audit trail shows what was blocked, not why the system was confident in what it returned.

### Option C: Governance-First Architecture (Selected)
- Pre-invocation control layer (decide whether to call the LLM at all)
- Categorical grounding status (not confidence scores)
- Dual response contracts (user-facing + auditor-facing)
- Policy-as-data configuration (rules externalized to YAML)
- Structured refusal taxonomy

**Selected because:** Audit defensibility is built in, not bolted on. Every decision point is logged. Refusal is a first-class outcome. Configuration changes don't require code deployments.

---

## Key Decisions

### Decision 1: Categorical Grounding Status (Not Confidence Scores)

**The choice:** Replace probabilistic confidence scores with categorical grounding status: `FULLY_GROUNDED`, `PARTIALLY_GROUNDED`, `UNGROUNDED`, `REFUSED`.

**Why this matters:** Confidence scores (e.g., "82% confident") are intuitive for ML engineers but meaningless for compliance reviewers. What does 82% mean? Is 78% acceptable? Where's the threshold?

Categorical status forces binary clarity:
- `FULLY_GROUNDED` = every claim traces to retrieved content
- `REFUSED` = system declined to answer (with a specific reason code)

**Regulatory connection:** SR 11-7 principles emphasize that model outputs should be interpretable by reviewers who are accountable for decisions but not responsible for model design. Categorical status achieves this; confidence scores don't.

### Decision 2: Dual Response Contracts (User + Auditor)

**The choice:** Design two response schemas — one optimized for the end user, one optimized for audit/compliance review.

**User contract includes:**
- Answer text with inline citations
- Grounding status
- Suggested follow-up actions (if refused or partial)

**Auditor contract includes:**
- Everything in user contract
- Full retrieval trace (query → chunks → ranking → selection)
- Policy rules evaluated
- Refusal reason codes
- Timestamps and session identifiers

**Why this matters:** Users need usable answers. Auditors need reconstructable decision trails. Optimizing for one audience degrades the other. Dual contracts serve both without compromise.

**Regulatory connection:** SEC 17a-4 requires that records be "readily accessible" and "reproducible." The auditor contract is designed so that any interaction can be reconstructed months later.

### Decision 3: Policy-as-Data (Externalized Configuration)

**The choice:** Define all policy rules, refusal conditions, and access controls in YAML configuration files — not hardcoded in application logic.

**Configuration files created:**
- `refusal-taxonomy.yaml` — When and why the system refuses
- `policy-constraints.yaml` — Prohibited phrases, required disclaimers, topic restrictions
- `role-permissions.yaml` — Who can access which content tiers
- `corpus-registry.yaml` — What content is approved for retrieval

**Why this matters:** Compliance requirements change. New prohibited phrases get added. Access policies shift. If these rules live in code, every change requires a deployment, QA cycle, and release. If they live in configuration, policy teams can update rules through governed change management — without engineering tickets.

**Operational benefit:** Separating policy from code also clarifies accountability. Engineering owns the system; compliance owns the rules.

### Decision 4: Structured Refusal as First-Class Outcome

**The choice:** Treat refusal as a designed behavior, not an error state. Create a taxonomy of refusal reasons with severity levels and user guidance.

**Refusal codes include:**
- `NO_ELIGIBLE_DOCS` — Query outside corpus scope
- `INSUFFICIENT_GROUNDING` — Found content, but not enough to answer reliably
- `POLICY_BLOCKED` — User lacks access or query violates constraints
- `AMBIGUOUS_QUERY` — Can't determine intent; clarification needed
- `CONFLICTING_SOURCES` — Sources disagree; escalation required

**Why this matters:** Most RAG implementations treat "I don't know" as a failure. In compliance contexts, refusing to answer is often the *correct* behavior. A structured taxonomy makes refusals:
- Predictable (same conditions → same refusal)
- Actionable (user knows what to do next)
- Auditable (reviewer knows why the system declined)

---

## Tradeoffs Acknowledged

| We Gained | We Gave Up |
|-----------|------------|
| Audit defensibility at every decision point | Development speed — more components to build |
| Deterministic refusal behavior | Some "could have answered" cases now refuse |
| Policy changes without deployments | Configuration complexity — more files to manage |
| Dual-audience optimization | Response payload size (auditor trace is verbose) |
| Model-portable architecture | Tighter coupling to our abstraction layer |

**Important assumption:** This design assumes human review remains available for escalations — not as a substitute for system-level governance. The goal is to reduce routine escalations, not eliminate human judgment.

**The hardest tradeoff:** Categorical grounding means some queries that *could* get a "pretty good" answer will instead get a refusal. We accepted this because in compliance contexts, "pretty good" isn't good enough — and a refusal with guidance is more useful than a confident-sounding guess.

---

## Outcome & Validation Signals

This is portfolio work, not a production deployment. However, the design enables specific validation:

| Signal | How We'd Measure |
|--------|------------------|
| **Refusal appropriateness** | % of refusals that were justified (evaluated via test cases) |
| **Grounding accuracy** | % of citations that correctly reference source passages |
| **Trace completeness** | Can any interaction be reconstructed from logs? |
| **Policy compliance** | Zero prohibited phrases in outputs; required disclaimers present |
| **Reviewer trust** | Qualitative: Would a compliance officer trust this output? |

**Test cases created:** Five structured scenarios validating each refusal code path (see `/evaluation/test-cases/`).

**Evaluation scorecard:** Six-dimension rubric for assessing output quality (see `/evaluation/scorecard.md`).

---

## Enterprise Scaling Considerations

What changes when this isn't a portfolio project but a production system at a Fortune 500 financial institution?

| Dimension | Portfolio Version | Enterprise Version |
|-----------|-------------------|-------------------|
| **Corpus size** | Sample documents | 10,000+ policy documents across business lines |
| **User base** | Single user | 5,000+ compliance staff across regions |
| **Access control** | Simple role tiers | Integration with enterprise IAM (Active Directory, Okta) |
| **Audit retention** | Local logs | 7-year retention in immutable audit store |
| **Model hosting** | OpenAI API | Private endpoint (Azure OpenAI, AWS Bedrock) for data sovereignty |
| **Change management** | Direct config edits | Policy changes go through compliance review board |
| **Monitoring** | Manual review | Real-time dashboards, alerting on refusal rate spikes |
| **Incident response** | Ad hoc | Documented runbooks, on-call rotation, regulatory notification procedures |

**Key insight:** The architecture decisions (dual contracts, policy-as-data, structured refusals) scale cleanly. What changes at enterprise scale is operational rigor around the architecture — not the architecture itself.

**Ownership model:** Product owns the contract between engineering and compliance, ensuring governance rules remain enforceable without becoming implementation-specific. Engineering owns system reliability; compliance owns rule content; product owns the boundary.

---

## Open Questions

Decisions I'd want to revisit with more data or stakeholder input:

1. **Refusal threshold tuning** — Is `PARTIALLY_GROUNDED` too conservative? Would users prefer more answers with caveats vs. more refusals with guidance?

2. **Confidence as secondary signal** — Should auditor traces include probabilistic scores even if user responses don't? Could be useful for model monitoring without affecting UX.

3. **Multi-turn context** — Current design is single-turn. How would grounding status work across a conversation where context accumulates?

4. **Human-in-the-loop escalation** — When `CONFLICTING_SOURCES` fires, what's the actual escalation workflow? Design assumes someone receives it — but who, and how?

---

## Related Artifacts

- [Architecture: Component Design](../modules/rag-assistant/architecture/component-design.md)
- [Config: Refusal Taxonomy](../modules/rag-assistant/config/refusal-taxonomy.yaml)
- [Config: Policy Constraints](../modules/rag-assistant/config/policy-constraints.yaml)
- [Docs: Response Contract](../modules/rag-assistant/docs/response-contract.md)
- [Docs: Trace Schema](../modules/rag-assistant/docs/trace-schema.md)
- [Evaluation: Scorecard](../evaluation/scorecard.md)
- [Evaluation: Test Cases](../modules/rag-assistant/evaluation/test-cases/)

---

*This case study documents design decisions for a portfolio project demonstrating AI product thinking in regulated environments. It reflects governance patterns and architectural choices, not production deployment outcomes.*