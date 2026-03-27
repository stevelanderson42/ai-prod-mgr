import sys
from pathlib import Path

from dotenv import load_dotenv

from state import CaseState

# Load .env from the repo root
load_dotenv(Path(__file__).resolve().parent.parent.parent.parent / ".env", override=True)

# Add Module 5 src to path for retrieval imports
_RAG_SRC = str(Path(__file__).resolve().parent.parent.parent / "rag-knowledge-pilot" / "src")
if _RAG_SRC not in sys.path:
    sys.path.insert(0, _RAG_SRC)

FALLBACK_SNIPPETS = [
    "FINRA Rule 2111: suitability obligations require advisors to have reasonable basis...",
    "Reg BI: broker-dealers must act in best interest of retail customer...",
]


def retrieve_policy(state: CaseState) -> CaseState:
    """Node 3: Retrieve relevant policy snippets from the Module 5 RAG corpus.

    Falls back to hardcoded snippets if retrieval fails.
    """
    query = f"{state['issue_category']} {state['regulatory_trigger']} compliance policy"

    try:
        from retrieval import retrieve
        from embeddings import OpenAIEmbeddingProvider

        provider = OpenAIEmbeddingProvider()
        chunks = retrieve(query, provider, top_k=3)

        policy_snippets = [chunk["text"] for chunk in chunks]
        sources = [chunk["source"] for chunk in chunks]

        state["policy_snippets"] = policy_snippets

        state["trace"].append({
            "step": "retrieve_policy",
            "input_summary": query,
            "output_summary": f"Retrieved {len(chunks)} policy chunks from Module 5 corpus",
            "key_outputs": {
                "sources": sources,
            },
        })

    except Exception as e:
        state["policy_snippets"] = FALLBACK_SNIPPETS

        state["trace"].append({
            "step": "retrieve_policy",
            "input_summary": query,
            "output_summary": f"Fallback: RAG retrieval failed ({e}), used hardcoded snippets",
            "key_outputs": {
                "fallback_reason": str(e),
            },
        })

    return state
