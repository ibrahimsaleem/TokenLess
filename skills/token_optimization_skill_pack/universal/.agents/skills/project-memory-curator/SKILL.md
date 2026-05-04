---
name: project-memory-curator
description: Create or clean project memory files such as CLAUDE.md, AGENTS.md, .windsurf rules, and README-for-agents files so agents get useful context without token bloat.
---

# Project Memory Curator

## Goal
Keep persistent agent instructions short, specific, and high-signal.

## Instructions
When creating or editing memory/rule files:

1. Store only durable facts that apply repeatedly.
2. Remove motivational text, generic best practices, duplicated rules, and outdated notes.
3. Use directory-scoped instructions when possible instead of one huge root file.
4. Keep root-level instructions short because they may be always-on.
5. Move long references, examples, and playbooks into supporting files loaded only when needed.
6. Prefer concrete commands, paths, constraints, and conventions.
7. Add "When to use" guidance so skills/rules activate only when useful.

## Recommended Sections
- Project purpose: 1-2 lines
- Build/test commands
- Key paths
- Architecture map
- Security constraints
- Coding conventions
- Do-not-touch / generated files
- Token-saving instructions

## Anti-patterns
Avoid:
- "Write clean code"
- "Follow best practices"
- Large architecture essays
- Repeating README content
- Full API docs pasted into memory

## Output Contract
Return:
- Proposed file path
- New concise content
- What was removed and why
