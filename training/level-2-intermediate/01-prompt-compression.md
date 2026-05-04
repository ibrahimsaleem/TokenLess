# Lesson: prompt compression

## Techniques

- Replace narrative with **bullets** and **constraints** (“max 120 words”, “return JSON only”).
- Collapse **multi-message** history into a summary + last user turn.
- Remove duplicated error stacks; keep **one** canonical stack frame line.

## Anti-patterns

- Pasting entire JSON logs into the user message.
- Shipping the company handbook in the system prompt.

## Practice

Rewrite a verbose internal prompt to **≤ 40%** token estimate (use `scripts/check-context-size.py` on a saved `.txt`).

## Read next

- [02-model-routing.md](02-model-routing.md)
