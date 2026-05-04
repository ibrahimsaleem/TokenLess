---
name: mcp-tool-minimizer
description: Reduce token overhead from MCP servers and tools. Use when choosing MCP tools, adding MCP servers, debugging MCP context bloat, or deciding whether to query GitHub, Jira, docs, memory, databases, or search tools.
---

# MCP Tool Minimizer

## Goal
Use MCP only when it saves more context than it adds.

## Instructions
Before using an MCP server/tool:

1. State the exact question the tool should answer.
2. Check whether built-in search, local grep, CLI, or existing context is enough.
3. Prefer one targeted MCP call over broad exploration.
4. Disable, ignore, or avoid unrelated MCP servers for this task.
5. Do not include large tool outputs directly in the conversation. Summarize only the relevant facts.
6. Never ask MCP tools to fetch entire repositories, full issue histories, or large docs unless the task explicitly requires it.
7. If a tool returns too much data, extract a short index first, then fetch only the needed item.

## Tool Selection Rule
Use MCP when:
- The needed data is external to the repo or conversation.
- A targeted query can replace pasting large files/docs.
- The tool returns structured, filtered output.

Avoid MCP when:
- Local search can answer it.
- The tool description or output will add more context than the answer is worth.
- The task is simple enough for current context.

## Output Contract
Return:
- MCP needed? yes/no
- Tool/server selected
- Query to run
- Expected small result
- Fallback if too much data is returned
