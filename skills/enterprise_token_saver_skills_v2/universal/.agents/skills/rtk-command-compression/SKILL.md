---
name: rtk-command-compression
description: Use RTK-style command output compression to reduce noisy Bash/terminal output before it enters agent context. Use for git, tests, grep, tree, ls, docker, package managers, logs, and build commands.
---

# RTK Command Compression

## Purpose
Prevent terminal output from flooding the LLM context.

RTK-style compression is useful because many coding agents waste tokens on command output from:
- `tree`
- `ls`
- `cat`
- `grep` / `rg`
- `git status`
- `git diff`
- `git log`
- `npm test`
- `pytest`
- `cargo test`
- `docker ps`
- build logs
- linter output

## Core Rule
Before running a command, ask:

> Do I need the full output, or only the actionable summary?

Prefer summarized output unless the exact lines are needed for a code edit.

## If RTK Is Installed
Use RTK or rely on the installed hook:

```bash
rtk git status
rtk git diff
rtk pytest
rtk npm test
rtk tree
rtk rg "pattern"
```

If the hook is installed, ordinary commands may be rewritten automatically. Still keep commands targeted.

## If RTK Is Not Installed
Use native shell compression:

```bash
git status --short
git diff --stat
git diff --name-only
git log --oneline -20
rg "pattern" --line-number --context 2
find . -maxdepth 3 -type f | head -100
pytest -q
npm test -- --runInBand
```

## Do Not Do This
Avoid:
- `cat` on large files
- `tree` from repo root without depth
- full CI logs unless needed
- dumping generated files
- reading lockfiles unless dependency resolution is the issue
- repeating failed commands without changing the approach

## Command Selection Table

| Need | Prefer | Avoid |
|---|---|---|
| What changed? | `git diff --name-only` then targeted `git diff path` | full repo diff |
| Test failure | `pytest -q` then one failing test verbose | full test log |
| Find code | `rg pattern --context 2` | opening many files |
| Project map | `find . -maxdepth 3` or code graph | full `tree` |
| Docker status | `docker ps --format` | verbose inspect |

## Output Format
After commands, return:

```md
## Command Summary
- Command:
- Useful result:
- Noise removed:
- Next targeted command:
```
