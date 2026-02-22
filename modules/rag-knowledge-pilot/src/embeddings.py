"""
Embeddings module — vector encoding for corpus chunks.

TODO: Implement vector embeddings (e.g., sentence-transformers or OpenAI embeddings).
      For Step 1, retrieval uses simple token overlap in retrieval.py.
"""


def embed_text(text: str) -> list[float]:
    """Return a vector embedding for the given text.

    TODO: Replace with actual embedding model call.
    """
    raise NotImplementedError("Vector embeddings not yet implemented — using token overlap.")


def embed_corpus(chunks: list[str]) -> list[list[float]]:
    """Embed all corpus chunks and return a list of vectors.

    TODO: Replace with batch embedding and optional caching.
    """
    raise NotImplementedError("Vector embeddings not yet implemented — using token overlap.")
