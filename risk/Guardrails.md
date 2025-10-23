# Guardrails

## Refusal Policy
- Refuse when confidence < threshold or when request is unsafe/out-of-policy.

## Safety Checks
- Prompt filters: banned topics list
- Output filters: Regex/heuristics to block sensitive content
- Red‑team prompts: See `/evals/datasets/redteam.jsonl`

## Metrics
- Target refusal rate band for OOS: 5–10%
- Hallucination rate: < 3% on gold set
