"""
Retrieval module — vector retrieval over the compliance corpus.

Uses OpenAI embeddings with a lightweight file-based vector index
(no external vector DB dependency needed).
"""

import json
import math
from pathlib import Path

from embeddings import OpenAIEmbeddingProvider

# --- Paths -------------------------------------------------------------------

MODULE_DIR = Path(__file__).resolve().parent.parent
CORPUS_DIR = MODULE_DIR / "corpus"
INDEX_PATH = MODULE_DIR / "results" / "vector_index.json"

# --- Chunking config ---------------------------------------------------------

CHUNK_SIZE = 500   # characters
CHUNK_OVERLAP = 100


# --- Corpus loading and chunking ---------------------------------------------

def load_corpus() -> list[dict]:
    """Load all Markdown policy documents from the corpus directory."""
    docs = []
    for md_file in sorted(CORPUS_DIR.glob("*.md")):
        if md_file.name == "README.md":
            continue
        content = md_file.read_text(encoding="utf-8")
        docs.append({"source": md_file.name, "content": content})
    return docs


def chunk_document(source: str, content: str) -> list[dict]:
    """Split a document into overlapping character-level chunks with metadata."""
    chunks = []
    start = 0
    chunk_id = 0
    while start < len(content):
        end = min(start + CHUNK_SIZE, len(content))
        chunks.append({
            "id": f"{source}::chunk-{chunk_id}",
            "text": content[start:end],
            "source_file": source,
            "chunk_id": chunk_id,
            "start_char": start,
            "end_char": end,
        })
        chunk_id += 1
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


# --- Vector math (stdlib only) -----------------------------------------------

def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


# --- Index management --------------------------------------------------------

def build_index(provider: OpenAIEmbeddingProvider) -> None:
    """Embed all corpus chunks and persist the index to disk. Skip if exists."""
    if INDEX_PATH.exists():
        return

    corpus = load_corpus()
    all_chunks = []
    for doc in corpus:
        all_chunks.extend(chunk_document(doc["source"], doc["content"]))

    texts = [c["text"] for c in all_chunks]
    vectors = provider.embed_texts(texts)

    index_data = []
    for chunk, vector in zip(all_chunks, vectors):
        index_data.append({
            "id": chunk["id"],
            "text": chunk["text"],
            "source_file": chunk["source_file"],
            "chunk_id": chunk["chunk_id"],
            "start_char": chunk["start_char"],
            "end_char": chunk["end_char"],
            "embedding": vector,
        })

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index_data, f)


def load_index() -> list[dict]:
    """Load the persisted vector index from disk."""
    with open(INDEX_PATH, encoding="utf-8") as f:
        return json.load(f)


# --- Retrieval ---------------------------------------------------------------

def retrieve(query: str, provider: OpenAIEmbeddingProvider, top_k: int = 3) -> list[dict]:
    """Retrieve the top-k corpus chunks by cosine similarity.

    Returns a list of dicts with keys: rank, score, source, text.
    """
    # Build index on first run
    if not INDEX_PATH.exists():
        build_index(provider)

    index = load_index()
    query_vec = provider.embed_texts([query])[0]

    scored = []
    for entry in index:
        sim = cosine_similarity(query_vec, entry["embedding"])
        scored.append({
            "score": round(sim, 4),
            "source": entry["source_file"],
            "text": entry["text"][:200],
        })

    scored.sort(key=lambda x: x["score"], reverse=True)

    results = []
    for i, item in enumerate(scored[:top_k]):
        item["rank"] = i + 1
        results.append(item)
    return results
