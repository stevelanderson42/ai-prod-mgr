# Requirements Guardrails — Heuristics v0.1

## Purpose

Define the pre-invocation checks that mitigate risk before an AI model 
is called in a regulated FinServ workflow.

This module sits between user input and model invocation, acting as a 
"pre-flight checklist" that:
- Identifies queries requiring human review
- Flags compliance triggers before they become violations
- Reduces ambiguity that leads to unreliable responses
- Routes requests to appropriate handling paths

---

## Non-Goals / Explicit Exclusions

This module does NOT:
- **Determine suitability** — That requires full client profile, risk tolerance, 
  and fiduciary analysis that only a licensed advisor can perform
- **Generate investment recommendations** — All recommendation requests are 
  escalated, never answered
- **Provide tax or legal advice** — These queries are redirected with explanation
- **Replace compliance review** — This is a pre-filter, not a compliance determination
- **Evaluate model output quality** — That's a separate post-invocation concern

**Why document non-goals:**
Scope creep in AI systems creates liability. Explicitly stating boundaries 
prevents misuse and demonstrates mature product thinking.

---

## Risk Categories

### 1. Suitability Risk
**Definition:** Query implies personalized financial advice that requires 
understanding of the user's full financial picture.

**Topic labels that trigger:** `suitability`, `retirement` (when combined with action verbs)

**Trigger patterns:**
- "Should I..." + investment action
- "What's best for my situation"
- "Is this suitable for..."
- Requests for recommendations without stated constraints

**Why this matters:**
Reg BI and suitability requirements mean personalized advice without proper 
context creates regulatory exposure. The model cannot know if advice is 
suitable without information it doesn't have.

**Guardrail action:** ESCALATE to human advisor

---

### 2. Compliance Risk
**Definition:** Query contains language that could trigger FINRA 2210 
violations if repeated in a response.

**Trigger patterns:**
- Absolute promises: "guarantee," "definitely," "can't lose"
- Unsubstantiated claims: "best performing," "top rated" without citation
- Misleading comparisons: Selective timeframes, cherry-picked data
- Performance predictions: "will go up," "always makes money"

**Why this matters:**
FINRA 2210 governs communications with the public. AI-generated content 
is subject to the same review requirements as human-written content.

**Guardrail action:** BLOCK and request rephrasing

---

### 3. Ambiguity Risk
**Definition:** Query lacks sufficient context for a reliable response.

**Trigger patterns:**
- Pronoun references without antecedent: "it," "that," "the thing"
- Missing timeframes: "recently," "a while ago"
- Unclear scope: "my account" without specification
- Assumed context: "like we discussed," "the usual"

**Why this matters:**
Ambiguous queries lead to hallucinated context. The model will guess 
rather than ask for clarification, creating unreliable outputs.

**Guardrail action:** CLARIFY before proceeding

---

### 4. Out-of-Scope Risk
**Definition:** Query cannot be answered from approved sources or falls 
outside the assistant's designated domain.

**Topic labels that trigger:** `competitor`, `tax`, `legal`, `current_events`

**Trigger patterns:**
- Competitor questions: "What does Fidelity offer?"
- Tax advice: "What are the tax implications?"
- Legal questions: "Is this legal in my state?"
- Current events: "What happened in the market today?"

**Why this matters:**
Responses outside the approved corpus risk hallucination and 
institutional liability.

**Guardrail action:** REDIRECT with explanation

---

## Classification Logic

### Two-Step Classification Approach

**Step 1: Topic Classification**
Determine what the query is ABOUT before assessing risk.

| Topic Label | Description | Example |
|-------------|-------------|---------|
| `account` | Account info, transactions, history | "What were my last 3 trades?" |
| `retirement` | 401k, IRA, pension questions | "What's my 401k balance?" |
| `suitability` | Advice, recommendations, "should I" | "Should I sell my stocks?" |
| `general` | Hours, holidays, basic info | "When does the market close?" |
| `competitor` | Questions about other firms | "What does Vanguard charge?" |
| `tax` | Tax implications, IRS rules | "Is this tax deductible?" |
| `legal` | Legal questions, state laws | "Is this legal in California?" |
| `unknown` | Cannot be classified | Ambiguous or novel queries |

**Step 2: Risk Assessment**
Based on topic + content, determine action.

| Condition | Action | Routing |
|-----------|--------|---------|
| Suitability triggers detected | ESCALATE | Human advisor queue |
| Compliance violation language | BLOCK | Compliance review |
| High ambiguity (2+ indicators) | CLARIFY | Request more context |
| Out-of-scope topic | REDIRECT | Explain limitation + suggest alternative |
| None of the above | PROCEED | Standard processing with guardrails |

### Decision Flow
```
1. Classify topic
2. Check for BLOCK triggers (compliance) → Stop immediately
3. Check for ESCALATE triggers (suitability) → Route to human
4. Check for REDIRECT triggers (out of scope) → Explain limitation
5. Check for CLARIFY triggers (ambiguity) → Request context
6. If none triggered → PROCEED with standard guardrails
```

### Current Limitations
- Keyword-based matching misses contextual nuance
- No semantic understanding of intent
- False positives on legitimate educational queries
- Cannot detect sarcasm or hypotheticals
- Single-turn only — no conversation history awareness

[Add limitations discovered in Python exercise]

---

## Escalation Triggers

| Condition | Action | Routing | SLA |
|-----------|--------|---------|-----|
| Suitability keywords + account context | ESCALATE | Human advisor queue | 4 hours |
| Compliance violation language | BLOCK | Compliance review | Immediate |
| 2+ ambiguity indicators | CLARIFY | Request more context | Immediate |
| Out-of-scope topic detected | REDIRECT | Explain + suggest alternative | Immediate |
| Confidence < threshold | FLAG | Add disclaimer to response | Immediate |
| Repeated escalations (3+ in session) | ESCALATE | Supervisor review | 1 hour |

---

## Logging & Audit Fields

Every guardrail invocation must log the following for SR 11-7 compliance 
and 17a-4 recordkeeping:

| Field | Description | Example |
|-------|-------------|---------|
| `timestamp` | UTC timestamp of classification | 2025-12-15T14:32:01Z |
| `session_id` | Unique session identifier | sess_abc123 |
| `query_hash` | Hash of original query (PII protection) | sha256:7f3a... |
| `topic_label` | Classified topic | suitability |
| `risk_scores` | Risk levels by category | {suit: high, comp: low, amb: low} |
| `triggered_rules` | Which rules fired | [SUIT_001, SUIT_003] |
| `action` | Final decision | escalate |
| `model_version` | Classifier version | guardrails_v0.1 |
| `override` | Was decision overridden? | false |
| `override_by` | Who overrode (if applicable) | null |

**Retention:** Per 17a-4, logs must be retained for 6 years.

**Access:** Compliance and audit teams only.

---

## Regulatory Anchors

### FINRA Rule 2210 (Communications with the Public)
- All communications must be fair, balanced, and not misleading
- Applies to AI-generated content equally
- **Guardrail implementation:** Block absolute claims, require balanced presentation

### SEC Regulation Best Interest (Reg BI)
- Recommendations must be in client's best interest
- Requires reasonable basis and customer-specific suitability
- **Guardrail implementation:** Escalate personalized advice requests

### Model Risk Management (SR 11-7)
- Models must be validated before deployment
- Ongoing monitoring required
- Documentation of model behavior mandatory
- **Guardrail implementation:** Log all invocations, track override rates, version control

### Books & Records (17a-4)
- Communications must be preserved in non-rewritable format
- 6-year retention requirement
- **Guardrail implementation:** Immutable audit trail for all interactions

---

## Connection to AI Query Sequence

This section aligns with the **FinServ AI Query Lifecycle** sequence diagrams and supporting explanations in my public Notion portfolio:

[View FinServ AI Query Lifecycle →](https://www.notion.so/stevelanderson42/FinServ-AI-Query-Lifecycle-2bea7858746d809c86acdd89cd9f7e86?source=copy_link)

### Phase 1 — Context Assembly
Guardrails apply at:
- **Query receipt:** Initial topic classification
- **Context validation:** Ambiguity detection

Key checks:
- Is the query clear enough to proceed?
- What topic domain does this fall into?

### Phase 2 — Reasoning  
Guardrails apply at:
- **Pre-inference validation:** Risk assessment before model call

Key checks:
- Does this trigger suitability escalation?
- Does this contain compliance violations?
- Is this in-scope for the assistant?

### Phase 3 — Execution & Synthesis
Guardrails apply at:
- **Post-inference validation:** Output checking (separate module)

Key checks:
- Are citations present and valid?
- Does response contain prohibited language?
- Is uncertainty appropriately flagged?

---

## Evidence: Prompt Experiments

The following experiments from Week 1 informed this heuristics design:

### Experiment 01: Suitability Classification
**Finding:** Vague classification prompts produce inconsistent results. 
Structured output + explicit label definitions = reliable classification.

**Applied to guardrails:** Topic classification uses explicit category definitions.

### Experiment 02: Compliance Rewrite  
**Finding:** "Be compliant" is too vague. Specific rewrite rules 
(remove guarantees, remove predictions) produce reliable results.

**Applied to guardrails:** Compliance triggers are specific patterns, not concepts.

### Experiment 04: Ambiguity Detection
**Finding:** The model can identify when a request is unclear and generate 
appropriate clarifying questions.

**Applied to guardrails:** Ambiguity detection as pre-check before proceeding.

### Experiment 05: Grounded Citation
**Finding:** Without strict grounding rules, models hallucinate answers to 
out-of-scope questions. With grounding: "NOT_IN_DOCUMENT" response.

**Applied to guardrails:** Out-of-scope detection prevents hallucination.

---

## Future Considerations (v0.2+)

- Semantic classification vs. keyword matching (embeddings-based)
- Confidence scoring for edge cases
- Human-in-the-loop feedback integration
- Model-specific tuning (different triggers for different models)
- Integration with RAG retrieval confidence scores
- Conversation-aware classification (multi-turn context)
- A/B testing framework for rule refinement

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v0.1 | Dec 2025 | Initial heuristics framework |