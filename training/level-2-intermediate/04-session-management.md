# Lesson: Session management for agents and chat apps

**Level:** Intermediate — Level 2  
**Time:** 25 minutes  
**Prerequisites:** [03-prompt-caching.md](03-prompt-caching.md)

---

## Learning objectives

By the end of this lesson you will be able to:

1. Choose the right history strategy (rolling window, summarize-and-continue, or fresh session) for a given application type.
2. Implement a rolling window history manager in Python.
3. Drop tool call payloads after extracting their value.
4. Know when to use the `compact-handoff` skill vs `/clear` in an agent session.

---

## The problem: history that never stops growing

Conversation history is the single most common cause of unexpected token cost growth. Every turn adds to the accumulated input on the next request. A 30-turn chatbot session at 400 tokens per turn generates 12 000 tokens of history, on top of the system prompt, tools, and retrieved context — before the model produces a single word of response.

Without management, history grows linearly without bound and eventually either hits the context limit or silently degrades in quality.

---

## Strategy 1: Rolling window (n turns)

Keep the last N turns of conversation and discard older ones. Simplest to implement; works well when each turn is largely self-contained.

```python
MAX_TURNS = 15  # keep last 15 turns (user + assistant pairs)

def trim_history(messages: list[dict]) -> list[dict]:
    """Keep only the last MAX_TURNS message pairs."""
    non_system = [m for m in messages if m["role"] != "system"]
    trimmed = non_system[-(MAX_TURNS * 2):]  # pairs
    system = [m for m in messages if m["role"] == "system"]
    return system + trimmed
```

**When to use:** Chatbots and short-session interactive apps where old turns are rarely referenced.

**Risk:** If the user refers to something from turn 3 and MAX_TURNS is 15 and they are at turn 20, that information is gone. Choose N based on median session length, not worst case.

---

## Strategy 2: Summarize and continue

After a defined number of turns (or when history exceeds a token budget), send the current history to the model and ask it to summarize the key facts. Replace the full history with the summary plus the last 2–3 turns.

```python
SUMMARY_TRIGGER_TURNS = 20

def maybe_summarize(monitor, messages: list[dict]) -> list[dict]:
    if len(messages) < SUMMARY_TRIGGER_TURNS * 2:
        return messages
    # Summarize oldest N-5 turns
    to_summarize = messages[:-5]
    summary_response = call_llm(
        model="fast-small-model",  # cheap; summary is a simple task
        prompt="Summarize the following conversation concisely "
               "(key facts only, ~150 tokens):\n\n" + format_turns(to_summarize)
    )
    summary_msg = {"role": "system", "content": f"[Prior session summary]: {summary_response}"}
    return [summary_msg] + messages[-5:]
```

**When to use:** Longer sessions where cross-turn context matters (e.g. debugging sessions where the model needs to remember what was tried three steps ago).

**Note:** The summarization call itself costs tokens. Use a small model for it.

---

## Strategy 3: Fresh session with handoff

For clearly distinct tasks, the cheapest option is to start a new session with a compact handoff note from the previous one. This is common in agentic workflows where distinct "phases" (plan, implement, review) can run independently.

Handoff note (~100 tokens):
```
## Handoff from: [implementation phase]
Completed: Payment service refactored to use Stripe SDK v4.
Changed files: payments/service.py, payments/models.py, tests/test_payments.py.
Outstanding: Integration tests need updated fixtures.
Next: Run integration test suite, fix failing fixtures.
```

A new session starts with only this note and the new task prompt.

**When to use:** Agentic pipelines with distinct phases; any case where you can cleanly separate "done" from "next".

---

## Dropping tool call payloads

In multi-step agent sessions, each tool call and its result is added to the conversation history. A file-read tool call that returns 3 000 tokens of source code stays in history for every subsequent turn — even if the model already extracted the information it needed.

**Pattern:** After a tool result has been used (the model has responded to it), replace the payload with a compressed reference:

```python
def compress_tool_result(tool_result_message: dict) -> dict:
    """Replace a large tool result with a summary reference."""
    original = tool_result_message["content"]
    if len(original) > 500:  # only compress large results
        tool_result_message["content"] = f"[Tool result retrieved and used — {len(original)} chars. Summary: ...]"
    return tool_result_message
```

This requires application-level history management (not relying on the provider to manage history automatically).

---

## In CLI agents

- **`/compact`** — summarize and continue the current session. Use after completing a logical unit of work within the same epic.
- **`/clear`** — clear history and start fresh. Use when moving to a fully different task with no cross-session context needed.
- **`compact-handoff` skill** (from `skills/token_optimization_skill_pack/`) — automated compact that writes a structured handoff note before clearing.

Prefer `/compact` over long accumulation; prefer `/clear` over `/compact` when tasks are genuinely unrelated.

---

## Common misconceptions

**"The model handles long contexts just fine."** The context window may be 200 000 tokens, but quality degrades at high utilization. Managing history keeps requests in the quality zone.

**"Dropping old tool results will confuse the model."** If the model has already incorporated the information from a tool result (its next response reflected that information), it does not need the raw payload again. What it needs is the fact it derived — which is already in its response.

**"Summarization is too expensive."** At one summarization every 20 turns, and using a small model, the cost is negligible compared to the savings from keeping history under control.

---

## You know this lesson when…

- You have chosen an explicit history strategy for at least one feature in your application and coded it.
- You can implement a rolling window and a summarize-and-continue function from memory or from minimal reference.
- You know the difference between `/compact` and `/clear` and when to use each.

---

## Read next

- [05-tokenwatch-integration.md](05-tokenwatch-integration.md)
