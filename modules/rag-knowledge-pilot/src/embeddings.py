"""
Embeddings module — embedding provider abstraction for corpus and query encoding.
"""

import os
from openai import OpenAI


DEFAULT_MODEL = "text-embedding-3-small"


class OpenAIEmbeddingProvider:
    """Wraps the OpenAI embeddings API."""

    def __init__(self):
        self.model = os.environ.get("OPENAI_EMBEDDING_MODEL", DEFAULT_MODEL)
        self.client = OpenAI()  # reads OPENAI_API_KEY from env

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Embed a list of texts and return a list of float vectors."""
        results = []
        # Batch in groups of 100 to stay within API limits
        batch_size = 100
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            response = self.client.embeddings.create(model=self.model, input=batch)
            results.extend([item.embedding for item in response.data])
        return results
