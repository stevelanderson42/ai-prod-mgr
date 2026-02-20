# Corpus

**Approved document collections for the Compliance Retrieval Assistant**

---

## Purpose

This folder contains the approved corpus that the CRA retrieves from. In a production environment, this would be a managed vector store populated by the Corpus Pipeline. For portfolio demonstration, this folder holds sample documents and explains the corpus architecture.

> **Key Principle:** The CRA only retrieves from approved, versioned corpus releases. No real-time ingestion. No unreviewed content.

---

## Contents

```
corpus/
├── README.md              # This file
└── sample-documents/      # 10 example documents for testing
    ├── doc-001-finra-2210-summary.md
    ├── doc-002-prohibited-phrases.md
    ├── doc-003-retention-policy.md
    ├── doc-004-supervisory-escalation.md
    ├── doc-005-risk-disclosure-template.md
    ├── doc-006-advisor-guidance.md
    ├── doc-007-model-governance-notes.md
    ├── doc-008-books-records-policy.md
    ├── doc-009-client-communication-standards.md
    └── doc-010-internal-compliance-faq.md
```

---

## Corpus Architecture

### How Documents Enter the Corpus

```
Source Documents
       │
       ▼
┌─────────────────┐
│  Corpus Pipeline │
│                 │
│  1. Ingest      │
│  2. Validate    │
│  3. Chunk       │
│  4. Embed       │
│  5. Review  ◄───┼── Compliance Approval Required
│  6. Publish     │
└────────┬────────┘
         │
         ▼
   Approved Corpus
   (versioned release)
```

### Corpus Releases

Every corpus update is a versioned, immutable release:

| Field | Example | Purpose |
|-------|---------|---------|
| `release_id` | v2025.01.06 | Unique identifier |
| `published_at` | 2025-01-06T00:00:00Z | When published |
| `approved_by` | compliance-review-board | Governance trail |
| `approval_ticket` | CRB-2025-001 | Audit reference |

See [config/corpus-registry.yaml](../config/corpus-registry.yaml) for release tracking.

---

## Collections

The corpus is organized into collections by content type and sensitivity:

| Collection | Description | Sensitivity |
|------------|-------------|-------------|
| `compliance-policies` | Internal compliance policies and standards | Tier 1 (Public) |
| `regulatory-guidance` | External regulatory rules and guidance | Tier 1 (Public) |
| `internal-procedures` | Operational procedures and workflows | Tier 2 (Internal) |
| `enforcement-actions` | Regulatory enforcement actions | Tier 3 (Sensitive) |
| `regulatory-correspondence` | Correspondence with regulators | Tier 3 (Sensitive) |
| `internal-investigations` | Internal investigation reports | Tier 4 (Privileged) |
| `legal-memoranda` | Legal analysis and opinions | Tier 4 (Privileged) |

Access to collections is controlled by user role. See [config/role-permissions.yaml](../config/role-permissions.yaml).

---

## Document Requirements

Every document in the corpus must include:

### Required Metadata

| Field | Description |
|-------|-------------|
| `doc_id` | Unique identifier |
| `title` | Human-readable title |
| `source` | Origin (SEC, FINRA, internal) |
| `effective_date` | When document became effective |
| `collection` | Which collection it belongs to |

### Optional Metadata

| Field | Description |
|-------|-------------|
| `supersedes` | List of doc_ids this replaces |
| `jurisdiction` | Geographic applicability |
| `document_type` | Policy, procedure, guidance, rule |
| `expiration_date` | When document expires |
| `review_date` | Next scheduled review |

---

## Chunking Strategy

Documents are chunked before embedding:

| Setting | Value | Rationale |
|---------|-------|-----------|
| Strategy | Semantic | Preserve meaning over fixed size |
| Target size | 512 tokens | Balance context vs. precision |
| Overlap | 50 tokens | Maintain continuity across chunks |
| Respect boundaries | Yes | Don't split mid-sentence |

See [config/corpus-registry.yaml](../config/corpus-registry.yaml) for full index configuration.

---

## Sample Documents

The `sample-documents/` folder contains example documents for testing and demonstration:

| Document | Collection | Purpose |
|----------|------------|---------|
| doc-001-finra-2210-summary.md | regulatory-guidance | FINRA Rule 2210 — Communications with the Public (Summary) |
| doc-002-prohibited-phrases.md | compliance-policies | Prohibited Phrases in Client Communications |
| doc-003-retention-policy.md | internal-procedures | Records Retention Policy |
| doc-004-supervisory-escalation.md | internal-procedures | Supervisory Escalation Guide |
| doc-005-risk-disclosure-template.md | compliance-policies | Risk Disclosure Template |
| doc-006-advisor-guidance.md | compliance-policies | Advisor Guidance — Suitability and Best Interest |
| doc-007-model-governance-notes.md | compliance-policies | Model Governance Notes — AI in Compliance Workflows |
| doc-008-books-records-policy.md | internal-procedures | Books & Records Policy (Simplified) |
| doc-009-client-communication-standards.md | compliance-policies | Client Communication Standards |
| doc-010-internal-compliance-faq.md | compliance-policies | Internal Compliance FAQ |

### Sample Document Format

```yaml
---
doc_id: sample-policy-001
title: Sample Compliance Policy
source: internal
effective_date: 2025-01-01
collection: compliance-policies
document_type: policy
---

# Policy Title

Policy content goes here...
```

---

## Why Versioned Releases?

Point-in-time auditability:

> "What did the system know when it answered this question on January 5th?"

Every trace includes `corpus_release_id`. Combined with release history, this enables:

- Reconstructing what content was available at query time
- Identifying if stale content caused incorrect answers
- Demonstrating audit compliance (17a-4 alignment)

---

## What This Folder Does NOT Contain

- ❌ Real customer data
- ❌ Actual regulatory documents (copyright considerations)
- ❌ Production vector indices
- ❌ Embeddings or model artifacts

For portfolio purposes, this folder demonstrates the *architecture* of corpus management, not production content.

---

## Related Artifacts

- [config/corpus-registry.yaml](../config/corpus-registry.yaml) — Release tracking and index configuration
- [config/role-permissions.yaml](../config/role-permissions.yaml) — Collection access controls
- [docs/trace-schema.md](../docs/trace-schema.md) — How corpus_release_id appears in traces
- [architecture/component-design.md](../architecture/component-design.md) — Retrieval Client component

---

*This folder structure demonstrates corpus governance patterns for regulated AI systems.*