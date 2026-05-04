# MCP: token-saving patterns and policy

The Model Context Protocol (MCP) lets agents call tools. **Each server contributes tool definitions to context**, so unused MCP servers are pure overhead.

## Categories that usually save tokens

1. **Code graph / AST MCP** — answers “which files matter?” before wide reads. Example: [code-review-graph](https://github.com/tirth8205/code-review-graph) (see also `skills/enterprise_token_saver_skills_v2/docs/MCP_TOKEN_SAVERS.md`).
2. **Documentation retrieval** — returns **top-k** chunks instead of pasting manuals.
3. **Memory MCP** — stores durable notes outside the chat window (with hygiene: TTL, size caps).
4. **Issue/PR MCP** — fetch **one** ticket or thread by id.
5. **Log/search MCP** — return **filtered slices**, not full logs.

## Policy checklist

- **Project-scope** MCP configs before global.
- **Disable** servers not needed for the current task (in Claude Code, review MCP list regularly).
- Require **limits**: `top_k`, max characters, time windows.
- **Summarize** large tool results before continuing multi-step reasoning.
- **Never** send secrets through tools or logs.

## When MCP is the wrong tool

Prefer ordinary **CLI commands** and local scripts when they avoid registering large tool schemas in the agent.

## Further reading

- [Model Context Protocol](https://modelcontextprotocol.io)
- Enterprise pack doc: [../skills/enterprise_token_saver_skills_v2/docs/MCP_TOKEN_SAVERS.md](../skills/enterprise_token_saver_skills_v2/docs/MCP_TOKEN_SAVERS.md)
