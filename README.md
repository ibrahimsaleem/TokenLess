# TokenLess

[![Version](https://img.shields.io/badge/version-1.2.3-blue)](https://github.com/ibrahimsaleem/TokenLess/releases)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE.md)
[![Python](https://img.shields.io/badge/python-3.9+-blue)](https://www.python.org/downloads/)
[![Repo](https://img.shields.io/badge/GitHub-TokenLess-181717?logo=github)](https://github.com/ibrahimsaleem/TokenLess)

**Token optimization hub** for teams building AI-powered applications: structured documentation, employee training paths, developer guidelines, system-prompt templates, Markdown skill packs (Claude Code, Windsurf, cross-agent layouts), and **TokenWatch** — a zero-dependency Python library for local cost tracking and budgets.

**Repository:** [github.com/ibrahimsaleem/TokenLess](https://github.com/ibrahimsaleem/TokenLess)

---

## Start here

| I want to… | Go to |
|------------|--------|
| Understand what this repo contains in one pass | [docs/00-OVERVIEW.md](docs/00-OVERVIEW.md) |
| **Run the LiteLLM gateway demo** | [litellm-harness/README.md](litellm-harness/README.md) |
| Follow training with schedule and levels | [training/README.md](training/README.md) |
| Copy rules into engineering practice | [guidelines/DEVELOPER-GUIDELINES.md](guidelines/DEVELOPER-GUIDELINES.md) |
| Drop TokenWatch into code today | [TokenWatch quick start](#tokenwatch-library--quick-start) below → [SKILL.md](SKILL.md) |
| Install agent skills into another project | [skills/README.md](skills/README.md) and `bash scripts/install-skills.sh` |

---

## Who this is for

| Audience | What you get |
|----------|-------------|
| **Software engineers** building LLM features | Training (Levels 1–3), guidelines with PR checklists, system-prompt templates, TokenWatch integration |
| **Tech leads and staff engineers** | Architecture patterns (Level 3), enterprise rollout in skill packs, case studies, skill deployment |
| **New hires on AI teams** | First-week path below, beginner training, cheat sheet, [templates/](templates/) |
| **Security / compliance reviewers** | DEVELOPER-GUIDELINES (secrets/PII), [docs/04-mcp-guide.md](docs/04-mcp-guide.md), [.contextignore.template](templates/.contextignore.template) |
| **Product managers** | Cost framing and pilot design in [docs/07-case-studies.md](docs/07-case-studies.md) |

---

## Repository structure

Everything below lives at the root of this repo unless noted.

```
TokenLess/
├── README.md                 ← You are here — navigation hub
├── LICENSE.md                ← MIT license
├── tokenless-manifest.yaml   ← Pack metadata (skills / hubs — copy to manifest.yaml if required)
├── SKILL.md                  ← TokenWatch as an installable skill + full integration notes
├── tokenwatch.py             ← Core library (no pip deps — standard library only)
│
├── litellm-harness/          ← LiteLLM gateway demo (NEW)
│   ├── app.py                ← Rich terminal chat UI entry point
│   ├── gateway.py            ← LiteLLM orchestration (guardrails → compress → LLM → track)
│   ├── guardrails.py         ← Prompt injection, PII, content policy, size guard
│   ├── compressor.py         ← Heuristic + optional LLMLingua prompt compression
│   ├── token_tracker.py      ← Token counting + cost via LiteLLM + TokenWatch integration
│   ├── proxy_config.yaml     ← LiteLLM proxy server (enterprise gateway mode)
│   ├── requirements.txt      ← litellm, rich, python-dotenv
│   └── README.md             ← Setup and feature docs
│
├── docs/                     ← Reference documentation (read in order for onboarding)
│   ├── 00-OVERVIEW.md
│   ├── 01-core-concepts.md
│   ├── 02-optimization-techniques.md
│   ├── 03-tool-guides/
│   │   ├── api-usage.md      ← HTTP APIs, caching, headers
│   │   ├── claude-code.md
│   │   ├── copilot.md
│   │   ├── ide-extensions.md ← VS Code–family extensions (Cline, Continue, etc.)
│   │   └── windsurf.md
│   ├── 04-mcp-guide.md
│   ├── 05-tools-and-platforms.md
│   ├── 06-competency-framework.md
│   ├── 07-case-studies.md
│   └── 08-resources.md
│
├── training/                 ← Curricula by skill level
│   ├── README.md             ← Suggested weeks + links to levels
│   ├── level-1-beginner/
│   ├── level-2-intermediate/
│   └── level-3-expert/
│
├── guidelines/               ← Rules and decision aids
│   ├── DEVELOPER-GUIDELINES.md
│   ├── SYSTEM-PROMPT-GUIDE.md
│   ├── MODEL-SELECTION-GUIDE.md
│   ├── CONTEXT-WINDOW-GUIDE.md
│   └── QUICK-REFERENCE-CHEATSHEET.md
│
├── system-prompts/           ← Annotated prompt templates + README
├── skills/                   ← 15 skills in two packs — see skills/README.md
│   ├── token_optimization_skill_pack/
│   └── enterprise_token_saver_skills_v2/
│
├── scripts/                  ← CLI wrappers + installers — see scripts/README.md
├── templates/                ← Lean CLAUDE.md, AGENTS.md, ignore starters
│
├── deep-research-report (4).md   ← Original merged research (traceability)
└── context.txt                   ← Source conversation log for skill packs / research (optional read)
```

**Root files worth knowing**

| File | Purpose |
|------|---------|
| `tokenwatch.py` | Import `TokenWatch` in your app or run helpers from `scripts/` |
| `SKILL.md` | Agent-facing skill doc + generic `after_llm_call` pattern for any provider |
| `tokenless-manifest.yaml` | Package metadata for hubs and catalogs; copy to `manifest.yaml` if the target requires that exact filename |
| `deep-research-report (4).md` | Single-file archive of research split across `docs/` |
| `context.txt` | Historical provenance for generated assets — not required reading |

---

## Documentation reading order

Use this sequence for **new hires** or anyone onboarding to token optimization in one sitting:

| Step | Doc | Topic |
|------|-----|--------|
| 1 | [docs/00-OVERVIEW.md](docs/00-OVERVIEW.md) | Hub map, roles, rollout pointers |
| 2 | [docs/01-core-concepts.md](docs/01-core-concepts.md) | Tokens, windows, billing |
| 3 | [docs/02-optimization-techniques.md](docs/02-optimization-techniques.md) | Compression, RAG, routing, sessions |
| 4 | [docs/03-tool-guides/](docs/03-tool-guides/) | Your IDE / API surface |
| 5 | [docs/04-mcp-guide.md](docs/04-mcp-guide.md) | MCP overhead and policy |
| 6 | [docs/05-tools-and-platforms.md](docs/05-tools-and-platforms.md) | Monitoring, OSS helpers |
| 7 | [docs/06-competency-framework.md](docs/06-competency-framework.md) | Skill levels for teams |
| 8 | [docs/07-case-studies.md](docs/07-case-studies.md) | Pilots and reported outcomes |
| 9 | [docs/08-resources.md](docs/08-resources.md) | External links and references |

For **hands-on learning**, pair the docs above with **[training/README.md](training/README.md)** (Week 1 → Level 1, Weeks 2–3 → Level 2 + pilot, Week 4+ → Level 3 / OSS pilots).

---

## Requirements

- **Python 3.9+** for `tokenwatch.py` and `scripts/`. No third-party packages required for the library — standard library only.
- **Git Bash, WSL, or macOS/Linux shell** for `scripts/install-skills.sh` and `scripts/audit-claude-md.sh`.
- **Claude Code, Windsurf, or another MCP-compatible agent** if you use the skill packs as shipped.

---

## Suggested first week (new hire onboarding)

**Day 1 (~60 min):** [docs/00-OVERVIEW.md](docs/00-OVERVIEW.md) → [docs/01-core-concepts.md](docs/01-core-concepts.md) → [training/level-1-beginner/01-what-are-tokens.md](training/level-1-beginner/01-what-are-tokens.md) (exercise).

**Day 2 (~90 min):** Finish Level 1 (`02`–`04`), apply five quick optimizations from [training/level-1-beginner/04-first-optimizations.md](training/level-1-beginner/04-first-optimizations.md), run `bash scripts/install-skills.sh .`.

**Day 3–5 (~2–3 hr):** [training/level-2-intermediate/](training/level-2-intermediate/), integrate TokenWatch into one path, run `python scripts/compare_models.py --in 2000 --out 500`, read [guidelines/DEVELOPER-GUIDELINES.md](guidelines/DEVELOPER-GUIDELINES.md).

**End of week:** Pick a cost driver to fix; schedule a token review using [training/level-3-expert/05-monitoring-at-scale.md](training/level-3-expert/05-monitoring-at-scale.md).

---

## Quick reference: folders at a glance

| Folder | Contents |
|--------|----------|
| [docs/](docs/) | Concepts through resources + IDE/API tool guides |
| [training/](training/) | Lessons L1–L3 with exercises and rubrics — **schedule:** [training/README.md](training/README.md) |
| [guidelines/](guidelines/) | Engineering rules, prompts, models, context, cheat sheet |
| [system-prompts/](system-prompts/) | Five templates + design notes — **index:** [system-prompts/README.md](system-prompts/README.md) |
| [skills/](skills/) | Two packs, 15 skills — **index:** [skills/README.md](skills/README.md) |
| [scripts/](scripts/) | Cost/compare/context helpers — **index:** [scripts/README.md](scripts/README.md) |
| [templates/](templates/) | Starter `CLAUDE.md`, `AGENTS.md`, ignore files |

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

**Provider helpers** (token counts taken from the response object):

```python
monitor.record_from_anthropic_response(response, task_label="summarize")
monitor.record_from_openai_response(response, task_label="classify")
```

Full API, pricing table notes, and generic usage extraction: **[SKILL.md](SKILL.md)**.

---

## Scripts (CLI)

From repo root with Python 3.9+:

```bash
python scripts/compare_models.py --in 2000 --out 500 --top 10
python scripts/estimate-cost.py claude-sonnet-4-5-20250929 --in 5000 --out 1000
python scripts/check-context-size.py path/to/prompt.txt
bash scripts/audit-claude-md.sh
bash scripts/install-skills.sh /path/to/your/app
```

Details: [scripts/README.md](scripts/README.md).

---

## Published skills (15 total)

| Pack | Location |
|------|----------|
| v1 — Token optimization | [skills/token_optimization_skill_pack/](skills/token_optimization_skill_pack/) |
| v2 — Enterprise token saver | [skills/enterprise_token_saver_skills_v2/](skills/enterprise_token_saver_skills_v2/) |

Indexed list and install paths: **[skills/README.md](skills/README.md)**.

---

## Companion open-source repositories

| Repo | Role |
|------|------|
| [alexgreensh/token-optimizer](https://github.com/alexgreensh/token-optimizer) | Structural audit: memory, skills, MCP bloat |
| [rtk-ai/rtk](https://github.com/rtk-ai/rtk) | Compress noisy terminal output |
| [tirth8205/code-review-graph](https://github.com/tirth8205/code-review-graph) | Graph-guided code context |

Pilot ideas: [docs/07-case-studies.md](docs/07-case-studies.md).

---

## Contributing and customizing

This repo is maintained as an **internal handbook + library** you can fork or vendor. When you change prompts or agent config:

- Follow [guidelines/SYSTEM-PROMPT-GUIDE.md](guidelines/SYSTEM-PROMPT-GUIDE.md) (versioning + regression checks).
- Prefer starting new projects from [templates/](templates/).

---

## License

MIT — see [LICENSE.md](LICENSE.md).

© 2026 Ibrahim Saleem — [github.com/ibrahimsaleem/TokenLess](https://github.com/ibrahimsaleem/TokenLess)
