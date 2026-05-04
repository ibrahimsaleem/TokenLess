# Model selection guide

Use a **task taxonomy** and measure quality. Defaults below are rules of thumb—validate on your data.

## Task taxonomy

| Task type | Typical tier | Notes |
|-----------|----------------|-------|
| Intent detection, routing, tagging | Smallest / fastest | Accept some error; sample-check |
| Summarization of long internal docs | Mid tier or smallest with chunking | Watch output length caps |
| Code completion, localized bugfix | Mid tier | Pair with tests |
| Multi-file refactor, architecture | Large tier | Require plan + tests |
| High-stakes security review | Large tier + human | Budget separately |

## Reference pricing (USD per 1M tokens)

Synced from `tokenwatch.py` as of package version **1.2.3**. **Always confirm** against live provider pages before budgeting.

| Model | Input / 1M | Output / 1M |
|-------|------------|-------------|
| claude-haiku-4-5-20251001 | $1.00 | $5.00 |
| claude-sonnet-4-5-20250929 | $3.00 | $15.00 |
| claude-opus-4-6 | $5.00 | $25.00 |
| gpt-4.1-nano | $0.10 | $0.40 |
| gpt-4.1-mini | $0.40 | $1.60 |
| gpt-4.1 | $2.00 | $8.00 |
| gpt-5 | $1.25 | $10.00 |
| gpt-5.2 | $1.75 | $14.00 |
| gemini-2.5-flash-lite | $0.10 | $0.40 |
| gemini-2.5-flash | $0.30 | $2.50 |
| gemini-2.5-pro | $1.25 | $10.00 |

Full table: see `PROVIDER_PRICING` in [tokenwatch.py](../tokenwatch.py). Add custom deployment ids there for local cost tracking.

## Escalation policy (example)

1. Try **cheapest** model with strict output schema.
2. If automated checks fail (tests, JSON parse, confidence score), **retry once** with mid tier.
3. If still failing, **large tier** or human—never loop blindly.

## Compare before you spend

```python
from tokenwatch import TokenWatch
m = TokenWatch()
for row in m.compare_models(2000, 500)[:8]:
    print(row["model"], row["cost_usd"])
```

Or CLI: `python scripts/compare_models.py --in 2000 --out 500 --top 8`
