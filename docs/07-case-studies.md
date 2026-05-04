# Case studies and published patterns

## Dependency-aware prompting

Teams have reported large reductions by combining:

1. A **specific, short** `CLAUDE.md` with real project decisions (not generic advice).
2. A **dependency or impact graph** so the agent opens only files in the blast radius instead of scanning the tree.

Published community write-ups describe **order-of-magnitude** fewer tokens for the same answer when graph guidance replaces naive file reads.

## Hybrid “agent OS” routing

Architectures that send **easy** steps to a small local model and **hard** steps to a frontier API can cut total cloud tokens substantially, at the cost of more engineering. Semantic retrieval instead of brute-force grep is a recurring theme in such reports.

## Prompt caching at scale

Providers document **large savings** for repeated static prefixes (e.g. long policies, tool manifests). Gains depend on traffic shape—measure cache hit rate.

## Copilot and model choice

Practitioner guidance: use **lighter** models for routine edits; escalate only when the task needs broader reasoning or multi-file refactors.

## How to use this internally

- Pick **one** service team for a 4-week pilot (graph MCP **or** RTK **or** token-optimizer audit—not all three day one).
- Instrument: tokens per task, files read, dollars per story point.
- Retrospective: quality regressions, developer satisfaction, CI time.

See rollout phases: [../skills/enterprise_token_saver_skills_v2/docs/ENTERPRISE_ROLLOUT.md](../skills/enterprise_token_saver_skills_v2/docs/ENTERPRISE_ROLLOUT.md).
