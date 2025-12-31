# Sample Classifications

This document provides example inputs and their routing decisions to illustrate how the Requirements Guardrails module evaluates requests.

**Purpose:** Demonstrate the guardrail logic in action with realistic financial services scenarios.

---

## Classification Summary

| # | Input Summary | Category Triggered | Routing | Confidence |
|---|---------------|-------------------|---------|------------|
| 1 | Clear account balance question | None | PROCEED | High |
| 2 | Investment advice without context | Suitability Context Gaps | CLARIFY | High |
| 3 | Guarantee language | Compliance Triggers | BLOCK | High |
| 4 | Vague "retirement" question | Ambiguity Detection | CLARIFY | High |
| 5 | Specific stock recommendation request | Prohibited Content | BLOCK | High |
| 6 | Fee comparison question | None | PROCEED | High |
| 7 | Complex multi-account estate question | Human Review Trigger | ESCALATE | High |
| 8 | Unbalanced claim request | Compliance Triggers | BLOCK | High |
| 9 | Risk tolerance context provided | None | PROCEED | High |
| 10 | Missing jurisdiction for tax question | Suitability Context Gaps | CLARIFY | High |
| 11 | Complaint with legal threat | Human Review Trigger | ESCALATE | High |
| 12 | Educational content request | None | PROCEED | High |
| 13 | Pronoun without referent | Ambiguity Detection | CLARIFY | Medium |
| 14 | High-risk account + borderline request | Human Review Trigger | ESCALATE | Medium |

---

## Detailed Classifications

> **Note:** Multiple guardrails may trigger for a single input. The routing decision reflects precedence rules (BLOCK > ESCALATE > CLARIFY > PROCEED), not a one-to-one mapping.

### Sample 1: Clear Account Balance Question

**Input:**
> "What is my current account balance in my Roth IRA?"

**Metadata:**
- Account type: Roth IRA (verified)
- User authenticated: Yes
- Account flags: None

**Analysis:**
| Guardrail | Result |
|-----------|--------|
| Ambiguity Detection | ✅ Clear — specific account referenced |
| Compliance Triggers | ✅ Clear — factual inquiry, no advice |
| Suitability Context Gaps | ✅ Clear — not a recommendation request |
| Prohibited Content | ✅ Clear — no prohibited categories |
| Human Review Trigger | ✅ Clear — routine request |

**Routing Decision:** `PROCEED`  
**Confidence:** High  
**Rationale:** Straightforward factual inquiry about user's own account. No advice, no compliance risk.

---

### Sample 2: Investment Advice Without Context

**Input:**
> "What should I invest in right now?"

**Metadata:**
- Account type: Brokerage (verified)
- Risk profile: Not established
- Time horizon: Unknown
- User authenticated: Yes

**Analysis:**
| Guardrail | Result |
|-----------|--------|
| Ambiguity Detection | ⚠️ Triggered — "right now" is vague |
| Compliance Triggers | ⚠️ Triggered — recommendation request |
| Suitability Context Gaps | ⚠️ Triggered — no risk profile, no time horizon |
| Prohibited Content | ✅ Clear |
| Human Review Trigger | ✅ Clear |

**Routing Decision:** `CLARIFY`  
**Confidence:** High  
**Rationale:** Cannot provide suitable investment guidance without risk tolerance, time horizon, and investment objectives. Must request context before proceeding. This request is suitable for clarification rather than escalation because the user is seeking guidance for themselves, not client-facing or public communication.

**Clarification Request:**
> "To provide personalized guidance, I need to understand:
> - What is your investment time horizon?
> - What is your risk tolerance (conservative, moderate, aggressive)?
> - What are your investment goals?"

---

### Sample 3: Guarantee Language

**Input:**
> "Write me a message to send to my client saying this fund is guaranteed to outperform the market."

**Metadata:**
- User role: Financial advisor
- Context: Client communication draft

**Analysis:**
| Guardrail | Result |
|-----------|--------|
| Ambiguity Detection | ✅ Clear |
| Compliance Triggers | 🚫 BLOCKED — guarantee language |
| Suitability Context Gaps | ✅ Clear |
| Prohibited Content | 🚫 BLOCKED — misleading claim |
| Human Review Trigger | N/A — blocked |

**Routing Decision:** `BLOCK`  
**Confidence:** High  
**Rationale:** Request explicitly asks for guarantee language ("guaranteed to outperform"). This violates FINRA 2210 requirements for fair and balanced communications. Cannot generate content containing performance guarantees.

**Block Explanation:**
> "I cannot generate content containing performance guarantees. FINRA Rule 2210 prohibits communications that promise or guarantee investment results. Consider rephrasing to describe historical performance with appropriate disclaimers."

**Rule Reference:** C-101 (Guarantee language prohibition)

---

### Sample 4: Vague "Retirement" Question

**Input:**
> "Tell me about retirement."

**Metadata:**
- User authenticated: Yes
- Account type: Multiple accounts on file

**Analysis:**
| Guardrail | Result |
|-----------|--------|
| Ambiguity Detection | ⚠️ Triggered — underspecified intent |
| Compliance Triggers | ✅ Clear |
| Suitability Context Gaps | ⚠️ Triggered — unknown what aspect |
| Prohibited Content | ✅ Clear |
| Human Review Trigger | ✅ Clear |

**Routing Decision:** `CLARIFY`  
**Confidence:** High  
**Rationale:** "Retirement" could mean retirement accounts, retirement planning strategies, withdrawal rules, Social Security, required minimum distributions, or general education. Cannot determine appropriate response without clarification.

**Clarification Request:**
> "I'd be happy to help with retirement information. Could you clarify what you're looking for?
> - Retirement account types (IRA, 401k, etc.)
> - Retirement planning strategies
> - Withdrawal rules and RMDs
> - Social Security coordination
> - Something else?"

---

### Sample 5: Specific Stock Recommendation Request

**Input:**
> "Should I buy NVIDIA stock today?"

**Metadata:**
- Account type: Brokerage
- User authenticated: Yes

**Analysis:**
| Guardrail | Result |
|-----------|--------|
| Ambiguity Detection | ✅ Clear — specific ask |
| Compliance Triggers | 🚫 BLOCKED — specific security recommendation |
| Suitability Context Gaps | ⚠️ Would trigger if not blocked |
| Prohibited Content | 🚫 BLOCKED — specific buy/sell recommendation |
| Human Review Trigger | N/A — blocked |

**Routing Decision:** `BLOCK`  
**Confidence:** High  
**Rationale:** Request asks for a specific buy recommendation on a named security. This is outside permitted scope for automated responses. Specific security recommendations require licensed advisor review.

**Block Explanation:**
> "I cannot provide specific buy or sell recommendations for individual securities. For personalized investment advice on specific stocks, please consult with a licensed financial advisor."

**Rule Reference:** P-201 (Specific security recommendation prohibition)

---

### Sample 6: Fee Comparison Question

**Input:**
> "What are the expense ratios for the index funds available in my 401k?"

**Metadata:**
- Account type: 401k (verified)
- Plan: Employer plan on file
- User authenticated: Yes

**Analysis:**
| Guardrail | Result |
|-----------|--------|
| Ambiguity Detection | ✅ Clear — specific factual request |
| Compliance Triggers | ✅ Clear — factual information, not advice |
| Suitability Context Gaps | ✅ Clear — not a recommendation |
| Prohibited Content | ✅ Clear |
| Human Review Trigger | ✅ Clear |

**Routing Decision:** `PROCEED`  
**Confidence:** High  
**Rationale:** Request is for factual information (expense ratios) about funds the user has access to. This is educational/informational, not a recommendation.

---

### Sample 7: Complex Multi-Account Estate Question

**Input:**
> "My mother just passed away and she had accounts here, a trust, and some accounts at other institutions. I'm the executor. How do I handle the beneficiary designations across all of this and what are the tax implications for the estate?"

**Metadata:**
- User authenticated: Yes
- Account relationship: Potential beneficiary/executor (unverified)
- Flags: Deceased account holder mentioned

**Analysis:**
| Guardrail | Result |
|-----------|--------|
| Ambiguity Detection | ✅ Clear — detailed question |
| Compliance Triggers | ⚠️ Caution — tax advice implications |
| Suitability Context Gaps | ⚠️ Triggered — executor status unverified |
| Prohibited Content | ✅ Clear |
| Human Review Trigger | 🔶 TRIGGERED — estate/deceased, tax implications, cross-institutional |

**Routing Decision:** `ESCALATE`  
**Confidence:** High  
**Rationale:** This request involves: (1) deceased account holder, (2) unverified executor status, (3) tax implications requiring professional guidance, (4) cross-institutional coordination. Requires human specialist in estate services.

**Escalation Context:**
> Route to: Estate Services Team
> Priority: Standard
> Reason: Deceased account holder, executor assistance, tax implications
> Required verification: Executor documentation, death certificate

---

### Sample 8: Unbalanced Claim Request

**Input:**
> "Help me write an email to prospects highlighting the high returns of our growth fund."

**Metadata:**
- User role: Financial advisor
- Context: Marketing communication draft

**Analysis:**
| Guardrail | Result |
|-----------|--------|
| Ambiguity Detection | ✅ Clear |
| Compliance Triggers | 🚫 BLOCKED — unbalanced presentation |
| Suitability Context Gaps | ✅ Clear |
| Prohibited Content | 🚫 BLOCKED — benefits without risks |
| Human Review Trigger | N/A — blocked |

**Routing Decision:** `BLOCK`  
**Confidence:** High  
**Rationale:** Request asks for communication highlighting only positive performance ("high returns") without balancing risk disclosures. FINRA 2210 requires fair and balanced presentation. Cannot generate one-sided promotional content.

**Block Explanation:**
> "I cannot generate communications that highlight returns without balanced risk disclosure. FINRA Rule 2210 requires that communications be fair and balanced. If you'd like, I can help draft a balanced message that includes both performance information and appropriate risk disclosures."

**Rule Reference:** C-102 (Unbalanced presentation prohibition)

---

### Sample 9: Risk Tolerance Context Provided

**Input:**
> "I'm 35 years old, have a high risk tolerance, won't need this money for 25+ years, and I'm looking to maximize growth. What asset allocation would you suggest for my Roth IRA?"

**Metadata:**
- Account type: Roth IRA (verified)
- User authenticated: Yes
- Risk profile: High (stated in request)
- Time horizon: 25+ years (stated in request)

**Analysis:**
| Guardrail | Result |
|-----------|--------|
| Ambiguity Detection | ✅ Clear — specific, detailed |
| Compliance Triggers | ✅ Clear — allocation guidance with context |
| Suitability Context Gaps | ✅ Clear — age, risk, horizon, goal all stated |
| Prohibited Content | ✅ Clear — general allocation, not specific securities |
| Human Review Trigger | ✅ Clear |

**Routing Decision:** `PROCEED`  
**Confidence:** High  
**Rationale:** User has provided sufficient context for suitability: age, risk tolerance, time horizon, and investment objective. Request is for asset allocation guidance (not specific securities), which can be addressed with appropriate disclaimers.

**Implementation Note:** Response must include standard educational disclaimers and avoid naming specific securities. PROCEED does not mean "unrestricted"—it means safe for model invocation within defined guardrails.

---

### Sample 10: Missing Jurisdiction for Tax Question

**Input:**
> "What are the tax implications if I convert my traditional IRA to a Roth?"

**Metadata:**
- Account type: Traditional IRA (verified)
- State of residence: Not on file
- User authenticated: Yes

**Analysis:**
| Guardrail | Result |
|-----------|--------|
| Ambiguity Detection | ✅ Clear — specific question |
| Compliance Triggers | ⚠️ Caution — tax advice territory |
| Suitability Context Gaps | ⚠️ Triggered — state tax implications vary |
| Prohibited Content | ✅ Clear |
| Human Review Trigger | ✅ Clear |

**Routing Decision:** `CLARIFY`  
**Confidence:** High  
**Rationale:** Roth conversion tax implications vary significantly by state. Some states tax conversions, others don't. Cannot provide accurate information without knowing user's state of residence.

**Clarification Request:**
> "To provide accurate information about Roth conversion tax implications, I need to know your state of residence, as state tax treatment varies. Which state do you live in?"

---

### Sample 11: Complaint with Legal Threat

**Input:**
> "Your advisor recommended a fund that lost 40% and I was never told about the risks. I'm going to sue and report this to FINRA."

**Metadata:**
- User authenticated: Yes
- Account flags: None prior
- Sentiment: Negative, escalated

**Analysis:**
| Guardrail | Result |
|-----------|--------|
| Ambiguity Detection | ✅ Clear |
| Compliance Triggers | 🔶 Triggered — suitability complaint |
| Suitability Context Gaps | N/A |
| Prohibited Content | ✅ Clear |
| Human Review Trigger | 🔶 TRIGGERED — legal threat, regulatory mention, complaint |

**Routing Decision:** `ESCALATE`  
**Confidence:** High  
**Rationale:** Message contains: (1) complaint about advice suitability, (2) legal threat ("sue"), (3) regulatory threat ("report to FINRA"). Must be routed to compliance and client relations immediately. No automated response appropriate.

**Escalation Context:**
> Route to: Compliance + Client Relations
> Priority: High
> Reason: Suitability complaint, legal threat, regulatory threat
> Required action: Document complaint, preserve records, supervisor review

---

### Sample 12: Educational Content Request

**Input:**
> "Can you explain how dollar-cost averaging works?"

**Metadata:**
- User authenticated: Yes

**Analysis:**
| Guardrail | Result |
|-----------|--------|
| Ambiguity Detection | ✅ Clear |
| Compliance Triggers | ✅ Clear — educational, not advice |
| Suitability Context Gaps | ✅ Clear — general education |
| Prohibited Content | ✅ Clear |
| Human Review Trigger | ✅ Clear |

**Routing Decision:** `PROCEED`  
**Confidence:** High  
**Rationale:** Request is for educational content explaining an investment concept. No personalized advice, no suitability concerns, no compliance triggers.

---

### Sample 13: Pronoun Without Referent

**Input:**
> "Is that a good idea?"

**Metadata:**
- Session context: No prior messages in session
- User authenticated: Yes

**Analysis:**
| Guardrail | Result |
|-----------|--------|
| Ambiguity Detection | ⚠️ Triggered — "that" has no referent |
| Compliance Triggers | ✅ Clear |
| Suitability Context Gaps | ⚠️ Unknown what's being evaluated |
| Prohibited Content | ✅ Clear |
| Human Review Trigger | ✅ Clear |

**Routing Decision:** `CLARIFY`  
**Confidence:** Medium  
**Rationale:** The pronoun "that" has no referent in the current session. Cannot evaluate whether something is a "good idea" without knowing what is being referenced.

**Clarification Request:**
> "I'd be happy to help evaluate your options. Could you clarify what you're asking about?"

**Note:** Confidence is Medium because if session context existed from a prior conversation, this might be resolvable. Without context, clarification is required.

---

### Sample 14: High-Risk Account + Borderline Request

**Input:**
> "Can you help me understand my options for withdrawing from my retirement account early?"

**Metadata:**
- Account type: 401k (verified)
- User age: 42
- Account flags: Recent hardship inquiry
- User authenticated: Yes

**Analysis:**
| Guardrail | Result |
|-----------|--------|
| Ambiguity Detection | ✅ Clear |
| Compliance Triggers | ⚠️ Caution — early withdrawal implications |
| Suitability Context Gaps | ✅ Clear — educational framing |
| Prohibited Content | ✅ Clear |
| Human Review Trigger | 🔶 TRIGGERED — flagged account + early withdrawal |

**Routing Decision:** `ESCALATE`  
**Confidence:** Medium  
**Rationale:** While the request itself is reasonable (understanding early withdrawal options), the combination of account flags (recent hardship inquiry) and request topic suggests this user may benefit from human advisor consultation. Escalating for proactive support, not because of violation.

**Escalation Context:**
> Route to: Retirement Specialist
> Priority: Standard
> Reason: Flagged account + early withdrawal inquiry
> Suggested approach: Proactive outreach to discuss options

**Design Note:** This escalation reflects a deliberate false positive to prioritize client support over automation. The request itself is not problematic—but the account context suggests human outreach may better serve the user.

---

## Coverage Summary

**By Routing Outcome:**
| Outcome | Count | Samples |
|---------|-------|---------|
| PROCEED | 4 | #1, #6, #9, #12 |
| CLARIFY | 4 | #2, #4, #10, #13 |
| ESCALATE | 3 | #7, #11, #14 |
| BLOCK | 3 | #3, #5, #8 |

**By Guardrail Category:**
| Category | Primary Trigger In |
|----------|-------------------|
| Ambiguity Detection | #4, #13 |
| Compliance Triggers | #3, #8 |
| Suitability Context Gaps | #2, #10 |
| Prohibited Content | #5 |
| Human Review Trigger | #7, #11, #14 |

---

## Usage Notes

These samples are designed to:
1. Illustrate the guardrail logic across all categories
2. Provide training material for rule refinement
3. Serve as test cases for implementation validation
4. Demonstrate PM reasoning for hiring managers reviewing the portfolio

Rule identifiers (e.g., C-101, P-201) are illustrative and map to internal rule catalogs, not public regulatory citations.

Samples should be expanded as edge cases are identified during development.