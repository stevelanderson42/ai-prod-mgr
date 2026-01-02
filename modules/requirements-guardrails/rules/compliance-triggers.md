# Compliance Triggers

**Module:** Requirements Guardrails  
**Purpose:** Define patterns that trigger compliance review or escalation based on regulatory requirements.

---

## Overview

Compliance triggers identify requests or content that require human review due to regulatory risk. These patterns are derived primarily from:

- **FINRA Rule 2210** — Communications with the Public
- **FINRA Rule 2111** — Suitability
- **SEC Regulation Best Interest** — Broker-dealer standard of conduct
- **FINRA Rule 2020** — Use of Manipulative, Deceptive or Other Fraudulent Devices

**Default routing:** ESCALATE (to compliance review queue)

---

## Trigger Category 1: Prohibited Language Patterns

Language that violates FINRA 2210 standards for fair and balanced communication.

### 1.1 Performance Guarantees

Any language suggesting guaranteed returns or outcomes.

| Pattern Type | Examples | Regulation |
|--------------|----------|------------|
| Explicit guarantees | "guaranteed returns," "risk-free," "can't lose" | FINRA 2210(d)(1)(A) |
| Implied certainty | "will definitely," "always performs," "never fails" | FINRA 2210(d)(1)(A) |
| Superlatives without basis | "best investment," "safest option," "highest returns" | FINRA 2210(d)(1)(B) |

**Detection keywords:**
```
guarantee*, certain*, risk-free, can't lose, will definitely, 
always, never, best, safest, highest, lowest risk, sure thing
```

### 1.2 Predictions and Projections

Forward-looking statements presented as fact.

| Pattern Type | Examples | Regulation |
|--------------|----------|------------|
| Market predictions | "the market will," "stocks are going to" | FINRA 2210(d)(1)(F) |
| Specific price targets | "will reach $X," "expect it to hit" | FINRA 2210(d)(1)(F) |
| Timing claims | "by next quarter," "within 6 months" | FINRA 2210(d)(1)(F) |

**Detection keywords:**
```
will reach, going to, expect* to, by [time], within [time],
predict*, project*, forecast* (when stated as fact)
```

### 1.3 Omission of Material Risk

Presenting benefits without corresponding risks.

| Pattern Type | Examples | Regulation |
|--------------|----------|------------|
| One-sided presentation | Benefits listed without risks | FINRA 2210(d)(1)(A) |
| Buried disclaimers | Risk mentioned only in fine print | FINRA 2210(d)(1)(A) |
| Minimized downsides | "minimal risk," "little downside" | FINRA 2210(d)(1)(A) |

**Detection approach:**
- Flag content that mentions returns/benefits without risk disclosure
- Check for balance between opportunity and risk language

---

## Trigger Category 2: Suitability Red Flags

Patterns suggesting potential suitability violations per FINRA 2111.

### 2.1 Unsuitable Recommendations

| Pattern Type | Examples | Regulation |
|--------------|----------|------------|
| Risk mismatch signals | Conservative investor asking about options, leveraged products | FINRA 2111(a) |
| Liquidity mismatch | Retiree considering illiquid alternatives | FINRA 2111(a) |
| Concentration risk | "put everything in," "all-in on" | FINRA 2111(a) |
| Time horizon mismatch | Long-term product for short-term need | FINRA 2111(a) |

**Detection heuristics:**
- User profile indicates conservative → request involves aggressive products
- User indicates near-term liquidity need → request involves illiquid investments
- Language suggesting concentration ("all," "everything," "only")

### 2.2 Missing Suitability Context

Requests where suitability assessment is required but context is missing.

| Scenario | Missing Context | Required Action |
|----------|-----------------|-----------------|
| Investment recommendation request | Risk tolerance, time horizon, financial situation | ESCALATE for profile completion |
| Retirement advice | Age, retirement timeline, income needs | ESCALATE for context gathering |
| Account type guidance | Tax situation, employment status, existing accounts | ESCALATE for assessment |

---

## Trigger Category 3: Regulatory Boundary Violations

Requests that cross regulatory lines.

### 3.1 Investment Advice Without Registration

| Pattern | Risk | Response |
|---------|------|----------|
| "Should I buy X?" | Constitutes investment advice | ESCALATE — requires licensed representative |
| "Is X a good investment?" | Implies recommendation | ESCALATE — requires suitability review |
| "What would you recommend?" | Direct advice request | ESCALATE — cannot provide without assessment |

### 3.2 Tax Advice

| Pattern | Risk | Response |
|---------|------|----------|
| "How do I avoid taxes on..." | Tax avoidance strategy request | ESCALATE — requires tax professional |
| "Is this tax deductible?" | Specific tax determination | ESCALATE — requires qualified tax advice |
| "What's the tax impact of..." | Tax calculation request | CLARIFY scope, then ESCALATE if specific |

### 3.3 Legal Advice

| Pattern | Risk | Response |
|---------|------|----------|
| "Is this legal?" | Legal determination | ESCALATE — requires legal counsel |
| "Can I be sued for..." | Legal risk assessment | ESCALATE — requires legal counsel |
| "What are my rights?" | Legal advice request | ESCALATE — requires legal counsel |

---

## Trigger Category 4: Manipulation and Fraud Indicators

Patterns suggesting potential market manipulation or fraudulent activity.

### 4.1 Market Manipulation Language

| Pattern | Concern | Regulation |
|---------|---------|------------|
| "pump," "dump," "squeeze" | Potential manipulation scheme | FINRA 2020 |
| Coordinated buying language | "we should all buy," "let's drive up" | SEC Rule 10b-5 |
| Artificial price influence | "make it go up," "force short sellers" | FINRA 2020 |

**Routing:** BLOCK + flag for compliance review

### 4.2 Suspicious Activity Indicators

| Pattern | Concern | Response |
|---------|---------|----------|
| Structuring language | "split it up to avoid," "under the limit" | SAR trigger → ESCALATE |
| Source of funds concerns | Unusual large deposits, unclear origin | BSA/AML → ESCALATE |
| Third-party control | "my friend wants me to," "someone asked me to" | Potential fraud → ESCALATE |

---

## Implementation Notes

**For engineering handoff:**

### Detection Priority Order
1. Manipulation/fraud indicators (highest risk) → immediate BLOCK/ESCALATE
2. Regulatory boundary violations → ESCALATE
3. Suitability red flags → ESCALATE with context
4. Prohibited language → ESCALATE for review

### Classifier Design
- Use narrow, validated classifiers for subjective patterns (implied guarantees, tone)
- Rule-based matching for explicit keywords and patterns
- Maintain audit trail of which trigger fired and why

### False Positive Management
- Compliance triggers should err toward escalation (false positives acceptable)
- Track escalation-to-action ratio to calibrate sensitivity
- Educational/hypothetical framing may reduce escalation priority but does not eliminate it

**Metrics to monitor:**

- Escalation rate by trigger category
- Time-to-resolution for escalated items
- False positive rate (escalations dismissed without action)
- Trigger co-occurrence patterns

---

## Regulatory References

| Regulation | Full Title | Key Requirement |
|------------|------------|-----------------|
| FINRA 2210 | Communications with the Public | Fair, balanced, not misleading |
| FINRA 2111 | Suitability | Reasonable basis for recommendations |
| FINRA 2020 | Manipulative and Deceptive Devices | Prohibition on fraud and manipulation |
| SEC Reg BI | Regulation Best Interest | Act in retail customer's best interest |
| SEC 10b-5 | Employment of Manipulative Devices | Anti-fraud provisions |

---

## Related Documents

- [Sample Classifications](../evidence/sample-classifications.md) — Examples of ESCALATE routing
- [Ambiguity Heuristics](./ambiguity-heuristics.md) — When to CLARIFY vs. ESCALATE
- [Prohibited Content](./prohibited-content.md) — Hard blocks (no escalation, immediate reject)
- [ADR-001: Routing Logic](../architecture/ADR-001-routing-logic.md) — Deterministic routing rationale