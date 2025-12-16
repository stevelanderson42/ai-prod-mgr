
### Responsible AI (per the Azure AI-900 and Google AI publications) and guardrails

| Responsible AI Principle | FinServ Translation | Guardrail Implementation |
| --- | --- | --- |
| Fairness | Suitability, Reg BI | Pre-check for personalized advice triggers → escalate |
| Explainability | Audit trails (17a-4) | Require citation in all responses, log reasoning |
| Accountability | SR 11-7 governance | Log all model invocations with metadata |
| Privacy | KYC/AML handling | Block PII in prompts, mask in responses |
| Safety | Hallucination prevention | Require grounding, add uncertainty flags |
| Transparency | Communication standards | Disclose AI involvement where required |