"""
Generation module — grounded answer synthesis from retrieved chunks.

Generates cited answers ONLY when retrieval produces grounded results.
Refuses to generate when grounding criteria are not met.

Design principles:
    - Citations are mandatory, not decorative
    - The model sees only retrieved chunks, never the full corpus
    - Refusal is a first-class output, not an error
    - Token usage is tracked to support cost instrumentation (item #4)
"""

import os
from dataclasses import dataclass

from openai import OpenAI


DEFAULT_MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """\
You are a compliance knowledge assistant for a financial services firm.
You answer questions using ONLY the provided source excerpts. You must
follow these rules strictly:

1. ONLY use information present in the provided excerpts. Never add
   outside knowledge, even if you know the answer.
2. CITE every claim by referencing the source file in brackets,
   e.g. [policy_margin.md]. A sentence without a citation is not
   permitted.
3. If the excerpts do not contain enough information to answer the
   question fully, say so explicitly. Do not guess or extrapolate.
4. Use clear, professional language appropriate for an internal
   compliance audience.
5. Keep answers concise — typically 2-5 sentences.
"""


def _build_user_prompt(query: str, chunks: list[dict]) -> str:
    """Assemble the user message with query and retrieved excerpts."""
    excerpt_lines = []
    for c in chunks:
        excerpt_lines.append(f"--- Source: {c['source']} (score: {c['score']:.2f}) ---")
        excerpt_lines.append(c["text"].strip())
        excerpt_lines.append("")

    excerpts_block = "\n".join(excerpt_lines)

    return (
        f"Source excerpts:\n\n{excerpts_block}\n"
        f"Question: {query}\n\n"
        f"Answer the question using only the excerpts above. "
        f"Cite each claim with the source filename in brackets."
    )


@dataclass
class GenerationResult:
    """Structured output from the generation layer."""
    answer: str
    sources_cited: list[str]
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


def generate_answer(query: str, chunks: list[dict]) -> GenerationResult:
    """Generate a grounded, cited answer from retrieved chunks.

    Args:
        query: The user's compliance question.
        chunks: Retrieved chunk dicts with keys: rank, score, source, text.

    Returns:
        GenerationResult with the answer text, cited sources, and token usage.
    """
    model = os.environ.get("OPENAI_GENERATION_MODEL", DEFAULT_MODEL)
    client = OpenAI()

    user_prompt = _build_user_prompt(query, chunks)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=500,
        temperature=0,
    )

    answer = response.choices[0].message.content.strip()
    usage = response.usage

    # Extract which sources were actually cited in the answer
    sources_cited = []
    for c in chunks:
        if c["source"] in answer:
            sources_cited.append(c["source"])

    return GenerationResult(
        answer=answer,
        sources_cited=sources_cited,
        model=model,
        prompt_tokens=usage.prompt_tokens,
        completion_tokens=usage.completion_tokens,
        total_tokens=usage.total_tokens,
    )


# --- Refusal response (no LLM call needed) -----------------------------------

REFUSAL_MESSAGES = {
    "INSUFFICIENT_EVIDENCE": (
        "I don't have sufficient evidence in the policy corpus to answer "
        "this question reliably. This query should be routed to a compliance "
        "specialist for manual review."
    ),
    "OUT_OF_SCOPE": (
        "This question falls outside the scope of the compliance policy "
        "corpus. No relevant documents were found."
    ),
}


def generate_refusal(refusal_code: str) -> GenerationResult:
    """Return a structured refusal — no LLM call, zero cost.

    Args:
        refusal_code: The refusal reason code from classification.

    Returns:
        GenerationResult with a templated refusal message and zero token usage.
    """
    message = REFUSAL_MESSAGES.get(
        refusal_code,
        "Unable to generate a grounded answer for this query."
    )

    return GenerationResult(
        answer=message,
        sources_cited=[],
        model="none (refusal — no LLM call)",
        prompt_tokens=0,
        completion_tokens=0,
        total_tokens=0,
    )