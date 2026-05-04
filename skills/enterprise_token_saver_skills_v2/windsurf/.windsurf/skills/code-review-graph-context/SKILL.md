---
name: code-review-graph-context
description: Use a local code graph or MCP graph retrieval before reading many files. Use for code review, impact analysis, debugging, architecture mapping, onboarding, and large monorepos.
---

# Code Review Graph Context

## Purpose
Use graph-based retrieval so the agent reads only the files affected by the task.

This skill is for projects using `code-review-graph` or a similar MCP server that builds a local code knowledge graph.

## When to Use
Use before:
- Code reviews
- Pull request review
- Multi-file refactors
- Debugging unknown impact
- Architecture explanation
- Onboarding to a large repo
- Security review of a code path

## First Principle
Do not scan the whole repo. Query the graph for the minimal blast radius.

## Suggested Setup
If the tool is available:

```bash
code-review-graph build
```

If it is not configured:

```bash
pip install code-review-graph
code-review-graph install --platform claude-code
code-review-graph install --platform windsurf
code-review-graph build
```

Use `uvx` or enterprise-approved package managers if required by your organization.

## Graph-First Workflow
1. Identify changed files or target symbols.
2. Query graph impact/blast radius.
3. Read only:
   - changed files
   - direct callers
   - direct dependencies
   - relevant tests
   - security-sensitive config
4. Summarize the graph result before reading files.
5. Expand depth only when evidence shows hidden impact.

## Ignore File
Create `.code-review-graphignore` to exclude tracked noise:

```gitignore
generated/**
*.generated.ts
vendor/**
node_modules/**
dist/**
build/**
coverage/**
*.min.js
*.min.css
```

## Review Output
Return:

```md
# Graph-Guided Review

## Changed / Target Files
- ...

## Blast Radius
- Callers:
- Dependencies:
- Tests:
- Config:

## Files Read
- ...

## Files Intentionally Not Read
- ...

## Findings
1.
2.
3.
```

## Escalation
Read more files only if:
- the graph shows cross-service impact
- tests reference hidden behavior
- security-sensitive auth/data paths are involved
- the graph is stale or incomplete
