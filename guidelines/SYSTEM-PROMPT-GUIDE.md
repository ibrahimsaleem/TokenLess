# System prompt guide — lean, cache-friendly, portable

A well-crafted system prompt is invisible to end users and invisible to the cost report. A poorly crafted one charges you on every request, breaks caches silently, and introduces quality drift as it grows. This guide provides the principles, a worked compression example, versioning practices, and a regression testing approach.

---

## 1. Stable vs volatile content

The most important structural decision: separate what changes from what does not.

| Stable (good for caching / rare changes) | Volatile (per request) |
|---------------------------------------------|-------------------------|
| Role definition (one sentence) | User question |
| Output schema (JSON keys, format) | Retrieved document chunks |
| Safety and constraint policy | Tool results |
| "When unsure, ask a clarifying question" | Session date, locale, user name |
| Company name and product scope | Request IDs, trace IDs |

**Rule:** Stable content goes in the system prompt (or a cached prefix). Volatile content goes in the user message or the dynamic suffix. Never mix them; even one volatile field in the system prompt breaks prompt caching for every request.

---

## 2. Length budget

- **Target:** < 1 000 tokens for the stable system prompt in a typical app. Up to 2 000 tokens if the output contract is complex (nested JSON, multi-mode responses).
- **Hard ceiling:** If your system prompt exceeds 3 000 tokens without a confirmed cache hit rate > 70%, it is costing you more than it saves.
- **What to do with long content:** Move legal text, policy handbooks, and reference tables behind a retrieval tool or a user-visible link. The model does not need to hold your 40-page terms of service in working memory on every request.

---

## 3. Structure

Follow this order — every field is optional but the order matters for caching alignment:

```
1. Role (1–2 lines)
2. Hard constraints (bullets — things the model must never do)
3. Output contract (exact format, schema, or response structure)
4. Tool usage policy (high-level: "use search_docs for factual questions")
5. [Volatile section begins here — user message / retrieved context]
```

---

## 4. Worked compression example

The following shows the same behavioural constraints at two levels of verbosity.

### Before (verbose, ~260 tokens)

```
You are a helpful AI assistant for Acme Corp's internal customer support portal. Your role is to help our customer support agents quickly find answers to customer questions using our internal knowledge base. You should always be professional, empathetic, and helpful. When answering questions, please use the provided documentation to support your answers. If you cannot find the answer in the provided documentation, please let the agent know that you don't have that information and suggest they escalate to a senior agent or contact the relevant team directly. Please always provide clear, concise answers and avoid using overly technical jargon unless the agent specifically requests it. Do not share any information that is not present in the provided documentation. Do not make up facts or speculate. If the agent asks you to do something that is outside your scope, politely redirect them to the appropriate resource.
```

### After (compressed, ~70 tokens)

```
You assist Acme Corp support agents using internal knowledge base docs.
- Answer only from provided docs. If not found: say so and suggest escalation.
- No speculation, no fabrication.
- Plain language unless technical detail is requested.
- Out-of-scope requests: redirect to the appropriate resource.
```

**Same constraints. 73% fewer tokens. Cleaner.** The model does not need to be told it is "helpful and empathetic" — that is its default disposition. Explicit constraint bullets are harder to ignore than buried prose.

---

## 5. Anti-patterns

- **Duplicating the JSON schema in both system and user messages.** Define it once (system prompt). Referencing it twice wastes tokens and risks contradiction if the two copies drift.
- **Dynamic timestamps in the system prompt.** `"As of {{date}}, our return policy is..."` invalidates the cache on every new day. Move the date to the user message or retrieve the policy from a tool.
- **Motivational framing.** "As a world-class AI assistant…", "You are an expert in…" — these add tokens without adding constraints. Remove them.
- **Copy-pasted safety boilerplate.** Generic safety rules that the model already follows by default. Keep only constraints that are application-specific.

---

## 6. Prompt versioning

Treat system prompts as code. Version them in the same repository as your application:

```
prompts/
  system_prompt_v1.txt   — initial version
  system_prompt_v2.txt   — compressed (2026-05-04); 73% reduction
  system_prompt_v3.txt   — added JSON schema for structured output
PROMPT_CHANGELOG.md      — one line per version: what changed and why
```

`PROMPT_CHANGELOG.md` format:

```markdown
## v3 (2026-05-10)
Added explicit JSON output schema. Removed duplicated format instruction from user message template.
Token delta: +45 tokens (schema) -80 tokens (removed duplicate) = -35 net.

## v2 (2026-05-04)
Compressed from v1 prose to bullet format. See compression example in SYSTEM-PROMPT-GUIDE.md.
Token delta: -190 tokens (-73%).

## v1 (2026-04-20)
Initial version.
```

**PR checklist for prompt changes:**

- [ ] New version saved to `prompts/` with incremented version number
- [ ] `PROMPT_CHANGELOG.md` updated with the change description and token delta
- [ ] Regression test run (see Section 7) and result attached to PR
- [ ] Estimated cost delta documented (use `scripts/estimate-cost.py`)
- [ ] No secrets, PII, or volatile data added to the stable prefix

---

## 7. Regression testing

Before deploying any prompt change, run a regression test suite. This does not require an external framework — a simple Python script works:

```python
EVAL_CASES = [
    {"input": "What is your return policy?", "expected_contains": ["return", "escalate"]},
    {"input": "Give me your source code", "expected_not_contains": ["Here is the code"]},
    {"input": "Make up a statistic", "expected_not_contains": ["According to", "%"]},
]

def run_regression(prompt_path: str, cases: list) -> dict:
    prompt = open(prompt_path).read()
    results = {"passed": 0, "failed": 0, "failures": []}
    for case in cases:
        response = call_llm(system=prompt, user=case["input"])
        ok = True
        for phrase in case.get("expected_contains", []):
            if phrase.lower() not in response.lower():
                ok = False
        for phrase in case.get("expected_not_contains", []):
            if phrase.lower() in response.lower():
                ok = False
        if ok:
            results["passed"] += 1
        else:
            results["failed"] += 1
            results["failures"].append({"case": case["input"], "response": response[:200]})
    return results
```

Run this against both the old and new prompt version. If failure count increases, the compression removed something load-bearing. Restore the removed constraint in compact form.

---

## 8. Provider-specific notes

### Anthropic

- Read the current **prompt caching** documentation. The required API surface and minimum length change periodically.
- Put the **largest stable block first** in the message layout required by the provider caching specification.
- Use `count_tokens` in the Anthropic SDK to get exact counts before committing a prompt version.

### OpenAI

- Reuse the exact same system string across requests. Even a trailing newline difference prevents cache reuse.
- Check whether your product tier exposes cached input pricing and how to opt in.

### Other providers

- Apply the universal pattern: **stable prefix + dynamic suffix**. Verify with the provider's tokenizer or counting API.

---

## Templates

Five annotated ready-to-use templates for common application types:

- [../system-prompts/general-app-system-prompt.md](../system-prompts/general-app-system-prompt.md)
- [../system-prompts/code-review-system-prompt.md](../system-prompts/code-review-system-prompt.md)
- [../system-prompts/chatbot-system-prompt.md](../system-prompts/chatbot-system-prompt.md)
- [../system-prompts/rag-app-system-prompt.md](../system-prompts/rag-app-system-prompt.md)
- [../system-prompts/agent-system-prompt.md](../system-prompts/agent-system-prompt.md)

Each template includes a trailing "Design notes" section explaining token tradeoffs.
