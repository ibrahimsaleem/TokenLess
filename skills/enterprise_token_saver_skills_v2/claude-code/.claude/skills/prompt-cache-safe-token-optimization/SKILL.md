---
name: prompt-cache-safe-token-optimization
description: Optimize tokens without breaking prompt cache stability. Use when editing always-on prompts, system prompts, CLAUDE.md, API prompts, or long-running agent sessions.
---

# Prompt Cache Safe Token Optimization

## Purpose
Save tokens without accidentally increasing cost by invalidating cached prompt prefixes.

## Principle
Stable prefixes are valuable. Avoid frequent edits to content that appears at the beginning of every request.

## Safe Optimizations
- Reduce always-on instructions between sessions.
- Move long procedures into skills loaded only when needed.
- Keep system prompts stable and versioned.
- Put volatile user/task data after stable system/developer content.
- Use prompt caching for large stable context.
- Use compact summaries at task boundaries.
- Use RAG for changing documents instead of pasting them into the system prompt.

## Risky Optimizations
Avoid:
- Rewriting system prompts every turn.
- Injecting timestamps into the system prompt.
- Randomly reordering few-shot examples.
- Adding changing telemetry to the prefix.
- Editing prior conversation/context blocks mid-session.
- Huge dynamic policy blocks before stable content.

## API Prompt Layout
Recommended order:

```text
1. Stable system policy
2. Stable tool/schema instructions
3. Stable examples, if needed
4. Cached long reference context
5. Retrieved task-specific context
6. User request
7. Output schema
```

## Output Format
Return:

```md
# Cache-Safe Optimization Review

## Stable Prefix
- ...

## Volatile Content to Move Later
- ...

## Content to Cache
- ...

## Content to Retrieve Instead of Paste
- ...

## Risks
- ...
```
