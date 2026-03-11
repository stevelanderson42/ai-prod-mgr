# Model Governance Notes (Demo)

Goal:
Demonstrate governance-by-design for AI-assisted responses.

Controls:
- Trace every response with corpus_release_id and retrieved sources.
- Record retrieval scores and snippets used.
- Separate user-facing response vs auditor-facing response.

Known limitations:
- Lexical retrieval can miss semantic matches.
- Snippet extraction may pick partial context.
- This demo does not use embeddings or LLMs.

Audit expectations:
- Show which documents were used.
- Show why they were selected (scores).
- Show disclaimers or refusal behavior when applicable.
