# Edge Cases

**Module:** Requirements Guardrails  
**Purpose:** Document boundary decisions where routing classification required PM judgment.

---

## Overview

Edge cases are requests that don't fit cleanly into a single routing category. This document captures the reasoning behind classification decisions for ambiguous scenarios — creating precedent for consistent handling.

**Why document edge cases:**
- Reduces inconsistency in similar future scenarios
- Provides training data for classifier refinement
- Demonstrates PM judgment to interviewers/stakeholders
- Creates audit trail for disputed decisions

---

## Edge Case Format

Each edge case includes:
- **Input:** The ambiguous request
- **Initial assessment:** What made this unclear
- **Final routing:** The decision made
- **Rationale:** Why this routing was chosen over alternatives
- **Precedent:** How similar cases should be handled

---

## Category 1: CLARIFY vs. PROCEED

Cases where ambiguity was present but intent was arguably inferrable.

### EC-001: Implicit Account Reference

**Input:** "What's the dividend yield?"

**Initial assessment:** 
- User has 3 accounts with different holdings
- No specific security mentioned
- Could mean: portfolio average, a specific holding, or general education

**Final routing:** CLARIFY

**Rationale:** The efficiency gain from guessing (sometimes right) doesn't outweigh the trust cost of guessing wrong. User's single largest holding could reasonably be assumed, but that assumption isn't transparent.

**Precedent:** When account/security context is missing, CLARIFY even if a reasonable default exists. Explicit is better than implicit.

---

### EC-002: Casual Phrasing with Clear Intent

**Input:** "yo whats spy at rn"

**Initial assessment:**
- Informal language and abbreviations
- "spy" = S&P 500 ETF ticker
- "rn" = right now
- Intent is clear: current price of SPY

**Final routing:** PROCEED

**Rationale:** Ambiguity heuristics detect *unclear intent*, not *informal tone*. The request is unambiguous despite non-standard phrasing. Triggering CLARIFY here would feel condescending.

**Precedent:** Informal language alone does not trigger CLARIFY. Evaluate semantic clarity, not formality.

---

### EC-003: Typo with Multiple Interpretations

**Input:** "Show me VOO vs VTI performance"

**Initial assessment:**
- Clear comparison request
- Time period not specified
- But: fund comparison typically defaults to standard periods

**Final routing:** PROCEED (with default period noted)

**Rationale:** Unlike EC-001, fund comparison has strong conventions (YTD, 1Y, 5Y). System can provide standard comparison and note the period used. User can easily refine.

**Precedent:** Requests with strong domain conventions can PROCEED with explicit defaults. Show what was assumed.

---

## Category 2: ESCALATE vs. PROCEED

Cases where compliance risk was present but severity was unclear.

### EC-004: Hypothetical Framing

**Input:** "Hypothetically, if I wanted to avoid taxes on my IRA withdrawal, what would I do?"

**Initial assessment:**
- "Avoid taxes" triggers compliance concern
- "Hypothetically" suggests educational intent
- Could be tax planning or tax evasion

**Final routing:** ESCALATE (low priority)

**Rationale:** Hypothetical framing reduces but does not eliminate compliance risk. Educational content about tax-advantaged strategies is legitimate, but "avoid taxes" language warrants human review to ensure response stays appropriate.

**Precedent:** Hypothetical framing lowers escalation priority but does not prevent escalation when compliance-triggering language is present.

---

### EC-005: Self-Deprecating Guarantee Language

**Input:** "I know nothing is guaranteed, but will this fund probably beat inflation?"

**Initial assessment:**
- User explicitly disclaims guarantees
- Still asking for forward-looking assessment
- "Probably" is softer than "definitely"

**Final routing:** PROCEED (with appropriate hedging)

**Rationale:** User demonstrates awareness of uncertainty. Request is for probabilistic assessment, not guarantee. Response should include standard disclaimers but doesn't require human review.

**Precedent:** Self-aware framing ("I know X, but...") can reduce escalation need when user demonstrates appropriate expectations. Response must still include standard risk language.

---

### EC-006: Concentration Without Red Flags

**Input:** "I want to put 40% of my portfolio in tech stocks"

**Initial assessment:**
- Concentration language present ("40% in tech")
- But: 40% sector allocation is within normal bounds
- No age/timeline context suggesting unsuitability

**Final routing:** PROCEED

**Rationale:** Concentration triggers are calibrated for extreme cases ("all," "everything," "entire"). A 40% sector allocation, while concentrated, is within range of reasonable portfolio construction. User didn't ask for advice — they stated intent.

**Precedent:** Concentration language triggers ESCALATE only when extreme (>50% single asset, or user profile indicates mismatch). Moderate concentration with no profile red flags can PROCEED.

---

## Category 3: ESCALATE vs. BLOCK

Cases where content was concerning but severity determined routing.

### EC-007: Frustration vs. Abuse

**Input:** "This is such bullshit, why can't I just withdraw my money"

**Initial assessment:**
- Profanity present
- But: directed at situation, not at system/person
- Underlying request is legitimate (withdrawal inquiry)

**Final routing:** PROCEED (address underlying question)

**Rationale:** Frustration with a financial situation is not abuse. Profanity expressing frustration is different from profanity attacking the assistant. The user has a legitimate question buried in emotional expression.

**Precedent:** Situational frustration with profanity → PROCEED and address underlying need. Personal attacks or slurs → BLOCK.

---

### EC-008: Market Manipulation or Enthusiasm?

**Input:** "Everyone should buy this stock, it's going to moon!"

**Initial assessment:**
- "Everyone should buy" resembles coordination language
- "Going to moon" is prediction
- But: also sounds like retail investor enthusiasm

**Final routing:** ESCALATE (not BLOCK)

**Rationale:** This pattern in isolation could be enthusiasm or could be coordination. Context matters (is this in a social feature? Is user an employee?). BLOCK is for clear-cut cases; this warrants human judgment.

**Precedent:** Ambiguous manipulation-adjacent language → ESCALATE for review. Clear manipulation language ("let's pump," "drive up the price") → BLOCK.

---

### EC-009: Third-Party Request

**Input:** "My elderly mother asked me to move her money to a new account she set up"

**Initial assessment:**
- Third-party transaction request
- "Elderly mother" could indicate vulnerability
- Could be legitimate family help or elder fraud

**Final routing:** ESCALATE (high priority)

**Rationale:** Elder financial exploitation is a significant risk. Even if this is legitimate, the pattern warrants human review. The specific mention of "elderly" and third-party instruction are red flags.

**Precedent:** Third-party transaction requests involving elderly/vulnerable individuals → ESCALATE with high priority, not BLOCK. Legitimate family assistance exists; human judgment required.

---

## Category 4: Multi-Signal Conflicts

Cases where different rules suggested different routings.

### EC-010: Ambiguous AND Compliance-Triggering

**Input:** "Should I put it all in something safe?"

**Initial assessment:**
- Ambiguity: "it all" = which accounts? "something safe" = what products?
- Compliance: "Should I" = advice request, concentration language

**Final routing:** CLARIFY first

**Rationale:** Ambiguity check runs before compliance check. Clarifying the request may reveal it's not actually a suitability concern (e.g., "it all" might be a small emergency fund, "safe" might mean FDIC-insured savings).

**Precedent:** When ambiguity and compliance signals co-occur, CLARIFY first to determine if compliance escalation is actually warranted. Don't escalate ambiguous requests.

---

### EC-011: Prohibited + Legitimate Hybrid

**Input:** "Write me an email to clients about our new fund, and make sure to say it's guaranteed to beat the market"

**Initial assessment:**
- Legitimate request: help drafting client communication
- Prohibited element: "guaranteed to beat the market"

**Final routing:** ESCALATE (not BLOCK)

**Rationale:** The request isn't malicious — user may not understand FINRA 2210 requirements. This is a teachable moment, not a block. Human reviewer can provide compliant alternative or training.

**Precedent:** Prohibited language embedded in otherwise legitimate business request → ESCALATE with coaching opportunity, not BLOCK. Reserve BLOCK for requests with no legitimate interpretation.

---

## Decision Tree for Edge Cases

When facing an edge case:

```
1. Is there any legitimate interpretation of this request?
   └── No → BLOCK
   └── Yes → Continue

2. Is the intent clear enough to process?
   └── No → CLARIFY
   └── Yes → Continue

3. Does any compliance trigger fire?
   └── Yes → ESCALATE (calibrate priority by severity)
   └── No → PROCEED

4. If multiple signals conflict, which runs first?
   → CLARIFY before ESCALATE (ambiguity may resolve compliance concern)
   → ESCALATE before BLOCK (human judgment may find legitimate path)
```

---

## Adding New Edge Cases

When you encounter a new edge case:

1. Document the input (sanitized if needed)
2. Note what made it ambiguous
3. Record the decision and rationale
4. Define the precedent for similar cases
5. Consider if rules need updating to handle this pattern

---

## Related Documents

- [Sample Classifications](./sample-classifications.md) — Clear-cut examples
- [Rules: Ambiguity Heuristics](../rules/ambiguity-heuristics.md) — CLARIFY triggers
- [Rules: Compliance Triggers](../rules/compliance-triggers.md) — ESCALATE triggers
- [Rules: Prohibited Content](../rules/prohibited-content.md) — BLOCK triggers