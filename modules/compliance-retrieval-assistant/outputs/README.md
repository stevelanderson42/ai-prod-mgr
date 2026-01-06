# Outputs

**Example responses from the Compliance Retrieval Assistant**

---

## Purpose

This folder contains example CRA outputs demonstrating the response contract in action. These examples show what users actually receive — including successful answers, partial grounding, and various refusal scenarios.

---

## Contents

```
outputs/
├── README.md       # This file
└── examples/       # Sample response files
```

---

## Response Contract Summary

All CRA responses follow the structure defined in [docs/response-contract.md](../docs/response-contract.md):

```json
{
  "trace_id": "uuid",
  "timestamp": "ISO-8601",
  "query": "user's original question",
  "grounding_status": "FULLY_GROUNDED | PARTIALLY_GROUNDED | REFUSED",
  "answer": "response text or null",
  "citations": [...],
  "refusal": {...} or null,
  "metadata": {
    "corpus_release_id": "version",
    "sources_consulted": n,
    "model_provider": "provider or null",
    "processing_time_ms": n
  }
}
```

---

## Grounding Status Examples

### FULLY_GROUNDED

All claims in the answer are supported by retrieved passages.

**User sees:**
- Complete answer
- Inline citations [1], [2], etc.
- Full confidence in the response

**Example query:** "What are the FINRA 2210 requirements for retail communications?"

---

### PARTIALLY_GROUNDED

Some claims are supported; others are explicitly marked as unsupported.

**User sees:**
- Answer with supported portions cited
- Clear warning about unsupported portions
- Guidance on what to verify

**Example query:** "What are the documentation requirements for this type of transaction?" *(when corpus covers some but not all aspects)*

---

### REFUSED

Cannot provide a grounded answer.

**User sees:**
- No answer (answer field is null)
- Refusal code and reason
- Helpful guidance on next steps
- Suggestions for alternatives

**Example queries:**
- "What's the policy?" → `AMBIGUOUS_QUERY`
- "What about cryptocurrency?" → `NO_ELIGIBLE_DOCS`
- "Show me the investigation findings" → `POLICY_BLOCKED`
- *(Conflicting sources found)* → `CONFLICTING_SOURCES`

---

## Example Files

The `examples/` folder contains sample response files:

| Example | Grounding Status | Demonstrates |
|---------|------------------|--------------|
| *(To be added)* | | |

### Planned Examples

- [ ] `fully-grounded-simple.json` — Basic successful answer
- [ ] `fully-grounded-multi-source.json` — Answer citing multiple documents
- [ ] `partially-grounded.json` — Some claims unsupported
- [ ] `refusal-no-eligible-docs.json` — Out of scope query
- [ ] `refusal-insufficient-grounding.json` — Found passages, can't answer
- [ ] `refusal-policy-blocked.json` — Access denied
- [ ] `refusal-ambiguous-query.json` — Needs clarification
- [ ] `refusal-conflicting-sources.json` — Sources disagree

---

## How Examples Support Development

### For Implementation

Reference examples validate that code produces correct output structure:
- JSON schema matches contract
- All required fields present
- Refusal codes map correctly
- Citations format properly

### For Testing

Examples serve as expected outputs for test cases:
- Compare actual response against expected
- Validate grounding status logic
- Verify refusal code selection

### For Documentation

Examples demonstrate the user experience:
- What users actually see
- How refusals are communicated
- How citations appear

---

## What This Folder Does NOT Contain

- ❌ Production responses
- ❌ Real user queries
- ❌ Actual corpus content
- ❌ Sensitive compliance guidance

For portfolio purposes, this folder demonstrates the *structure* of CRA outputs, not production data.

---

## Related Artifacts

- [docs/response-contract.md](../docs/response-contract.md) — Full response specification
- [config/refusal-taxonomy.yaml](../config/refusal-taxonomy.yaml) — Refusal code definitions
- [evaluation/test-cases/](../evaluation/test-cases/) — Test scenarios with expected outputs
- [docs/trace-schema.md](../docs/trace-schema.md) — Corresponding audit records

---

*This folder demonstrates CRA output patterns and response contract implementation.*