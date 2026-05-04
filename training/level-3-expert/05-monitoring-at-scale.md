# Lesson: Monitoring at scale

**Level:** Expert — Level 3  
**Time:** 40 minutes  
**Prerequisites:** [04-agent-architectures.md](04-agent-architectures.md); TokenWatch integration from Level 2

---

## Learning objectives

By the end of this lesson you will be able to:

1. Define and instrument the five golden signals for LLM token monitoring.
2. Design a two-layer monitoring stack (local development + production).
3. Set up budget alerts per team and per route using TokenWatch and provider consoles.
4. Conduct a weekly token review and translate findings into engineering actions.
5. Build a minimal reporting artifact that a non-technical stakeholder can read.

---

## The five golden signals for LLM monitoring

These five metrics capture cost, efficiency, and health for any LLM-powered application:

| Signal | Definition | Unit | Action threshold |
|--------|------------|------|-----------------|
| Input tokens per request | Average input tokens, by route and task type | tokens | >20% increase week-over-week: investigate |
| Output tokens per request | Average output tokens, by route and task type | tokens | >20% increase: check max_tokens setting |
| Cost per user-day | Total daily spend ÷ active users | USD | >budget alert %: review top task labels |
| Budget breach rate | % of requests that exceed the per-request budget | % | Any breach: fix or raise the budget intentionally |
| Model tier mix | % of calls going to each tier (small / mid / large) | % | Large tier >30%: review routing rules |

Instrument all five from the start. Adding metrics retroactively after a cost incident is harder and less useful than having a baseline.

---

## Two-layer monitoring stack

### Layer 1: Local development (TokenWatch)

TokenWatch records every API call locally during development, staging, and CI. It is zero-dependency, zero-data-sharing, and provides immediate feedback in the development loop.

**Setup:**
```python
from tokenwatch import TokenWatch

monitor = TokenWatch(storage_path=".tokenwatch")
monitor.set_budget(monthly_usd=50.0, alert_at_percent=80.0)

# In each route or agent call:
monitor.record_from_anthropic_response(response, task_label=task_type)

# In a health-check endpoint or CLI:
print(monitor.format_dashboard())
```

**What to review weekly:** Top-5 task labels by cost. Model tier mix. Budget utilization trend.

### Layer 2: Production (provider console + optional proxy)

For production workloads, the authoritative cost source is the provider's billing console (Anthropic Console, OpenAI Usage Dashboard). These show:

- Total spend by day, model, and key.
- Token volume by model.
- Rate limit events.

If you need per-route or per-user breakdowns in production, add a proxy layer (Helicone, LangSmith, or LiteLLM self-hosted). Evaluate data residency implications before choosing a cloud proxy for regulated workloads.

**One source of truth per use case:**
- Finance and billing: provider console.
- Engineering drill-down: TokenWatch (dev) or proxy tracing (prod).
- Do not split responsibility — pick one source per question.

---

## Budget alerts per team and route

Token budget governance works best when costs are visible at the team and feature level, not just in aggregate.

**Per team:**
- Each team or service gets a monthly token budget, agreed with finance or platform engineering.
- TokenWatch (or the proxy) is configured with that budget and set to alert at 80%.
- The team owns the alert response: investigate, optimize, or request a budget increase.

**Per route/endpoint:**
- Set a per-request ceiling (`max_tokens` on the output side) for each distinct endpoint.
- For high-volume routes, also set a daily ceiling tracked against the provider console.
- Alert when a route's average input or output tokens increase >20% week-over-week.

**Example budget matrix:**

| Route | Expected tokens/request (input + output) | Daily call volume | Monthly estimate |
|-------|------------------------------------------|-------------------|-----------------|
| /summarize | 1 200 in + 300 out | 5 000 | ~$1 350 |
| /codegen | 3 000 in + 800 out | 500 | ~$560 |
| /classify | 200 in + 15 out | 50 000 | ~$180 |

Track actual vs expected monthly. Deviations >15% trigger a review.

---

## The weekly token review

Run a 30-minute weekly review using the following agenda:

1. **Pull the dashboard:** `print(monitor.format_dashboard())` or open the proxy tracing UI.
2. **Review the top-5 expensive task labels.** For each: is the cost proportional to business value? Is the model tier appropriate?
3. **Check the model tier mix.** If >30% of calls are going to the large tier: which task types are escalating? Is escalation justified by actual quality failures?
4. **Check budget utilization trend.** Increasing faster than usage growth? Find the new source of bloat.
5. **Review the breach rate.** Any route consistently breaching per-request limits? Either the limit is wrong or the request pattern changed.

Capture the top 2–3 actions from the review as engineering tickets. Run it consistently; the value comes from the trend data accumulated over time, not from any single week's snapshot.

---

## Reporting to non-technical stakeholders

A brief monthly token report for product and finance stakeholders:

```markdown
## AI API Cost Report — [Month] [Year]

**Total spend:** $[X] ([Y]% of budget)
**Active features:** [list]
**Cost per user-day:** $[Z]

**Highlights:**
- /summarize reduced 22% after prompt compression (Lesson 1 applied).
- /codegen dominates at 41% of total spend — expected for code-generation volume.
- Budget on track for month; alert threshold not triggered.

**Next month actions:**
- Route /classify to small model (currently on mid tier — saves estimated $[X]/month).
- Review /qa context growth — input tokens increased 18% last month.
```

Keep it to one page. Focus on trends and actions, not raw numbers.

---

## Tool selection reference

| Question | Tool |
|----------|------|
| What did we spend in total this month? | Provider console |
| Which feature/task costs the most? | TokenWatch task labels |
| Is caching working? | Cache hit rate in API response metadata |
| Why did input tokens spike last Tuesday? | Proxy trace with full request logs |
| Is our routing working as designed? | TokenWatch model tier mix |

---

## Acceptance criteria

- [ ] All five golden signals are instrumented in at least one production or staging service.
- [ ] Budget alerts are configured per team (not just per key).
- [ ] You have conducted at least one weekly token review using the agenda above and produced at least two action items.
- [ ] You can write a one-page monthly cost report from the available data without additional investigation.
- [ ] The team's "source of truth" for each monitoring question is decided and documented.

---

## Further reading

- [../../docs/05-tools-and-platforms.md](../../docs/05-tools-and-platforms.md) — tool selection matrix
- [../../guidelines/DEVELOPER-GUIDELINES.md](../../guidelines/DEVELOPER-GUIDELINES.md) — Rule 5: Monitor usage
- [../../scripts/README.md](../../scripts/README.md) — CLI monitoring scripts
