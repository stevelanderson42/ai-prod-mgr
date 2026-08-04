# Advisor Transition Risk — Demo Plan

## Purpose

Demonstrate that advisor attrition and client attrition are not independent metrics but a single causal chain. In a wealth management firm where client relationships sit with individual advisors, an advisor departure is the largest single driver of client loss. This demo models that chain explicitly across three stages and makes the arithmetic visible.

All data is synthetic. The UI states this clearly.

---

## 1. Scoring Models

**Note on weights.** All weights in this section are illustrative. In a production system they would be calibrated against observed departure outcomes — historical advisor departures and the household-level retention results that followed. That data is unavailable in a synthetic demo. The weights here encode assumptions about relative signal importance, stated explicitly below, and produce the correct band assignments for the designed test cases in Section 3.

### 1A. Advisor Flight Risk

**What it answers:** Which advisors are likely to depart in the next 6–12 months?

**Output:** Band assignment (Elevated / Watch / Stable), not a decimal score.

**Thresholds:** Elevated >= 55, Watch 30–54, Stable < 30 (internal 0–100 scale, never shown to user).

| Signal | Max Points | Scoring Logic | Assumption |
|--------|-----------|---------------|------------|
| **Comp ratio** (advisor comp / peer-segment median) | 20 | <0.85 → 20; 0.85–0.94 → 14; 0.95–1.04 → 4; >=1.05 → 0 | Assumes below-market compensation is the strongest structured predictor of voluntary departure because advisors have high visibility into peer compensation and a liquid labor market. |
| **Production trend** (trailing-12mo AUM growth minus firm average) | 20 | <= -8% → 20; -4% to -8% → 14; -1% to -4% → 8; >=-1% → 0 | Assumes declining relative production signals either disengagement or client loss, both of which precede departure. An advisor whose book is shrinking relative to peers has less reason to stay and less to lose by leaving. |
| **Tenure bucket** | 10 | 2–5 years → 10; 5–8 years → 6; <2 or >8 → 2 | Assumes 2–5 years is the peak mobility window: the advisor has a portable book but has not yet accumulated enough deferred compensation, non-compete exposure, or organizational embeddedness to make departure costly. |
| **Organizational events** (passed over for promotion, manager change, compliance action — binary flags) | 15 | Each flag adds 5, capped at 15 | Assumes discrete organizational shocks loosen attachment. Each is individually ambiguous but they are additive — two concurrent events are meaningfully more predictive than one. |
| **Engagement decline** (% drop in CRM entries + client meetings, trailing 90 days vs. prior period) | 15 | >=40% decline → 15; 20–39% → 10; 10–19% → 5; <10% → 0 | Assumes behavioral withdrawal — fewer CRM updates, fewer logged meetings — is the closest available leading indicator of imminent departure. |
| **Free-text sentiment** (manager notes, HR notes — keyword/phrase match on a curated dictionary) | 20 | Match count and severity mapped to 0–20. See dictionary below. | Assumes manager and HR notes contain signal that structured fields miss, particularly for advisors who are outwardly performing but privately disengaged. Weighted high enough that strong text signal alone can push an otherwise-Stable advisor into Watch. |

**Free-text sentiment dictionary** (curated, not ML):
- High-signal phrases (each 7 pts, capped at 20): "exploring options," "recruiter contact," "not feeling valued," "considering leaving," "unhappy with direction"
- Medium-signal phrases (each 4 pts): "frustrated with," "looking at other," "not sure about future here," "comp discussion"
- Low-signal phrases (each 2 pts): "distracted lately," "less engaged," "skipping team meetings"

**UI note on free-text:** When free-text sentiment appears in the top-3 contributing factors, the triggering note excerpts are shown inline. A persistent disclaimer reads: *"In production, manager and HR notes would be access-restricted by role. Shown here for demonstration."*

### 1B. Household Baseline Risk

**What it answers:** How likely is this household to leave the firm regardless of what their advisor does?

**Output:** Band (High / Moderate / Low). Thresholds: High >= 55, Moderate 25–54, Low < 25.

| Signal | Max Points | Scoring Logic | Assumption |
|--------|-----------|---------------|------------|
| **Fee percentile** (household's effective fee vs. firm median for segment) | 20 | >=80th → 20; 60th–79th → 12; 40th–59th → 5; <40th → 0 | Assumes households paying well above median for their segment are more likely to leave when any additional irritant appears, because fee sensitivity is latent until activated by a triggering event. |
| **Trailing performance vs. benchmark** (household portfolio, 12mo) | 25 | <= -4% → 25; -2% to -4% → 16; -1% to -2% → 8; >=-1% → 0 | Assumes underperformance relative to benchmark is the most visible and emotionally salient driver of client dissatisfaction, because clients compare their returns to publicized indices. Weighted highest in this score. |
| **Service complaints** (count, trailing 12mo) | 20 | >=3 → 20; 2 → 14; 1 → 7; 0 → 0 | Assumes operational failures — errors, delays, unresolved issues — erode trust independently of investment outcomes and compound with each occurrence. |
| **Net flow trend** (net withdrawals as % of AUM, trailing 6mo) | 20 | >= 15% net withdrawal → 20; 8–14% → 12; 3–7% → 5; <3% → 0 | Assumes money leaving the account is the most direct behavioral signal of impending departure — clients withdraw assets before formally closing an account. |
| **Satisfaction survey** (last score, 1–10 scale) | 15 | <=4 → 15; 5–6 → 10; 7–8 → 4; >=9 → 0; missing → 8 (penalize absence) | Assumes self-reported satisfaction is informative despite known biases. Missing survey is penalized at moderate weight because non-response weakly correlates with disengagement. |

### 1C. Household Follow Likelihood

**What it answers:** If this household's advisor departs, how likely are they to follow the advisor rather than stay with the firm?

**Output:** Band (High / Moderate / Low). Thresholds: High >= 55, Moderate 25–54, Low < 25.

| Signal | Max Points | Scoring Logic | Assumption |
|--------|-----------|---------------|------------|
| **Advisor tenure ratio** (years with this advisor / years with firm) | 25 | >=0.9 → 25; 0.7–0.89 → 18; 0.5–0.69 → 10; <0.5 → 3 | Assumes a ratio near 1.0 means the client has never known another advisor at the firm and equates the advisor relationship with the firm relationship. Weighted highest because it captures relationship concentration directly. |
| **Acquisition origin** (did the household arrive through the advisor's acquired/recruited book?) | 20 | Yes → 20; No → 0 | Assumes clients who were brought in through an advisor's prior practice have already demonstrated willingness to follow that advisor across firms. Binary because the historical fact either applies or it doesn't. |
| **Service breadth** (count of distinct service lines: investments, planning, banking, insurance, trust) | 15 | 1 service → 15; 2 → 10; 3 → 5; >=4 → 0 | Assumes each additional service line creates a switching cost (new banking relationship, new insurance carrier, etc.) and creates a touchpoint with someone other than the primary advisor. |
| **Firm contacts** (number of firm employees the household has interacted with in last 12mo, excluding primary advisor) | 15 | 0 → 15; 1 → 10; 2 → 5; >=3 → 0 | Assumes multiple firm touchpoints create an independent relationship with the institution. A household that only knows one person at the firm has no separate reason to stay. |
| **Digital engagement** (portal logins per month, trailing 6mo average) | 10 | <1 → 10; 1–3 → 6; 4–8 → 3; >8 → 0 | Assumes active portal use indicates a relationship with the firm's platform and tools, not just the advisor. Weighted lower because portal usage alone is a weaker signal than direct human relationships. |
| **Communication exclusivity** (% of all firm communications routed solely through primary advisor) | 15 | >=85% → 15; 65–84% → 10; 40–64% → 5; <40% → 0 | Assumes that if the advisor is the sole communication channel, the firm has no independent relationship with the household. The advisor is the firm, functionally. |

### 1D. Minimum Data Requirements

A score is produced only when enough signals have reliable data. Signals are classified into two categories when they cannot contribute normally:

- **Missing:** No data exists for this signal (e.g., no satisfaction survey on file, acquisition origin unknown).
- **Unreliable:** Data exists but the underlying quantity is too thin to trust (e.g., tenure ratio computed from less than 1 year of data, portal logins of zero that could mean "never set up" rather than "chooses not to use").

Both categories count toward a data-sufficiency threshold. If more than 2 of 6 signals (follow likelihood) or more than 2 of 5 signals (baseline risk) are missing or unreliable, the system outputs **"Insufficient data"** instead of a band, with a list stating which signals are absent and which are present but unreliable, and why.

For advisors, all structured signals are assumed available from firm systems. Free-text is optional and scored as 0 when absent.

---

## 2. Data Model

### Entities

**Advisor**
| Field | Type | Notes |
|-------|------|-------|
| advisor_id | string | e.g., "ADV-001" |
| name | string | Synthetic name |
| team | string | e.g., "Northeast", "West" |
| tenure_years | float | Years at firm |
| comp_ratio | float | Advisor comp / peer-segment median |
| production_trend_pct | float | Trailing 12mo AUM growth minus firm average |
| org_events | list[string] | e.g., ["passed_over", "manager_change"] |
| engagement_decline_pct | float | % decline in CRM + meeting activity |
| free_text_notes | list[string] | Manager/HR note excerpts |
| book_aum | float | Total AUM of assigned households |
| household_count | int | Number of households |
| status | string | "active" or "departed" |
| departure_date | string or null | ISO date if departed |
| score_as_of_date | string or null | For departed advisors: the date the score snapshot was taken (90 days pre-departure). Null for active advisors. |
| flight_risk_score | int | 0–100, internal (used for sorting, never displayed) |
| flight_risk_band | string | "Elevated" / "Watch" / "Stable" |
| flight_risk_factors | list[{signal, value, points, note_excerpt?}] | Top 3 contributing factors. note_excerpt included when free-text sentiment is a top factor. |
| concentration_pct | float | % of book AUM in high-follow-likelihood households. Calculated as: exposed_aum / book_aum. Households with "Insufficient data" follow likelihood are excluded from the numerator (not counted as high-follow) but included in the denominator (still part of book AUM). |
| exposed_aum | float | AUM in high-follow-likelihood households |
| has_unscored_households | bool | True if any household in this advisor's book has "Insufficient data" for follow likelihood. When true, the UI shows a note: "N households ($XM AUM) could not be scored for follow likelihood due to insufficient data." |

**Household**
| Field | Type | Notes |
|-------|------|-------|
| household_id | string | e.g., "HH-0001" |
| name | string | Synthetic family name |
| advisor_id | string | FK to advisor |
| aum | float | Household AUM ($1M–$15M typical, up to $40M) |
| firm_tenure_years | float | Years as firm client |
| advisor_tenure_years | float | Years with current advisor |
| acquisition_origin | string or null | "advisor_book" / "firm_originated" / null (unknown) |
| service_lines | list[string] | e.g., ["investments", "planning", "trust"] |
| firm_contacts_count | int or null | Non-advisor firm contacts, trailing 12mo. Null if unknown. |
| portal_logins_monthly | float or null | Avg monthly portal logins, trailing 6mo. Null if account never activated. |
| communication_exclusivity_pct | float or null | % of comms through advisor only. Null if unknown. |
| fee_percentile | int | Effective fee percentile within segment |
| perf_vs_benchmark_pct | float or null | 12mo performance vs benchmark. Null if < 6 months history. |
| service_complaints_12mo | int | Count of complaints |
| net_flow_pct | float or null | Net flows as % of AUM, trailing 6mo. Null if < 6 months history. |
| satisfaction_score | int or null | Last survey, 1–10. Null if no survey. |
| baseline_risk_score | int or null | 0–100 or null if insufficient data |
| baseline_risk_band | string | "High" / "Moderate" / "Low" / "Insufficient data" |
| baseline_risk_factors | list[{signal, value, points}] | Top 3 contributing (empty if insufficient data) |
| baseline_missing_signals | list[{signal, reason}] | Present only when band is "Insufficient data" |
| follow_likelihood_score | int or null | 0–100 or null if insufficient data |
| follow_likelihood_band | string | "High" / "Moderate" / "Low" / "Insufficient data" |
| follow_likelihood_factors | list[{signal, value, points}] | Top 3 contributing (empty if insufficient data) |
| follow_missing_signals | list[{signal, reason}] | Present only when band is "Insufficient data" |

**Transition Plan Entry** (one per household for each departed advisor)
| Field | Type | Notes |
|-------|------|-------|
| household_id | string | FK to household |
| advisor_id | string | FK to departed advisor |
| status | string | "not_started" / "scheduled" / "contacted" / "retained" / "lost" |
| assigned_to | string | Name of covering advisor or relationship manager |
| last_contact_date | string or null | ISO date |
| next_action | string | e.g., "Schedule intro call with new advisor" |
| follow_likelihood_band | string | Carried from household score |
| baseline_risk_band | string | Carried from household score |

**Evaluation Case**
| Field | Type | Notes |
|-------|------|-------|
| case_id | string | e.g., "CASE-ADV-1" |
| case_type | string | "advisor" or "household" |
| label | string | Human-readable case name |
| description | string | What this case tests |
| input_values | dict | The exact field values used |
| expected_band | string | Expected output band |
| actual_band | string | What the scoring logic produced |
| pass | bool | expected == actual |

---

## 3. Designed Cases

### 3A. Advisor Cases

All three advisor cases are planted first, then ~32 random advisors are generated around them with scores distributed mostly in Watch and Stable bands (~10% Elevated, ~25% Watch, ~65% Stable).

---

**CASE-ADV-1: Clear Elevated Risk — "Marcus Webb"**

The obvious case. Multiple structured signals fire simultaneously.

| Signal | Value | Points |
|--------|-------|--------|
| Comp ratio | 0.83 | 20/20 |
| Production trend | -9% | 20/20 |
| Tenure | 4 years | 10/10 |
| Org events | ["passed_over", "manager_change"] | 10/15 |
| Engagement decline | 45% | 15/15 |
| Free-text notes | ["solid performer, no concerns noted"] | 0/20 |
| **Total** | | **75 → Elevated** |

Top 3 factors displayed: Production trend (-9% vs. firm avg), Comp ratio (0.83x peer median), Engagement decline (45% drop).

Book: 42 households, $185M AUM. This advisor's book contains all four designed household cases.

---

**CASE-ADV-2: Subtle Risk — "Diana Chen"**

Structured signals look clean. The risk lives in free-text notes from her manager.

| Signal | Value | Points |
|--------|-------|--------|
| Comp ratio | 1.02 | 4/20 |
| Production trend | +1% | 0/20 |
| Tenure | 3 years | 10/10 |
| Org events | [] | 0/15 |
| Engagement decline | 8% | 0/15 |
| Free-text notes | ["mentioned recruiter contact at industry event", "seems less engaged in team planning, exploring options", "not feeling valued after comp review"] | 20/20 |
| **Total** | | **34 → Watch** |

Top 3 factors displayed: Manager notes ("recruiter contact," "exploring options," "not feeling valued" — *in production these would be access-restricted*), Tenure (3 years, peak mobility window), Comp ratio (1.02x, at market).

This case exists to show that a purely structured model would rate her Stable. The free-text signal is what pushes her into Watch.

---

**CASE-ADV-3: Retrospective — "James Okafor" (illustrative, not validation)**

Already departed. Status is "departed," departure_date is set. The UI shows what the model would have scored 90 days before departure, using the snapshotted input values from that date. A label reads: *"Score as of [date], 90 days before departure."*

This is a single illustrative example of what the model would have said before a known departure. It is not a validation of the model — validating would require running the scoring logic against a population of historical departures and measuring discrimination, which requires real outcome data unavailable in a synthetic demo.

| Signal | Value (as of 90 days pre-departure) | Points |
|--------|--------------------------------------|--------|
| Comp ratio | 0.88 | 14/20 |
| Production trend | -6% | 14/20 |
| Tenure | 6 years | 6/10 |
| Org events | ["compliance_action"] | 5/15 |
| Engagement decline | 42% | 15/15 |
| Free-text notes | ["frustrated with new compliance requirements", "brought up comp discussion in one-on-one"] | 8/20 |
| **Total** | | **62 → Elevated** |

Book at departure: 28 households, $120M AUM. Transition plan entries exist for his households, showing a mix of retained / in-progress / lost statuses.

---

### 3B. Household Cases

All four are in Marcus Webb's book (CASE-ADV-1).

---

**CASE-HH-1: High Follow, Low Baseline — "The Paterson Family"**

Happy with the firm's service but their entire relationship is through Marcus. If he leaves, they follow.

| Signal (Follow Likelihood) | Value | Points |
|----------------------------|-------|--------|
| Advisor tenure ratio | 7yr / 7yr = 1.0 | 25/25 |
| Acquisition origin | advisor_book | 20/20 |
| Service breadth | 1 (investments only) | 15/15 |
| Firm contacts | 1 | 10/15 |
| Portal logins/mo | 2 | 6/10 |
| Communication exclusivity | 78% | 10/15 |
| **Follow total** | | **86 → High** |

| Signal (Baseline Risk) | Value | Points |
|-------------------------|-------|--------|
| Fee percentile | 45th | 5/20 |
| Perf vs benchmark | +1.2% | 0/25 |
| Service complaints | 0 | 0/20 |
| Net flow trend | -1% | 0/20 |
| Satisfaction score | 9 | 0/15 |
| **Baseline total** | | **5 → Low** |

AUM: $8.2M. Retention priority if Marcus departs — satisfied but entirely advisor-attached.

---

**CASE-HH-2: Low Follow, High Baseline — "The Nakamura Family"**

Long firm tenure, multiple firm relationships, but independently dissatisfied. May leave whether or not Marcus does.

| Signal (Follow Likelihood) | Value | Points |
|----------------------------|-------|--------|
| Advisor tenure ratio | 2yr / 14yr = 0.14 | 3/25 |
| Acquisition origin | firm_originated | 0/20 |
| Service breadth | 4 (investments, planning, banking, trust) | 0/15 |
| Firm contacts | 4 | 0/15 |
| Portal logins/mo | 7 | 3/10 |
| Communication exclusivity | 25% | 0/15 |
| **Follow total** | | **6 → Low** |

| Signal (Baseline Risk) | Value | Points |
|-------------------------|-------|--------|
| Fee percentile | 82nd | 20/20 |
| Perf vs benchmark | -3.5% | 16/25 |
| Service complaints | 3 | 20/20 |
| Net flow trend | -10% | 12/20 |
| Satisfaction score | 4 | 15/15 |
| **Baseline total** | | **83 → High** |

AUM: $4.5M. Needs attention regardless of advisor retention — the problem is fees, performance, and service quality.

---

**CASE-HH-3: Low on Both — "The Brennan Family"**

Deeply embedded in the firm, connected to multiple people, and largely satisfied. Low risk on every dimension.

| Signal (Follow Likelihood) | Value | Points |
|----------------------------|-------|--------|
| Advisor tenure ratio | 3yr / 10yr = 0.3 | 3/25 |
| Acquisition origin | firm_originated | 0/20 |
| Service breadth | 5 (all lines) | 0/15 |
| Firm contacts | 5 | 0/15 |
| Portal logins/mo | 15 | 0/10 |
| Communication exclusivity | 20% | 0/15 |
| **Follow total** | | **3 → Low** |

| Signal (Baseline Risk) | Value | Points |
|-------------------------|-------|--------|
| Fee percentile | 44th | 5/20 |
| Perf vs benchmark | +2.8% | 0/25 |
| Service complaints | 0 | 0/20 |
| Net flow trend | +5% (net inflows) | 0/20 |
| Satisfaction score | 8 | 4/15 |
| **Baseline total** | | **9 → Low** |

AUM: $12.1M. Largest household in the book but lowest risk. Demonstrates that AUM and risk are not correlated.

---

**CASE-HH-4: Insufficient Signal — "The Domingo Account"**

New account, sparse data. The system declines to score rather than guess.

| Signal (Follow Likelihood) | Value | Status | Points |
|----------------------------|-------|--------|--------|
| Advisor tenure ratio | 0.3yr / 0.3yr = 1.0 | **Unreliable** — denominator < 1 year; ratio will converge as tenure grows | (25, but flagged) |
| Acquisition origin | null | **Missing** — not yet recorded in CRM | — |
| Service breadth | 1 | Present | 15/15 |
| Firm contacts | null | **Missing** — insufficient interaction history | — |
| Portal logins/mo | 0 | **Unreliable** — account portal never activated; cannot distinguish "doesn't use" from "never set up" | (10, but flagged) |
| Communication exclusivity | null | **Missing** — insufficient interaction history | — |
| **Follow total** | | **Insufficient data** (3 missing + 2 unreliable, exceeds threshold of 2) | |

| Signal (Baseline Risk) | Value | Status | Points |
|-------------------------|-------|--------|--------|
| Fee percentile | 50th | Present | 5/20 |
| Perf vs benchmark | null | **Missing** — less than 6 months of history | — |
| Service complaints | 0 | Present | 0/20 |
| Net flow trend | null | **Missing** — less than 6 months of history | — |
| Satisfaction score | null | **Missing** — no survey sent | — |
| **Baseline total** | | **Insufficient data** (3 missing, exceeds threshold of 2) | |

AUM: $1.8M. UI shows "Insufficient data" with the list of which signals are missing and which are present but unreliable, with the reason for each.

---

## 4. Views

### Color System

Single hue: **indigo** (HSL ~235). Three intensity levels:
- Dark indigo: Elevated / High (risk or likelihood)
- Medium indigo: Watch / Moderate
- Light indigo: Stable / Low
- Gray: Insufficient data

### Navigation

State-based view switching — no router. The app maintains a simple state object tracking the current view and selected advisor ID. A persistent breadcrumb component reflects the current position in the cascade (Advisor List → Advisor Name → Transition Plan) and each segment is clickable to navigate back.

### 4A. Advisor List View (Stage 1)

**Decision statement** (shown at top of view): *"Which advisor departures would create the largest client exposure?"*

**Synthetic data banner**: Persistent top bar across all views — *"This demo uses synthetic data. No real clients or advisors are represented."*

**Layout**: Sortable table with the following columns:

| Column | Content |
|--------|---------|
| Advisor | Name |
| Risk Band | Elevated / Watch / Stable, colored pill |
| Top Factors | Top 3 contributing factors, inline text (e.g., "Comp 0.83x peer, Production -9%, Engagement -45%"). When free-text is a factor, shows note excerpts with access-restriction disclaimer. |
| Book AUM | Total AUM, abbreviated (e.g., "$185M") |
| Exposed AUM | Sum of AUM for high-follow-likelihood households, abbreviated |
| Concentration | Exposed AUM / Book AUM, shown as percentage and a small bar |
| Households | Count |
| Status | Active / Departed. Departed advisors show score_as_of_date: *"Score as of [date], 90 days pre-departure"* |

**Default sort**: By risk band (Elevated first), then by exposed AUM descending within band.

**Interaction**: Clicking an active advisor row navigates to the Household Exposure view (Stage 2). Clicking a departed advisor navigates to the Transition Plan view (Stage 3).

**Key design point**: The Concentration column is the payoff of the two-score model. Two advisors can both be Elevated risk, but one has 80% of their book in high-follow households while another has 20%. The exposure is 4x different despite the same flight risk.

### 4B. Household Exposure View (Stage 2)

**Breadcrumb**: Advisor List → **[Advisor Name]**

**Decision statement**: *"If [Advisor Name] departs, which households need proactive outreach?"*

**Summary header**:
- Advisor name, risk band
- Book AUM (total)
- Exposed AUM (high-follow households)
- Concentration percentage

**Layout**: Sortable table:

| Column | Content |
|--------|---------|
| Household | Family name |
| AUM | Household AUM, abbreviated |
| Follow Likelihood | Band (colored pill) + top 3 factors inline. "Insufficient data" shows missing/unreliable signal list. |
| Baseline Risk | Band (colored pill) + top 3 factors inline. "Insufficient data" shows missing/unreliable signal list. |

**Default sort**: By follow likelihood band (High first), then by AUM descending.

**Interaction**: Read-only. No further drill-down — the household level is the terminal detail view in the cascade. The transition plan view is reached by clicking a departed advisor from Stage 1.

**Key design point**: The two-column score display (follow likelihood and baseline risk side by side) is the core modeling distinction made visible. The two-score model implies different interventions, not just different levels of attention. High follow / low baseline calls for building a second firm relationship before any departure occurs — the household is satisfied but has no reason to stay if the advisor leaves. Low follow / high baseline is a fee, performance, or service problem that a retention play aimed at the advisor relationship would not address — these households need service remediation regardless of advisor status.

### 4C. Transition Plan View (Stage 3)

**Breadcrumb**: Advisor List → **[Advisor Name]** → Transition Plan

**Decision statement**: *"How much of [Advisor Name]'s book has been retained, and what remains at risk?"*

**Temporal label**: *"Advisor departed [date]. Risk scores shown are as of [score_as_of_date], 90 days pre-departure."*

**Summary header** — AUM waterfall:
- **Retained**: Households marked "retained" — AUM sum, with percentage of total
- **In Progress**: Households in "scheduled" or "contacted" — AUM sum
- **Not Started**: Households in "not_started" — AUM sum
- **Lost**: Households marked "lost" — AUM sum

Displayed as a single horizontal stacked bar using indigo intensity (retained = lightest, lost = darkest).

**Layout**: Sortable table:

| Column | Content |
|--------|---------|
| Household | Family name |
| AUM | Household AUM, abbreviated |
| Status | not_started / scheduled / contacted / retained / lost (colored pill) |
| Assigned To | Covering advisor name |
| Last Contact | Date |
| Next Action | Text description of next step |
| Follow Likelihood | Band (from original scoring) |
| Baseline Risk | Band (from original scoring) |

**Default sort**: By status priority (not_started first — these need action), then by AUM descending.

**Read-only**: All data is display-only from the synthetic dataset. No mock interactivity.

**Key design point**: The exposed AUM from Stage 1 decomposes here into retained / in-progress / lost. This is the same number tracked through all three stages of the cascade.

### 4D. Evaluation View

**Accessed via**: A top-level tab alongside the main advisor list, labeled "Evaluation."

**Disclaimer** (shown at top): *"This section verifies that the scoring code produces the expected band assignments for a set of designed test cases. It confirms the implementation matches its specification. It does not validate the model — that would require running the scoring logic against historical departure outcomes, which are unavailable in a synthetic demo."*

**Layout**:
- Overall pass rate as a large number (e.g., "7 / 7 passing")
- Table of test cases:

| Column | Content |
|--------|---------|
| Case ID | e.g., CASE-ADV-1 |
| Label | e.g., "Clear elevated risk — Marcus Webb" |
| Type | Advisor / Household |
| Description | What the case tests (one sentence) |
| Expected | Expected band |
| Actual | Actual band produced by scoring |
| Result | Pass / Fail (colored) |

- Expandable rows showing all input values and point-by-point scoring breakdown

---

## 5. File and Folder Structure

```
modules/advisor-transition-risk/
├── PLAN.md                          # This file
├── data/
│   ├── generate.py                  # Main script: generates all data, writes JSON
│   ├── scoring.py                   # Signal definitions, weights, scoring functions
│   ├── cases.py                     # Designed case specifications (the 7 cases above)
│   ├── evaluation.py                # Runs designed cases against scoring, outputs pass/fail
│   └── output/
│       └── data.json                # Complete output consumed by frontend
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts               # base: '/advisor-transition-risk/'
│   ├── public/
│   │   └── data.json                # Copied from data/output/ during build
│   └── src/
│       ├── main.tsx
│       ├── App.tsx                   # State-based view switching, no router
│       ├── types.ts                 # TypeScript types mirroring data model
│       ├── theme.ts                 # Indigo color scale, band-to-color mapping
│       ├── views/
│       │   ├── AdvisorListView.tsx   # Stage 1
│       │   ├── HouseholdView.tsx     # Stage 2
│       │   ├── TransitionView.tsx    # Stage 3
│       │   └── EvaluationView.tsx    # Test cases
│       └── components/
│           ├── Breadcrumb.tsx
│           ├── RiskBand.tsx          # Colored pill component
│           ├── FactorList.tsx        # Inline top-3 factors
│           ├── AumBar.tsx            # Stacked horizontal bar
│           ├── SortableTable.tsx     # Reusable sortable table
│           └── SyntheticBanner.tsx   # "Synthetic data" warning bar
└── README.md                        # How to generate data and run locally
```

---

## 6. Build Sequence

**Phase 1 — Data generation (Python)**
1. Implement `scoring.py`: signal definitions, weight tables, scoring functions, band thresholds, minimum-data rules (including missing vs. unreliable distinction)
2. Implement `cases.py`: the 7 designed cases with exact input values from Section 3
3. Implement `evaluation.py`: run cases through scoring, output pass/fail
4. Implement `generate.py`: create ~35 advisors (including 3 designed), ~1,000 households (including 4 designed), transition plan entries for the departed advisor, write `data.json`
5. Verify: run evaluation, confirm 7/7 pass

**Phase 2 — Frontend scaffold**
6. Initialize Vite + React + TypeScript project in `frontend/`
7. Define types in `types.ts`, implement state-based view switching in `App.tsx` (no React Router)
8. Implement `theme.ts` with indigo color scale
9. Build shared components: `SyntheticBanner`, `RiskBand`, `FactorList`, `Breadcrumb`, `SortableTable`

**Phase 3 — Views**
10. Advisor List View (Stage 1) — table, sorting, click-through, concentration column
11. Household Exposure View (Stage 2) — header summary, dual-score table with factor display
12. Transition Plan View (Stage 3) — AUM waterfall bar, status table, temporal labels
13. Evaluation View — disclaimer, pass/fail table with expandable detail

**Phase 4 — Deploy**
14. Configure Vite base path: `/advisor-transition-risk/`
15. Copy `data.json` into `public/`
16. Build static output; copy to separate GitHub Pages repo under `/advisor-transition-risk/` subpath
