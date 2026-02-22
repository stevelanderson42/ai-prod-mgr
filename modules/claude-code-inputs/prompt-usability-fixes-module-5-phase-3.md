Apply minimal, high-impact usability fixes to Module 5 without expanding scope.

Target module:
modules/rag-knowledge-pilot/

Changes required:

1) Graceful missing OPENAI_API_KEY handling (no stack trace)
- In src/main.py, add a small helper function require_openai_key().
- Before constructing OpenAIEmbeddingProvider(), call require_openai_key().
- If OPENAI_API_KEY is missing, print a short friendly message with:
  - PowerShell example: $env:OPENAI_API_KEY="sk-..."
  - Bash example: export OPENAI_API_KEY=sk-...
- Exit with code 2 (SystemExit(2)).

2) Add a --reindex flag to force rebuilding the persisted vector index
- In src/main.py, add argparse flag: --reindex
- In src/retrieval.py, add function delete_index() that removes:
  modules/rag-knowledge-pilot/results/vector_index.json
  if it exists.
- In src/main.py, import delete_index from retrieval.
- If args.reindex is true, call delete_index() before build_index(provider).

3) Clean up src/retrieval.py if needed
- Ensure retrieval.py does NOT contain any accidental sys.path manipulation or imports of itself.
- retrieval.py should only include corpus loading/chunking, cosine similarity, index build/load/delete, and retrieve().

4) Retrieval result content (small correction)
- In src/retrieval.py retrieve(), return the FULL chunk text in the returned results (do not truncate to 200 chars).
- Do not change main.py output format; it can keep printing rank/score/source only.

Constraints:
- Keep main.py under ~150 lines.
- Do not add new dependencies or frameworks.
- Keep changes minimal and readable.

After applying changes:
- Show a concise diff summary (files changed + what changed).
- Provide commands to run:
  a) python modules/rag-knowledge-pilot/src/main.py --help
  b) python modules/rag-knowledge-pilot/src/main.py --query "Can a client trade options without a signed options agreement?"
  c) python modules/rag-knowledge-pilot/src/main.py --evaluate

  Also:
If modules/rag-knowledge-pilot/results/vector_index.json exists,
delete it once after applying these changes so the next evaluation run
rebuilds from a clean index.