---
name: token-optimizer-audit
description: Audit structural token waste in Claude Code or agentic coding sessions. Use when checking CLAUDE.md, MEMORY.md, skills, MCP servers, compaction health, context quality, prompt cache safety, or session token waste.
---

# Token Optimizer Audit

## Purpose
Find token waste that is not solved by token counting: bloated memory, unused skills, stale rules, duplicate system prompts, broken compaction handoffs, noisy tools, and unnecessary MCP context.

## When to Use
Use this skill before or during:
- Long Claude Code sessions
- Repo onboarding
- Large refactors
- Adding new MCP servers
- Creating or editing `CLAUDE.md`, `AGENTS.md`, `.windsurf/rules`, or Skills
- Investigating high model spend or slow agent behavior

## Operating Rules
1. Do not read the full repo first.
2. Start with configuration and context sources:
   - `CLAUDE.md`
   - `MEMORY.md`
   - `AGENTS.md`
   - `.claude/skills/`
   - `.windsurf/skills/`
   - `.windsurf/rules/`
   - `.mcp.json` or MCP config files
   - `.contextignore`
   - `.code-review-graphignore`
3. Identify always-on content first. Always-on files are the most expensive because they repeat every turn.
4. Move long procedures out of always-on files into Skills.
5. Move directory-specific rules into scoped `AGENTS.md` files.
6. Prefer small skill descriptions and supporting files loaded only when needed.
7. Do not modify existing conversation history or cached prompt prefixes mid-session.
8. If Token Optimizer is installed, use its local audit commands instead of manual guessing.

## Suggested Commands
Run only commands that are safe and available:

```bash
python3 ~/.claude/token-optimizer/skills/token-optimizer/scripts/measure.py memory-review --apply
python3 ~/.claude/token-optimizer/skills/token-optimizer/scripts/measure.py attention-score
python3 ~/.claude/token-optimizer/skills/token-optimizer/scripts/measure.py git-context --json
python3 ~/.claude/token-optimizer/skills/token-optimizer/scripts/measure.py compression-stats --days 30
```

If installed as a plugin, use:

```text
/token-optimizer
/token-coach
```

## Audit Checklist
Score each area as Healthy / Warning / High Waste:

- Root `CLAUDE.md` length and duplication
- Root `AGENTS.md` length and duplication
- Stale memories or unresolved TODOs
- Skills installed but never used
- Multiple skills with overlapping purpose
- MCP servers enabled but unused
- Repeated file reads
- Repeated failed tool calls
- Large command outputs
- Large generated files being read
- Compaction handoffs missing decisions
- Premium model used for simple edits

## Output Format
Return a concise report:

```md
# Token Optimization Audit

## Highest Waste Items
1.
2.
3.

## Safe Fixes Now
- ...

## Move to Skills
- ...

## Move to Scoped Rules / AGENTS.md
- ...

## Ignore / Exclude
- ...

## Tooling Recommendation
- Token Optimizer:
- RTK:
- Code Review Graph:

## Expected Impact
- Low / Medium / High
```
