# Sample Corpus Documents

These 10 documents are **synthetic compliance content created for demo and evaluation purposes**. They are not production policies, legal guidance, or approved compliance materials.

## Purpose

- Provide a realistic but fictional corpus for the `minirag.py` retrieval demo
- Enable repeatable evaluation runs against the module scorecard
- Demonstrate the evidence package output format (citations, trace, audit bundle)

## What's Here

| Document | Topic |
|----------|-------|
| doc-001-finra-2210-summary.md | FINRA 2210 communications requirements |
| doc-002-prohibited-phrases.md | Prohibited language in client communications |
| doc-003-retention-policy.md | Record retention requirements |
| doc-004-supervisory-escalation.md | Supervisory review and escalation procedures |
| doc-005-risk-disclosure-template.md | Risk disclosure language templates |
| doc-006-advisor-guidance.md | Advisor communication guidance |
| doc-007-model-governance-notes.md | Model governance and validation notes |
| doc-008-books-records-policy.md | Books and records policy summary |
| doc-009-client-communication-standards.md | Client communication standards |
| doc-010-internal-compliance-faq.md | Internal compliance FAQ |

## Important

- **Corpus release ID:** `sample-docs-v1` (tracked in `config/corpus-registry.yaml`)
- **Not legal advice.** Content is illustrative and loosely modeled on real regulatory themes, but should not be used for actual compliance decisions.
- **Stable for evaluation.** These documents should not be edited without updating the release ID, as existing evaluation results and evidence packages reference this version.