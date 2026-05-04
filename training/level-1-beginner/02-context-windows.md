# Lesson 2: Context windows

**Level:** Beginner — Level 1  
**Time:** 20 minutes  
**Prerequisites:** [01-what-are-tokens.md](01-what-are-tokens.md)

---

## Learning objectives

By the end of this lesson you will be able to:

1. Explain what a context window is and what fills it.
2. Calculate how much of a model's context window is realistically usable for content.
3. Describe what happens at each failure mode (truncation, quality degradation, hard rejection).
4. Apply the 50% utilization rule when designing an AI feature.

---

## What is a context window?

The **context window** is the maximum number of tokens a model can process in a single forward pass. Everything the model "sees" in one request — system prompt, conversation history, tool definitions, retrieved chunks, and the output budget — must fit inside this limit.

Think of it as working memory. Once full, something has to give: either the request is rejected, the input is truncated (oldest content dropped), or the model's attention degrades.

**Current typical limits (verify on provider pages before building):**

| Model family | Approximate window |
|--------------|-------------------|
| GPT-4 class | 128 000 tokens |
| Claude 3.x / 4.x | 200 000 tokens |
| Gemini 1.5 / 2.x | 1 000 000 tokens |
| Smaller / faster models | 4 000 – 32 000 tokens |

Larger windows do not mean you should fill them. They mean you have more headroom to handle edge cases.

---

## What fills the context window?

A typical request to an LLM API consumes tokens from multiple sources simultaneously:

```
Total context = system_prompt
              + tool_definitions (MCP / function calling)
              + conversation_history (all prior turns)
              + retrieved_chunks (from RAG / doc injection)
              + user_message
              + output_reservation (max_tokens setting)
```

Each of these competes for the same budget. A team that adds three new MCP servers has just silently added 3 000–6 000 tokens to every request, even before the user types a word.

---

## Failure modes

**1. Hard rejection.** The provider returns a 400-class error because the input exceeds the limit. The user sees a failure. The application must handle this case.

**2. Truncation.** The SDK or provider silently drops content from one end (usually the oldest conversation turns) to fit. The model never knows what was cut. Common result: model "forgets" the original task or repeats work already done.

**3. Quality degradation ("lost in the middle").** Even within limit, a model's ability to attend to middle content weakens as context length grows. A 180 000-token prompt can produce worse answers than a 20 000-token prompt with the same relevant content, because the model's attention distributes across more noise.

**4. Latency inflation.** Processing time scales with input token count. A bloated prompt that could be 5 000 tokens at 12 000 tokens adds perceptible latency — without adding any useful information.

---

## Common misconceptions

**"A 200 000 token window means I can safely use 180 000 tokens."** In practice, quality and latency considerations mean you should treat the effective limit as 40–60% of the advertised number for production workloads. Reserve the rest for headroom.

**"If the request doesn't error, the context is fine."** Not necessarily. Truncation can happen silently, and quality degradation has no error signal — the model just produces worse outputs.

**"Conversation history doesn't matter much."** A 30-turn conversation easily accumulates 40 000–80 000 tokens before any tools or system prompt. History management is one of the highest-leverage optimizations available.

**"Larger models have bigger windows so this is less important."** Larger windows reduce the likelihood of hard truncation but do not eliminate quality degradation, latency cost, or per-token billing. The economics change; the discipline does not.

---

## The 50% utilization rule

For production features, design so that a **typical request sits below 50% of the model's context window**. This provides:

- Headroom for conversation growth without hitting limits mid-session.
- Buffer for tool calls and retrieved content to expand.
- Protection against prompt variations between users.

To find your typical utilization: instrument a representative sample of requests with `tokenwatch.py` (input tokens field) and plot the distribution. The p95 value should sit under your target ceiling.

---

## 2-minute exercise

Estimate the context breakdown for one of your AI features:

1. Count the tokens in your system prompt (use `scripts/check-context-size.py` or divide character count by 4).
2. Estimate how many turns a typical session runs and how many tokens per turn (user + assistant).
3. How many MCP servers are configured? Estimate 300 tokens per server per tool, and count the tools.
4. Add these up. Where do you stand against 50% of your model's window?

Write down: system prompt tokens + history estimate + tool overhead = total vs ceiling.

---

## You know this lesson when…

- You can calculate the effective usable tokens for a given request by subtracting system, tool, and output overhead from the model window.
- You can describe all four failure modes to a teammate and say which one each manifests as.
- You applied the 50% rule to at least one real feature and identified whether headroom is adequate.

---

## Read next

- [03-billing-basics.md](03-billing-basics.md)
- Reference: [../../guidelines/CONTEXT-WINDOW-GUIDE.md](../../guidelines/CONTEXT-WINDOW-GUIDE.md)
