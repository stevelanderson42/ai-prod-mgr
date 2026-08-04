"""
Evaluation harness: runs designed cases through scoring logic
and reports pass/fail for each.

Usage:
    python evaluation.py
"""

import json
import sys
from scoring import score_advisor, score_household_baseline, score_household_follow
from cases import ADVISOR_CASES, HOUSEHOLD_CASES


def evaluate_advisor_case(case: dict) -> dict:
    result = score_advisor(case["input"])
    actual_band = result["flight_risk_band"]
    passed = actual_band == case["expected_band"]
    return {
        "case_id": case["case_id"],
        "case_type": "advisor",
        "label": case["label"],
        "description": case["description"],
        "expected_band": case["expected_band"],
        "actual_band": actual_band,
        "actual_score": result["flight_risk_score"],
        "factors": result["flight_risk_factors"],
        "pass": passed,
    }


def evaluate_household_case(case: dict) -> list[dict]:
    """Returns two results: one for follow likelihood, one for baseline risk."""
    follow_result = score_household_follow(case["input"])
    baseline_result = score_household_baseline(case["input"])

    follow_passed = follow_result["follow_likelihood_band"] == case["expected_follow_band"]
    baseline_passed = baseline_result["baseline_risk_band"] == case["expected_baseline_band"]

    return [
        {
            "case_id": f'{case["case_id"]}-follow',
            "case_type": "household-follow",
            "label": f'{case["label"]} (follow likelihood)',
            "description": case["description"],
            "expected_band": case["expected_follow_band"],
            "actual_band": follow_result["follow_likelihood_band"],
            "actual_score": follow_result["follow_likelihood_score"],
            "factors": follow_result["follow_likelihood_factors"],
            "missing_signals": follow_result.get("follow_missing_signals", []),
            "pass": follow_passed,
        },
        {
            "case_id": f'{case["case_id"]}-baseline',
            "case_type": "household-baseline",
            "label": f'{case["label"]} (baseline risk)',
            "description": case["description"],
            "expected_band": case["expected_baseline_band"],
            "actual_band": baseline_result["baseline_risk_band"],
            "actual_score": baseline_result["baseline_risk_score"],
            "factors": baseline_result["baseline_risk_factors"],
            "missing_signals": baseline_result.get("baseline_missing_signals", []),
            "pass": baseline_passed,
        },
    ]


def run_evaluation() -> list[dict]:
    results = []

    for case in ADVISOR_CASES:
        results.append(evaluate_advisor_case(case))

    for case in HOUSEHOLD_CASES:
        results.extend(evaluate_household_case(case))

    return results


def print_results(results: list[dict]) -> None:
    passed = sum(1 for r in results if r["pass"])
    total = len(results)

    print(f"\n{'='*70}")
    print(f"  EVALUATION: {passed} / {total} passing")
    print(f"{'='*70}\n")

    for r in results:
        status = "PASS" if r["pass"] else "FAIL"
        score_str = f"score={r['actual_score']}" if r["actual_score"] is not None else "no score"
        print(f"  [{status}] {r['case_id']}: {r['label']}")
        print(f"         Expected: {r['expected_band']}  |  "
              f"Actual: {r['actual_band']} ({score_str})")

        if r["factors"]:
            factors_str = ", ".join(
                f'{f["signal"]}={f["points"]}pts' for f in r["factors"]
            )
            print(f"         Top factors: {factors_str}")

        if r.get("missing_signals"):
            for ms in r["missing_signals"]:
                print(f"         [{ms['signal']}] {ms['reason']}")

        if not r["pass"]:
            print(f"         *** FAILED ***")
        print()

    print(f"{'='*70}")
    if passed == total:
        print(f"  All {total} cases passing.")
    else:
        print(f"  {total - passed} FAILURE(S)")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    results = run_evaluation()
    print_results(results)

    # Also write results to JSON for the frontend
    with open("output/evaluation.json", "w") as f:
        json.dump(results, f, indent=2)

    # Exit with error code if any failures
    if not all(r["pass"] for r in results):
        sys.exit(1)
