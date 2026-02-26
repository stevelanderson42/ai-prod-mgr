"""
RAG Knowledge Pilot — Streamlit UI

Launch from the repository root:
    streamlit run modules/rag-knowledge-pilot/src/app.py
"""

import json
import os
import sys
from pathlib import Path

# Ensure src/ modules are importable
sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st
from embeddings import OpenAIEmbeddingProvider
from retrieval import retrieve, build_index
from reflection import reformulate_query
from generation import generate_answer, generate_refusal

# --- Page config --------------------------------------------------------------

st.set_page_config(
    page_title="RAG Knowledge Pilot",
    page_icon="🔍",
    layout="wide",
)

# --- API key check ------------------------------------------------------------

if not os.environ.get("OPENAI_API_KEY"):
    st.error(
        "**OPENAI_API_KEY not set.** "
        "Set it in your terminal before launching:\n\n"
        '`$env:OPENAI_API_KEY="sk-..."` (PowerShell)  \n'
        "`export OPENAI_API_KEY=sk-...` (Bash)"
    )
    st.stop()

# --- Initialize provider and index (cached) -----------------------------------

@st.cache_resource
def get_provider():
    return OpenAIEmbeddingProvider()

@st.cache_resource
def ensure_index(_provider):
    build_index(_provider)
    return True

provider = get_provider()
ensure_index(provider)

# --- Helper -------------------------------------------------------------------

def classify_result(chunks, threshold):
    """Determine grounding status from top retrieval score."""
    if not chunks:
        return {"grounding_status": "REFUSED", "refusal_code": "OUT_OF_SCOPE"}
    top_score = chunks[0]["score"]
    if top_score >= threshold:
        return {"grounding_status": "GROUNDED", "refusal_code": "NONE"}
    return {"grounding_status": "REFUSED", "refusal_code": "INSUFFICIENT_EVIDENCE"}

# --- Apply pending state from example buttons (before widgets render) ----------

if "_pending_threshold" in st.session_state:
    st.session_state["threshold_slider"] = st.session_state.pop("_pending_threshold")
if "_pending_query" in st.session_state:
    st.session_state["query_field"] = st.session_state.pop("_pending_query")

# --- Sidebar controls ---------------------------------------------------------

with st.sidebar:
    st.markdown("### Controls")

    threshold = st.slider(
        "Grounding threshold",
        min_value=0.30,
        max_value=0.80,
        value=0.45,
        step=0.05,
        key="threshold_slider",
        help="Minimum similarity score required to ground an answer.",
    )

    reflection_on = st.toggle("Reflection (bounded retry)", value=True)
    generate_on = st.toggle("Generate answer", value=True)

    st.markdown("---")
    st.caption(
        "**Threshold** controls how conservative the system is. "
        "Higher = more refusals, fewer hallucination risks.  \n"
        "**Reflection** reformulates borderline queries and retries once.  \n"
        "**Generate answer** off = retrieve-only mode (no LLM call)."
    )

# --- Header -------------------------------------------------------------------

st.title("🔍 RAG Knowledge Pilot")
st.caption(
    "Compliance knowledge assistant with grounded retrieval, "
    "structured refusal, and bounded reflection."
)

# --- How to use instructions --------------------------------------------------

st.markdown(
    "**How to use this demo:**  \n"
    "1\\.  Select one of the example scenarios below (Grounded answer, Refusal, or Reflection recovery)  \n"
    "2\\.  Press **Run** to see the system's response  \n"
    "3\\.  Try another scenario, or type your own compliance question and press **Run** again"
)

# --- Example query buttons ----------------------------------------------------

example_cols = st.columns([1, 1, 1.3, 1.7])
with example_cols[0]:
    if st.button("📗 Grounded answer", use_container_width=True):
        st.session_state["_pending_query"] = "What are the margin requirements for a new account?"
        st.session_state["_pending_threshold"] = 0.45
        st.rerun()
with example_cols[1]:
    if st.button("🚫 Refusal", use_container_width=True):
        st.session_state["_pending_query"] = "What is the firm's vacation policy?"
        st.session_state["_pending_threshold"] = 0.45
        st.rerun()
with example_cols[2]:
    if st.button("🔄 Reflection recovery", use_container_width=True):
        st.session_state["_pending_query"] = "Do clients need approval before trading options?"
        st.session_state["_pending_threshold"] = 0.70
        st.rerun()

# --- Query input (form with Run button) ---------------------------------------

with st.form("query_form", clear_on_submit=False):
    query = st.text_input(
        "Ask a compliance question",
        placeholder="e.g. What are the margin requirements for a new account?",
        key="query_field",
    )
    submitted = st.form_submit_button("Run", type="primary", use_container_width=True)

if not submitted or not query:
    st.stop()

# --- Retrieval + Reflection + Generation --------------------------------------

try:
    with st.spinner("Retrieving and generating..."):
        TOP_K = 3
        chunks = retrieve(query, provider, top_k=TOP_K)
        classification = classify_result(chunks, threshold)

        reflection_used = False
        reformulated = None
        original_top_score = chunks[0]["score"] if chunks else 0.0
        retry_chunks = None

        if classification["grounding_status"] == "REFUSED" and reflection_on:
            reflection_used = True
            reformulated = reformulate_query(query, chunks)
            retry_chunks = retrieve(reformulated, provider, top_k=TOP_K)
            retry_class = classify_result(retry_chunks, threshold)
            if retry_class["grounding_status"] == "GROUNDED":
                classification = retry_class
                chunks = retry_chunks

        gen_result = None
        if generate_on:
            if classification["grounding_status"] == "GROUNDED":
                gen_result = generate_answer(query, chunks)
            else:
                gen_result = generate_refusal(classification["refusal_code"])

except Exception as e:
    st.error(f"**Error during retrieval or generation:** {e}")
    st.caption("Check your OPENAI_API_KEY and network connection.")
    st.stop()

# --- Status badges (native st.metric) ----------------------------------------

is_grounded = classification["grounding_status"] == "GROUNDED"
top_score = chunks[0]["score"] if chunks else 0.0

bcol1, bcol2, bcol3, bcol4 = st.columns(4)
if is_grounded:
    bcol1.metric("Status", "GROUNDED ✅")
else:
    bcol1.metric("Status", "REFUSED 🚫", delta=classification["refusal_code"], delta_color="inverse")
bcol2.metric("Top Score", f"{top_score:.2f}")
bcol3.metric("Threshold", f"{threshold:.2f}")
if reflection_used:
    reflection_recovered = classification["grounding_status"] == "GROUNDED" and retry_chunks is not None
    if reflection_recovered:
        bcol4.metric("Reflection", "Recovered ✅")
    else:
        bcol4.metric("Reflection", "Attempted 🔄")
else:
    bcol4.metric("Reflection", "Not needed" if reflection_on else "Off")

st.markdown("---")

# --- Two-column results -------------------------------------------------------

left_col, right_col = st.columns([3, 2])

# --- Left column: Answer or Refusal ------------------------------------------

with left_col:
    if is_grounded and gen_result:
        st.markdown("#### Answer")
        st.markdown(gen_result.answer)

        cited = sorted(set(gen_result.sources_cited))
        if cited:
            st.success(f"📄 **Sources:** {', '.join(cited)}")

        if reflection_used:
            st.info(
                f"🔄 **Reflection recovered this answer.** "
                f"Original score ({original_top_score:.2f}) was below threshold "
                f"({threshold:.2f}). Reformulated query scored "
                f"{chunks[0]['score']:.2f}."
            )

    elif is_grounded and not gen_result:
        st.markdown("#### Retrieval Result")
        st.success(
            f"**GROUNDED** — top score {top_score:.2f} exceeds threshold {threshold:.2f}.  \n"
            f"Answer generation is off. Enable it in the sidebar to see a synthesized response."
        )

    elif not is_grounded and gen_result:
        st.markdown("#### Unable to Answer")
        st.warning(gen_result.answer)

        if reflection_used and retry_chunks:
            retry_top = retry_chunks[0]["score"] if retry_chunks else 0.0
            st.caption(
                f"Reflection attempted reformulation but retry score "
                f"({retry_top:.2f}) remained below threshold ({threshold:.2f})."
            )

    else:
        st.markdown("#### Retrieval Result")
        st.error(
            f"**REFUSED** — top score {top_score:.2f} is below threshold {threshold:.2f}.  \n"
            f"Answer generation is off. The system would refuse this query."
        )

# --- Right column: Retrieval table --------------------------------------------

with right_col:
    st.markdown("#### Retrieved Chunks")

    for c in chunks:
        score = c["score"]
        if score >= threshold:
            st.metric(
                label=f"Rank {c['rank']} · {c['source']}",
                value=f"{score:.2f}",
                delta="above threshold",
                delta_color="normal",
            )
        elif score >= threshold - 0.10:
            st.metric(
                label=f"Rank {c['rank']} · {c['source']}",
                value=f"{score:.2f}",
                delta="borderline",
                delta_color="off",
            )
        else:
            st.metric(
                label=f"Rank {c['rank']} · {c['source']}",
                value=f"{score:.2f}",
                delta="below threshold",
                delta_color="inverse",
            )

# --- Advanced / Debug expander ------------------------------------------------

with st.expander("Advanced / Debug"):
    if gen_result and gen_result.total_tokens > 0:
        tcol1, tcol2, tcol3, tcol4 = st.columns(4)
        tcol1.metric("Prompt Tokens", gen_result.prompt_tokens)
        tcol2.metric("Completion Tokens", gen_result.completion_tokens)
        tcol3.metric("Total Tokens", gen_result.total_tokens)
        tcol4.metric("Model", gen_result.model)
    elif gen_result:
        st.caption("No LLM call — refusal served from template (zero cost).")
    else:
        st.caption("Answer generation off — no LLM call made.")

    if reflection_used:
        st.markdown("**Reflection Details**")
        st.markdown(f"Reformulated query: *{reformulated}*")
        retry_score = retry_chunks[0]["score"] if retry_chunks else 0.0
        st.markdown(
            f"Original top score: {original_top_score:.2f} → "
            f"Retry top score: {retry_score:.2f}"
        )

    st.markdown("**Evidence (Retrieved Chunk Text)**")
    for c in chunks:
        st.markdown(
            f"**Rank {c['rank']}** · `{c['source']}` · score: {c['score']:.2f}"
        )
        st.code(c["text"].strip(), language=None)

    # JSON download
    result_json = {
        "query": query,
        "grounding_status": classification["grounding_status"],
        "refusal_code": classification["refusal_code"],
        "threshold": threshold,
        "controls": {
            "generate_on": generate_on,
            "reflection_on": reflection_on,
        },
        "llm_called": gen_result is not None and gen_result.total_tokens > 0,
        "retrieved_chunks": [
            {"rank": c["rank"], "score": c["score"], "source": c["source"]}
            for c in chunks
        ],
    }
    if reflection_used:
        result_json["reflection"] = {
            "triggered": True,
            "reformulated_query": reformulated,
            "original_top_score": original_top_score,
            "retry_top_score": retry_chunks[0]["score"] if retry_chunks else 0.0,
        }
    if gen_result:
        result_json["generation"] = {
            "answer": gen_result.answer,
            "sources_cited": gen_result.sources_cited,
            "model": gen_result.model,
            "tokens": {
                "prompt": gen_result.prompt_tokens,
                "completion": gen_result.completion_tokens,
                "total": gen_result.total_tokens,
            },
        }

    st.download_button(
        label="📥 Download result as JSON",
        data=json.dumps(result_json, indent=2),
        file_name="rag_pilot_result.json",
        mime="application/json",
    )