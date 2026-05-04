# Lesson: agent architectures

## Patterns

- **Router model** (small) chooses tool and specialist.
- **Planner + workers** with isolated contexts instead of one mega-thread.
- **Human-in-the-loop** checkpoints to avoid expensive rollbacks.

## Failure mode

Too many subagents each re-loading the same system prompt—**deduplicate** shared instructions via files/skills, not copy-paste.

## Read next

- [05-monitoring-at-scale.md](05-monitoring-at-scale.md)
