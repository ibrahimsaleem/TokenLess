# Token Optimization Skill Pack for Claude Code and Windsurf

This pack contains ready-to-copy Markdown skills for reducing token waste in AI coding workflows.

## What is included

- `context-budget-planner`
- `rag-first-repo-navigation`
- `mcp-tool-minimizer`
- `compact-handoff`
- `small-model-router`
- `minimal-output-contract`
- `project-memory-curator`

## Recommended installation

### Claude Code

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

### Windsurf / Cascade

Workspace-level:

```bash
mkdir -p .windsurf/skills
cp -R windsurf/.windsurf/skills/* .windsurf/skills/
```

Global:

```bash
mkdir -p ~/.codeium/windsurf/skills
cp -R windsurf/.windsurf/skills/* ~/.codeium/windsurf/skills/
```

### Cross-agent option

If your tool supports the open Agent Skills layout:

```bash
mkdir -p .agents/skills
cp -R universal/.agents/skills/* .agents/skills/
```

## Suggested enterprise rollout

1. Start with `context-budget-planner`, `rag-first-repo-navigation`, and `compact-handoff`.
2. Pilot in 2-3 active engineering repos.
3. Ask builders to use `@context-budget-planner` before large tasks.
4. Add the root `AGENTS.md` only after trimming it; root AGENTS.md can become always-on in some tools.
5. Use `.windsurf/rules/token-frugal-defaults.md` only if you want a lightweight always-on policy.
6. Avoid installing duplicate copies in the same workspace unless you know how your tool resolves conflicts.

## Notes

These files are deliberately short. Token optimization skills should not become token waste.
