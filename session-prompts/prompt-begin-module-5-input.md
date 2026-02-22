In my repo, create a new executable module at:

modules/rag-knowledge-pilot/

Goal: a runnable, measured “RAG Knowledge Pilot” module that will become my primary executable demo artifact (feature-first, not academic).

STEP 1 (do now): create the folder structure + scaffolding files + a metric-first README + a small corpus + realistic evaluation queries.

Create these paths:
- modules/rag-knowledge-pilot/README.md
- modules/rag-knowledge-pilot/src/main.py
- modules/rag-knowledge-pilot/src/embeddings.py
- modules/rag-knowledge-pilot/src/retrieval.py
- modules/rag-knowledge-pilot/src/evaluation.py
- modules/rag-knowledge-pilot/corpus/README.md
- modules/rag-knowledge-pilot/corpus/policy_margin.md
- modules/rag-knowledge-pilot/corpus/policy_options_approval.md
- modules/rag-knowledge-pilot/corpus/policy_suitability.md
- modules/rag-knowledge-pilot/corpus/policy_comms_standard.md
- modules/rag-knowledge-pilot/evaluation/test_queries.json
- modules/rag-knowledge-pilot/evaluation/expected_outcomes.json
- modules/rag-knowledge-pilot/results/.gitkeep

Corpus requirements:
- Write 3–4 small Markdown documents (1–2 paragraphs each) in /corpus/ that look like internal compliance policy excerpts.
- Topics to cover:
  1) margin requirements basics and restrictions
  2) options trading approval / options agreement requirement
  3) suitability obligations / customer profile / risk tolerance
  4) communications standards (advertising/communications must be fair and balanced, no promissory statements, recordkeeping reminders)
- Keep them synthetic (no copying real policy text). Use clear headings and short bullet lists where helpful.

README requirements:
1) Title: “RAG Knowledge Pilot — Measured Retrieval System”
2) First screen must be:
   - Performance Summary table with placeholder values (XX%)
   - Quick Start with a single command that runs main.py on a sample query
3) Below the fold:
   - “What it does” (4 bullets)
   - “How it’s structured” (one short paragraph)
   - “How evaluation works” (bullets)
4) Include a “Not production” note: this is a pilot/demo/evaluation harness—no production claims.
5) Include a one-sentence note explicitly linking to Module 4 as the governance architecture this pilot operationalizes (with a relative link to the Module 4 folder).

Code scaffolding requirements:
- main.py must run without errors immediately (even before embeddings are implemented).
- main.py should accept a --query argument and print:
  - the query
  - a placeholder list of retrieved chunks (for now, load the corpus markdown files and return the top 3 by simple token overlap)
  - a placeholder “grounding_status” and “refusal_code”
- Add TODO markers where vector retrieval and embeddings will be added later.
- Keep it deterministic and dependency-light (standard library only for Step 1).

Evaluation requirements:
- test_queries.json: include 15 realistic, domain-context compliance-style questions.
  - Mix: 9 should-ground, 4 should-refuse, 2 ambiguous/edge.
  - Make the queries sound like real questions a business/compliance partner would ask, not generic strings.
- expected_outcomes.json: for each query include expected action: "ground" or "refuse" and, if refuse, include a placeholder reason_code (e.g., "OUT_OF_SCOPE", "INSUFFICIENT_EVIDENCE", "POLICY_PROHIBITED") and a short rationale string.

Do not add any external frameworks yet (no langchain, no langgraph). Keep it minimal and runnable.

After creating files:
1) Output a concise tree of modules/rag-knowledge-pilot/
2) Confirm that running main.py with the sample query works (show the command and expected console output shape).
keep main.py under ~150 lines for Step 1.