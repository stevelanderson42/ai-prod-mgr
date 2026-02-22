"""
Retrieval module — find the most relevant corpus chunks for a query.

Step 1: simple token-overlap scoring (no external dependencies).
TODO: Replace with vector-similarity retrieval once embeddings.py is implemented.
"""

import re
from pathlib import Path

CORPUS_DIR = Path(__file__).resolve().parent.parent / "corpus"


def load_corpus() -> list[dict]:
    """Load all Markdown documents from the corpus directory.

    Returns a list of dicts with keys: 'source', 'content'.
    """
    docs = []
    for md_file in sorted(CORPUS_DIR.glob("*.md")):
        if md_file.name == "README.md":
            continue
        content = md_file.read_text(encoding="utf-8")
        docs.append({"source": md_file.name, "content": content})
    return docs


def tokenize(text: str) -> set[str]:
    """Lowercase split on non-alphanumeric characters."""
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def score_overlap(query_tokens: set[str], doc_tokens: set[str]) -> float:
    """Return Jaccard-like overlap score between query and document tokens."""
    if not query_tokens or not doc_tokens:
        return 0.0
    intersection = query_tokens & doc_tokens
    return len(intersection) / len(query_tokens)


def retrieve(query: str, top_k: int = 3) -> list[dict]:
    """Retrieve the top-k corpus chunks by token overlap with the query.

    TODO: Replace token-overlap scoring with vector-similarity search.

    Returns a list of dicts with keys: 'source', 'score', 'snippet'.
    """
    corpus = load_corpus()
    query_tokens = tokenize(query)

    scored = []
    for doc in corpus:
        doc_tokens = tokenize(doc["content"])
        score = score_overlap(query_tokens, doc_tokens)
        snippet = doc["content"][:200].replace("\n", " ").strip()
        scored.append({
            "source": doc["source"],
            "score": round(score, 4),
            "snippet": snippet,
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
