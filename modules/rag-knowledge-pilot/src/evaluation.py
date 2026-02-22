"""
Evaluation module — compare retrieval results against expected outcomes.

TODO: Expand to compute full metric suite (grounding accuracy, refusal accuracy,
      top-k relevance) once vector retrieval is in place.
"""

import json
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent.parent / "evaluation"


def load_test_queries() -> list[dict]:
    """Load test queries from evaluation/test_queries.json."""
    path = EVAL_DIR / "test_queries.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_expected_outcomes() -> dict:
    """Load expected outcomes keyed by query id."""
    path = EVAL_DIR / "expected_outcomes.json"
    with open(path, encoding="utf-8") as f:
        outcomes = json.load(f)
    return {item["id"]: item for item in outcomes}


def evaluate_single(query_id: str, retrieved: list[dict], expected: dict) -> dict:
    """Evaluate a single query result against its expected outcome.

    TODO: Implement full scoring logic (source match, refusal detection).
    """
    return {
        "query_id": query_id,
        "expected_action": expected.get("expected_action"),
        "actual_action": "ground",  # TODO: implement refusal detection
        "top_source": retrieved[0]["source"] if retrieved else None,
        "expected_source": expected.get("expected_source"),
        "pass": None,  # TODO: compute pass/fail
    }
