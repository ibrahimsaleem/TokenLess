# Anthropic / OpenAI APIs in applications

When **your product** calls LLM APIs, you control the full prompt. This is where token optimization has the highest ROI.

## System prompts

- Keep the system message **minimal, stable, and cache-friendly** (where caching exists).
- Split **policy** (stable) from **user data** (volatile).

## Caching (Anthropic)

- Align static prefixes across requests; monitor cache-related usage fields in responses.
- Read current docs for **minimum cacheable length**, TTL, and pricing.

## Streaming

- Streaming improves **perceived** latency; it does not reduce billed output tokens. Still set reasonable **`max_tokens`** / output limits.

## History

- Store only **N** turns or a **rolling summary** plus recent verbatim messages.
- Drop tool traces you do not need in future turns (summarize outcomes instead).

## Model tiers

- Default to the **smallest** model that meets quality bars; escalate with measurement.
- See [guidelines/MODEL-SELECTION-GUIDE.md](../../guidelines/MODEL-SELECTION-GUIDE.md) and `tokenwatch.py` pricing table.

## Batching and throughput

- Use provider **batch** APIs where appropriate for offline workloads.

## Instrumentation

- Log **input/output tokens** per route; pair with [TokenWatch](../../tokenwatch.py) for local cost dashboards in development.

## Official references

- [Anthropic prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Anthropic token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting)
- [Anthropic models and pricing](https://platform.claude.com/docs/en/about-claude/models/overview)
- [OpenAI usage](https://platform.openai.com/account/usage)
