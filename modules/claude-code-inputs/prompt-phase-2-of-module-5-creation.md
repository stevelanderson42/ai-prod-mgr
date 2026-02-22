Implement Phase 2 for modules/rag-knowledge-pilot: replace lexical baseline retrieval with OpenAI-embeddings + Chroma vector retrieval, while keeping the module minimal and runnable.

Constraints:
- Do NOT add langchain/langgraph. Keep it plain Python.
- Keep main.py under ~150 lines.
- Prefer small, readable functions over abstraction.
- Add only the minimum dependencies needed.

Work items:

1) Dependencies / setup
- Add modules/rag-knowledge-pilot/requirements.txt with:
  - chromadb
  - openai
  - tiktoken (only if needed; otherwise omit)
- Update modules/rag-knowledge-pilot/README.md:
  - Add a short “Setup” section above Quick Start:
    - pip install -r modules/rag-knowledge-pilot/requirements.txt
    - export OPENAI_API_KEY=...
  - Keep it concise.

2) EmbeddingProvider (src/embeddings.py)
- Implement a simple EmbeddingProvider interface:
  - embed_texts(list[str]) -> list[list[float]]
- Implement OpenAIEmbeddingProvider using the OpenAI Python SDK.
  - Model name should be configurable via env var OPENAI_EMBEDDING_MODEL with a sane default.
- Add a minimal helper to batch embed texts.

3) Vector store + retrieval (src/retrieval.py)
- Implement Chroma-backed retrieval:
  - Build / persist an index under modules/rag-knowledge-pilot/results/chroma_db (or similar).
  - Ingest all *.md files under modules/rag-knowledge-pilot/corpus/.
  - Chunk documents with explicit chunk_size and overlap (configurable constants).
  - Store chunks with metadata: source_file, chunk_id, start_char/end_char (or similar).
- Retrieval function:
  - retrieve(query, top_k=3) -> list of {rank, score, source, text}
  - Include similarity/distance score from Chroma in the returned results.

4) main.py (src/main.py)
- Replace lexical scoring with vector retrieval:
  - Initialize OpenAIEmbeddingProvider
  - Build/load Chroma index (create if missing; otherwise reuse)
  - Retrieve top 3 chunks
  - Print output in the existing “Example output shape” style:
    query, retrieved_chunks (rank/score/source), grounding_status, refusal_code
- For now, grounding_status can be a simple heuristic:
  - If top score meets a threshold, GROUNDED else INSUFFICIENT_EVIDENCE
  - Threshold should be configurable (constant or env var)
- Keep refusal codes simple: NONE vs INSUFFICIENT_EVIDENCE vs OUT_OF_SCOPE

5) Evaluation harness (src/evaluation.py)
- Wire evaluation to the vector retrieval path:
  - Iterate test queries from evaluation/test_queries.json
  - For each query, run retrieval + threshold decision
  - Compare to expected_outcomes.json action/refusal_code
  - Compute:
    - GAR (groundable queries where decision==GROUNDED)
    - RCR (refuse-worthy queries where decision==REFUSE with correct code)
    - Avg top-chunk score
- Save a JSON report in modules/rag-knowledge-pilot/results/ (timestamped filename).
- Print a short summary to console after a run.

6) Keep corpus + queries as-is (do not rewrite them).

After implementing:
- Show the updated module tree.
- Provide the exact commands to:
  a) run one query
  b) run evaluation and generate results

  Additional constraints (important):

- Persist the Chroma database under:
  modules/rag-knowledge-pilot/results/chroma_db
  Do not rebuild the index on every run. Reuse if it exists.

- Keep the grounding threshold simple:
  - Use a single constant or environment variable (e.g., GROUNDING_THRESHOLD).
  - No dynamic threshold tuning yet.
  - No complex scoring heuristics.

- Keep implementation straightforward and readable.
  Avoid premature abstraction or additional frameworks.