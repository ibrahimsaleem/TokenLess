---
name: context-budget-planner
description: Plan a task with a strict context budget before reading files or using tools. Use for large refactors, debugging sessions, repo exploration, architecture reviews, or any task that could require many file reads.
---

# Context Budget Planner

## Goal
Reduce token waste before execution by deciding what context is truly needed.

## Instructions
Before doing the task, create a short context plan:

1. Restate the target outcome in one sentence.
2. List the smallest set of files, symbols, logs, docs, or commands needed.
3. Prefer search, grep, symbols, and dependency paths before reading full files.
4. Do not read entire directories, generated files, lockfiles, build artifacts, vendor folders, or large docs unless absolutely required.
5. If the task can be solved with the current file plus 1-3 related files, stay within that scope.
6. Ask for confirmation only when the task is destructive, security-sensitive, or ambiguous enough to risk wrong changes.
7. After each phase, summarize what is known and what remains unknown in no more than 8 bullets.

## Output Contract
Return:
- Scope
- Minimal context needed
- Files/tools to inspect first
- Files/tools to avoid
- Execution plan

## Anti-patterns
Avoid:
- "I'll inspect the whole repo."
- Opening many files just to understand naming.
- Re-reading files already summarized.
- Long explanations when a concise plan is enough.
