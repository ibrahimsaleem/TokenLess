# Lesson: Prompt caching (provider-specific)

**Level:** Intermediate — Level 2  
**Time:** 25 minutes  
**Prerequisites:** [02-model-routing.md](02-model-routing.md)

---

## Learning objectives

By the end of this lesson you will be able to:

1. Explain what prompt caching is and which providers offer it.
2. Structure a request to maximize cache hit rate.
3. Instrument cache hit rate monitoring for a production endpoint.
4. Identify when caching is unlikely to help and why.

---

## What is prompt caching?

When you send a request to an LLM API, the provider's system computes a key-value (KV) representation of the input tokens. Prompt caching allows providers to store this KV computation and reuse it for subsequent requests that share an identical leading prefix — billing those prefix tokens at a reduced rate (typically 10–25% of the normal input price).

In practical terms: if your system prompt is 5 000 tokens and every request shares that identical prefix, a cache hit means you pay for 5 000 tokens at a fraction of normal cost instead of full price. On a high-traffic endpoint, this can reduce input costs by 30–60%.

---

## Which providers support it (as of 2026)

| Provider | Caching mechanism | Minimum prefix length |
|----------|------------------|-----------------------|
| Anthropic | Explicit cache_control markers in message blocks | ~1 024 tokens |
| OpenAI | Automatic prefix caching for prompts > 1 024 tokens | ~1 024 tokens |
| Google (Gemini) | Context caching via explicit cache object creation | ~32 000 tokens |

**Always verify the current documentation.** Pricing and minimum requirements change. Do not build architecture assumptions on cached pricing before confirming with the provider's current API reference.

---

## How to structure a request for maximum cache hits

The rule is simple: **stable content first, volatile content last**.

```
Request structure for cache alignment:

[System prompt — stable, identical across requests]
[Tool definitions — stable, identical across requests]
[Reference documents — stable, or per-user-session]
[Retrieved chunks — semi-volatile, changes per query]
[Conversation history — volatile, grows per turn]
[Current user message — unique per request]
```

Any content in the volatile tail does not matter for caching — it is always unique. Any content in the stable prefix must be byte-identical across requests to be cached.

### Common pitfall: hidden instability

These elements silently break cache hits even when the prompt looks stable:

- **Timestamps** embedded in the system prompt ("As of {{date}}, our policy is…").
- **Request IDs** or trace identifiers in the prefix.
- **Trailing whitespace** differences from template rendering.
- **User names or session IDs** injected into what looks like a static header.

Move all volatile data to the tail. If the stable prefix truly cannot be separated from volatile data, caching will not help — accept that and move on to other optimizations.

---

## Monitoring cache hit rate

For Anthropic, the API response usage object includes `cache_read_input_tokens` and `cache_creation_input_tokens`. Log these per request:

```python
usage = response.usage
cache_read = getattr(usage, "cache_read_input_tokens", 0) or 0
cache_write = getattr(usage, "cache_creation_input_tokens", 0) or 0
regular = usage.input_tokens - cache_read - cache_write

# Hit rate for this request (if cache_read > 0, it was a hit)
```

Track the hit rate as a 7-day rolling average. A healthy high-traffic endpoint should reach 70–90% hit rate once the cache is warm. A rate under 20% suggests the prefix is not stable enough.

---

## When caching will not help

- **Low-traffic endpoints.** The cache entry expires (Anthropic: ~5 minutes; verify current docs). If requests arrive less frequently than the TTL, the cache is never warm.
- **Unique-per-user prompts.** If the system prompt includes per-user personalization in the leading block, no two requests share a prefix.
- **Very short prompts.** Most providers require a minimum prefix length (e.g. 1 024 tokens for Anthropic). If your system prompt is under this threshold, caching does not apply.

In these cases: focus on prompt compression (Lesson 1) and model routing (Lesson 2) instead.

---

## You know this lesson when…

- You can list the three conditions a prefix must meet to benefit from caching (byte-identical, stable, above minimum length).
- You have reviewed your highest-traffic endpoint and can say whether caching applies and why.
- If caching does apply: you have restructured the request to put the stable prefix first and are logging cache hit rate.

---

## Read next

- [04-session-management.md](04-session-management.md)
- API-level detail: [../../docs/03-tool-guides/api-usage.md](../../docs/03-tool-guides/api-usage.md)
