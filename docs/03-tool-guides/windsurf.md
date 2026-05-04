# Windsurf (Cascade): token-aware usage

Cascade combines **retrieval**, **rules**, and **MCP** tools. Token cost scales with how much context and how many tool definitions you load.

## RAG-first behavior

Cascade retrieves relevant snippets instead of sending the entire repo. Help it by:

- Clear module boundaries and naming.
- Keeping generated/vendor trees out of default context (ignore files).

## Plan before execute

Use **plan mode** or ask for an outline first. Fixing a bad plan early avoids wasted file reads and edits.

## Rules and memories

- Put stable facts in **`.windsurfrules`** / project rules (keep them concise; very long rules become always-on cost).
- Use **memories** for durable project notes where the product stores them locally without re-pasting into every prompt (see Windsurf docs for current behavior).

## MCP hygiene

- Each enabled MCP server adds **tool metadata** to context. Disable servers not needed for the task.
- Prefer **CLI tools** (`gh`, cloud CLIs) when they replace large static tool schemas.

## Official references

- [Cascade overview](https://docs.windsurf.com/cascade/overview)
- [Context awareness](https://docs.windsurf.com/fundamentals/context-awareness)

## Repo-specific skills

Install the TokenLess skill packs under `skills/` into `.windsurf/skills/` (see `skills/README.md`).
