# Level 2 — Intermediate

## Objectives

- Compress prompts and histories deliberately.
- Route models by risk tier; use caching features where applicable.
- Integrate **TokenWatch** in a dev environment for one service.
- Install at least **one** skill from `skills/token_optimization_skill_pack` locally.

## Read in order

1. [01-prompt-compression.md](01-prompt-compression.md)
2. [02-model-routing.md](02-model-routing.md)
3. [03-prompt-caching.md](03-prompt-caching.md)
4. [04-session-management.md](04-session-management.md)
5. [05-tokenwatch-integration.md](05-tokenwatch-integration.md)
6. Docs: [../../docs/02-optimization-techniques.md](../../docs/02-optimization-techniques.md), [../../docs/03-tool-guides/](../../docs/03-tool-guides/)

## Exercise (2–4 hours)

Instrument **one** API route in a staging app: log provider usage metadata + run `TokenWatch.record_usage` for a day. Present top **three** `task_label` values by cost.
