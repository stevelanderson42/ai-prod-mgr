# Regulatory Governance Context

**External regulatory constraints that shape AI product design**

**Purpose:** Design assumptions, not legal advice

---

## What This Folder Contains

This folder documents the **external regulatory requirements and governance expectations** that informed the design assumptions, architectural decisions, and controls across the Regulated AI Workflow Toolkit.

It is not legal advice.  
It is not a compliance checklist.  
It is not a claim of regulatory authority.

It is an explicit statement of the **rules of the game I assumed** while designing these systems.

---

## Why This Exists

AI products in regulated industries don't fail because models are weak — they fail because organizations don't understand the constraints under which those products must operate.

Every design decision in this portfolio was shaped by a regulatory context:

- **Why does the RAG Assistant refuse instead of guess?** → Reg BI suitability requirements
- **Why are audit trails non-negotiable?** → SEC 17a-4 books and records
- **Why is documentation so detailed?** → SR 11-7 model risk management
- **Why do guardrails check for "fair and balanced" language?** → FINRA 2210 communication standards

This folder makes those connections explicit — so readers understand *why* the designs look the way they do.

---

## How to Read These Documents

Each regulation file follows a consistent structure:

| Section | Purpose |
|---------|---------|
| **Summary** | What the regulation governs (plain English) |
| **Key Regulatory Language** | Verbatim excerpts with citations |
| **Core Expectations** | Examiner-perspective requirements |
| **Product & Architecture Implications** | What this forces you to do as a PM |
| **Where This Shows Up in the Portfolio** | Links to modules, ADRs, and case studies |

This structure keeps each file **auditable, interview-ready, and focused on real constraints**.

---

## Regulatory References

### Financial Services (FinServ)

These are examiner-driven requirements that directly shape product design in broker-dealer and investment advisory contexts.

| Document | Regulation | Governs |
|----------|------------|---------|
| [SR 11-7](finserv/sr-11-7-model-risk.md) | Federal Reserve / OCC Guidance | Model risk management, documentation, validation |
| [SEC 17a-4](finserv/sec-17a-4-books-records.md) | 17 C.F.R. § 240.17a-4 | Books & records, audit trails, retention |
| [FINRA 2210](finserv/finra-2210-communications.md) | FINRA Rule 2210 | Communications with the public |
| [Reg BI](finserv/reg-bi-suitability.md) | 17 C.F.R. § 240.15l-1 | Best interest, suitability, customer profile |

### AI Governance (Cross-Industry)

These frameworks and directives shape expectations for AI products across regulated industries — not just financial services.

| Document | Framework | Governs |
|----------|-----------|---------|
| [NIST AI RMF](ai-governance/nist-ai-rmf.md) | NIST AI Risk Management Framework | Risk identification, measurement, mitigation |
| [EU AI Act](ai-governance/eu-ai-act.md) | European Union AI Act | High-risk AI system requirements |
| [US Executive Guidance](ai-governance/us-executive-ai-guidance.md) | Executive Order 14110 | Federal AI safety and governance direction |

---

## Interpretation Notes

Regulations require interpretation. Where I've made judgment calls about how a regulation applies to AI product design, those interpretations are documented in [interpretation-notes.md](interpretation-notes.md).

This separation signals:
- **Intellectual honesty** — I'm not claiming my interpretation is authoritative
- **Auditability** — Readers can distinguish regulatory text from my application of it
- **Interview readiness** — I can discuss both the regulation and my reasoning

---

## What This Is NOT

- ❌ Legal advice or compliance certification
- ❌ A claim that these products are "compliant"
- ❌ A substitute for legal, compliance, or risk review
- ❌ An exhaustive regulatory inventory

> **PM DECISION:** This folder exists to make design assumptions explicit. It demonstrates regulatory literacy, not regulatory authority.

---

## How This Strengthens the Portfolio

With this context documented, case studies and design decisions can reference regulatory drivers directly:

**Instead of:**
> "We implemented audit trails for compliance."

**The case study says:**
> "Given SEC 17a-4 audit trail requirements and SR 11-7 documentation expectations, the system was designed to preserve immutable, time-stamped records of all retrieval and generation events."

That single sentence signals:
- Governance literacy
- Systems thinking
- Senior PM instincts

---

*Part of the Regulated AI Workflow Toolkit — demonstrating governance-first AI product design for regulated industries.*