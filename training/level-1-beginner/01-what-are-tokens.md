# Lesson 1: What are tokens?

**Level:** Beginner — Level 1  
**Time:** 15 minutes  
**Prerequisites:** None

---

## Learning objectives

By the end of this lesson you will be able to:

1. Define what a token is in the context of LLM APIs.
2. Estimate the token count of a text sample without using a tokenizer.
3. Explain why token count matters for both cost and performance.
4. Identify which parts of a typical prompt consume the most tokens.

---

## What is a token?

A **token** is the basic unit of text that a language model processes. When you send a request to an LLM API, the text does not arrive as characters or words — it is first split into tokens by a **tokenizer** specific to that model family.

Tokens map roughly to syllables or short words in English:

| Text | Approximate token count |
|------|------------------------|
| `"Hello"` | 1 token |
| `"Hello, world!"` | 4 tokens |
| `"function calculateTotal(items) {"` | 8 tokens |
| A 200-word paragraph | ~250–280 tokens |
| A 1 000-line code file | ~3 000–8 000 tokens depending on density |

The tokenization algorithm differs by model family. OpenAI uses BPE (Byte Pair Encoding) via `tiktoken`. Anthropic uses a similar sub-word scheme. As a result, the same sentence can produce different token counts on different providers.

---

## Why engineers should care

**1. Cost is metered by token.** Cloud LLM APIs charge separately for **input tokens** (your prompt, system instructions, conversation history, tool definitions) and **output tokens** (the model's response). Output is typically more expensive per token. A system prompt that could be compressed from 800 tokens to 300 tokens saves money on every single request in perpetuity.

**2. Latency grows with input size.** Larger prompts take longer to process. For user-facing features, a bloated system prompt can add perceptible latency without adding any value.

**3. Context limits are finite.** Every model has a maximum token limit for a single request (its context window). Once exceeded, the provider either rejects the request, truncates the input, or the application must split the work. Hitting this ceiling mid-task is a runtime error.

**4. Quality can degrade at high usage.** Research shows that models attend less reliably to content buried in the middle of very long contexts (the "lost in the middle" effect). Lean prompts that put key instructions at the beginning and end tend to produce more reliable outputs.

---

## Practical intuition without a tokenizer

You do not need a tokenizer for a rough estimate. Use these heuristics:

- **English prose:** 1 token ≈ 3.5–4 characters. Divide character count by 4.
- **Code:** varies. Identifiers split differently; symbols often tokenize individually. Estimate ~4 characters/token for C-style code, ~2.5 for symbol-dense languages like Lisp or shell.
- **JSON:** structure characters (braces, quotes, colons) each contribute tokens. A 1 KB JSON object is roughly 300–500 tokens.
- **`scripts/check-context-size.py`** in this repo: takes a file or string and prints a rough estimate without calling any API.

---

## Common misconceptions

**"Tokens = words."** Not quite. Short common words ("the", "and", "is") may each be one token, but unusual words, variable names, and URL fragments can be multiple tokens. Code is almost always more token-dense per line than prose.

**"Output tokens cost the same as input tokens."** Almost never true. Output is typically billed at 3–5× the input rate. Always check the current pricing page for your provider.

**"The context window is always available."** The advertised window (e.g. 200 000 tokens) is the theoretical maximum. In practice your budget is smaller: tool definitions, conversation history, and the output reservation all reduce what is available for your actual content.

**"Smaller models always produce fewer tokens."** Model size affects quality, not output verbosity. A small model can produce equally long (or longer) responses if not constrained by `max_tokens`.

---

## 2-minute exercise

1. Open any system prompt from your current project (or copy one from `system-prompts/` in this repo).
2. Count the characters (most editors show this in the status bar, or use `wc -m file.txt`).
3. Divide by 4 to get a rough token estimate.
4. Identify the single largest block of text. Is it load-bearing or decorative?

Write down: the estimated token count, the largest block, and whether you could compress it by 25% without changing the behaviour.

---

## You know this lesson when…

- You can estimate the token cost of a prompt within ±30% without running a tokenizer.
- You can explain to a non-technical stakeholder why a "short" prompt matters to the API bill.
- You identified at least one section in your current project's prompts that could be compressed.

---

## Read next

- [02-context-windows.md](02-context-windows.md) — how token counts relate to model limits
- Deep dive: [../../docs/01-core-concepts.md](../../docs/01-core-concepts.md)
