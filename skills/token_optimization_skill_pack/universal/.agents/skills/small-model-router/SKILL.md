---
name: small-model-router
description: Choose the cheapest capable model or subagent for a task. Use when deciding between Haiku, Sonnet, Opus, GPT-4-class models, small local models, or subagents.
---

# Small Model Router

## Goal
Route work to the smallest model or agent that can complete it safely.

## Instructions
Classify the task:

### Small / Cheap Model
Use for:
- Formatting
- Simple code edits
- Test generation from clear patterns
- Commit messages
- Short summaries
- Lint/error explanation
- File discovery and read-only exploration

### Mid Model
Use for:
- Multi-file code changes
- Debugging with uncertain root cause
- Security review of a limited code path
- API design with known requirements

### Large / Premium Model
Use only for:
- Architecture decisions
- Novel security threat modeling
- Complex agent planning
- Ambiguous production-risk changes
- Cross-system reasoning

## Subagent Rule
Use a read-only subagent for exploration whenever possible. Keep implementation in the main session after the subagent returns a concise summary.

## Output Contract
Return:
- Task tier
- Recommended model/agent
- Why the cheaper option is sufficient or not
- Token-saving constraint for execution
