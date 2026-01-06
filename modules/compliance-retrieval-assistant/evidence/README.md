# Evidence

**Audit evidence packages for the Compliance Retrieval Assistant**

---

## Purpose

This folder stores evidence packages — detailed records of CRA interactions that enable deep audit review. While every interaction generates a trace, evidence packages capture the *complete context* needed for regulatory inquiry or incident investigation.

> **Key Principle:** If a regulator asks "Why did the system say X on date Y?", we can reconstruct exactly what happened.

---

## Contents

```
evidence/
├── README.md       # This file
└── samples/        # Example evidence packages
```

---

## What is an Evidence Package?

An evidence package is a self-contained bundle capturing everything about a single interaction:

```
evidence-package-{trace_id}/
├── trace.json              # Complete trace record
├── query.txt               # Original user query
├── response.json           # Full response as delivered
├── retrieved/              # All retrieved passages
│   ├── passage-001.json
│   ├── passage-002.json
│   └── ...
├── config-snapshot/        # Policy config at query time
│   ├── policy-constraints.yaml
│   ├── role-permissions.yaml
│   └── corpus-registry.yaml
└── manifest.json           # Package metadata and checksums
```

---

## When Evidence Packages Are Created

Not every interaction generates a full evidence package. They are created:

| Trigger | Sampling Rate | Retention |
|---------|---------------|-----------|
| Refusal (any code) | 100% | Permanent |
| Escalation triggered | 100% | Permanent |
| Conflicting sources detected | 100% | Permanent |
| Random sampling | 10% | Standard (7 years) |
| On-demand (audit request) | As requested | Per request |

---

## Evidence Package Manifest

Each package includes a manifest with integrity verification:

```json
{
  "trace_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2025-01-06T14:30:01.000Z",
  "package_version": "1.0",
  "trigger": "refusal",
  "files": [
    {"name": "trace.json", "sha256": "a1b2c3..."},
    {"name": "query.txt", "sha256": "d4e5f6..."},
    {"name": "response.json", "sha256": "g7h8i9..."}
  ],
  "total_size_bytes": 15234,
  "retention_class": "permanent"
}
```

---

## How Evidence Packages Support Audit

### Scenario: Regulatory Inquiry

> "On January 5th, an analyst received guidance about restricted securities. Show us what the system retrieved and why it answered as it did."

**With evidence package:**
1. Locate package by trace_id or date range
2. Review `query.txt` — what the user actually asked
3. Review `retrieved/` — exactly what passages were found
4. Review `config-snapshot/` — what policy was in effect
5. Review `trace.json` — step-by-step decision path
6. Verify integrity via manifest checksums

### Scenario: Incident Investigation

> "We suspect the system gave incorrect guidance last week. Can you identify affected interactions?"

**With evidence packages:**
1. Query by date range and corpus_release_id
2. Identify interactions using the affected corpus version
3. Review evidence packages to assess impact
4. Compare against corrected corpus

---

## Retention Classes

| Class | Duration | Applied To |
|-------|----------|------------|
| `standard` | 7 years | Normal interactions (sampled) |
| `extended` | 10 years | Enforcement-related content |
| `permanent` | Indefinite | Refusals, escalations, conflicts |

Retention aligns with regulatory expectations (17a-4, SR 11-7).

---

## Storage Considerations

In a production environment:

| Requirement | Approach |
|-------------|----------|
| Immutability | Append-only storage, no modification after write |
| Integrity | SHA-256 checksums for all files |
| Durability | Redundant storage with backup |
| Accessibility | Indexed for retrieval by trace_id, date, trigger type |
| Security | Access restricted to audit/compliance roles |

---

## Sample Evidence Packages

The `samples/` folder contains example evidence packages demonstrating the structure:

| Sample | Scenario | Purpose |
|--------|----------|---------|
| *(To be added)* | | |

---

## What This Folder Does NOT Contain

- ❌ Production audit data
- ❌ Real user queries
- ❌ Actual retrieved passages
- ❌ Sensitive compliance content

For portfolio purposes, this folder demonstrates the *architecture* of evidence preservation, not production data.

---

## Related Artifacts

- [docs/trace-schema.md](../docs/trace-schema.md) — Trace record structure (what goes in trace.json)
- [docs/response-contract.md](../docs/response-contract.md) — Response structure (what goes in response.json)
- [config/policy-constraints.yaml](../config/policy-constraints.yaml) — Evidence sampling configuration
- [config/refusal-taxonomy.yaml](../config/refusal-taxonomy.yaml) — Refusal triggers for evidence creation

---

*This folder demonstrates evidence preservation patterns for auditable AI systems.*