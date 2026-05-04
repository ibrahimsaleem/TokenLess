# Developer guidelines — AI applications with LLM APIs

These rules apply to **every** service that calls a hosted LLM with an API key.

## 1. Instrument before optimizing

- Log **model id**, **input tokens**, **output tokens**, and **latency** per route.
- Use `task_label` (feature name) and optional `session_id` / tenant id in your telemetry.
- In development, use [TokenWatch](../tokenwatch.py) to learn distributions before changing prompts.

## 2. Always-on context is expensive

- Root `AGENTS.md`, `CLAUDE.md`, and global IDE rules are often loaded **every** turn. Keep them short.
- Put long procedures in **skills** or internal docs linked from a single line.

## 3. Retrieval beats bulk paste

- Use **RAG**, symbol search, graph MCP, or server-side search instead of attaching whole repositories or logs.

## 4. Model routing is mandatory

- Define which routes use **small** vs **large** models. Document the escalation path.
- See [MODEL-SELECTION-GUIDE.md](MODEL-SELECTION-GUIDE.md).

## 5. MCP and tools are part of the prompt

- Each tool definition consumes context. Disable unused servers.
- Enforce `top_k`, `max_bytes`, and timeouts on custom tools.

## 6. Secrets and PII

- Do not send secrets, card data, or production PII to third-party LLMs unless contractually allowed.
- Redact logs before they become model input.

## 7. Output caps

- Set **maximum output tokens** everywhere it is safe. Open-ended generation is a cost and quality risk.

## 8. History policy

- Ship a **documented** history strategy: sliding window, summarization, or archive-and-reference.

## 9. Prompt changes are code changes

- Version prompts in git; review them like schema changes.
- Pair prompt diffs with **token delta** estimates.

## 10. Templates

- Start new repos from [../templates/](../templates/) for lean `CLAUDE.md` / `AGENTS.md` / ignore files.

## Quick reference

- [QUICK-REFERENCE-CHEATSHEET.md](QUICK-REFERENCE-CHEATSHEET.md)
