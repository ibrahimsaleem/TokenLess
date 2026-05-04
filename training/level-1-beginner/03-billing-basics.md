# Lesson 3: Billing basics

**Level:** Beginner — Level 1  
**Time:** 20 minutes  
**Prerequisites:** [02-context-windows.md](02-context-windows.md)

---

## Learning objectives

By the end of this lesson you will be able to:

1. Explain how cloud LLM APIs bill for input and output tokens separately.
2. Calculate the approximate cost of a request given a pricing table.
3. Identify which request components drive the most spend.
4. Describe the three main pricing models (metered, subscription, self-hosted) and when each is appropriate.

---

## How LLM billing works

Cloud LLM providers charge per **million tokens** (MTok), split into input and output:

```
cost = (input_tokens / 1_000_000) × input_rate_per_mtok
     + (output_tokens / 1_000_000) × output_rate_per_mtok
```

Output is almost always more expensive than input because generating a token requires more compute than reading one. Typical multipliers range from 3× to 5× more expensive per output token.

**Example calculation (illustrative — verify current pricing before budgeting):**

Suppose a model charges $3.00 per MTok input and $15.00 per MTok output. A request with 1 200 input tokens and 400 output tokens costs:

```
input:  (1200 / 1_000_000) × $3.00  = $0.0036
output: (400  / 1_000_000) × $15.00 = $0.0060
total per request: $0.0096 ≈ $0.01
```

At 10 000 such requests per day: $96/day → $2 880/month.

Now compress the system prompt by 50% (saving 300 input tokens per request) and cap output at 250 tokens:

```
input:  (900  / 1_000_000) × $3.00  = $0.0027
output: (250  / 1_000_000) × $15.00 = $0.0038
total per request: $0.0065
```

At 10 000 requests/day: $65/day → $1 950/month. A **32% reduction** from prompt discipline alone.

---

## Prompt caching and discounted input

Some providers offer **prompt caching**: if the leading portion of your prompt matches a previous request byte-for-byte, the cached input tokens are billed at a significantly reduced rate (often 10–25% of the normal input price).

To benefit:
- Keep the stable prefix (system prompt, tool definitions, reference material) byte-identical across requests.
- Place the volatile content (user query, session history) after the stable prefix.
- Monitor the cache-hit indicator in the API response.

Cache hits only apply within a cache TTL (typically minutes, not hours). High-traffic endpoints benefit most. Low-traffic or unique-per-user prompts rarely see meaningful caching gains.

---

## Three pricing models

### Metered API (pay per token)

The most common model for direct API access (Anthropic, OpenAI, Google, Mistral, etc.). You pay exactly for what you use. Predictable at low scale; can surprise at high scale if usage patterns are not monitored.

**Best for:** Development, staging, controlled production features with known call rates.

### Subscription with token pooling

Some products (GitHub Copilot, certain IDE integrations) bundle usage into a flat fee with a shared pool. Individual calls are not directly billed; heavy users can exhaust the pool.

**Best for:** Individual developer tools where the vendor has optimized for typical usage patterns. Harder to optimize because feedback loop is indirect.

### Self-hosted models

Run a model on your own infrastructure. No per-token billing, but hardware, energy, and operational costs apply. Context window optimization matters for throughput and latency, not cost per call.

**Best for:** High-volume regulated workloads, data-residency requirements, or scenarios where the cloud metered cost exceeds hardware cost.

---

## Where most spend goes in practice

Based on typical application profiles:

1. **Conversation history accumulation** — often 40–70% of input tokens in chatbot-style apps. Grows indefinitely if not managed.
2. **System prompt repetition** — a 2 000-token system prompt multiplied by every request in a high-traffic service.
3. **Uncapped output** — if `max_tokens` is not set or is set too high, verbose completions balloon output costs.
4. **MCP / tool definitions** — every registered tool contributes schema tokens to every request. Three unused servers can add 3 000+ tokens of overhead silently.
5. **RAG over-retrieval** — injecting k=20 retrieved chunks when k=3 would have been sufficient.

Identify which of these applies to your system first, before optimizing anything else.

---

## Common misconceptions

**"Output is cheap — I'll just set max_tokens high to be safe."** Output at 5× input rate is the most expensive token category. Setting a generous ceiling allows billing spikes on verbose completions.

**"I'm on a subscription so token cost doesn't matter."** Subscription tools still have pool limits, and the underlying provider economics influence feature availability and pricing. Lean usage also means lower latency for subscription-billed tools.

**"Caching is automatic."** Prompt caching requires deliberate request structuring. Read the provider documentation for the specific API surface and cache markers before assuming it applies.

---

## 2-minute exercise

Run `python scripts/estimate-cost.py` with the token counts from your exercise in Lesson 1. Compare two scenarios:

1. Baseline: original system prompt token count, typical output length.
2. Compressed: 50% system prompt tokens, output capped at 60% of baseline.

Note the monthly cost difference at 1 000 requests/day, 5 000/day, and 10 000/day.

---

## You know this lesson when…

- You can calculate the monthly cost of a feature given a pricing table and an estimated request volume.
- You can identify the top spend driver in your application (history, system prompt, output, tools, or RAG).
- You know whether prompt caching applies to your provider and have either enabled it or explicitly decided not to.

---

## Read next

- [04-first-optimizations.md](04-first-optimizations.md)
- Run: `python ../../scripts/compare_models.py --help` (available after Level 2 setup)
