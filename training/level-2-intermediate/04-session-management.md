# Lesson: session management for agents

## Chat apps

- Rolling window of N turns **or** summary + turns.
- Drop tool call payloads after you have extracted the answer.

## CLI agents (Claude Code, etc.)

- Handoff note → `/compact` → continue, or `/clear` for new epic.
- Skills: `compact-handoff` in `skills/token_optimization_skill_pack`.

## IDE agents

- Plan first; reject broad tool plans that touch the whole repo without search.

## Read next

- [05-tokenwatch-integration.md](05-tokenwatch-integration.md)
