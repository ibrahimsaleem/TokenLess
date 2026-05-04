---
description: Token-frugal defaults for Cascade and agentic coding.
activation: always_on
---

# Token-Frugal Agent Defaults

- Search before reading full files.
- Prefer graph/MCP retrieval when it returns a narrow answer.
- Do not inspect generated files, lockfiles, build artifacts, vendor folders, test snapshots, or logs unless they are directly relevant.
- Use Skills for long procedures instead of always-on rules.
- Keep command output short: use `--short`, `--stat`, `--name-only`, `-q`, `--context 2`, and limits.
- Use MCP only with targeted queries and small result sizes.
- Summarize durable decisions before compaction or task switching.
