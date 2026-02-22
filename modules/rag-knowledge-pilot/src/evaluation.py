"""
Evaluation harness — score retrieval results against expected outcomes.

Computes GAR, RCR, and average top-chunk similarity.
Saves a timestamped JSON report to results/.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from retrieval import retrieve
from reflection import reformulate_query
from embeddings import OpenAIEmbeddingProvider

MODULE_DIR = Path(__file__).resolve().parent.parent
EVAL_DIR = MODULE_DIR / "evaluation"
RESULTS_DIR = MODULE_DIR / "results"

GROUNDING_THRESHOLD = float(os.environ.get("GROUNDING_THRESHOLD", "0.45"))


def load_test_queries() -> list[dict]:
    with open(EVAL_DIR / "test_queries.json", encoding="utf-8") as f:
        return json.load(f)


def load_expected_outcomes() -> dict:
    with open(EVAL_DIR / "expected_outcomes.json", encoding="utf-8") as f:
        outcomes = json.load(f)
    return {item["id"]: item for item in outcomes}


def classify(chunks: list[dict]) -> dict:
    """Same threshold logic as main.py."""
    if not chunks:
        return {"grounding_status": "REFUSED", "refusal_code": "OUT_OF_SCOPE"}
    top_score = chunks[0]["score"]
    if top_score >= GROUNDING_THRESHOLD:
        return {"grounding_status": "GROUNDED", "refusal_code": "NONE"}
    return {"grounding_status": "REFUSED", "refusal_code": "INSUFFICIENT_EVIDENCE"}


def run_evaluation(provider: OpenAIEmbeddingProvider, reflection_enabled: bool = True) -> dict:
    """Run all test queries, compute metrics, save report, and print summary."""
    queries = load_test_queries()
    expected = load_expected_outcomes()

    results = []
    ground_correct = 0
    ground_total = 0
    refuse_correct = 0
    refuse_total = 0
    top_scores = []
    reflection_count = 0

    for q in queries:
        qid = q["id"]
        chunks = retrieve(q["query"], provider, top_k=3)
        decision = classify(chunks)
        reflected = False

        # Reflection loop: retry once if below threshold
        if decision["grounding_status"] == "REFUSED" and reflection_enabled:
            reflected = True
            reflection_count += 1
            reformulated = reformulate_query(q["query"], chunks)
            retry_chunks = retrieve(reformulated, provider, top_k=3)
            retry_decision = classify(retry_chunks)
            if retry_decision["grounding_status"] == "GROUNDED":
                decision = retry_decision
                chunks = retry_chunks

        exp = expected.get(qid, {})

        top_score = chunks[0]["score"] if chunks else 0.0
        top_scores.append(top_score)

        expected_action = exp.get("expected_action", "ground")
        actual_action = "ground" if decision["grounding_status"] == "GROUNDED" else "refuse"

        if expected_action == "ground":
            ground_total += 1
            if actual_action == "ground":
                ground_correct += 1
        elif expected_action == "refuse":
            refuse_total += 1
            if actual_action == "refuse":
                refuse_correct += 1

        results.append({
            "query_id": qid,
            "query": q["query"],
            "category": q.get("category"),
            "expected_action": expected_action,
            "actual_action": actual_action,
            "top_score": round(top_score, 4),
            "top_source": chunks[0]["source"] if chunks else None,
            "grounding_status": decision["grounding_status"],
            "refusal_code": decision["refusal_code"],
            "reflection_triggered": reflected,
        })

    gar = (ground_correct / ground_total * 100) if ground_total else 0.0
    rcr = (refuse_correct / refuse_total * 100) if refuse_total else 0.0
    avg_top = sum(top_scores) / len(top_scores) if top_scores else 0.0

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "threshold": GROUNDING_THRESHOLD,
        "reflection_enabled": reflection_enabled,
        "metrics": {
            "GAR": round(gar, 1),
            "RCR": round(rcr, 1),
            "avg_top_chunk_score": round(avg_top, 4),
        },
        "counts": {
            "ground_correct": ground_correct,
            "ground_total": ground_total,
            "refuse_correct": refuse_correct,
            "refuse_total": refuse_total,
            "reflection_triggered": reflection_count,
            "total_queries": len(queries),
        },
        "details": results,
    }

    # Save report
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    report_path = RESULTS_DIR / f"eval_{ts}.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    # Print summary
    print("=" * 50)
    print("RAG Knowledge Pilot — Evaluation Summary")
    print("=" * 50)
    print(f"Threshold:              {GROUNDING_THRESHOLD}")
    print(f"Reflection:             {'ON' if reflection_enabled else 'OFF'}")
    print(f"Reflection triggered:   {reflection_count}/{len(queries)} queries")
    print(f"Grounded Answer Rate:   {gar:.1f}%  ({ground_correct}/{ground_total})")
    print(f"Refusal Correctness:    {rcr:.1f}%  ({refuse_correct}/{refuse_total})")
    print(f"Avg Top-Chunk Score:    {avg_top:.4f}")
    print(f"Report saved:           {report_path.name}")
    print("-" * 50)
    for r in results:
        match = "pass" if r["expected_action"] == r["actual_action"] else "MISS"
        print(f"  {r['query_id']}  {match:<5}  exp={r['expected_action']:<7} act={r['actual_action']:<7} score={r['top_score']:.2f}")
    print("=" * 50)

    return report
