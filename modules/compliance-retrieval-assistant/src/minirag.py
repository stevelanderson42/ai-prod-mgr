#!/usr/bin/env python3
"""
minirag.py — Minimal deterministic lexical RAG demo.

Loads .md files from corpus/sample-documents/, scores them by token overlap
with the query, selects top 3, extracts snippets, and writes a full evidence
package. No embeddings, no vector DB, no external APIs, no LLM calls.
"""

import argparse
import json
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths (relative to this script)
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
MODULE_DIR = SCRIPT_DIR.parent
CORPUS_DIR = MODULE_DIR / "corpus" / "sample-documents"
OUTPUT_DIR = MODULE_DIR / "evidence" / "samples" / "sample-001"

# ---------------------------------------------------------------------------
# Tokeniser (deliberately simple — lowercase + split on non-alpha)
# ---------------------------------------------------------------------------

def tokenize(text: str) -> list[str]:
    return [t for t in re.split(r"[^a-z0-9]+", text.lower()) if t]


def unique_tokens(text: str) -> set[str]:
    return set(tokenize(text))

# ---------------------------------------------------------------------------
# Corpus loader
# ---------------------------------------------------------------------------

def load_corpus(corpus_dir: Path) -> list[dict]:
    docs = []
    for fp in sorted(corpus_dir.glob("*.md")):
        content = fp.read_text(encoding="utf-8")
        docs.append({
            "doc_id": fp.stem,
            "filename": fp.name,
            "content": content,
        })
    return docs

# ---------------------------------------------------------------------------
# Scoring — token-overlap (Jaccard-like)
# ---------------------------------------------------------------------------

def score_documents(query: str, docs: list[dict]) -> list[dict]:
    q_tokens = unique_tokens(query)
    scored = []
    for doc in docs:
        d_tokens = unique_tokens(doc["content"])
        overlap = q_tokens & d_tokens
        score = len(overlap) / len(q_tokens) if q_tokens else 0.0
        scored.append({**doc, "score": round(score, 4), "matched_tokens": sorted(overlap)})
    scored.sort(key=lambda d: d["score"], reverse=True)
    return scored

# ---------------------------------------------------------------------------
# Snippet extractor — finds the best paragraph containing query tokens
# ---------------------------------------------------------------------------

def extract_snippet(content: str, query_tokens: set[str], max_len: int = 300) -> str:
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    best, best_score = "", 0
    for para in paragraphs:
        p_tokens = unique_tokens(para)
        overlap = len(query_tokens & p_tokens)
        if overlap > best_score:
            best_score = overlap
            best = para
    if len(best) > max_len:
        best = best[:max_len].rsplit(" ", 1)[0] + "…"
    return best

# ---------------------------------------------------------------------------
# Response builders
# ---------------------------------------------------------------------------

def build_user_response(trace_id: str, query: str, top_docs: list[dict],
                        query_tokens: set[str]) -> dict:
    citations = []
    answer_parts = []
    for doc in top_docs:
        snippet = extract_snippet(doc["content"], query_tokens)
        citations.append({
            "source_id": doc["doc_id"],
            "source_title": doc["filename"],
            "passage": snippet,
        })
        answer_parts.append(snippet)

    grounding = "FULLY_GROUNDED" if len(top_docs) >= 2 else "PARTIALLY_GROUNDED"
    return {
        "trace_id": trace_id,
        "query": query,
        "grounding_status": grounding,
        "answer": " ".join(answer_parts),
        "citations": citations,
        "refusal": None,
    }


def build_auditor_response(trace_id: str, query: str, scored: list[dict],
                           top_k: int) -> dict:
    return {
        "trace_id": trace_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "corpus_release_id": "sample-docs-v1",
        "retrieval": {
            "total_documents": len(scored),
            "passages_retrieved": top_k,
            "passages_above_threshold": sum(1 for d in scored if d["score"] > 0),
            "top_scores": [
                {"doc_id": d["doc_id"], "score": d["score"]}
                for d in scored[:top_k]
            ],
        },
        "decision": {
            "grounding_status": "FULLY_GROUNDED" if top_k >= 2 else "PARTIALLY_GROUNDED",
            "refusal_code": None,
            "rationale_codes": [
                f"GROUNDED_BY_{d['doc_id'].upper()}" for d in scored[:top_k]
            ],
        },
    }

# ---------------------------------------------------------------------------
# Trace builder
# ---------------------------------------------------------------------------

def build_trace(trace_id: str, query: str, scored: list[dict]) -> dict:
    return {
        "trace_id": trace_id,
        "run_timestamp": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "corpus_dir": str(CORPUS_DIR),
        "total_documents_loaded": len(scored),
        "scores": [
            {"doc_id": d["doc_id"], "score": d["score"],
             "matched_tokens": d["matched_tokens"]}
            for d in scored
        ],
    }

# ---------------------------------------------------------------------------
# Evidence-package markdown
# ---------------------------------------------------------------------------

def build_evidence_md(query: str, user_resp: dict, auditor_resp: dict,
                      trace: dict) -> str:
    lines = [
        "# Evidence Package — sample-001",
        "",
        f"**Generated:** {trace['run_timestamp']}",
        f"**Trace ID:** {trace['trace_id']}",
        "",
        "## Query",
        "",
        f"> {query}",
        "",
        "## Grounding Status",
        "",
        f"`{user_resp['grounding_status']}`",
        "",
        "## Citations",
        "",
    ]
    for c in user_resp["citations"]:
        lines += [
            f"### {c['source_id']} — {c['source_title']}",
            "",
            f"> {c['passage']}",
            "",
        ]
    lines += [
        "## Retrieval Summary",
        "",
        f"- Documents loaded: {auditor_resp['retrieval']['total_documents']}",
        f"- Passages retrieved: {auditor_resp['retrieval']['passages_retrieved']}",
        f"- Above threshold: {auditor_resp['retrieval']['passages_above_threshold']}",
        "",
        "## Top Scores",
        "",
        "| Doc ID | Score |",
        "|--------|-------|",
    ]
    for s in auditor_resp["retrieval"]["top_scores"]:
        lines.append(f"| {s['doc_id']} | {s['score']} |")
    lines += ["", "---", "*Generated by minirag.py — deterministic lexical RAG demo*"]
    return "\n".join(lines) + "\n"

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Minimal lexical RAG demo")
    parser.add_argument("--query", required=True, help="Query string")
    parser.add_argument("--top-k", type=int, default=3, help="Number of top docs")
    args = parser.parse_args()

    trace_id = str(uuid.uuid4())
    query_tokens = unique_tokens(args.query)

    # Load & score
    docs = load_corpus(CORPUS_DIR)
    scored = score_documents(args.query, docs)
    top_docs = scored[: args.top_k]

    # Build responses
    user_resp = build_user_response(trace_id, args.query, top_docs, query_tokens)
    auditor_resp = build_auditor_response(trace_id, args.query, scored, args.top_k)
    trace = build_trace(trace_id, args.query, scored)
    evidence_md = build_evidence_md(args.query, user_resp, auditor_resp, trace)

    # Write outputs
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "query.txt").write_text(args.query + "\n", encoding="utf-8")
    (OUTPUT_DIR / "response_user.json").write_text(
        json.dumps(user_resp, indent=2) + "\n", encoding="utf-8")
    (OUTPUT_DIR / "response_auditor.json").write_text(
        json.dumps(auditor_resp, indent=2) + "\n", encoding="utf-8")
    (OUTPUT_DIR / "trace.json").write_text(
        json.dumps(trace, indent=2) + "\n", encoding="utf-8")
    (OUTPUT_DIR / "evidence_package.md").write_text(evidence_md, encoding="utf-8")

    # Console summary
    print(f"Trace ID:  {trace_id}")
    print(f"Query:     {args.query}")
    print(f"Corpus:    {len(docs)} documents loaded")
    print(f"Top {args.top_k}:")
    for d in top_docs:
        print(f"  {d['doc_id']:40s}  score={d['score']}")
    print(f"\nGrounding: {user_resp['grounding_status']}")
    print(f"Output:    {OUTPUT_DIR}/")
    print("Files:     query.txt, response_user.json, response_auditor.json, "
          "trace.json, evidence_package.md")


if __name__ == "__main__":
    main()
