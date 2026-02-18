# Rules Directory

**Module:** Requirements Guardrails  
**Purpose:** Classification logic that powers routing decisions.

---

## Contents

| File | Routing Outcome | Description |
|------|-----------------|-------------|
| [ambiguity-heuristics.md](./ambiguity-heuristics.md) | CLARIFY | Patterns indicating unclear user intent requiring clarification |
| [compliance-triggers.md](./compliance-triggers.md) | ESCALATE | Regulatory patterns requiring human compliance review |
| [prohibited-content.md](./prohibited-content.md) | BLOCK | Content that receives immediate rejection |

---

## How These Files Work Together

```
User Request
     │
     ▼
┌─────────────────────┐
│ Prohibited Content? │──── Yes ──▶ BLOCK
└─────────────────────┘
     │ No
     ▼
┌─────────────────────┐
│ Compliance Trigger? │──── Yes ──▶ ESCALATE
└─────────────────────┘
     │ No
     ▼
┌─────────────────────┐
│ Ambiguous Request?  │──── Yes ──▶ CLARIFY
└─────────────────────┘
     │ No
     ▼
   PROCEED
```

**Evaluation order matters:** Prohibited content is checked first (immediate rejection), then compliance triggers (escalation), then ambiguity (clarification). Only requests passing all three checks proceed to the RAG Assistant.

---

## Design Principles

1. **Explicit over implicit** — Every rule has documented rationale
2. **Examples over abstractions** — Concrete patterns, not vague categories  
3. **Err toward safety** — When uncertain, escalate rather than proceed
4. **Auditable decisions** — Each classification maps to specific rule

---

## Maintenance Notes

These rules require periodic review:

- **Quarterly:** Compliance trigger updates based on regulatory changes
- **As needed:** Prohibited content updates based on emerging abuse patterns
- **Monthly:** Ambiguity heuristics refinement based on clarification loop metrics

---

## Related Documents

- [Sample Classifications](../evidence/sample-classifications.md) — Rules applied to real examples
- [ADR-001: Routing Logic](../architecture/ADR-001-routing-logic.md) — Why deterministic routing
- [Module README](../README.md) — Overall guardrails architecture