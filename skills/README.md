# Published skill packs (Markdown)

Two packs ship in this repository. Skills are **short** `SKILL.md` files (often with YAML frontmatter) so agents load them **on demand** instead of bloating always-on context.

## Pack v1 — `token_optimization_skill_pack/`

Foundational habits for any repo using Claude Code, Windsurf, or cross-agent `.agents` layouts.

| Skill | Purpose |
|-------|---------|
| `context-budget-planner` | Plan minimum context before reads/tools. |
| `rag-first-repo-navigation` | Search / symbols / grep before whole-file reads. |
| `mcp-tool-minimizer` | Avoid unnecessary MCP breadth. |
| `compact-handoff` | Short summaries before `/compact`, `/clear`, or task switches. |
| `small-model-router` | Route trivial work to smaller / cheaper models. |
| `minimal-output-contract` | Enforce compact response shapes. |
| `project-memory-curator` | Keep `CLAUDE.md`, `AGENTS.md`, rules, and memory lean. |

Paths:

- Claude Code: `token_optimization_skill_pack/claude-code/.claude/skills/<skill>/SKILL.md`
- Windsurf: `token_optimization_skill_pack/windsurf/.windsurf/skills/<skill>/SKILL.md`
- Universal: `token_optimization_skill_pack/universal/.agents/skills/<skill>/SKILL.md`
- Rules / workflow: `token_optimization_skill_pack/windsurf/.windsurf/rules/`, `.../workflows/`

## Pack v2 — `enterprise_token_saver_skills_v2/`

Adds integrations aligned with high-impact OSS tools (see [docs/05-tools-and-platforms.md](../docs/05-tools-and-platforms.md)).

| Skill | Purpose |
|-------|---------|
| `token-optimizer-audit` | Structural audit mindset (memory, skills, MCP, compaction). |
| `rtk-command-compression` | Shrink noisy terminal output before it hits context. |
| `code-review-graph-context` | Graph-first navigation for review / blast radius. |
| `mcp-token-saver` | MCP hygiene patterns. |
| `project-memory-slimmer` | Aggressive pruning guidance for project memory files. |
| `prompt-cache-safe-token-optimization` | Safer static-prefix patterns for caching. |
| `token-frugal-code-review` | Review with minimal context. |
| `context-ignore-curator` | Ignore / exclude paths that should never enter context. |

Paths mirror v1 under `enterprise_token_saver_skills_v2/claude-code/`, `.../windsurf/`, `.../universal/`, plus `docs/` and `examples/`.

## One-command install

From a **Git Bash** shell (or Linux/macOS), at your **application repo root**:

```bash
bash /path/to/TokenLess/scripts/install-skills.sh .
```

Or clone TokenLess beside your app and use a relative path. The script copies **both** packs into `.claude/skills`, `.windsurf/skills`, `.windsurf/rules`, `.windsurf/workflows`, and `.agents/skills` without deleting unrelated files.

## Manual install snippets

### Claude Code (project)

```bash
mkdir -p .claude/skills
cp -R /path/to/TokenLess/skills/enterprise_token_saver_skills_v2/claude-code/.claude/skills/* .claude/skills/
cp -R /path/to/TokenLess/skills/token_optimization_skill_pack/claude-code/.claude/skills/* .claude/skills/
```

### Windsurf (workspace)

```bash
mkdir -p .windsurf/skills .windsurf/rules .windsurf/workflows
cp -R /path/to/TokenLess/skills/enterprise_token_saver_skills_v2/windsurf/.windsurf/skills/* .windsurf/skills/
cp -R /path/to/TokenLess/skills/token_optimization_skill_pack/windsurf/.windsurf/skills/* .windsurf/skills/
cp -R /path/to/TokenLess/skills/enterprise_token_saver_skills_v2/windsurf/.windsurf/rules/* .windsurf/rules/ 2>/dev/null || true
cp -R /path/to/TokenLess/skills/enterprise_token_saver_skills_v2/windsurf/.windsurf/workflows/* .windsurf/workflows/ 2>/dev/null || true
```

### Cross-agent `.agents`

```bash
mkdir -p .agents/skills
cp -R /path/to/TokenLess/skills/enterprise_token_saver_skills_v2/universal/.agents/skills/* .agents/skills/
cp -R /path/to/TokenLess/skills/token_optimization_skill_pack/universal/.agents/skills/* .agents/skills/
```

## Companion OSS repositories

- https://github.com/alexgreensh/token-optimizer  
- https://github.com/rtk-ai/rtk  
- https://github.com/tirth8205/code-review-graph  

## Enterprise rollout

See `enterprise_token_saver_skills_v2/docs/ENTERPRISE_ROLLOUT.md`.
