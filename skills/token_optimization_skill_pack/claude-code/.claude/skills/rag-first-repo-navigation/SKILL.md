---
name: rag-first-repo-navigation
description: Navigate large codebases with retrieval-first behavior. Use when locating implementation details, dependencies, tests, APIs, or architecture without loading excessive files.
---

# RAG-First Repo Navigation

## Goal
Find the right context using search and structure before reading full content.

## Instructions
Use this order:

1. Identify exact symbols, filenames, routes, configs, test names, or package names from the user's request.
2. Use semantic/code search, grep, file search, or symbol lookup first.
3. Read only the smallest relevant snippets around matches.
4. Build a dependency path: caller -> target -> tests -> config.
5. Read full files only when local snippets are insufficient.
6. Stop searching once enough evidence exists to answer or implement safely.
7. Summarize the discovered context before making changes.

## Retrieval Budget
Default budget:
- 3-5 searches
- 3-7 files maximum
- 100-200 lines per file unless editing requires more

Escalate only if:
- The code path crosses services/packages
- Tests fail and require deeper tracing
- Security or production-impacting behavior is involved

## Output Contract
Return:
- Search terms used
- Relevant files found
- Minimal files read
- Decision or proposed edit
