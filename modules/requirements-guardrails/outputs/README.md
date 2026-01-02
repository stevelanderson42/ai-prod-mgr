# Outputs Directory

**Module:** Requirements Guardrails  
**Purpose:** Demonstrate what the module produces — structured decision records for audit and compliance.

---

## Contents

| File | Description |
|------|-------------|
| [routing-decision-log.md](./routing-decision-log.md) | Sample audit trail with decision records for all routing outcomes |

---

## Key Artifacts

### Routing Decision Log

The primary output of the Requirements Guardrails module. Each request produces a structured record containing:

- **Routing decision** — PROCEED, CLARIFY, ESCALATE, or BLOCK
- **Triggered rules** — Which specific rules fired
- **Rationale** — Human-readable explanation
- **Metadata** — Processing time, classifier versions, flags

### Output Contract

Downstream systems (particularly the Compliance RAG Assistant) consume these outputs. The contract guarantees:

1. Every request gets exactly one routing decision
2. Decisions include traceable rule references
3. PROCEED requests include downstream target
4. ESCALATE requests include priority and tags
5. BLOCK requests do not log prohibited content

---

## Compliance Value

These outputs enable:

- **Audit trails** — Every decision is explainable and queryable
- **Regulatory reporting** — Aggregated metrics for compliance reviews
- **Pattern detection** — Trend analysis for emerging risks
- **Quality monitoring** — False positive/negative tracking

---

## Related Documents

- [Rules Directory](../rules/) — Classification logic that generates these outputs
- [Evidence: Sample Classifications](../evidence/sample-classifications.md) — Input examples
- [Module README](../README.md) — Overall architecture