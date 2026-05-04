# TokenLess documentation overview

This repository is a **token optimization hub** for teams building AI-powered applications. It combines:

1. **TokenWatch** (`tokenwatch.py`) — local Python library for recording usage, budgets, model comparison, and dashboards (no extra dependencies).
2. **Documentation** (`docs/`) — structured guides split from the enterprise research report.
3. **Training paths** (`training/`) — beginner, intermediate, and expert curricula with exercises.
4. **Developer guidelines** (`guidelines/`) — rules, system-prompt patterns, model selection, context windows, and a one-page cheat sheet.
5. **System prompt templates** (`system-prompts/`) — copy-paste starting points for common app types.
6. **Skill packs** (`skills/`) — Markdown skills for Claude Code, Windsurf, and cross-agent `.agents` layouts.
7. **Scripts** (`scripts/`) — small helpers around TokenWatch and repo hygiene.
8. **Templates** (`templates/`) — lean `CLAUDE.md`, `AGENTS.md`, and ignore-file starters.

## How to navigate

| You want to… | Start here |
|----------------|------------|
| Understand tokens, billing, and context | [01-core-concepts.md](01-core-concepts.md) |
| Learn optimization patterns (RAG, caching, routing) | [02-optimization-techniques.md](02-optimization-techniques.md) |
| Tune a specific tool (Copilot, Windsurf, Claude Code, APIs) | [03-tool-guides/](03-tool-guides/) |
| MCP policy and token-saving server patterns | [04-mcp-guide.md](04-mcp-guide.md) |
| External tools, monitoring, OSS repos | [05-tools-and-platforms.md](05-tools-and-platforms.md) |
| Define team competency levels | [06-competency-framework.md](06-competency-framework.md) |
| Read case studies | [07-case-studies.md](07-case-studies.md) |
| Official links and communities | [08-resources.md](08-resources.md) |
| Hands-on learning | [../training/README.md](../training/README.md) |
| Non-negotiable engineering rules | [../guidelines/DEVELOPER-GUIDELINES.md](../guidelines/DEVELOPER-GUIDELINES.md) |
| Install agent skills | [../skills/README.md](../skills/README.md) |

## Full consolidated source

The original merged research document is kept at the repository root as `deep-research-report (4).md` for traceability. The numbered files under `docs/` are editorial splits of that material plus cross-links to this repo’s skills and templates.

## External repositories (high impact)

These complement counting/monitoring with **structural** token savings:

- [alexgreensh/token-optimizer](https://github.com/alexgreensh/token-optimizer) — audits memory, compaction, CLAUDE.md bloat, MCP overhead.
- [rtk-ai/rtk](https://github.com/rtk-ai/rtk) — compresses noisy terminal output before it enters agent context.
- [tirth8205/code-review-graph](https://github.com/tirth8205/code-review-graph) — MCP + local code graph for precise, smaller context during review.

Repository: [github.com/ibrahimsaleem/TokenLess](https://github.com/ibrahimsaleem/TokenLess)
