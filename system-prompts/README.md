# System prompt templates

Five annotated starting points for common AI application patterns, each designed to be cache-friendly, concise, and easy to validate. Each template includes a "Design notes" section explaining the token tradeoffs behind its structure.

---

## Template index

| File | Use when | Estimated base tokens |
|------|-----------|----------------------|
| [general-app-system-prompt.md](general-app-system-prompt.md) | Default assistant behind your API or product | ~80–100 |
| [chatbot-system-prompt.md](chatbot-system-prompt.md) | Customer-facing chat with tool calling | ~80–120 |
| [code-review-system-prompt.md](code-review-system-prompt.md) | PR / diff review bots and CI agents | ~70 |
| [rag-app-system-prompt.md](rag-app-system-prompt.md) | Retrieval-heavy Q&A with citation | ~70 |
| [agent-system-prompt.md](agent-system-prompt.md) | Autonomous multi-tool agents with a loop | ~85 |

---

## How to use these templates

1. **Copy the raw file** into your `prompts/` directory as `system_prompt_v1.txt`.
2. **Replace all `[BRACKETED]` placeholders** with application-specific values.
3. **Read the Design notes** section at the bottom of the file. Understand the stable-vs-volatile split and decide whether you need to adjust the structure for your caching requirements.
4. **Measure the token count** using `python scripts/check-context-size.py --file prompts/system_prompt_v1.txt`.
5. **Run a smoke test** against 5–10 representative inputs before deploying.
6. **Version the prompt** as described in `guidelines/SYSTEM-PROMPT-GUIDE.md` Section 6.

---

## Template design principles

All five templates follow the same structural principles:

### 1. Stable content first

Everything that does not change between requests (role, constraints, output format) appears at the top of the prompt. This ensures that provider prompt caching can take effect on the stable prefix. Volatile content (user context, retrieved chunks, session state) goes in the user message.

### 2. Minimal footprint

Each template is under 120 tokens at its base size. This is intentional: start minimal and add only what you measure as necessary. Decorative prose ("You are a world-class expert…") is omitted.

### 3. Explicit output contract

Every template specifies the output format explicitly (JSON keys, bullets, or structured sections). This reduces output verbosity, prevents format guessing, and allows `max_tokens` to be set tightly.

### 4. Anti-hallucination patterns

The RAG template uses `cite-or-abstain` (INSUFFICIENT_CONTEXT response). The code review template prohibits speculative claims. The agent template uses a WORKLOG pattern to keep reasoning transparent and bounded. These patterns reduce the need for expensive re-prompting when outputs fail validation.

### 5. Design notes per template

Each file ends with a `### Design notes (token and quality)` section explaining:
- How the stable vs volatile split works for that template.
- Caching implications (whether the base size is above the provider minimum).
- When to shorten further.
- Customization knobs (which placeholders have meaningful defaults vs must-change values).

---

## Combining templates

For complex applications, you may need to combine elements from multiple templates. Common combinations:

- **RAG + chatbot:** Use the RAG template's cite-or-abstain pattern + the chatbot template's tool calling discipline.
- **Agent + code review:** Use the agent loop structure + the code review input assumption (diff only, not full files).
- **General app + structured output:** Use the general template's hard rules + an explicit JSON schema block from the code review template.

When combining, watch the total token count: combined templates can easily exceed 200 tokens for the stable section, which is fine if you need the constraints, but audit carefully for redundancy.

---

## Versioning and regression testing

Before deploying any modified template:

1. Run `python scripts/check-context-size.py --file prompts/system_prompt_v1.txt` and record the token estimate.
2. Compare against the baseline (original template token count).
3. Run your regression test suite against both versions.
4. If the token count increased > 20% without a clear justification, remove the added content.

See [../guidelines/SYSTEM-PROMPT-GUIDE.md](../guidelines/SYSTEM-PROMPT-GUIDE.md) for full versioning and regression guidance.
