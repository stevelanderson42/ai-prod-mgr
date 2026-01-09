# SEC Regulation Best Interest (Reg BI)

**Regulatory Citation:** 17 C.F.R. § 240.15l-1  
**Effective Date:** June 30, 2020  
**Regulator:** U.S. Securities and Exchange Commission (SEC)  
**Type:** Federal Regulation — legally binding, examiner-enforced

---

## Summary

Regulation Best Interest requires broker-dealers to act in the **best interest of retail customers** when making securities recommendations. Unlike the older "suitability" standard, Reg BI imposes a higher duty: recommendations must be made without placing the firm's interest ahead of the customer's.

The core premise: **generic recommendations are prohibited**. The system must have sufficient customer context — or refuse to proceed. A recommendation appropriate for "someone" is not appropriate for "this specific customer" without knowing their profile.

For AI systems, Reg BI means: if the model generates anything that could be interpreted as a recommendation, it must be grounded in that customer's investment profile — or the system must refuse. Statements like "this is generally a good product" are not compliant without customer-specific context.

> *This document interprets Reg BI from a product and architecture perspective, not as a legal or compliance directive.*

---

## Key Regulatory Language

### On the Best Interest Obligation

> "A broker, dealer, or a natural person who is an associated person of a broker or dealer, when making a recommendation of any securities transaction or investment strategy involving securities... to a retail customer, shall act in the **best interest** of the retail customer at the time the recommendation is made, without placing the financial or other interest of the broker, dealer, or natural person... ahead of the interest of the retail customer."
>
> — *17 C.F.R. § 240.15l-1(a)(1)*

### On the Care Obligation

> "The broker, dealer, or natural person... exercise reasonable diligence, care, and skill to:
> 
> (i) Understand the potential risks, rewards, and costs associated with the recommendation...  
> (ii) Have a reasonable basis to believe that the recommendation could be in the best interest of **at least some retail customers**...  
> (iii) Have a reasonable basis to believe that the recommendation is in the best interest of **a particular retail customer** based on that retail customer's investment profile."
>
> — *17 C.F.R. § 240.15l-1(a)(2)(ii)*

### On Customer Investment Profile

> "The investment profile includes, but is not limited to, the retail customer's age, other investments, financial situation and needs, tax status, investment objectives, investment experience, investment time horizon, liquidity needs, risk tolerance, and any other information the retail customer may disclose..."
>
> — *17 C.F.R. § 240.15l-1(a)(2)(ii)(C)*

### On Disclosure Obligation

> "Prior to or at the time of the recommendation, provide the retail customer, in writing, full and fair disclosure of all material facts relating to the scope and terms of the relationship..."
>
> — *17 C.F.R. § 240.15l-1(a)(2)(i)*

---

## Core Expectations

From an examiner's perspective, Reg BI requires:

### Customer Investment Profile (Must Be Known)
- **Risk tolerance** — Conservative, moderate, aggressive
- **Time horizon** — Short-term, intermediate, long-term
- **Financial situation** — Income, net worth, existing assets
- **Investment objectives** — Growth, income, preservation, speculation
- **Liquidity needs** — Access requirements for funds
- **Investment experience** — Sophistication level
- **Tax status** — Relevant tax considerations
- **Age** — Life stage considerations

### The Four Component Obligations

| Obligation | Requirement |
|------------|-------------|
| **Disclosure** | Provide material facts about the relationship, fees, conflicts |
| **Care** | Reasonable diligence to understand and recommend appropriately |
| **Conflict of Interest** | Identify, disclose, and mitigate conflicts |
| **Compliance** | Written policies and procedures to achieve compliance |

### Reasonable Basis Standard
- **General suitability** — Could this be appropriate for *some* customers?
- **Customer-specific suitability** — Is this appropriate for *this* customer?
- **Quantitative suitability** — Is the recommended frequency/volume appropriate?

All three must be satisfied for a compliant recommendation.

---

## Product & Architecture Implications

For AI systems that touch investment guidance, Reg BI creates concrete design requirements:

| Expectation | What It Means for AI Systems |
|-------------|------------------------------|
| **No generic recommendations** | "What should I invest in?" without profile data → must clarify when feasible, and refuse when sufficient context cannot be obtained |
| **Context is mandatory** | Risk tolerance, time horizon, etc. are required inputs, not optional |
| **Personalization ≠ recommendation** | Showing "popular funds" differs from "you should buy this" |
| **Refusal is compliant; guessing is not** | A system that declines without context is safer than one that speculates |
| **Audit trail for recommendations** | If the system makes a recommendation, profile and reasoning must be logged |
| **Profile completeness check** | System must verify sufficient profile data exists before generating advice |

### The Suitability Gate

This is the key architectural implication:

> Before generating any response that could be interpreted as a recommendation, the system must verify:
> 1. Customer profile data is available
> 2. Profile data is sufficient for the type of guidance requested
> 3. The response can be grounded in that specific customer's context

If any condition fails, the system must clarify when feasible, and refuse when sufficient context cannot be obtained — not generate generic guidance.

---

## Where This Shows Up in the Portfolio

| Artifact | How Reg BI Informed It |
|----------|------------------------|
| **Requirements Guardrails** | "Suitability & User Context Gaps" category — routes to CLARIFY when profile data is missing |
| **Guardrails Output Contract** | `missing_context` field explicitly lists required suitability fields |
| **Compliance Retrieval Assistant** | Refusal taxonomy includes `INSUFFICIENT_GROUNDING` for context-dependent queries |
| **Trace Schema** | Preserves customer profile snapshot at time of recommendation |
| **Response Contract** | `grounding_status` indicates whether response is personalized or general |

### Specific Design Decisions Driven by Reg BI

| Decision | Reg BI Driver |
|----------|---------------|
| Suitability context check in Guardrails | Care Obligation requires customer-specific basis |
| CLARIFY routing for missing profile | Cannot recommend without knowing the customer |
| Refusal over generic advice | Generic recommendations violate best interest standard |
| Profile snapshot in trace | Must document what was known at time of recommendation |
| Separate "education" from "recommendation" | Educational content has different obligations than recommendations |

---

## Common Examiner Questions (Applied Lens)

Based on Reg BI, examiners may ask:

1. **"How do you know this recommendation was suitable for this customer?"**  
   → Trace includes customer profile snapshot and reasoning for recommendation.

2. **"What customer information did the system have access to?"**  
   → Profile data logged with each interaction; gaps trigger CLARIFY routing.

3. **"What happens if the system doesn't have enough information?"**  
   → Guardrails route to CLARIFY; system requests specific missing context.

4. **"How do you distinguish education from recommendation?"**  
   → Guardrails classify intent; different paths for informational vs. advisory queries.

5. **"Show me the basis for this recommendation."**  
   → Trace schema includes retrieved sources, profile match, and decision rationale.

---

## Key Distinction: Reg BI vs. FINRA Suitability vs. Fiduciary

| Standard | Applies To | Requirement |
|----------|------------|-------------|
| **FINRA Suitability** (legacy) | Broker-dealers | Recommendation must be "suitable" |
| **Reg BI** | Broker-dealers | Recommendation must be in customer's "best interest" |
| **Fiduciary Duty** | Investment advisers | Ongoing duty to act in client's best interest |

Reg BI raised the bar above FINRA suitability but is not identical to fiduciary duty:
- **Reg BI** = best interest *at time of recommendation*
- **Fiduciary** = ongoing best interest duty

For purposes of this portfolio, the system is designed to meet Reg BI requirements — the highest standard applicable to broker-dealer AI systems.

---

## Key Distinction: Education vs. Recommendation

Not every AI response triggers Reg BI. The regulation applies to **recommendations**, not all communications.

| Response Type | Reg BI Applies? | Example |
|---------------|-----------------|---------|
| **General education** | No | "Here's how bonds work" |
| **Product information** | No | "This fund has a 0.5% expense ratio" |
| **Implicit recommendation** | Yes | "This fund would be good for retirement" |
| **Explicit recommendation** | Yes | "Based on your goals, consider this fund" |
| **Personalized suggestion** | Yes | "Given your risk tolerance, you might prefer..." |

An implicit recommendation exists when the content suggests or nudges a specific action, even without explicit language such as "buy" or "invest."

The line is whether a reasonable customer would interpret the response as advice to take action. When in doubt, treat it as a recommendation.

For purposes of this portfolio, any AI-generated content that could reasonably be interpreted as investment guidance is treated as a recommendation subject to Reg BI.

---

## Relationship to Other Regulations

| Regulation | Relationship to Reg BI |
|------------|------------------------|
| **FINRA 2210** | 2210 governs *how* you communicate; Reg BI governs *what* you recommend |
| **SEC 17a-4** | Reg BI requires documentation of recommendation basis; 17a-4 governs retention |
| **SR 11-7** | If the recommendation comes from a model, SR 11-7 governs model documentation |

These regulations intersect at recommendations:
- **Reg BI** determines *whether* you can make the recommendation
- **FINRA 2210** determines *how* you communicate it
- **17a-4** determines *how long* you keep the records
- **SR 11-7** determines *how you document* the model making it

A compliant AI recommendation system must satisfy all four simultaneously.

---

## References

- [17 C.F.R. § 240.15l-1 (eCFR Full Text)](https://www.ecfr.gov/current/title-17/chapter-II/part-240/section-240.15l-1)
- [SEC Reg BI Fact Sheet](https://www.sec.gov/info/smallbus/secg/regulation-best-interest)
- [SEC Reg BI FAQ](https://www.sec.gov/tm/faq-regulation-best-interest)
- [SEC Reg BI Small Entity Compliance Guide](https://www.sec.gov/info/smallbus/secg/regulation-best-interest)

---

*Part of the [Regulatory Governance Context](../README.md) — documenting the external constraints that shape AI product design.*