# Scoring — Evaluation Model

## Purpose

This folder contains documentation for the scoring model that evaluates AI opportunities across three dimensions and produces a composite score.

## Scoring Dimensions

| Dimension | What It Measures | Direction |
|-----------|------------------|-----------|
| **Business Value** | Impact on KPIs, revenue, cost, CX | Higher = stronger opportunity |
| **Implementation Feasibility** | Technical complexity, data availability, effort | Higher = more feasible |
| **Regulatory Complexity** | Compliance burden, data sensitivity, controls required | Higher = more complex (inverted for composite) |

## Scoring Scale

All dimensions use a **1–5 scale**:

| Score | Label |
|-------|-------|
| 1 | Very Low |
| 2 | Low |
| 3 | Medium |
| 4 | High |
| 5 | Very High |

## Composite Score

The composite score combines all three dimensions using configurable weights:

```
Composite = (Value × W_v) + (Feasibility × W_f) + ((6 - Regulatory) × W_r)
```

Regulatory complexity is inverted so that lower complexity contributes positively.

See [scoring-model.md](scoring-model.md) for full details including weight configuration guidance.

## Files in This Folder

| File | Purpose |
|------|---------|
| `scoring-model.md` | Complete scoring model documentation with weights |

## Related ADRs

- [ADR-0004 - ROI Scoring Model Design](../../../architecture/decisions/ADR-0004%20-%20ROI%20Scoring%20Model%20Design.md)

---

*See main [README](../README.md) for module overview.*