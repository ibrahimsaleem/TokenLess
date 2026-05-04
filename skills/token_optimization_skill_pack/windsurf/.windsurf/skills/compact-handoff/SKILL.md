---
name: compact-handoff
description: Compact long AI coding sessions into a short handoff summary. Use before /compact, /clear, context reset, switching tasks, creating PRs, or handing work to another agent or teammate.
---

# Compact Handoff

## Goal
Preserve the important state while dropping stale conversation history.

## Instructions
Create a compact handoff with only durable facts:

1. Objective: one sentence.
2. Current status: done / in progress / blocked.
3. Files changed or inspected.
4. Key decisions made.
5. Commands/tests run and results.
6. Open questions or risks.
7. Next 3 actions.
8. Anything explicitly not to do.

## Compression Rules
- Do not include chat history.
- Do not include long logs; summarize errors by root cause.
- Do not repeat requirements already stored in project files unless they changed.
- Keep the handoff under 300 words unless the user asks for more.
- If using Claude Code, recommend `/compact` after generating the handoff.
- If switching tasks, recommend `/clear` after saving the handoff.

## Output Template
```md
# Handoff Summary

## Objective
...

## Status
...

## Files
...

## Decisions
...

## Tests / Commands
...

## Risks
...

## Next Actions
1.
2.
3.
```
