# Advisor Transition Risk

**Live demo:** [https://stevelanderson42.github.io/advisor-transition-risk/](https://stevelanderson42.github.io/advisor-transition-risk/)

Advisor attrition and client attrition are usually tracked as separate metrics. At a wealth-management firm where the client relationship sits with an individual advisor, they are one causal chain: an advisor departure is among the largest single drivers of client loss, and a single exit can put an entire book in play at once.

This models that chain in three stages — which advisors may depart, which households would follow them out, and how much of the book a transition actually recovered.

All data is synthetic. No real clients or advisors are represented.

---

## The modeling decision

Household departure risk has two independent components, and collapsing them into a single score loses the thing that makes the output actionable.

**Baseline risk** — the likelihood a household leaves the firm regardless of who serves them. Driven by fees, performance, service failures, withdrawal behavior, and satisfaction.

**Follow likelihood** — the likelihood a household follows a specific advisor out the door, given that advisor departs. Driven by relationship concentration: tenure with the individual versus tenure with the firm, whether they arrived through that advisor's prior practice, how many service lines they use, how many people at the firm they know, portal engagement, and whether the advisor is their sole communication channel.

A household can be high on one and low on the other, and the two states call for entirely different responses. High follow with low baseline means a satisfied family whose only tie is one person — the intervention is to build a second relationship before anyone leaves. Low follow with high baseline is a fee, performance, or service problem that a retention play aimed at the advisor relationship would not address.

This is also why the advisor list shows a concentration column. Two advisors at identical flight risk can represent very different exposure depending on how much of their book is advisor-attached. In the generated data, one Elevated advisor carries 66% concentration and another carries 18% — the one you worry about is not the one most likely to leave, it's the one whose departure costs most.

---

## What's in it

Three tabs. The **Cascade** tab holds the three stages:

**Stage 1 — Advisor flight risk.** Six signals scored additively into Elevated / Watch / Stable bands. Bands rather than decimals: a score of 73 next to a named employee implies a calibration the model does not have.

**Stage 2 — Household exposure.** Baseline risk and follow likelihood scored and displayed side by side for every household in a selected advisor's book.

**Stage 3 — Transition plan.** For a departed advisor, the outreach sequence and an AUM waterfall showing retained, in progress, not started, and lost.

Navigation is a drill-down rather than a menu: clicking an advisor opens their book, and clicking a departed advisor opens their transition plan.

**Model / Definitions** — every signal, its point brackets, and the stated assumption behind its weight.

**Test Results** — eleven designed cases run against the scoring logic.

Every score decomposes into its top contributing factors inline, next to the band — never behind a click. A score whose reasoning requires a click is a score nobody trusts.

---

## Missing versus unreliable

Most systems treat absent data as a single condition. This distinguishes two:

**Missing** — no value exists. No satisfaction survey on file; acquisition origin never recorded.

**Unreliable** — a value exists but the underlying quantity is too thin to trust. A tenure ratio of 1.0 computed from 0.3 years over 0.3 years is arithmetically correct and substantively meaningless. Zero portal logins cannot distinguish "chooses not to use it" from "never activated."

When more than two signals in a score are missing or unreliable, the system returns **Insufficient data** rather than a band, and lists which signals are absent, which are present but untrustworthy, and why.

Concentration handles this the same way: households that could not be scored are excluded from the numerator but remain in the denominator, and any advisor whose book contains unscored households carries a visible note.

---

## Architecture

Python generates the synthetic data and computes every score offline, writing a single JSON file. A static React front end reads it. No server, no live inference, no API keys in client code.

That split is deliberate rather than expedient. The data is fixed and the scoring is deterministic, so nothing about the demo requires a live process at view time. The scoring logic lives in Python where it can be read and tested; the front end is a rendering layer.

Stack: Python, React, TypeScript, Vite. Deployed as static files to GitHub Pages.

---

## Running it

```
cd data
python generate.py          # writes output/data.json
python evaluation.py        # runs the designed test cases

cp output/data.json ../frontend/public/data.json

cd ../frontend
npm install
npm run dev                 # local
npm run build               # production, base path /advisor-transition-risk/
```

---

## What this is not

**The weights are illustrative.** They encode stated assumptions about relative signal importance, not fitted parameters. Real calibration would start with historical departures and the household retention outcomes that followed, and would almost certainly produce different weights than the ones here.

**The test suite verifies code against specification.** Eleven designed cases confirm the scoring implementation produces the bands the spec says it should. That is a unit test, not model validation. Validating the model would require running it against a population of real departures and measuring whether it discriminates.

**The retrospective advisor is one illustrative example.** A single departed advisor scored Elevated ninety days before leaving. One case is an illustration, not a backtest.

**The data is synthetic and was designed to exercise the logic.** Seven cases were specified deliberately and roughly a thousand households generated around them. Every number here was chosen to make the model's behavior visible.

---

## Decision log

**Bands, not decimals, for advisors.** A precise-looking number attached to a person's name reads as a verdict and implies precision the model doesn't have. Bands plus named contributing factors say *pay attention here*, which is the actual intent.

**Two scores, not one.** The single-score version is simpler and answers the wrong question. See above.

**Transparent additive scoring, not a fitted model.** With synthetic data there is nothing to fit against, and the point of the exercise is explicability. Every score decomposes into arithmetic a reader can check.

**Free-text signal included, with a caveat surfaced in the UI.** Manager and HR notes carry signal that structured fields miss — one designed advisor looks clean on every structured measure and is only visible through her notes. The interface states that in production those notes would be access-restricted by role. Scoring employees on manager commentary is not a neutral act, and the tool should say so.

**A single-hue color ramp, not red/amber/green.** Traffic lights on employee names read as a performance-management system. A neutral intensity gradient reads as an attention gradient, which is the honest framing.

**Read-only transition plan.** Mock state-change buttons would demonstrate nothing that the sequence and the running total don't already show.

**The dataset argued against its own thesis on the first pass.** The initial generation produced the highest-risk advisor at 5.3% concentration and the departed advisor at 8.3% — meaning the demo showed that the advisor most likely to leave had almost no exposure, and that his departure cost almost nothing. Every score was computed correctly. The data simply didn't exercise the logic in the way the argument required. That failure mode generalizes: a scoring model can be arithmetically sound and still tell you nothing, and you only find out by looking at what it produces on real distributions rather than by checking that the code runs.

---

## Files

```
data/
  scoring.py       signal definitions, weights, band thresholds, sufficiency rules
  cases.py         the seven designed cases
  evaluation.py    runs cases against scoring, reports pass/fail
  generate.py      synthetic data generation
frontend/
  src/views/       five views
  src/components/  shared table, band pill, factor list, AUM bar
PLAN.md            full specification, written before implementation
```

---

Built by **Steve L. Anderson** · [Portfolio](https://stevelanderson42.github.io) · [LinkedIn](https://www.linkedin.com/in/steve-l-anderson-1a16391/)
