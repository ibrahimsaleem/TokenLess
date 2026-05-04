# TokenLess documentation overview

This repository is a **token optimization hub** for every team building AI-powered applications with LLM APIs. It combines a working Python library, structured educational docs, training curricula, developer guidelines, system-prompt templates, ready-to-use agent skills, helper scripts, and lean project templates — all open-source (MIT).

---

## What is here and why it matters

Token cost and context quality are the two levers engineers most often ignore until something breaks or a bill surprises finance. This hub closes that gap with material you can actually use in a sprint:

1. **TokenWatch** (`tokenwatch.py`) — zero-dependency Python library. Records every API call, calculates cost from a pricing table, enforces budgets, compares models, and renders a terminal dashboard. No sign-up, no cloud sync.
2. **Docs** (`docs/`) — Nine structured guides split from enterprise research. Each covers one topic deeply enough to inform a decision or a PR review.
3. **Training paths** (`training/`) — Three levels: beginner (concepts), intermediate (applied), expert (architecture). Each lesson has objectives, exercises, and a "you know this when…" rubric.
4. **Developer guidelines** (`guidelines/`) — Non-negotiable engineering rules with PR checklist items, a model selection decision tree, a context-window reference, and a one-page cheat sheet.
5. **System prompt templates** (`system-prompts/`) — Five annotated starters for common AI app patterns, each with design notes explaining the token tradeoffs made.
6. **Skill packs** (`skills/`) — Fifteen Markdown SKILL.md files for Claude Code, Windsurf, and cross-agent `.agents` layouts. Copy them into any project in under a minute.
7. **Scripts** (`scripts/`) — CLI wrappers around TokenWatch functions, a Claude.md bloat auditor, and a one-command skill installer.
8. **Templates** (`templates/`) — Lean `CLAUDE.md`, `AGENTS.md`, `.contextignore`, and code-review graph ignore files ready to paste into a new project.

---

## How to navigate

| I want to… | Start here |
|------------|------------|
| Understand tokens, context windows, and billing | [01-core-concepts.md](01-core-concepts.md) |
| Learn reduction patterns (RAG, caching, routing) | [02-optimization-techniques.md](02-optimization-techniques.md) |
| Tune Copilot, Windsurf, Claude Code, or API apps | [03-tool-guides/](03-tool-guides/) |
| Understand and govern MCP server footprint | [04-mcp-guide.md](04-mcp-guide.md) |
| Pick monitoring tools; understand OSS helpers | [05-tools-and-platforms.md](05-tools-and-platforms.md) |
| Define skill levels for my team | [06-competency-framework.md](06-competency-framework.md) |
| Read case studies with real numbers | [07-case-studies.md](07-case-studies.md) |
| Get all official docs and community links | [08-resources.md](08-resources.md) |
| Do hands-on learning with exercises | [../training/README.md](../training/README.md) |
| Apply non-negotiable engineering rules | [../guidelines/DEVELOPER-GUIDELINES.md](../guidelines/DEVELOPER-GUIDELINES.md) |
| Install agent skills into a project | [../skills/README.md](../skills/README.md) |

---

## Onboarding paths by role

### Software engineer building LLM features

**Week 1:** Read `01-core-concepts.md`, `02-optimization-techniques.md`, and the tool guide for your IDE or CLI. Apply the cheat sheet in your next PR.

**Week 2:** Read `06-competency-framework.md`. Run `scripts/compare_models.py` against your typical token shapes. Instrument one route with TokenWatch. Install the v1 skill pack.

**Week 3:** Read `04-mcp-guide.md`. Audit CLAUDE.md / AGENTS.md with `scripts/audit-claude-md.sh`. Open `training/level-2-intermediate/` and complete at least one exercise.

### Tech lead or staff engineer

Read everything above, then: `07-case-studies.md` for pilot framing, `skills/enterprise_token_saver_skills_v2/docs/ENTERPRISE_ROLLOUT.md` for a phased plan, and `training/level-3-expert/` for architecture patterns.

### Security or compliance reviewer

Start with `guidelines/DEVELOPER-GUIDELINES.md` (rule 6: Secrets and PII), `04-mcp-guide.md` (policy checklist), `system-prompts/` (what hard rules are in each template), and `templates/.contextignore.template`.

---

## 30 / 60 / 90 day rollout

| Phase | Milestone | Resources |
|-------|-----------|-----------|
| Day 1–30 | Skills installed, cheat sheet adopted, CLAUDE.md / AGENTS.md pass audit | `skills/README.md`, `scripts/audit-claude-md.sh`, `guidelines/QUICK-REFERENCE-CHEATSHEET.md` |
| Day 31–60 | One route instrumented with TokenWatch, model routing policy documented | `training/level-2-intermediate/05-tokenwatch-integration.md`, `guidelines/MODEL-SELECTION-GUIDE.md` |
| Day 61–90 | Pilot one OSS tool (graph, RTK, or token-optimizer), metrics baseline set | `docs/07-case-studies.md`, `enterprise_token_saver_skills_v2/docs/ENTERPRISE_ROLLOUT.md` |

---

## External repositories (structural token savers)

| Repo | What it removes |
|------|-----------------|
| [alexgreensh/token-optimizer](https://github.com/alexgreensh/token-optimizer) | Bloated project memory, compaction health, MCP overhead |
| [rtk-ai/rtk](https://github.com/rtk-ai/rtk) | Noisy terminal output before it hits agent context |
| [tirth8205/code-review-graph](https://github.com/tirth8205/code-review-graph) | Wide repo scans replaced by graph-guided precise reads |

---

Source: [github.com/ibrahimsaleem/TokenLess](https://github.com/ibrahimsaleem/TokenLess)
