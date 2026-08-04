"""
Designed test cases for the advisor transition risk demo.

Three advisor cases and four household cases, with exact input values
that produce known band assignments when run through the scoring logic.
"""

# ---------------------------------------------------------------------------
# Advisor cases
# ---------------------------------------------------------------------------

ADVISOR_CASES = [
    {
        "case_id": "CASE-ADV-1",
        "label": "Clear elevated risk — Marcus Webb",
        "description": "Multiple structured signals fire simultaneously; "
                       "free-text is neutral.",
        "expected_band": "Elevated",
        "input": {
            "advisor_id": "ADV-WEBB",
            "name": "Marcus Webb",
            "team": "Northeast",
            "tenure_years": 4,
            "comp_ratio": 0.83,
            "production_trend_pct": -9,
            "org_events": ["passed_over", "manager_change"],
            "engagement_decline_pct": 45,
            "free_text_notes": ["solid performer, no concerns noted"],
            "status": "active",
            "departure_date": None,
            "score_as_of_date": None,
        },
        # Expected score breakdown: 20+20+10+10+15+0 = 75
    },
    {
        "case_id": "CASE-ADV-2",
        "label": "Subtle risk — Diana Chen",
        "description": "Structured signals look clean; free-text notes from "
                       "manager carry the signal.",
        "expected_band": "Watch",
        "input": {
            "advisor_id": "ADV-CHEN",
            "name": "Diana Chen",
            "team": "West",
            "tenure_years": 3,
            "comp_ratio": 1.02,
            "production_trend_pct": 1,
            "org_events": [],
            "engagement_decline_pct": 8,
            "free_text_notes": [
                "mentioned recruiter contact at industry event",
                "seems less engaged in team planning, exploring options",
                "not feeling valued after comp review",
            ],
            "status": "active",
            "departure_date": None,
            "score_as_of_date": None,
        },
        # Expected: 4+0+10+0+0+20 = 34
    },
    {
        "case_id": "CASE-ADV-3",
        "label": "Retrospective — James Okafor (illustrative, not validation)",
        "description": "Already departed; score snapshot from 90 days "
                       "pre-departure shows Elevated.",
        "expected_band": "Elevated",
        "input": {
            "advisor_id": "ADV-OKAFOR",
            "name": "James Okafor",
            "team": "Southeast",
            "tenure_years": 6,
            "comp_ratio": 0.88,
            "production_trend_pct": -6,
            "org_events": ["compliance_action"],
            "engagement_decline_pct": 42,
            "free_text_notes": [
                "frustrated with new compliance requirements",
                "brought up comp discussion in one-on-one",
            ],
            "status": "departed",
            "departure_date": "2026-05-01",
            "score_as_of_date": "2026-02-01",
        },
        # Expected: 14+14+6+5+15+8 = 62
    },
]


# ---------------------------------------------------------------------------
# Household cases — all in Marcus Webb's book (ADV-WEBB)
# ---------------------------------------------------------------------------

HOUSEHOLD_CASES = [
    {
        "case_id": "CASE-HH-1",
        "label": "High follow, low baseline — The Paterson Family",
        "description": "Satisfied household whose entire relationship is "
                       "through the advisor; high follow likelihood, low "
                       "baseline risk.",
        "expected_follow_band": "High",
        "expected_baseline_band": "Low",
        "input": {
            "household_id": "HH-PATERSON",
            "name": "The Paterson Family",
            "advisor_id": "ADV-WEBB",
            "aum": 8_200_000,
            "firm_tenure_years": 7,
            "advisor_tenure_years": 7,
            "acquisition_origin": "advisor_book",
            "service_lines": ["investments"],
            "firm_contacts_count": 1,
            "portal_logins_monthly": 2.0,
            "communication_exclusivity_pct": 78,
            "fee_percentile": 45,
            "perf_vs_benchmark_pct": 1.2,
            "service_complaints_12mo": 0,
            "net_flow_pct": -1,
            "satisfaction_score": 9,
        },
        # Follow: 25+20+15+10+6+10 = 86 → High
        # Baseline: 5+0+0+0+0 = 5 → Low
    },
    {
        "case_id": "CASE-HH-2",
        "label": "Low follow, high baseline — The Nakamura Family",
        "description": "Long firm tenure, multiple firm relationships, but "
                       "independently dissatisfied; low follow likelihood, "
                       "high baseline risk.",
        "expected_follow_band": "Low",
        "expected_baseline_band": "High",
        "input": {
            "household_id": "HH-NAKAMURA",
            "name": "The Nakamura Family",
            "advisor_id": "ADV-WEBB",
            "aum": 4_500_000,
            "firm_tenure_years": 14,
            "advisor_tenure_years": 2,
            "acquisition_origin": "firm_originated",
            "service_lines": ["investments", "planning", "banking", "trust"],
            "firm_contacts_count": 4,
            "portal_logins_monthly": 7.0,
            "communication_exclusivity_pct": 25,
            "fee_percentile": 82,
            "perf_vs_benchmark_pct": -3.5,
            "service_complaints_12mo": 3,
            "net_flow_pct": -10,
            "satisfaction_score": 4,
        },
        # Follow: 3+0+0+0+3+0 = 6 → Low
        # Baseline: 20+16+20+12+15 = 83 → High
    },
    {
        "case_id": "CASE-HH-3",
        "label": "Low on both — The Brennan Family",
        "description": "Deeply embedded, multiple firm relationships, "
                       "satisfied; low on both scores.",
        "expected_follow_band": "Low",
        "expected_baseline_band": "Low",
        "input": {
            "household_id": "HH-BRENNAN",
            "name": "The Brennan Family",
            "advisor_id": "ADV-WEBB",
            "aum": 12_100_000,
            "firm_tenure_years": 10,
            "advisor_tenure_years": 3,
            "acquisition_origin": "firm_originated",
            "service_lines": [
                "investments", "planning", "banking", "insurance", "trust"
            ],
            "firm_contacts_count": 5,
            "portal_logins_monthly": 15.0,
            "communication_exclusivity_pct": 20,
            "fee_percentile": 44,
            "perf_vs_benchmark_pct": 2.8,
            "service_complaints_12mo": 0,
            "net_flow_pct": 5,
            "satisfaction_score": 8,
        },
        # Follow: 3+0+0+0+0+0 = 3 → Low
        # Baseline: 5+0+0+0+4 = 9 → Low
    },
    {
        "case_id": "CASE-HH-4",
        "label": "Insufficient signal — The Domingo Account",
        "description": "New account with sparse data; system declines to "
                       "score, distinguishing missing from unreliable.",
        "expected_follow_band": "Insufficient data",
        "expected_baseline_band": "Insufficient data",
        "input": {
            "household_id": "HH-DOMINGO",
            "name": "The Domingo Account",
            "advisor_id": "ADV-WEBB",
            "aum": 1_800_000,
            "firm_tenure_years": 0.3,
            "advisor_tenure_years": 0.3,
            "acquisition_origin": None,       # missing
            "service_lines": ["investments"],
            "firm_contacts_count": None,       # missing
            "portal_logins_monthly": None,     # never activated
            "communication_exclusivity_pct": None,  # missing
            "fee_percentile": 50,
            "perf_vs_benchmark_pct": None,     # < 6 months
            "service_complaints_12mo": 0,
            "net_flow_pct": None,              # < 6 months
            "satisfaction_score": None,         # no survey
        },
        # Follow: insufficient (3 missing + 2 unreliable)
        # Baseline: insufficient (3 missing)
    },
]
