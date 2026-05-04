# Scripts

All Python scripts expect Python **3.9+** and run from the TokenLess repo root (or set `PYTHONPATH`).

| Script | Purpose |
|--------|---------|
| [check-context-size.py](check-context-size.py) | Rough token estimate for a text file or stdin |
| [estimate-cost.py](estimate-cost.py) | USD estimate via `TokenWatch.estimate_cost` |
| [compare-models.py](compare-models.py) | Rank models by cost for fixed in/out token shape |
| [audit-claude-md.sh](audit-claude-md.sh) | Warn if `CLAUDE.md` / `AGENTS.md` grow too large |
| [install-skills.sh](install-skills.sh) | Copy both skill packs into a target project |

Shell scripts require **Git Bash**, WSL, or macOS/Linux.
