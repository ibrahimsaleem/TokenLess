# System prompt guide — lean, cache-friendly, portable

## Split stable vs volatile

| Stable (good for caching / rare changes) | Volatile (per request) |
|---------------------------------------------|-------------------------|
| Role in one sentence | User question |
| Output schema (JSON keys) | Retrieved chunks |
| Safety policy summary | Tool results |
| “When unsure, ask a clarifying question” | Session date / locale |

## Length budget

- Target **< 1–2k tokens** for universal system content unless you have measured cache hits that justify more.
- Move long legal text behind a **retrieval tool** or user-visible link when possible.

## Structure

1. **Role** — one or two lines.
2. **Hard constraints** — bullets; include “do not expose secrets”.
3. **Output contract** — exact JSON or format; forbid markdown wrappers if you parse JSON.
4. **Tool usage** — when to call which class of tool (high level, not full tool JSON).

## Provider notes

### Anthropic

- Read current **prompt caching** documentation: marker placement, TTL, minimum lengths.
- Put the **largest stable block first** in the message layout required for caching.

### OpenAI

- Reuse the same system string across requests where possible; avoid accidental whitespace drift.
- Check whether your product tier exposes any **cached input** pricing and how to structure for it.

### Others

- Each provider differs. Copy this pattern: **stable prefix + dynamic suffix**, verify with their tokenizer or `count_tokens` equivalent.

## Anti-patterns

- Duplicating the same JSON schema in system **and** user messages.
- Putting dynamic timestamps in the system prompt (breaks caches and wastes tokens).

## Templates

See [../system-prompts/](../system-prompts/) for annotated examples.
