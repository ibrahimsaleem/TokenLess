# Lesson: TokenWatch integration

`tokenwatch.py` is zero-dependency. Use it in **development and staging** to learn spend patterns before wiring enterprise billing.

## Minimal pattern

```python
from tokenwatch import TokenWatch

m = TokenWatch(storage_path=".tokenwatch")
m.set_budget(monthly_usd=50.0, alert_at_percent=80.0)
m.record_usage("claude-haiku-4-5-20251001", 1200, 400, task_label="summarize")
print(m.format_dashboard())
```

## Provider helpers

- `record_from_anthropic_response`
- `record_from_openai_response`

See root [SKILL.md](../../SKILL.md) and [README.md](../../README.md).

## Exercise

Run `python ../../scripts/compare_models.py` with your typical token shape and paste results into your team wiki (redact nothing—it's local).

## Continue

[../level-3-expert/README.md](../level-3-expert/README.md)
