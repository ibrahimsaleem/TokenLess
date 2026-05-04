# Lesson: monitoring at scale

## Metrics

- Tokens (in/out) per route and per tenant.
- Cache hit rate (where applicable).
- Tool call count and **payload sizes**.
- Model tier mix.

## Actions

- Budget alerts per team (TokenWatch locally; provider consoles in prod).
- Weekly review of top **10** expensive `task_label` values.

## Tools

See [../../docs/05-tools-and-platforms.md](../../docs/05-tools-and-platforms.md). Choose **one** source of truth for finance and one for engineering drill-down.
