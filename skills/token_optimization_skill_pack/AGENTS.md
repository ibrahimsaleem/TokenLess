# AGENTS.md

## Token-Frugal Agent Instructions

Use this file as the minimal root-level agent guidance. Keep it short because some tools treat root AGENTS.md as always-on context.

### Defaults

- Start with the smallest useful context.
- Search before reading full files.
- Prefer snippets, symbols, tests, and dependency paths over entire files.
- Do not inspect generated files, build artifacts, lockfiles, vendor folders, or large docs unless required.
- Summarize discoveries before making multi-file changes.
- Use compact handoffs after long tasks.
- Prefer smaller/cheaper models or read-only exploration agents for simple tasks.
- Use MCP tools only when they return targeted data that replaces large pasted context.

### Good first questions for the agent

- What is the exact file/symbol/test/config needed?
- Can search answer this before reading files?
- What context can be dropped after this phase?
