# Module 3 — Session 3 Status (Streamlit UI + Deploy)

**Date:** May 21, 2026
**Session result:** Live demo deployed.

## Shipped

- Interactive Streamlit UI at https://requirements-guardrails.streamlit.app
- Compare Mode (sidebar toggle) demonstrating ADR-003 and ADR-004 mechanisms
- 5 canonical example buttons drawn from `evidence/sample-classifications.md` (Samples 1, 2, 3, 5, 9)
- Verdict panel: classification badge, driver rule, decision reason, missing-context
- Audit panels: triggered rules (with suppression/upgrade markers) and mechanisms applied
- 21/21 tests passing (15 acceptance + 6 Compare Mode)
- Classifier non-mutating refactor: `effective_classification` computed separately, addressing the ADR-004 v2 cleanup note
- Deployed to Streamlit Cloud

## Deferred — cleanup pass (Task 7: Module 3 README update)

1. **YAML rule descriptions read like dev docs.** Surface in any non-PROCEED non-CLARIFY verdict. Need calibration to reviewer-facing tone — 1–2 sentences, neutral.
2. **UTF-8 encoding glitch.** Em-dash rendering as `â€"` in at least one YAML description. Audit all `src/config/*.yaml` files for encoding mismatches.
3. **PROCEED with 0 rules fired could render more affirmatively.** Currently shows "Driver rule: _none (no rules fired)_" which is technically accurate but understates that rules were evaluated. Consider "All rules evaluated; none triggered."
4. **Mobile viewport.** [Confirm mobile rendering — note here if any column-stacking issues appear.]

## Architectural notes for next session

- Classifier signature is now `classify(query, apply_mechanisms: bool = True)`. Any future caller (including Module 4 integration) should default to `True`.
- `TriggeredRule` now carries `original_classification`, `effective_classification`, `suppressed_by_override`, `upgraded_by_produce_intent`. ADR-004's v2 cleanup of in-place mutation is done.
- `resolve_priority` now returns `(Classification, Category, TriggeredRule | None)`. The third element is the rule that won priority resolution.

## Next session (Task 7 — Module 3 README update)

Per the Notion Module Work plan:
- Rewrite Module 3 README to reflect working classifier + live demo
- Articulate composition story with Module 4 using Option 2 language
- Update status from "In Progress" to working
- Address the three polish items deferred from this session
- Estimated: 2–3 hours

Per the Notion plan ordering revision: PAUSE & REASSESS checkpoint after Task 7, before Task 8 (Module 4 README update).