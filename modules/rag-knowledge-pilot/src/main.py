#!/usr/bin/env python3
"""
RAG Knowledge Pilot — main entry point.

Accepts a --query argument, retrieves the most relevant corpus chunks using
simple token overlap, and prints a structured result with grounding status
and refusal code placeholders.

Usage:
    python main.py --query "What are the margin requirements for a new account?"

TODO: Replace token-overlap retrieval with vector-similarity search.
TODO: Add refusal detection logic based on score thresholds and scope checks.
TODO: Wire evaluation harness for batch scoring.
"""

import argparse
import json
import sys
from pathlib import Path

# Ensure src/ is importable when run directly
sys.path.insert(0, str(Path(__file__).resolve().parent))

from retrieval import retrieve  # noqa: E402

# --- Configuration -----------------------------------------------------------

DEFAULT_QUERY = "What are the margin requirements for a new customer account?"
TOP_K = 3
# TODO: Tune this threshold once vector retrieval is in place
GROUNDING_SCORE_THRESHOLD = 0.15


def classify_result(retrieved_chunks: list[dict]) -> dict:
    """Determine grounding status and refusal code from retrieval scores.

    TODO: Replace with a proper classifier / score-threshold model.
    """
    if not retrieved_chunks:
        return {
            "grounding_status": "refused",
            "refusal_code": "NO_CHUNKS_RETRIEVED",
        }

    top_score = retrieved_chunks[0]["score"]
    if top_score < GROUNDING_SCORE_THRESHOLD:
        return {
            "grounding_status": "refused",
            "refusal_code": "INSUFFICIENT_EVIDENCE",
        }

    return {
        "grounding_status": "grounded",
        "refusal_code": None,
    }


def format_output(query: str, chunks: list[dict], classification: dict) -> str:
    """Build a human-readable output block."""
    lines = [
        "=" * 60,
        "RAG Knowledge Pilot — Query Result",
        "=" * 60,
        "",
        f"Query:  {query}",
        "",
        f"Grounding Status:  {classification['grounding_status']}",
        f"Refusal Code:      {classification['refusal_code'] or '—'}",
        "",
        f"Retrieved Chunks (top {len(chunks)}):",
        "-" * 40,
    ]

    for i, chunk in enumerate(chunks, 1):
        lines.append(f"  [{i}] {chunk['source']}  (score: {chunk['score']})")
        lines.append(f"      {chunk['snippet'][:120]}...")
        lines.append("")

    lines.append("=" * 60)
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="RAG Knowledge Pilot — measured compliance retrieval"
    )
    parser.add_argument(
        "--query", "-q",
        type=str,
        default=DEFAULT_QUERY,
        help="The compliance question to retrieve against the corpus.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON instead of formatted text.",
    )
    args = parser.parse_args()

    # Retrieve
    chunks = retrieve(args.query, top_k=TOP_K)

    # Classify
    classification = classify_result(chunks)

    # Output
    if args.json:
        result = {
            "query": args.query,
            "grounding_status": classification["grounding_status"],
            "refusal_code": classification["refusal_code"],
            "retrieved_chunks": chunks,
        }
        print(json.dumps(result, indent=2))
    else:
        print(format_output(args.query, chunks, classification))


if __name__ == "__main__":
    main()
