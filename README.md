# TokenLess

**Token optimization hub** for teams building AI-powered applications: structured documentation, employee training paths, developer guidelines, system-prompt templates, Markdown skill packs for Claude Code and Windsurf, and **TokenWatch** — a zero-dependency Python library for local cost tracking and budgets.

Repository: [github.com/ibrahimsaleem/TokenLess](https://github.com/ibrahimsaleem/TokenLess)

---

## Who this is for

| Audience | What you get |
|----------|-------------|
| **Software engineers** building LLM features | Training path (Levels 1–3), guidelines with PR checklists, system-prompt templates, TokenWatch integration |
| **Tech leads and staff engineers** | Architecture patterns (Level 3), enterprise rollout plan, case studies with benchmarks, skill pack deployment |
| **New hires on AI teams** | Structured first-week path below, beginner training, cheat sheet, templates to bootstrap a project |
| **Security and compliance reviewers** | DEVELOPER-GUIDELINES Rule 6 (secrets/PII), MCP policy checklist, `.contextignore` template, system-prompt audit |
| **Product managers** | Cost per user-day framing, case study ROI numbers, pilot design guidance in `docs/07-case-studies.md` |

---

## Requirements

- **Python 3.9+** for `tokenwatch.py` and all `scripts/`. No third-party packages required — standard library only.
- **Git Bash, WSL, or macOS/Linux shell** for `scripts/install-skills.sh`.
- **Claude Code, Windsurf, or any MCP-compatible agent** to use the published skill packs.

---

## Suggested first week (new hire onboarding)

If you are new to the team and to token optimization, follow this path:

**Day 1 (60 minutes):**
1. Read [docs/00-OVERVIEW.md](docs/00-OVERVIEW.md) — understand the full picture and navigation.
2. Read [docs/01-core-concepts.md](docs/01-core-concepts.md) — tokens, context windows, billing basics.
3. Open [training/level-1-beginner/01-what-are-tokens.md](training/level-1-beginner/01-what-are-tokens.md) and complete the 2-minute exercise.

**Day 2 (90 minutes):**
4. Complete the remaining Level 1 lessons (`02`, `03`, `04`).
5. Apply the five first-optimizations to one prompt in your current project.
6. Install the skill packs into your project: `bash scripts/install-skills.sh .`

**Day 3–5 (2–3 hours):**
7. Work through [training/level-2-intermediate/](training/level-2-intermediate/) at your own pace.
8. Integrate TokenWatch into one script or route — run `python scripts/compare_models.py --in 2000 --out 500`.
9. Read [guidelines/DEVELOPER-GUIDELINES.md](guidelines/DEVELOPER-GUIDELINES.md) and check your project against the PR checklist items.

**By end of week:**
10. Identify your highest-spend task type and open a ticket to address it.
11. Schedule a 30-minute team token review using the agenda in `training/level-3-expert/05-monitoring-at-scale.md`.

---

## Navigate the repo

| Area | What you get |
|------|----------------|
| [docs/](docs/) | Nine structured guides: concepts, techniques, tool guides, MCP, monitoring, competency, case studies, resources |
| [training/](training/) | Three learning levels with objectives, exercises, misconceptions, and "you know this when…" rubrics |
| [guidelines/](guidelines/) | Non-negotiable dev rules with PR checklists, model selection decision tree, context-window reference, one-page cheat sheet |
| [system-prompts/](system-prompts/) | Five annotated starter prompts for common app types, each with design notes on token tradeoffs |
| [skills/](skills/) | **15** published skills across two packs (v1 and v2 enterprise) for Claude Code, Windsurf, and cross-agent layouts |
| [templates/](templates/) | Lean `CLAUDE.md`, `AGENTS.md`, and ignore-file starters — use these for every new AI project |
| [scripts/](scripts/) | CLI helpers for TokenWatch, context size estimation, model comparison, and one-command skill installation |
| [tokenwatch.py](tokenwatch.py) | The core library — zero-dependency, local-only, MIT licensed |

Full merged research source: [deep-research-report (4).md](deep-research-report%20(4).md)

---

## TokenWatch (library) — quick start

```python
from tokenwatch import TokenWatch

monitor = TokenWatch()
monitor.set_budget(daily_usd=1.0, weekly_usd=5.0, monthly_usd=15.0)
monitor.record_usage(
    model="claude-haiku-4-5-20251001",
    input_tokens=1200,
    output_tokens=400,
    task_label="summarize article",
)
print(monitor.format_dashboard())
```

**Provider helpers** (no manual token extraction required):

```python
# Anthropic
monitor.record_from_anthropic_response(response, task_label="summarize")

# OpenAI
monitor.record_from_openai_response(response, task_label="classify")
```

See [SKILL.md](SKILL.md) for the full API, generic provider pattern, and provider pricing reference.

---

## Scripts (CLI)

From repo root, with Python 3.9+:

```bash
# Compare cost of a typical request across all models in the pricing table
python scripts/compare_models.py --in 2000 --out 500 --top 10

# Estimate monthly cost at a given volume
python scripts/estimate-cost.py claude-sonnet-4-5-20250929 --in 5000 --out 1000

# Rough token estimate for any file (no API call)
python scripts/check-context-size.py path/to/prompt.txt

# Audit agent config files for bloat (Git Bash / WSL / macOS/Linux)
bash scripts/audit-claude-md.sh

# Install both skill packs into another project
bash scripts/install-skills.sh /path/to/your/app
```

---

## Published skills (15 total)

| Pack | Folder | Skills |
|------|--------|--------|
| v1 | [skills/token_optimization_skill_pack/](skills/token_optimization_skill_pack/) | 7 — context budget, RAG-first navigation, MCP minimizer, compact handoff, small-model router, minimal output contract, project memory curator |
| v2 Enterprise | [skills/enterprise_token_saver_skills_v2/](skills/enterprise_token_saver_skills_v2/) | 8 — token-optimizer audit, RTK compression, code-review-graph context, MCP token saver, memory slimmer, prompt-cache safe optimization, token-frugal code review, context-ignore curator |

Full index, manual install snippets, and reading order: [skills/README.md](skills/README.md)

---

## Companion open-source repositories

Use alongside TokenWatch to **remove** structural token waste, not just measure it:

| Repo | What it removes |
|------|-----------------|
| [alexgreensh/token-optimizer](https://github.com/alexgreensh/token-optimizer) | Bloated project memory, skills, MCP overhead, compaction health |
| [rtk-ai/rtk](https://github.com/rtk-ai/rtk) | Noisy terminal output before it enters agent context |
| [tirth8205/code-review-graph](https://github.com/tirth8205/code-review-graph) | Wide repo scans replaced by graph-guided precise context reads |

Pilot guidance: [docs/07-case-studies.md](docs/07-case-studies.md)

---

## License

MIT — see [LICENSE.md](LICENSE.md).

© 2026 Ibrahim Saleem — [github.com/ibrahimsaleem/TokenLess](https://github.com/ibrahimsaleem/TokenLess)
