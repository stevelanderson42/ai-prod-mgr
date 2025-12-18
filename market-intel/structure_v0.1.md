# Market Intelligence Monitor — Structure v0.1

## Purpose
Track competitor AI releases, regulatory updates, and industry changes 
that influence AI initiative prioritization.

## Signal Categories
- Competitor AI announcements
- Regulatory guidance updates
- Industry adoption patterns
- Technology capability changes
- Risk/failure case studies

## Tagging Schema

| Tag | Type | Description |
|-----|------|-------------|
| `source_type` | Category | competitor / regulator / analyst / vendor / incident |
| `signal_type` | Category | launch / guidance / trend / failure / acquisition |
| `domain` | Category | banking / wealth / insurance / healthcare / cross-sector |
| `relevance` | Rating | high / medium / low |
| `confidence` | Rating | high / medium / low — How reliable is this signal? |
| `actionability` | Rating | now / soon / watch — What should change (if anything)? |

## How Insights Feed ROI Engine
- High-relevance competitor moves → Increase urgency score
- Regulatory updates → Adjust compliance risk weighting
- Industry failures → Add to risk consideration factors
- Low-confidence signals → Flag for verification before acting

## Current Manual Workflow
- Weekly review of AI news sources
- Tagging in Notion database
- Monthly synthesis for strategic planning

## Future Automation Considerations (not for now)
- RSS/API ingestion
- Automated tagging with LLM
- Trend analysis and alerting
- Integration with ROI scoring model
```

**Why this matters:**
This primes Week 8 work without burning energy. You're defining structure, not building systems. The confidence + actionability tags prevent this from becoming a news scrapbook.

---

