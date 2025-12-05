# Experiment 04: Ambiguity Detection

## Goal

Detect when customer questions are too vague to answer safely, and generate appropriate clarifying questions instead of assuming intent.

## Why This Matters

In regulated financial services, answering vague questions with specific advice creates liability. "Help me with my money" could mean budgeting, debt payoff, retirement planning, or active investing — each requiring different expertise, disclosures, and suitability assessments. An AI that guesses wrong exposes the firm to regulatory risk.

---

## Prompt V1
```
You are a helpful financial assistant.

Customer question: Can you help me figure out what to do with my money?
```

## Output V1
```
Of course! I'd be happy to help you figure out what to do with your money. To start, it's important to assess your financial goals, risk tolerance, and time horizon. Are you looking to save for a specific goal, such as buying a house or retiring? Are you comfortable with taking on some risk in exchange for potentially higher returns, or do you prefer more conservative investments? And how soon do you need access to your money?

Once we have a better understanding of your financial situation and goals, we can explore different investment options that align with your objectives. This could include setting up a diversified investment portfolio, considering tax-advantaged accounts like IRAs or 401(k)s, or exploring other savings and investment vehicles.

Feel free to provide more information about your financial goals and preferences, and we can work together to come up with a personalized plan for managing your money.
```

## Observation

V1 demonstrated dangerous "helpfulness":

- **Jumped to advice:** Immediately discussed investment options, IRAs, 401(k)s
- **Offered personalized planning:** "We can work together to come up with a personalized plan"
- **Assumed investment context:** The customer might have meant budgeting or debt payoff
- **No guardrails:** Nothing prevented the model from going further into specific recommendations

The model optimized for being helpful, which in regulated environments means optimizing for risk. A compliance officer would flag this response immediately.

---

## Prompt V2 (Refined)
```
You are an AI assistant for a regulated financial institution.

Before answering any question, you must first assess whether the request is clear enough to respond safely.

Evaluate the customer question and return JSON in this exact format:

{
    "is_ambiguous": true/false,
    "ambiguity_reason": "explanation if ambiguous, empty string if clear",
    "clarifying_questions": ["question1", "question2"] or [],
    "safe_to_answer": true/false
}

Rules:
- Questions about specific financial actions (investing, moving money, retirement decisions) require specificity to answer safely
- Vague requests for "help" or "advice" without context are ambiguous
- If ambiguous, provide 2-3 clarifying questions to narrow scope
- Never assume what the customer means

Customer question: Can you help me figure out what to do with my money?
```

## Output V2
```json
{
    "is_ambiguous": true,
    "ambiguity_reason": "The request is vague and lacks specific details on what the customer needs assistance with.",
    "clarifying_questions": ["What are your financial goals?", "Are you looking to invest, save, or spend your money?", "Do you have a specific timeframe or amount in mind?"],
    "safe_to_answer": false
}
```

## What Changed in V2

| Element | V1 | V2 |
|---------|----|----|
| Role framing | "Helpful assistant" | "Regulated financial institution" |
| First action | Answer the question | Assess if safe to answer |
| Ambiguity handling | None — assume and proceed | Explicit detection and flagging |
| Output | Free-form advice | Structured assessment |
| Clarification | Embedded in advice | Separate, actionable questions |

---

## Takeaway

"Helpful" is not always safe. In regulated environments, the AI must be trained to pause before answering, not to maximize immediate helpfulness.

This requires:
1. **Ambiguity detection as a first step** — before generating any response
2. **Explicit safety assessment** — a `safe_to_answer` flag that downstream systems can enforce
3. **Clarifying questions** — so the conversation can continue productively without premature advice

The V1 pattern ("be helpful") is the default LLM behavior. Overriding it requires explicit instructions that prioritize safety over helpfulness.

---

## Connection to Toolkit

This pattern is essential for the **Requirements Guardrails** module, which must intercept unsafe queries before they reach the response generation layer. It also shapes the design of the **Compliance RAG Assistant**, where certain questions should trigger human escalation rather than AI-generated answers.