# Core concepts: tokens, context, billing

## Tokens

Tokens are the atomic units LLMs use to measure text (roughly 3–4 characters per token in English). **Billing is per token** for cloud APIs. Fewer tokens generally mean lower cost and often lower latency.

## Context window

The context window is the **maximum number of tokens** the model can consider in a single request (input + tool definitions + history + output budget). If you exceed it, content is truncated or the request fails.

Typical ranges (verify on each provider’s current docs):

- Claude Sonnet-class models: on the order of **200K** tokens for many workloads; some tiers advertise **1M** context for specific models.
- GPT-4 family: variants from **8K / 32K** up to **128K+** depending on product.
- Smaller or local models: often **8K–32K**.

Always check the **exact** model card before designing long-context features.

## Input vs output tokens

- **Input (prompt) tokens** include system instructions, user messages, retrieved documents, tool schemas, and conversation history.
- **Output (completion) tokens** are what the model generates.

Pricing is almost always **different** for input vs output. Output is often more expensive per token. That is why **verbose answers** and **unbounded `max_tokens`** hurt cost.

## Prompt vs completion in product design

“Prompt” in a product sense is everything you send before the model starts generating. Bloated system prompts, unused tool definitions, and stale chat history are the most common sources of waste.

## Billing and rate limits

- Each provider publishes **per-million-token** (or per-1K) rates by model.
- **Anthropic prompt caching** (where supported): repeated static prefix can be billed at a reduced rate; cached segments may also affect rate-limit accounting differently than uncached input—read current provider docs.
- **OpenAI**: pricing and any caching/discount features depend on the product; treat all sent tokens as billable unless documented otherwise.
- **GitHub Copilot** and similar IDE products: quotas and limits are subscription-based; behavior is less transparent than raw APIs but **context discipline** still improves quality and speed.

## Why this matters for applications

Overfull context increases **latency**, **cost**, and the risk that the model **loses** early instructions or hallucinates. Token optimization is not “optional polish”—it is part of reliability engineering for LLM apps.

See also: [02-optimization-techniques.md](02-optimization-techniques.md), [guidelines/MODEL-SELECTION-GUIDE.md](../guidelines/MODEL-SELECTION-GUIDE.md), and [guidelines/CONTEXT-WINDOW-GUIDE.md](../guidelines/CONTEXT-WINDOW-GUIDE.md).
