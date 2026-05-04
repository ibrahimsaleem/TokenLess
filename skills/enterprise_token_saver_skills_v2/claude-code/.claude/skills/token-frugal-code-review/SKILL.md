---
name: token-frugal-code-review
description: Perform a code review with minimal context by using git diff, graph impact, focused file reads, and concise findings.
---

# Token-Frugal Code Review

## Goal
Review code without reading the whole repository.

## Steps
1. Start with changed files:
   ```bash
   git diff --name-only HEAD
   git diff --stat HEAD
   ```
2. If available, query code-review-graph for blast radius.
3. Read only changed files plus direct callers/tests/config.
4. Use snippets, not full files, unless editing requires full context.
5. Group findings by severity.
6. Limit output to actionable items.

## Required Review Areas
- correctness
- security
- test coverage
- error handling
- backward compatibility
- performance risk
- secret leakage
- generated files accidentally changed

## Output Format
```md
# Code Review

## Context Used
- Changed files:
- Additional files read:
- Graph/MCP used:

## Findings
### High
- ...

### Medium
- ...

### Low
- ...

## Tests to Run
- ...

## Token-Saving Notes
- Files not read and why:
```
