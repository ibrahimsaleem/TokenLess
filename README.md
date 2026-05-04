# TokenLess

**Token optimization hub** for teams building AI-powered applications: documentation, employee training paths, developer guidelines, system-prompt templates, Markdown **skill packs** for Claude Code and Windsurf, and **TokenWatch** — a zero-dependency Python library for local cost tracking and budgets.

Repository: [github.com/ibrahimsaleem/TokenLess](https://github.com/ibrahimsaleem/TokenLess)

---

## Navigate the repo

| Area | What you get |
|------|----------------|
| [docs/](docs/) | Split guides: concepts, techniques, tool-specific playbooks, MCP, tools, competency, case studies, links |
| [training/](training/) | Three learning levels with exercises |
| [guidelines/](guidelines/) | Non-negotiable dev rules, model selection, context windows, system-prompt patterns, one-page cheat sheet |
| [system-prompts/](system-prompts/) | Annotated starter prompts for common app types |
| [skills/](skills/) | **15** published skills across two packs (v1 + v2 enterprise) |
| [templates/](templates/) | Lean `CLAUDE.md`, `AGENTS.md`, ignore-file starters |
| [scripts/](scripts/) | CLI helpers around TokenWatch + skill installer |
| [tokenwatch.py](tokenwatch.py) | Library + [SKILL.md](SKILL.md) + [manifest.yaml](manifest.yaml) |

Full merged research PDF-source equivalent: [deep-research-report (4).md](deep-research-report%20(4).md)

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

See [SKILL.md](SKILL.md) for full API and provider hooks.

---

## Scripts (CLI)

From repo root, with Python 3.9+:

```bash
python scripts/compare_models.py --in 2000 --out 500 --top 10
python scripts/estimate-cost.py claude-sonnet-4-5-20250929 --in 5000 --out 1000
python scripts/check-context-size.py path/to/prompt.txt
```

**Skill install** (Git Bash / WSL / macOS/Linux) into another project at `.`:

```bash
bash scripts/install-skills.sh /path/to/your/app
```

---

## Published skills (15 total)

| Pack | Folder | Skills |
|------|--------|--------|
| v1 | [skills/token_optimization_skill_pack/](skills/token_optimization_skill_pack/) | 7 — context budget, RAG-first nav, MCP minimizer, compact handoff, small-model router, minimal output contract, project memory curator |
| v2 | [skills/enterprise_token_saver_skills_v2/](skills/enterprise_token_saver_skills_v2/) | 8 — token-optimizer audit, RTK compression, code-review-graph context, MCP token saver, memory slimmer, prompt-cache safe optimization, token-frugal code review, context-ignore curator |

Index and manual install snippets: [skills/README.md](skills/README.md)

---

## Companion open-source repositories

Use alongside counting/monitoring to **remove** structural token waste:

| Repo | Why |
|------|-----|
| [alexgreensh/token-optimizer](https://github.com/alexgreensh/token-optimizer) | Audits bloated project memory, skills, MCP overhead, compaction health |
| [rtk-ai/rtk](https://github.com/rtk-ai/rtk) | Compresses large terminal output before it enters agent context |
| [tirth8205/code-review-graph](https://github.com/tirth8205/code-review-graph) | MCP + local graph for precise, smaller code review context |

---

## License

MIT — see [LICENSE.md](LICENSE.md).

© 2026 Ibrahim Saleem
