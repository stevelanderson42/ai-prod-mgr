"""
Scoring logic for advisor flight risk, household baseline risk,
and household follow likelihood.

All weights are illustrative. In production they would be calibrated
against observed departure outcomes.
"""

from typing import Optional

# ---------------------------------------------------------------------------
# Advisor Flight Risk
# ---------------------------------------------------------------------------

ADVISOR_BAND_THRESHOLDS = {"Elevated": 55, "Watch": 30}  # < 30 = Stable

# Free-text sentiment dictionary
HIGH_SIGNAL_PHRASES = [
    "exploring options",
    "recruiter contact",
    "not feeling valued",
    "considering leaving",
    "unhappy with direction",
]
MEDIUM_SIGNAL_PHRASES = [
    "frustrated with",
    "looking at other",
    "not sure about future here",
    "comp discussion",
]
LOW_SIGNAL_PHRASES = [
    "distracted lately",
    "less engaged",
    "skipping team meetings",
]


def _score_comp_ratio(ratio: float) -> int:
    if ratio < 0.85:
        return 20
    if ratio < 0.95:
        return 14
    if ratio < 1.05:
        return 4
    return 0


def _score_production_trend(pct: float) -> int:
    if pct <= -8:
        return 20
    if pct <= -4:
        return 14
    if pct <= -1:
        return 8
    return 0


def _score_tenure_bucket(years: float) -> int:
    if 2 <= years <= 5:
        return 10
    if 5 < years <= 8:
        return 6
    return 2


def _score_org_events(events: list[str]) -> int:
    return min(len(events) * 5, 15)


def _score_engagement_decline(pct: float) -> int:
    if pct >= 40:
        return 15
    if pct >= 20:
        return 10
    if pct >= 10:
        return 5
    return 0


def _score_free_text(notes: list[str]) -> int:
    combined = " ".join(notes).lower()
    total = 0
    for phrase in HIGH_SIGNAL_PHRASES:
        if phrase in combined:
            total += 7
    for phrase in MEDIUM_SIGNAL_PHRASES:
        if phrase in combined:
            total += 4
    for phrase in LOW_SIGNAL_PHRASES:
        if phrase in combined:
            total += 2
    return min(total, 20)


def _matched_phrases(notes: list[str]) -> list[str]:
    """Return the list of matched phrases for display purposes."""
    combined = " ".join(notes).lower()
    matched = []
    for phrase in HIGH_SIGNAL_PHRASES:
        if phrase in combined:
            matched.append(phrase)
    for phrase in MEDIUM_SIGNAL_PHRASES:
        if phrase in combined:
            matched.append(phrase)
    for phrase in LOW_SIGNAL_PHRASES:
        if phrase in combined:
            matched.append(phrase)
    return matched


def _band_from_score(score: int, thresholds: dict) -> str:
    """Generic band assignment. thresholds maps band name -> minimum score,
    checked in descending order of minimum."""
    for band, minimum in sorted(thresholds.items(), key=lambda x: -x[1]):
        if score >= minimum:
            return band
    # Below all thresholds
    if thresholds is ADVISOR_BAND_THRESHOLDS:
        return "Stable"
    return "Low"


def score_advisor(advisor: dict) -> dict:
    """Score an advisor and return score, band, and top-3 factors."""
    signals = [
        ("Comp ratio", advisor["comp_ratio"],
         _score_comp_ratio(advisor["comp_ratio"]), 20,
         f'{advisor["comp_ratio"]:.2f}x peer median'),
        ("Production trend", advisor["production_trend_pct"],
         _score_production_trend(advisor["production_trend_pct"]), 20,
         f'{advisor["production_trend_pct"]:+.0f}% vs. firm avg'),
        ("Tenure", advisor["tenure_years"],
         _score_tenure_bucket(advisor["tenure_years"]), 10,
         f'{advisor["tenure_years"]:.0f} years'),
        ("Org events", advisor["org_events"],
         _score_org_events(advisor["org_events"]), 15,
         ", ".join(advisor["org_events"]) if advisor["org_events"] else "none"),
        ("Engagement decline", advisor["engagement_decline_pct"],
         _score_engagement_decline(advisor["engagement_decline_pct"]), 15,
         f'{advisor["engagement_decline_pct"]:.0f}% drop'),
        ("Free-text sentiment", advisor["free_text_notes"],
         _score_free_text(advisor["free_text_notes"]), 20,
         ", ".join(_matched_phrases(advisor["free_text_notes"])) or "none"),
    ]

    total = sum(s[2] for s in signals)
    band = _band_from_score(total, ADVISOR_BAND_THRESHOLDS)

    # Top 3 factors by points (descending), break ties by max-points
    ranked = sorted(signals, key=lambda s: (-s[2], -s[3]))
    top3 = []
    for name, raw_value, points, max_pts, display_value in ranked[:3]:
        factor = {"signal": name, "value": display_value, "points": points}
        if name == "Free-text sentiment" and points > 0:
            factor["note_excerpt"] = ", ".join(
                f'"{p}"' for p in _matched_phrases(advisor["free_text_notes"])
            )
        top3.append(factor)

    return {
        "flight_risk_score": total,
        "flight_risk_band": band,
        "flight_risk_factors": top3,
    }


# ---------------------------------------------------------------------------
# Household Baseline Risk
# ---------------------------------------------------------------------------

BASELINE_BAND_THRESHOLDS = {"High": 55, "Moderate": 25}  # < 25 = Low


def _score_fee_percentile(pct: int) -> int:
    if pct >= 80:
        return 20
    if pct >= 60:
        return 12
    if pct >= 40:
        return 5
    return 0


def _score_perf_vs_benchmark(pct: float) -> int:
    if pct <= -4:
        return 25
    if pct <= -2:
        return 16
    if pct <= -1:
        return 8
    return 0


def _score_service_complaints(count: int) -> int:
    if count >= 3:
        return 20
    if count == 2:
        return 14
    if count == 1:
        return 7
    return 0


def _score_net_flow(pct: float) -> int:
    # pct is net flow as % of AUM; negative = withdrawals
    # We score on withdrawal magnitude, so use abs of negative
    withdrawal = -pct if pct < 0 else 0
    if withdrawal >= 15:
        return 20
    if withdrawal >= 8:
        return 12
    if withdrawal >= 3:
        return 5
    return 0


def _score_satisfaction(score: Optional[int]) -> int:
    if score is None:
        return 8  # penalize absence
    if score <= 4:
        return 15
    if score <= 6:
        return 10
    if score <= 8:
        return 4
    return 0


def score_household_baseline(household: dict) -> dict:
    """Score baseline risk. Returns score, band, factors, or insufficient-data."""
    # Check data sufficiency
    missing_signals = []
    perf = household.get("perf_vs_benchmark_pct")
    net_flow = household.get("net_flow_pct")
    satisfaction = household.get("satisfaction_score")

    if perf is None:
        missing_signals.append({
            "signal": "Trailing performance vs. benchmark",
            "reason": "Less than 6 months of history",
        })
    if net_flow is None:
        missing_signals.append({
            "signal": "Net flow trend",
            "reason": "Less than 6 months of history",
        })
    if satisfaction is None:
        missing_signals.append({
            "signal": "Satisfaction survey",
            "reason": "No survey on file",
        })

    if len(missing_signals) > 2:
        return {
            "baseline_risk_score": None,
            "baseline_risk_band": "Insufficient data",
            "baseline_risk_factors": [],
            "baseline_missing_signals": missing_signals,
        }

    # Score each signal
    signals = [
        ("Fee percentile", household["fee_percentile"],
         _score_fee_percentile(household["fee_percentile"]), 20,
         f'{household["fee_percentile"]}th percentile'),
        ("Trailing performance", perf,
         _score_perf_vs_benchmark(perf) if perf is not None else 0, 25,
         f'{perf:+.1f}% vs. benchmark' if perf is not None else "N/A"),
        ("Service complaints", household["service_complaints_12mo"],
         _score_service_complaints(household["service_complaints_12mo"]), 20,
         f'{household["service_complaints_12mo"]} in 12 months'),
        ("Net flow trend", net_flow,
         _score_net_flow(net_flow) if net_flow is not None else 0, 20,
         f'{net_flow:+.1f}% of AUM' if net_flow is not None else "N/A"),
        ("Satisfaction survey", satisfaction,
         _score_satisfaction(satisfaction), 15,
         f'{satisfaction}/10' if satisfaction is not None else "missing"),
    ]

    total = sum(s[2] for s in signals)
    band = _band_from_score(total, BASELINE_BAND_THRESHOLDS)
    ranked = sorted(signals, key=lambda s: (-s[2], -s[3]))
    top3 = [{"signal": s[0], "value": s[4], "points": s[2]} for s in ranked[:3]]

    return {
        "baseline_risk_score": total,
        "baseline_risk_band": band,
        "baseline_risk_factors": top3,
        "baseline_missing_signals": missing_signals,
    }


# ---------------------------------------------------------------------------
# Household Follow Likelihood
# ---------------------------------------------------------------------------

FOLLOW_BAND_THRESHOLDS = {"High": 55, "Moderate": 25}  # < 25 = Low

# Minimum tenure denominator for reliable ratio
MIN_TENURE_YEARS_FOR_RATIO = 1.0


def _score_advisor_tenure_ratio(
    advisor_tenure: float, firm_tenure: float
) -> tuple[int, Optional[dict]]:
    """Returns (points, unreliable_info_or_None)."""
    if firm_tenure < MIN_TENURE_YEARS_FOR_RATIO:
        return (0, {
            "signal": "Advisor tenure ratio",
            "reason": f"Denominator < 1 year ({firm_tenure:.1f} years); "
                      "ratio will converge as tenure grows",
        })
    ratio = advisor_tenure / firm_tenure if firm_tenure > 0 else 1.0
    if ratio >= 0.9:
        return (25, None)
    if ratio >= 0.7:
        return (18, None)
    if ratio >= 0.5:
        return (10, None)
    return (3, None)


def _score_acquisition_origin(origin: Optional[str]) -> tuple[int, Optional[dict]]:
    if origin is None:
        return (0, {
            "signal": "Acquisition origin",
            "reason": "Not yet recorded in CRM",
        })
    return (20 if origin == "advisor_book" else 0, None)


def _score_service_breadth(lines: list[str]) -> int:
    n = len(lines)
    if n <= 1:
        return 15
    if n == 2:
        return 10
    if n == 3:
        return 5
    return 0


def _score_firm_contacts(count: Optional[int]) -> tuple[int, Optional[dict]]:
    if count is None:
        return (0, {
            "signal": "Firm contacts",
            "reason": "Insufficient interaction history",
        })
    if count == 0:
        return (15, None)
    if count == 1:
        return (10, None)
    if count == 2:
        return (5, None)
    return (0, None)


def _score_portal_logins(
    logins: Optional[float], firm_tenure: float
) -> tuple[int, Optional[dict]]:
    if logins is None or (logins == 0 and firm_tenure < MIN_TENURE_YEARS_FOR_RATIO):
        return (0, {
            "signal": "Digital engagement",
            "reason": "Account portal never activated; cannot distinguish "
                      "'doesn't use' from 'never set up'",
        })
    if logins < 1:
        return (10, None)
    if logins <= 3:
        return (6, None)
    if logins <= 8:
        return (3, None)
    return (0, None)


def _score_comm_exclusivity(pct: Optional[float]) -> tuple[int, Optional[dict]]:
    if pct is None:
        return (0, {
            "signal": "Communication exclusivity",
            "reason": "Insufficient interaction history",
        })
    if pct >= 85:
        return (15, None)
    if pct >= 65:
        return (10, None)
    if pct >= 40:
        return (5, None)
    return (0, None)


def score_household_follow(household: dict) -> dict:
    """Score follow likelihood. Returns score, band, factors, or insufficient-data."""
    firm_tenure = household.get("firm_tenure_years", 0)

    # Evaluate each signal, collecting unreliable/missing info
    problems = []  # list of {signal, reason}

    tenure_pts, tenure_problem = _score_advisor_tenure_ratio(
        household.get("advisor_tenure_years", 0), firm_tenure
    )
    if tenure_problem:
        problems.append(tenure_problem)

    origin_pts, origin_problem = _score_acquisition_origin(
        household.get("acquisition_origin")
    )
    if origin_problem:
        problems.append(origin_problem)

    breadth_pts = _score_service_breadth(household.get("service_lines", []))

    contacts_pts, contacts_problem = _score_firm_contacts(
        household.get("firm_contacts_count")
    )
    if contacts_problem:
        problems.append(contacts_problem)

    portal_pts, portal_problem = _score_portal_logins(
        household.get("portal_logins_monthly"), firm_tenure
    )
    if portal_problem:
        problems.append(portal_problem)

    comm_pts, comm_problem = _score_comm_exclusivity(
        household.get("communication_exclusivity_pct")
    )
    if comm_problem:
        problems.append(comm_problem)

    # Data sufficiency: > 2 problems means insufficient data
    if len(problems) > 2:
        return {
            "follow_likelihood_score": None,
            "follow_likelihood_band": "Insufficient data",
            "follow_likelihood_factors": [],
            "follow_missing_signals": problems,
        }

    signals = [
        ("Advisor tenure ratio", tenure_pts, 25,
         f'{household.get("advisor_tenure_years", 0):.0f}yr / '
         f'{firm_tenure:.0f}yr'),
        ("Acquisition origin", origin_pts, 20,
         household.get("acquisition_origin", "unknown") or "unknown"),
        ("Service breadth", breadth_pts, 15,
         f'{len(household.get("service_lines", []))} service(s)'),
        ("Firm contacts", contacts_pts, 15,
         f'{household.get("firm_contacts_count", "unknown")}'),
        ("Digital engagement", portal_pts, 10,
         f'{household.get("portal_logins_monthly", 0):.1f} logins/mo'
         if household.get("portal_logins_monthly") is not None else "N/A"),
        ("Communication exclusivity", comm_pts, 15,
         f'{household.get("communication_exclusivity_pct", 0):.0f}%'
         if household.get("communication_exclusivity_pct") is not None
         else "N/A"),
    ]

    total = sum(s[1] for s in signals)
    band = _band_from_score(total, FOLLOW_BAND_THRESHOLDS)
    ranked = sorted(signals, key=lambda s: (-s[1], -s[2]))
    top3 = [{"signal": s[0], "value": s[3], "points": s[1]} for s in ranked[:3]]

    return {
        "follow_likelihood_score": total,
        "follow_likelihood_band": band,
        "follow_likelihood_factors": top3,
        "follow_missing_signals": problems,
    }


# ---------------------------------------------------------------------------
# Concentration metric
# ---------------------------------------------------------------------------

def compute_concentration(households: list[dict]) -> dict:
    """Compute exposed AUM and concentration for an advisor's book.

    Households with 'Insufficient data' follow likelihood are excluded from
    the numerator but included in the denominator (book AUM).
    """
    total_aum = sum(h["aum"] for h in households)
    exposed_aum = sum(
        h["aum"] for h in households
        if h.get("follow_likelihood_band") == "High"
    )
    unscored = [
        h for h in households
        if h.get("follow_likelihood_band") == "Insufficient data"
    ]

    concentration_pct = (exposed_aum / total_aum * 100) if total_aum > 0 else 0

    return {
        "exposed_aum": exposed_aum,
        "concentration_pct": round(concentration_pct, 1),
        "has_unscored_households": len(unscored) > 0,
        "unscored_count": len(unscored),
        "unscored_aum": sum(h["aum"] for h in unscored),
    }
