# Enterprise Token Saver Skills v2

Markdown skills/rules for Claude Code, Windsurf/Cascade, and cross-agent tools.

This pack focuses on token optimization, not just token counting.

## Included Skills

- `token-optimizer-audit`
- `rtk-command-compression`
- `code-review-graph-context`
- `mcp-token-saver`
- `project-memory-slimmer`
- `prompt-cache-safe-token-optimization`
- `token-frugal-code-review`
- `context-ignore-curator`

## Install: Claude Code

Project-level:

```bash
mkdir -p .claude/skills
cp -R claude-code/.claude/skills/* .claude/skills/
```

Personal/global:

```bash
mkdir -p ~/.claude/skills
cp -R claude-code/.claude/skills/* ~/.claude/skills/
```

## Install: Windsurf

Workspace-level:

```bash
mkdir -p .windsurf/skills
cp -R windsurf/.windsurf/skills/* .windsurf/skills/
cp -R windsurf/.windsurf/rules .windsurf/
cp -R windsurf/.windsurf/workflows .windsurf/
```

Global:

```bash
mkdir -p ~/.codeium/windsurf/skills
cp -R windsurf/.windsurf/skills/* ~/.codeium/windsurf/skills/
```

## Install: Cross-Agent

```bash
mkdir -p .agents/skills
cp -R universal/.agents/skills/* .agents/skills/
```

## External Tools to Consider

- Token Optimizer: https://github.com/alexgreensh/token-optimizer
- RTK: https://github.com/rtk-ai/rtk
- code-review-graph: https://github.com/tirth8205/code-review-graph

## Recommended Stack

For Claude Code power users:
1. Skills from this pack
2. Token Optimizer for audit/compaction/memory health
3. RTK for terminal output compression
4. code-review-graph for graph-guided repo context

For Windsurf users:
1. Skills from this pack
2. `.windsurf/rules/token-frugal-agent-defaults.md`
3. code-review-graph if MCP is approved
4. RTK where hooks are supported

## Important

Do not make root `AGENTS.md`, `CLAUDE.md`, or always-on Windsurf rules huge. Always-on context is the most expensive context.
