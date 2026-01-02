# Evidence Directory

**Module:** Requirements Guardrails  
**Purpose:** Demonstrate guardrail logic through concrete examples and documented edge cases.

---

## Contents

| File | Description |
|------|-------------|
| [sample-classifications.md](./sample-classifications.md) | 14 example inputs with routing decisions covering all outcomes |
| [edge-cases.md](./edge-cases.md) | 11 boundary decisions with PM rationale and precedent |

---

## Why Evidence Matters

Rules without examples are abstract. This folder provides:

- **Concrete demonstrations** of how rules apply to real requests
- **Edge case reasoning** showing PM judgment on ambiguous scenarios  
- **Training data** for classifier development and refinement
- **Interview material** — specific examples to discuss

---

## Sample Classifications vs. Edge Cases

| Artifact | Purpose | Characteristics |
|----------|---------|-----------------|
| Sample Classifications | Show rules working correctly | Clear-cut, unambiguous routing |
| Edge Cases | Document boundary decisions | Ambiguous, required judgment call |

Together, they demonstrate both the rule logic and the PM thinking that shaped it.

---

## Coverage

### By Routing Outcome

| Outcome | Sample Count | Edge Case Count |
|---------|--------------|-----------------|
| PROCEED | 3 | 4 |
| CLARIFY | 4 | 3 |
| ESCALATE | 4 | 4 |
| BLOCK | 3 | 0 |

### By Scenario Type

- Account/balance inquiries
- Investment research requests
- Suitability-adjacent questions
- Compliance language detection
- Informal/frustrated user language
- Third-party transaction requests
- Tax/legal boundary questions

---

## Using This Evidence

**For engineering handoff:** Sample classifications provide test cases for classifier validation.

**For compliance review:** Edge cases document precedent for disputed decisions.

**For interviews:** Specific examples demonstrate systems thinking and judgment.

---

## Related Documents

- [Rules Directory](../rules/) — Classification logic these examples demonstrate
- [Outputs Directory](../outputs/) — Decision log format examples populate
- [Experiments Directory](../experiments/) — Prompt work that informed rules