---
name: mcp-token-saver
description: Choose and use MCP servers in a token-efficient way. Use when adding MCP servers, querying external systems, deciding whether MCP should be used, or preventing MCP context bloat.
---

# MCP Token Saver

## Purpose
Use MCP servers only when they reduce context, not when they add noise.

## Decision Rule
Use MCP when the server can return a narrow answer that replaces large pasted context.

Avoid MCP when:
- local grep/search is enough
- the server returns huge unfiltered objects
- the task does not need external context
- the MCP server injects large tool descriptions for no benefit

## Recommended MCP Patterns

### Good
- Query one issue by ID
- Retrieve one architecture doc section
- Find tests affected by one changed function
- Get code graph blast radius
- Fetch a small diff or PR summary
- Retrieve top 5 search results, then open one

### Bad
- Fetch all issues
- Read an entire repo through MCP
- Dump full docs into context
- Enable every MCP server globally
- Keep unused MCP servers active in every project

## MCP Server Classes That Can Save Tokens
- Code graph / AST graph MCP
- Documentation retrieval MCP with scoped search
- Memory MCP with short summaries and TTL
- Ticket/issue MCP with ID-based lookup
- Log/search MCP with filtered query and limit
- Vector/RAG MCP with top-k and chunk limits

## Query Template
Before calling MCP, write:

```md
MCP goal:
Server:
Smallest query:
Max result size:
What I will ignore:
Fallback:
```

## Output Contract
After MCP use:

```md
## MCP Result Summary
- Server:
- Query:
- Useful facts:
- Omitted noisy output:
- Next action:
```
