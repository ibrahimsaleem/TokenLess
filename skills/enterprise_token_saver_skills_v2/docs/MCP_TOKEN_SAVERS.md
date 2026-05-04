# MCP Token-Saving Servers and Patterns

## Recommended token-saving MCP categories

1. Code graph / AST graph MCP
   - Purpose: answer "what files matter?" before the agent reads files.
   - Example tool: code-review-graph.

2. Documentation retrieval MCP
   - Purpose: retrieve top-k relevant doc chunks instead of pasting full docs.

3. Memory MCP
   - Purpose: short durable summaries with TTL, not unlimited conversation dumps.

4. Issue/PR MCP
   - Purpose: fetch one ticket, PR, or comment thread by ID.

5. Log/search MCP
   - Purpose: retrieve filtered log slices, not full logs.

## MCP policy

- Disable MCP servers not needed for the current project.
- Prefer project-scoped MCP config over global config.
- Require query limits, top-k, max chars, and filters.
- Summarize tool results before continuing.
- Do not expose secrets through MCP queries.
