# Ambiguity Heuristics

**Module:** Requirements Guardrails  
**Purpose:** Define classification criteria for detecting ambiguous requests that require clarification before processing.

---

## Overview

Ambiguous requests are those where user intent cannot be reliably determined from the input alone. Processing ambiguous requests risks:

- Providing irrelevant or misleading information
- Missing the user's actual need
- Wasting computational resources on wrong-path responses
- Creating compliance exposure through misinterpretation

**Default routing:** CLARIFY

---

## Ambiguity Categories

### 1. Referential Ambiguity

The request references something undefined or unclear.

| Pattern | Example | Why Ambiguous |
|---------|---------|---------------|
| Undefined "it/this/that" | "Can you explain how it works?" | No antecedent; could refer to any product, process, or concept |
| Unspecified account | "What's my balance?" | Which account? (checking, IRA, brokerage, 401k) |
| Vague time reference | "Show me recent activity" | Recent = today? This week? This quarter? |
| Unclear "the" reference | "Update the beneficiary" | Which account's beneficiary? |

**Detection heuristics:**
- Pronouns (it, this, that, they) without prior context in session
- Possessives (my, the) referencing ambiguous entities
- No account identifier when action requires one

---

### 2. Scope Ambiguity

The breadth or depth of the request is unclear.

| Pattern | Example | Why Ambiguous |
|---------|---------|---------------|
| Unbounded comparison | "Compare my options" | Which options? All available? A specific subset? |
| Open-ended "tell me about" | "Tell me about retirement" | Overview? Specific plans? Tax implications? Withdrawal rules? |
| Vague quantity | "Show me some funds" | How many? Filtered by what criteria? |
| Unclear depth | "Explain bonds" | Beginner overview or detailed mechanics? |

**Detection heuristics:**
- Requests containing "options," "choices," "alternatives" without constraints
- "Tell me about [broad topic]" without qualifiers
- Quantifiers like "some," "a few," "various" without specifics

---

### 3. Intent Ambiguity

The user's goal cannot be determined from the request.

| Pattern | Example | Why Ambiguous |
|---------|---------|---------------|
| Action vs. information | "IRA contribution limits" | Wants to know the limits? Wants to make a contribution? |
| Browse vs. transact | "401k rollover" | Researching options or initiating a rollover? |
| Self vs. other | "How do I add a beneficiary?" | For themselves or helping someone else? |
| Current vs. hypothetical | "What if I withdraw early?" | Planning to withdraw or just exploring? |

**Detection heuristics:**
- Noun phrases without verbs (could be query or action)
- Questions that could be educational or transactional
- Missing "I want to" or "Show me" framing

---

### 4. Temporal Ambiguity

Time-sensitive requests without clear timeframes.

| Pattern | Example | Why Ambiguous |
|---------|---------|---------------|
| Missing deadline context | "When should I rebalance?" | Based on what trigger? Calendar? Drift threshold? |
| Unclear "now" scope | "What are rates now?" | Current moment? Today's close? This week's range? |
| Vague future reference | "I'm planning to retire" | When? 1 year? 10 years? 20 years? |
| Unspecified period | "Show me performance" | YTD? 1 year? 5 years? Since inception? |

**Detection heuristics:**
- Retirement/planning questions without age or timeline
- Performance requests without date range
- "Current" or "now" in contexts where timing matters

---

## Clarification Response Patterns

When ambiguity is detected, the system should:

1. **Acknowledge the request** — Show the user their input was received
2. **Identify the ambiguity** — Briefly explain what's unclear
3. **Offer bounded choices** — Provide 2-4 specific options, not open-ended questions
4. **Preserve context** — Maintain session state for follow-up

**Example clarification responses:**

| Ambiguous Input | Clarification Response |
|-----------------|------------------------|
| "What's my balance?" | "I can show you balances for your accounts. Which would you like to see: Brokerage, IRA, or all accounts?" |
| "Tell me about retirement" | "I can help with retirement planning. Are you looking for: contribution limits, withdrawal rules, or account comparison?" |
| "Show me performance" | "For what time period would you like to see performance: YTD, 1 year, or 5 years?" |

---

## Edge Cases

### Ambiguity That Should NOT Trigger CLARIFY

| Scenario | Routing | Rationale |
|----------|---------|-----------|
| Typos with clear intent | PROCEED | "Wats my balnce in my IRA" → intent is clear |
| Informal phrasing | PROCEED | "yo how's my portfolio doing" → clear request despite tone |
| Missing punctuation | PROCEED | "show me spy price" → unambiguous despite formatting |

### Ambiguity That Should Escalate Instead

| Scenario | Routing | Rationale |
|----------|---------|-----------|
| Contradictory statements | ESCALATE | "I want safe investments with 20% returns" → needs human judgment |
| Emotional distress signals | ESCALATE | Ambiguity combined with urgency/distress → human review |
| Legal/tax complexity | ESCALATE | "How do I avoid taxes on this?" → compliance risk |

---

## Implementation Notes

**For engineering handoff:**

- Ambiguity detection runs BEFORE compliance checks
- Multiple ambiguity types can co-occur; surface the most actionable one
- Clarification should reduce ambiguity in one round when possible
- Track clarification loops; >2 rounds suggests UX problem, not user problem

**Metrics to monitor:**

- Clarification rate by request type
- Clarification-to-resolution ratio (1 round vs. multiple)
- User abandonment after clarification prompt
- False positive rate (users frustrated by unnecessary clarification)

---

## Related Documents

- [Sample Classifications](../evidence/sample-classifications.md) — Examples of CLARIFY routing
- [Compliance Triggers](./compliance-triggers.md) — When ambiguity escalates instead
- [ADR-001: Routing Logic](../architecture/ADR-001-routing-logic.md) — Why deterministic classification