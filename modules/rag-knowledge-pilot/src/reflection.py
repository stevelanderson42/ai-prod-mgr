"""
Reflection module — single-retry query reformulation for borderline retrievals.

When the top retrieval score falls below the grounding threshold, this module
uses OpenAI chat completion to reformulate the query and retry retrieval once.
"""

from openai import OpenAI

REFORMULATION_PROMPT = (
    "The following query did not retrieve strong results from a compliance "
    "policy corpus. Rewrite it as a clearer, more specific search query. "
    "Return only the rewritten query, nothing else."
)


def reformulate_query(original_query: str, top_chunks: list[dict]) -> str:
    """Use OpenAI chat to reformulate a query for better retrieval."""
    context = "\n".join(c["text"][:200] for c in top_chunks[:2]) if top_chunks else ""
    messages = [
        {"role": "system", "content": REFORMULATION_PROMPT},
        {"role": "user", "content": f"Original query: {original_query}\n\nTop retrieved context:\n{context}"},
    ]
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=100,
        temperature=0,
    )
    return response.choices[0].message.content.strip()
