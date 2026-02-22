#!/usr/bin/env python3
"""
RAG Knowledge Pilot — main entry point.

Usage:
    python main.py --query "What are the margin requirements for a new account?"
    python main.py --evaluate
"""

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from embeddings import OpenAIEmbeddingProvider         # noqa: E402
from retrieval import retrieve, build_index, delete_index  # noqa: E402
from reflection import reformulate_query                # noqa: E402

# --- Configuration -----------------------------------------------------------

DEFAULT_QUERY = "Can a client trade options without a signed options agreement?"
TOP_K = 3
GROUNDING_THRESHOLD = float(os.environ.get("GROUNDING_THRESHOLD", "0.45"))
REFLECTION_ENABLED = os.environ.get("REFLECTION_ENABLED", "true").lower() == "true"


def require_openai_key() -> None:
    """Exit gracefully if OPENAI_API_KEY is not set."""
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY is not set.\n")
        print("Set it before running:\n")
        print('  PowerShell:  $env:OPENAI_API_KEY="sk-..."')
        print("  Bash:        export OPENAI_API_KEY=sk-...")
        raise SystemExit(2)


# --- Classification ----------------------------------------------------------

def classify_result(chunks: list[dict]) -> dict:
    """Determine grounding status from top retrieval score."""
    if not chunks:
        return {"grounding_status": "REFUSED", "refusal_code": "OUT_OF_SCOPE"}

    top_score = chunks[0]["score"]
    if top_score >= GROUNDING_THRESHOLD:
        return {"grounding_status": "GROUNDED", "refusal_code": "NONE"}
    else:
        return {"grounding_status": "REFUSED", "refusal_code": "INSUFFICIENT_EVIDENCE"}


# --- Output formatting -------------------------------------------------------

def format_output(query: str, chunks: list[dict], classification: dict) -> str:
    lines = [
        f'query: "{query}"',
        "",
        "retrieved_chunks:",
    ]
    for c in chunks:
        lines.append(f"  - rank={c['rank']}  score={c['score']:.2f}  source={c['source']}")
    lines.append("")
    lines.append(f"grounding_status: {classification['grounding_status']}")
    lines.append(f"refusal_code: {classification['refusal_code']}")
    return "\n".join(lines)


# --- Main --------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="RAG Knowledge Pilot — measured compliance retrieval"
    )
    parser.add_argument(
        "--query", "-q", type=str, default=DEFAULT_QUERY,
        help="Compliance question to retrieve against the corpus.",
    )
    parser.add_argument(
        "--evaluate", action="store_true",
        help="Run the full evaluation harness instead of a single query.",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output results as JSON.",
    )
    parser.add_argument(
        "--reindex", action="store_true",
        help="Delete and rebuild the vector index before running.",
    )
    parser.add_argument(
        "--no-reflection", action="store_true",
        help="Disable the agentic reflection loop.",
    )
    args = parser.parse_args()

    require_openai_key()
    provider = OpenAIEmbeddingProvider()

    if args.reindex:
        delete_index()
    build_index(provider)

    reflection_on = REFLECTION_ENABLED and not args.no_reflection

    if args.evaluate:
        from evaluation import run_evaluation  # noqa: E402
        run_evaluation(provider, reflection_enabled=reflection_on)
        return

    chunks = retrieve(args.query, provider, top_k=TOP_K)
    classification = classify_result(chunks)
    reflection_used = False
    reformulated_query = None
    retry_chunks = None

    if classification["grounding_status"] == "REFUSED" and reflection_on:
        reformulated_query = reformulate_query(args.query, chunks)
        retry_chunks = retrieve(reformulated_query, provider, top_k=TOP_K)
        retry_class = classify_result(retry_chunks)
        if retry_class["grounding_status"] == "GROUNDED":
            classification = retry_class
            chunks = retry_chunks
        reflection_used = True

    if args.json:
        result = {
            "query": args.query,
            "grounding_status": classification["grounding_status"],
            "refusal_code": classification["refusal_code"],
            "retrieved_chunks": chunks,
            "reflection": {
                "triggered": reflection_used,
                "reformulated_query": reformulated_query,
                "retry_chunks": retry_chunks,
            } if reflection_used else {"triggered": False},
        }
        print(json.dumps(result, indent=2))
    else:
        print(format_output(args.query, chunks, classification))
        if reflection_used:
            print(f"\n[Reflection] Triggered — reformulated query: \"{reformulated_query}\"")
            if retry_chunks:
                print(f"[Reflection] Retry top score: {retry_chunks[0]['score']:.2f}")
            print(f"[Reflection] Final decision: {classification['grounding_status']}")


if __name__ == "__main__":
    main()
