---
name: minimal-output-contract
description: Produce concise, structured outputs to avoid verbose completions and repeated clarification loops. Use for API responses, coding plans, code reviews, summaries, PR descriptions, and enterprise reporting.
---

# Minimal Output Contract

## Goal
Reduce output tokens while improving clarity.

## Instructions
Before answering, choose the smallest useful output shape:
- Table for comparison
- Bullets for actions
- JSON/YAML for machine-readable output
- Patch/diff for code changes
- Checklist for procedures
- Short executive summary for managers

## Rules
1. No generic filler.
2. No repeated restatement of the full prompt.
3. No long explanations unless the user asks.
4. Prefer exact action items over background.
5. For code, provide only changed sections unless full file is needed.
6. For JSON, output valid JSON only.
7. For reviews, group findings by severity and file.

## Default Response Limits
- Simple answer: 5 bullets or less
- Plan: 7 steps or less
- Review: top 10 findings only
- Handoff: under 300 words
- API output: strict schema

## Output Contract
State the selected format, then produce it.
