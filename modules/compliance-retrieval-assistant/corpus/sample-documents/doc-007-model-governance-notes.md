# Model Governance Notes — AI in Compliance Workflows

**doc_id:** doc-007
**source:** Internal Compliance
**effective_date:** 2024-05-01
**collection:** compliance-policies

## Purpose

This document outlines governance requirements for AI and machine learning models used in compliance and advisory workflows, consistent with SR 11-7 model risk management guidance.

## Model Risk Management Principles

1. **Validation before deployment** — All models must undergo independent validation before production use.
2. **Ongoing monitoring** — Model performance must be monitored continuously with defined escalation thresholds.
3. **Documentation** — Model purpose, methodology, limitations, and assumptions must be documented.
4. **Change control** — Model changes require review and approval through the model governance committee.

## AI-Specific Requirements

### Grounding

AI systems that generate text for compliance or client-facing purposes must ground their outputs in approved source material. Ungrounded generation — where the model relies on training data rather than retrieved documents — is not permitted for regulated communications.

### Audit Trail

Every AI-generated output must have a traceable audit trail linking the output to its input, retrieved context, and decision logic. This is required for regulatory examination readiness.

### Hallucination Controls

Systems must implement controls to detect and prevent hallucinated content, including citation verification and grounding checks. Any output that cannot be traced to an approved source must be flagged or suppressed.

## Scope

These requirements apply to all AI models used in advisory, compliance, surveillance, and client communication workflows.
