# Claude Code: token-aware usage

Claude Code is a CLI-first coding agent. Token savings come from **scoping**, **memory hygiene**, and **tool/MCP discipline**.

## CLAUDE.md

- Keep `CLAUDE.md` **short and factual**: build commands, architecture boundaries, forbidden paths, test entrypoints.
- Long playbooks belong in **skills** (`.claude/skills/.../SKILL.md`) loaded on demand—not in always-on files.

## Task scoping

- Prefer **focused tasks** over “fix the whole repo.”
- Use **subagents** for isolated work; each spawn still costs tokens—keep spawn prompts minimal.

## Compaction and clearing

- Use **`/compact`** after a phase; write a **handoff summary** first (see `compact-handoff` skill in `skills/token_optimization_skill_pack`).
- Use **`/clear`** between unrelated tasks to drop stale history.

## Memory

- Prune auto-generated memory if it grows verbose; only a prefix may load each session—still worth curating.

## Tools and MCP

- Disable unused MCP servers in settings.
- Prefer **symbol navigation** and **search** over reading entire files.

## Usage visibility

- Use **`/usage`** (and provider dashboards) to catch runaway sessions.

## Official references

- [Memory](https://code.claude.com/docs/en/usage/memory)
- [Costs](https://code.claude.com/docs/en/costs)

## Repo-specific skills

Copy skills from `skills/token_optimization_skill_pack` and `skills/enterprise_token_saver_skills_v2` into `.claude/skills/` per `skills/README.md`.
