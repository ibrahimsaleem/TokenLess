# Lesson: Agent architectures for token efficiency

**Level:** Expert — Level 3  
**Time:** 45 minutes  
**Prerequisites:** [03-dependency-aware-prompting.md](03-dependency-aware-prompting.md)

---

## Learning objectives

By the end of this lesson you will be able to:

1. Describe three multi-agent architecture patterns and their token implications.
2. Design a planner + workers architecture with isolated sub-task contexts.
3. Implement shared instruction deduplication across multiple sub-agents.
4. Place human-in-the-loop checkpoints to prevent expensive rollbacks.
5. Identify the "mega-thread" anti-pattern and refactor it.

---

## Why architecture matters for token cost

In single-agent monolithic sessions, every piece of context — system prompt, tools, full conversation history — accumulates in one thread. When a task runs for 40+ turns covering multiple sub-tasks, the total input tokens per turn grows continuously as history accumulates, even if the current sub-task only needs context from the last 3–5 turns.

Multi-agent architectures can prevent this by isolating sub-task contexts. Each sub-agent session starts fresh (or with a compact handoff) and processes only what it needs. The orchestrating agent holds a high-level view; the sub-agents hold deep context for their specific slice.

---

## Pattern 1: Router model

A small, fast model classifies incoming requests and routes them to the appropriate specialist or tool.

```
User request
      ↓
  Router (small model, 20–50 tokens output)
      ↓ classifies as: codegen | qa | summarize | search
      ↓
  Specialist (mid or large model, appropriate tools and context)
```

**Token implication:** The router call itself is cheap (small model, minimal context). The specialist receives only the tools and system prompt relevant to its task type — not a combined prompt for all task types.

**Implementation note:** The router does not need conversation history. It only needs the current user message and a classification schema. Keep its context minimal by design.

---

## Pattern 2: Planner + workers

A planning model decomposes a large task into sub-tasks. Each sub-task is executed by a separate worker session that receives only the instructions and context for that sub-task.

```
Master task (e.g. "Refactor the payments module")
      ↓
  Planner → sub-task list
      ├── Worker 1: "Extract PaymentService to its own file"
      │     Context: payments/service.py + CLAUDE.md rule for file splits
      ├── Worker 2: "Update imports in all callers"
      │     Context: graph query result (caller files only) + diff from Worker 1
      └── Worker 3: "Write migration notes"
              Context: handoff summary from Workers 1 and 2 + CHANGELOG template
```

**Token implication:** Each worker starts fresh with a compact context (50–200 tokens of instruction + the specific files it needs). The cumulative context per worker is far smaller than a monolithic session that carries all prior turns.

**Key requirement:** Workers must hand off results via compact summaries (not full session exports) to keep the orchestrator's context small.

---

## Pattern 3: Human-in-the-loop checkpoints

For tasks with expensive rollback costs (database migrations, multi-file refactors, deployment steps), insert a human approval step between planning and execution.

```
Planner → plan summary → [HUMAN APPROVAL] → Workers
```

**Token implication:** If the plan is wrong and the agent runs for 30 turns before a human catches it, the wasted tokens and potential rollback cost are significant. A 60-second human review at the plan stage prevents this.

**Implementation:** The planner produces a structured plan (file list, change description, acceptance criteria) and pauses. When the human approves, the workers proceed. This is the `plan-first` strategy referenced in the enterprise skill pack.

---

## Shared instruction deduplication

The most common token waste in multi-agent systems: each sub-agent copies the same system prompt, safety rules, and coding standards into its own context.

**Anti-pattern:**
```
Worker 1 system prompt:
  [2000-token coding standards]
  [500-token safety rules]
  [100-token worker-specific instructions]

Worker 2 system prompt:
  [2000-token coding standards] ← identical copy
  [500-token safety rules]     ← identical copy
  [100-token worker-specific instructions]
```

**Better pattern:** Reference a shared instruction file (CLAUDE.md, AGENTS.md, or a skill file). Each worker's system prompt is minimal — only the worker-specific instructions plus a reference to the shared file:

```python
shared_instructions = load_skill("../../skills/token_optimization_skill_pack/")
worker_instructions = "Apply only to file: payments/service.py. Task: extract PaymentService class."
worker_system_prompt = worker_instructions  # shared_instructions loaded separately as skill
```

If the agent framework supports skills or AGENTS.md files, use those. Do not paste the shared instructions into every sub-agent message.

---

## The mega-thread anti-pattern

**What it is:** A single conversation thread that accumulates context across unrelated tasks because the session was never cleared. Example: a developer uses the same Claude Code session for the morning standup summary, a bug fix, a PR review, and writing a design doc — all without compacting or clearing.

**Token cost:** By the fourth task, the model receives 40 000+ tokens of history mostly irrelevant to the current task. Quality suffers and cost spikes.

**Fix:**
- Use `/compact` between major task boundaries.
- Use `/clear` when moving to a fully different domain.
- Adopt the `compact-handoff` skill from `skills/token_optimization_skill_pack/` to automate the handoff note before clearing.

---

## Failure modes

**Planner produces an over-complex decomposition.** If the planner creates 15 sub-tasks where 4 would suffice, the orchestration overhead (planning calls, handoff notes, coordination) may cost more than a single well-scoped monolithic session. Evaluate decomposition depth empirically.

**Workers re-derive context the planner already computed.** If the planner analyzed the dependency graph and every worker re-runs the same graph query, the savings from decomposition are eroded. Pass planner outputs to workers explicitly in the handoff note.

**Missing human checkpoint on a destructive operation.** An agent deletes or migrates data without a review step. Add a dry-run mode and a confirmation checkpoint to any worker that modifies persistent state.

---

## Acceptance criteria

- [ ] You can draw a planner + workers architecture diagram for a real task in your domain and label the context each component receives.
- [ ] Your sub-agent system prompts do not duplicate shared instructions — they reference a shared file or skill instead.
- [ ] Any destructive operation (file deletion, database change, deployment) has a human checkpoint or a dry-run mode before execution.
- [ ] You have eliminated at least one "mega-thread" pattern from your team's workflow.

---

## Read next

- [05-monitoring-at-scale.md](05-monitoring-at-scale.md)
