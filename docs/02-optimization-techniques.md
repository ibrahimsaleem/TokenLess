# General token optimization techniques

These patterns apply across every API provider, agent framework, and IDE tool. Apply them in order of effort — the highest-ROI ones require no code changes at all.

---

## 1. Prompt compression and summarization

### What it means

Replacing verbose instructions with tighter equivalents. A 400-word system prompt covering tone, formatting, safety rules, and examples can often be rewritten to under 100 tokens with no measurable quality drop.

### How to apply

- Replace prose paragraphs with **bullet constraints**: `- Output: JSON only. No markdown fences.`
- Combine duplicate safety rules into one block.
- Remove motivational framing ("As a helpful AI…"). The model knows.
- Move stable, long instructions into a cached prefix or a skill file that loads on demand.

### Worked example

**Before (verbose):**
```
You are an AI assistant for Acme Corp's internal HR portal. You should be helpful, friendly, and professional at all times. When users ask about policies, you should answer based on the provided policy documents. If you are unsure about anything, please let the user know and suggest they contact HR directly. Please always respond in a clear and concise manner and avoid jargon when possible.
```
Estimated: ~70 tokens.

**After (compressed):**
```
You assist Acme Corp employees with HR policy questions.
- Answer only from provided policy documents.
- If information is missing, say so and suggest contacting HR.
- Plain language, no jargon.
```
Estimated: ~35 tokens. Same behaviour.

### Anti-patterns

- Removing genuinely load-bearing constraints (e.g. "do not mention competitor names").
- Compressing so aggressively that the schema or safety rules become ambiguous.

### Measurement

Token delta between v_old and v_new using `scripts/check-context-size.py`. Target: 30–50% reduction on first pass.

---

## 2. Few-shot vs zero-shot tradeoff

### What it means

Few-shot examples add tokens but can dramatically improve output accuracy for unusual formats or niche tasks. Zero-shot is cheaper but depends on the model already knowing the domain well.

### Decision rule

1. Try **zero-shot** first with an explicit output schema.
2. If output fails the automated check (JSON parse, regex, test), add **one example**.
3. If still unreliable, add a second example and reconsider whether the task belongs on a smaller fine-tuned model.

### Anti-pattern

Including three or more examples for a task the model already handles correctly. This is a common source of avoidable input bloat.

---

## 3. Chunking strategies

### What it means

For inputs larger than a few thousand tokens (long documents, large diffs, log files): split into chunks and process each chunk, then aggregate results.

### Patterns

- **Fixed-size with overlap**: chunk at N characters, overlap last K characters to preserve cross-boundary context. Use when the document is homogeneous.
- **Semantic / paragraph chunking**: split at section headers or paragraph breaks. Retains meaning boundaries. Prefer for prose.
- **Code: function or class chunking**: split at the AST boundary (function/class def). Each chunk is self-contained enough to review or summarize independently.
- **Hierarchical**: summarize each chunk first, then summarize the summaries. Scales to very large corpora.

### Anti-patterns

- Sending a 50 MB log file as a single message.
- Using fixed-size chunks for code without caring about mid-function splits.
- Forgetting that the **aggregation step** also costs tokens — keep summaries short.

### Measurement

Max tokens per call stays below your target ceiling. Monitor with `scripts/check-context-size.py` on a sample chunk.

---

## 4. Retrieval-augmented generation (RAG)

### What it means

Index your knowledge (docs, code, tickets, policies) and retrieve only the top-k most relevant chunks instead of injecting the entire corpus. The model sees less; quality stays high if retrieval is accurate.

### Implementation sketch

1. **Embed** chunks at ingest time (provider embedding API or local model).
2. **Retrieve** top-k by cosine similarity at query time.
3. **Inject** only those chunks into the user or system message.
4. **Cap** the total retrieved context at a hard limit (e.g. 8 000 tokens) so runaway retrieval cannot blow the budget.

### Failure modes

- **Lost recall**: relevant chunk not returned because embedding space missed the user's phrasing. Mitigate with hybrid search (BM25 + vector).
- **Injection inflation**: returning k=20 chunks when k=3 would suffice. Set `top_k` conservatively and measure answer quality.
- **Stale index**: documents updated but embeddings not re-computed. Implement incremental re-indexing.

### Measurement

Tokens in the retrieval context block per query (average and p95). Track alongside answer correctness separately.

---

## 5. Prompt / prefix caching (provider-specific)

### What it means

Providers that support prompt caching can reuse a previously computed key-value cache for a static prefix in the request, billing a smaller rate for cache hits. This is most effective when a long stable prefix (system prompt + tool definitions + reference docs) appears identically across many requests.

### How to align for cache hits

- Keep the **stable prefix byte-identical** across requests. Even a trailing space difference will miss the cache.
- Put the **longest stable block first** in the message layout the provider expects for caching.
- Do not embed volatile data (timestamps, request IDs, user names) in the cached section.
- Monitor the cache-hit field in API responses and dashboard it.

### When it does not help

- Low-traffic endpoints where the cache entry expires between calls (check provider TTL — typically minutes).
- Requests where the "stable" section is actually unique per user.

### Anti-pattern

Assuming caching is on by default. Read the provider's documentation for the specific API surface and cache marker syntax before building around it.

---

## 6. Structured outputs

### What it means

Defining a strict output schema (JSON object, specific keys, enumerated values) so the model produces exactly what the downstream code expects without free-form prose.

### Direct token savings

Often modest on a per-call basis, but:

- Eliminates re-prompt rounds when output fails to parse.
- Enables shorter prompts because you remove lengthy "please format as…" prose.
- Lets you cap output tokens tightly because you know the exact output shape.

### Implementation

- Use provider JSON mode or function-calling / tool-calling output contracts.
- Define the schema once in the system prompt or skill file and cache it.

---

## 7. Model routing and tiering

### What it means

Using different model tiers for different task complexities. Small, fast, cheap models for simple extraction or routing; large models only when multi-step reasoning or broad context is genuinely required.

### Routing policy (example)

```
if task in ["classify", "extract", "route", "summarize_short"]:
    model = "fast-small"          # e.g. Haiku, gpt-4.1-nano
elif task in ["codegen", "review", "qa"]:
    model = "mid"                 # e.g. Sonnet, gpt-4.1
else:  # multi-file refactor, architecture planning
    model = "large"               # escalate only on failure
```

### Escalation discipline

- Escalate programmatically when output fails an automated check, **not** by default.
- Log which tier handled each request. Review the mix weekly.

### Anti-pattern

Using the largest available model for every call "to be safe." This commonly doubles or triples cost with no measurable quality gain on routine tasks.

### Measurement

Model tier mix by route (percentage of calls by tier). Track quality independently per tier.

---

## 8. Session management

### What it means

Trimming conversation history so stale context does not accumulate and consume the window.

### Strategies

- **Sliding window**: keep the last N turns; drop older ones.
- **Summarize and continue**: summarize completed work into a compact block, then start fresh with that block as a single history entry.
- **Fresh session**: for a completely new task, clear history entirely rather than appending to an existing thread.

### In CLI agents

Use compaction commands (`/compact`, handoff skills) after each major phase. See `skills/token_optimization_skill_pack/` for the `compact-handoff` skill.

### Anti-pattern

Appending indefinitely without review. A 60-turn conversation easily exceeds 50 000 input tokens, most of which the model cannot meaningfully attend to anyway.

---

## Next steps

- Tool-specific habits: [03-tool-guides/](03-tool-guides/)
- MCP patterns and audit: [04-mcp-guide.md](04-mcp-guide.md)
- Monitoring and OSS helpers: [05-tools-and-platforms.md](05-tools-and-platforms.md)
- Apply these techniques: [../training/level-2-intermediate/](../training/level-2-intermediate/)
