# Lesson: custom MCP servers

## When to build

You need **deterministic, small** answers where HTTP search or giant static docs would bloat context.

## API design rules

- Pagination, `top_k`, `max_bytes`, timeouts.
- Return **IDs** so the agent can follow up with a second narrow call instead of one megabyte blob.

## Governance

- Approved server list per team.
- Security review for data exfiltration paths.

## Read next

- [03-dependency-aware-prompting.md](03-dependency-aware-prompting.md)  
- Doc: [../../docs/04-mcp-guide.md](../../docs/04-mcp-guide.md)
