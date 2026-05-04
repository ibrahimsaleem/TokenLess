# Token optimization — one-page cheat sheet

## GitHub Copilot

1. Open only relevant files; close others.
2. Use specific symbols, paths, and `#` mentions to steer retrieval.
3. Write clear inline comments and names to reduce back-and-forth.
4. Split large tasks; start a new chat for unrelated work.

## Windsurf (Cascade)

1. Plan first (outline steps before execution).
2. Keep `.windsurfrules` concise; use memories for durable notes per product docs.
3. Trust retrieval; give keywords instead of pasting whole files.
4. Disable unused MCP servers; prefer CLI where it replaces bulky tool schemas.

## Claude Code

1. Keep `CLAUDE.md` factual and short; move playbooks to skills.
2. Handoff summary → `/compact`; `/clear` between unrelated epics.
3. Use focused subagents; prefer smaller models for trivial subtasks.
4. Check `/usage`; prune MCP and unused tools.

## APIs (Anthropic / OpenAI / others)

1. Cache or reuse static system content per provider capabilities.
2. Trim history (N turns or summary + recent).
3. Start with the smallest model that passes quality gates; escalate with metrics.
4. Set `max_tokens` / output caps appropriately; streaming is UX, not savings.

## General

1. Count before send (`tiktoken`, provider counters, or `scripts/check-context-size.py`).
2. Never duplicate policy text across layers (system + user + tools).
3. RAG instead of paste for large corpora.
4. Monitor spend and set alerts (TokenWatch in dev; provider dashboards in prod).

## High-impact OSS pilots

- [token-optimizer](https://github.com/alexgreensh/token-optimizer) — structural audit.
- [rtk](https://github.com/rtk-ai/rtk) — terminal output compression.
- [code-review-graph](https://github.com/tirth8205/code-review-graph) — graph MCP for tight context.
