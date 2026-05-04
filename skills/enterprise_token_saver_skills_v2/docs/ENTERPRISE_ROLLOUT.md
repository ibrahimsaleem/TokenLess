# Enterprise Rollout Plan

## Phase 1: Pilot
- 5-10 AI builders.
- Install skills only, no hooks.
- Measure subjective quality, speed, and repeated-context reduction.

## Phase 2: Tooling
- Add Token Optimizer for Claude Code users.
- Add RTK for terminal-heavy users.
- Add code-review-graph for large repos and code reviewers.

## Phase 3: Policy
- Standard root `CLAUDE.md` and `AGENTS.md` templates.
- Standard ignore files.
- Approved MCP server list.
- Model routing guidance.

## Phase 4: Metrics
Track:
- average files read per task
- repeated file reads
- command output size
- compaction frequency
- model tier usage
- subagent cost share
- number of active MCP servers
- time-to-complete review/refactor tasks
