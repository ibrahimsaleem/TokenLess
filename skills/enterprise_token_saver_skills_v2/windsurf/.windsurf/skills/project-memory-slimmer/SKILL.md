---
name: project-memory-slimmer
description: Slim down CLAUDE.md, AGENTS.md, MEMORY.md, .windsurf rules, and project README-for-agents files to reduce persistent context while preserving useful instructions.
---

# Project Memory Slimmer

## Purpose
Turn bloated always-on context into concise durable memory and on-demand Skills.

## What Belongs in Always-On Files
Keep only:
- project purpose in 1-2 lines
- build/test commands
- key paths
- security constraints
- coding conventions that apply everywhere
- generated/no-touch paths
- how to run token-saving tools

## What Does Not Belong
Move out:
- long procedures
- detailed tutorials
- historical notes
- repeated README content
- resolved TODOs
- generic advice
- full API docs
- examples that apply only sometimes
- meeting notes
- long prompt templates

## Where to Move Content
- Multi-step procedure -> Skill
- One-shot manual command -> Workflow
- Directory-specific convention -> subdirectory `AGENTS.md`
- Short behavior rule -> `.windsurf/rules`
- Long reference -> supporting file inside a Skill
- External context -> MCP/RAG
- Obsolete context -> delete

## Root File Target
Aim for:
- root `CLAUDE.md`: under 100 lines
- root `AGENTS.md`: under 75 lines
- each `.windsurf/rules/*.md`: under 40 lines
- skill `SKILL.md`: under 200 lines unless it is a rare manual skill

## Output Format
Return:

```md
# Memory Slimming Plan

## Keep Always-On
- ...

## Move to Skills
- ...

## Move to Scoped AGENTS.md
- ...

## Delete
- ...

## New Files to Create
- ...
```
