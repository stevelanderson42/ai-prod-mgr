# OWASP Top 10 for LLM Applications (2025)

**Industry Security Framework for Large Language Model Applications**

---

## What It Is

The OWASP Top 10 for Large Language Model Applications is a community-driven security awareness document published by the [Open Web Application Security Project (OWASP)](https://owasp.org/) Foundation. It identifies the most critical security vulnerabilities in LLM-based applications and provides actionable guidance for developers, security professionals, and product managers.

First released in 2023, the framework was updated for 2025 to reflect real-world incidents, evolving attack techniques, and changes in how organizations deploy LLMs — including the rise of agentic architectures and retrieval-augmented generation (RAG).

**Key characteristics:**
- Community-developed by security experts, AI practitioners, and industry professionals
- Technology-agnostic (applies to any LLM, not just specific vendors)
- Focused on application-level risks, not model training
- Updated based on real-world exploits and deployment patterns

---

## The 2025 Top 10

| Rank | Vulnerability | Description |
|------|---------------|-------------|
| **LLM01** | **Prompt Injection** | Manipulating LLMs via crafted inputs to bypass safety controls, exfiltrate data, or trigger unintended actions. Includes direct injection (user prompts) and indirect injection (embedded in external data). |
| **LLM02** | **Sensitive Information Disclosure** | LLMs revealing PII, credentials, proprietary data, or confidential business information in outputs — either from training data or runtime context. |
| **LLM03** | **Supply Chain** | Vulnerabilities from third-party models, training data, plugins, or components. Includes model poisoning via compromised sources like Hugging Face. |
| **LLM04** | **Data and Model Poisoning** | Corrupted training data or fine-tuning that introduces backdoors, biases, or compromised behavior into the model. |
| **LLM05** | **Improper Output Handling** | Failing to validate, sanitize, or constrain LLM outputs before passing them to downstream systems — enabling injection attacks, XSS, or code execution. |
| **LLM06** | **Excessive Agency** | Granting LLMs unchecked autonomy to take actions (API calls, database writes, tool use) without sufficient validation or human oversight. |
| **LLM07** | **System Prompt Leakage** | Exposure of system prompts that reveal security controls, business logic, or sensitive configuration — enabling targeted attacks. |
| **LLM08** | **Vector and Embedding Weaknesses** | Vulnerabilities in RAG pipelines, vector databases, and embedding-based retrieval — including poisoned embeddings and retrieval manipulation. |
| **LLM09** | **Misinformation** | LLMs generating false, misleading, or fabricated information (hallucinations) that users trust without verification. |
| **LLM10** | **Unbounded Consumption** | Resource exhaustion attacks causing denial of service, excessive costs ("denial of wallet"), or unauthorized model replication. |

---

## Why It Matters for Regulated AI

For organizations deploying LLMs in regulated environments, the OWASP Top 10 provides a critical security baseline:

### Prompt Injection is the #1 Threat

OWASP explicitly states:

> *"Prompt injection vulnerabilities are possible due to the nature of generative AI. Given the stochastic influence at the heart of the way models work, it is unclear if there are fool-proof methods of prevention."*

This is why **pre-invocation governance** (evaluating inputs before they reach the model) is essential — post-generation filtering alone cannot address attacks that succeed during generation.

### RAG-Specific Vulnerabilities Are Now Recognized

The 2025 update added **Vector and Embedding Weaknesses** (LLM08) as a dedicated category, reflecting that:
- 53% of organizations use RAG rather than fine-tuning
- Retrieval pipelines introduce their own attack surface
- Poisoned embeddings can manipulate what information reaches the model

### Excessive Agency Reflects Agentic Risk

As LLMs gain autonomy (tool use, API access, database operations), the risk of **unintended actions** increases. The framework emphasizes:
- Least privilege for LLM capabilities
- Human-in-the-loop for high-risk actions
- Logging and monitoring of all agent actions

### Compliance Implications

Many vulnerabilities map directly to regulatory concerns:

| OWASP Vulnerability | Regulatory Connection |
|---------------------|----------------------|
| Sensitive Information Disclosure | Privacy regulations, data protection |
| Misinformation | FINRA 2210 (fair and balanced communications) |
| Improper Output Handling | SR 11-7 (model risk management) |
| Excessive Agency | Audit trail requirements, authorization controls |
| Unbounded Consumption | Operational risk management |

---

## How It Connects to This Portfolio

### Case Study #1: Pre-Invocation Governance

The pre-invocation control plane directly addresses multiple OWASP vulnerabilities:

| OWASP Risk | How the Control Plane Addresses It |
|------------|-----------------------------------|
| **LLM01: Prompt Injection** | Intent classifiers detect adversarial patterns before model invocation |
| **LLM06: Excessive Agency** | Routing decisions constrain what capabilities are available per request |
| **LLM07: System Prompt Leakage** | Scope classifiers prevent out-of-bounds queries that might probe for system details |
| **LLM09: Misinformation** | Ambiguity detection refuses to answer questions that can't be grounded |

The key insight from OWASP: **pre-generation controls are necessary because attacks succeed during generation, before output filters can act.**

### Case Study #3: Retrieval Architecture

The compliance retrieval assistant addresses:

| OWASP Risk | How the Architecture Addresses It |
|------------|----------------------------------|
| **LLM08: Vector and Embedding Weaknesses** | Controlled corpus with verified sources; no user-uploaded content |
| **LLM05: Improper Output Handling** | Citation requirements and grounding checks before output delivery |
| **LLM09: Misinformation** | Retrieval-only mode available; refusal when grounding is insufficient |

---

## Key Quotes Referenced

These quotes from the OWASP Top 10 for LLM Applications (2025) are cited in the case studies:

**On prompt injection (LLM01):**
> *"Prompt injection vulnerabilities are possible due to the nature of generative AI. Given the stochastic influence at the heart of the way models work, it is unclear if there are fool-proof methods of prevention."*

**On mitigation strategies:**
> *"Separate and clearly denote untrusted content to limit its influence on user prompts."*

> *"Define sensitive categories and construct rules for identifying and handling such content."*

> *"Apply semantic filters and use string-checking to scan for non-allowed content."*

---

## OWASP's Recommended Mitigations

The framework recommends a defense-in-depth approach:

### Input Controls (Pre-Generation)
- Validate and sanitize all inputs
- Separate untrusted content from system prompts
- Apply semantic filters for sensitive categories
- Use string-checking for known attack patterns

### Output Controls (Post-Generation)
- Validate LLM outputs before downstream use
- Apply content filters and safety checks
- Enforce structured output formats where possible

### Architectural Controls
- Least privilege for LLM capabilities
- Human-in-the-loop for high-risk actions
- Comprehensive logging and monitoring
- Rate limiting and resource controls

### Governance Controls
- Regular security assessments and red-teaming
- Supply chain verification for models and data
- Incident response procedures for LLM-specific events

---

## Source Materials

### Official OWASP Resources

- **OWASP Top 10 for LLM Applications (2025)**  
  https://genai.owasp.org/llm-top-10/

- **Full PDF Document**  
  https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf

- **OWASP GenAI Security Project**  
  https://owasp.org/www-project-top-10-for-large-language-model-applications/

- **GitHub Repository**  
  https://github.com/OWASP/www-project-top-10-for-large-language-model-applications

### Related Frameworks

- [NIST AI Risk Management Framework](./nist-ai-rmf.md) — Federal guidance on AI governance
- [MITRE ATLAS](https://atlas.mitre.org/) — Adversarial threat landscape for AI systems

---

## Version History

| Version | Date | Notes |
|---------|------|-------|
| 2025 | November 2024 | Current version; added System Prompt Leakage, Vector/Embedding Weaknesses; expanded Excessive Agency and Misinformation |
| 1.1 | October 2023 | First stable release |
| 1.0 | August 2023 | Initial release |

---

*This document summarizes the OWASP Top 10 for LLM Applications (2025) for reference in the Regulated AI Workflow Toolkit. For authoritative guidance, consult the official OWASP documentation.*