<!-- Token note: high-level tool strategy only; actual JSON schemas live in API, not here. -->

You are an autonomous agent for **[TASK_CLASS]**.

## Loop

1. Plan: ≤5 bullets (no tool calls).
2. Act: one tool batch; prefer narrow queries.
3. Stop: when acceptance criteria below are met or you are blocked.

## Tool discipline

- Never request full directories; always use search/pagination parameters.
- After each tool: keep notes ≤120 words in `WORKLOG` style for your own reasoning.

## Acceptance criteria

- **[Criterion 1]**
- **[Criterion 2]**

## Stop conditions

- Max tool rounds: **[M]**. If exceeded, return partial results + `STOPPED_MAX_ROUNDS`.

---

### Design notes (token and quality)

**Why high-level tool strategy, not full schemas.** Tool schemas (JSON structure, parameter names, descriptions) are injected by the API's `tools` parameter — not the system prompt. Duplicating schema details in the system prompt doubles the token cost and creates a synchronization hazard (schema changes in code vs prompt drift). This template keeps only the strategy ("prefer narrow queries", "one tool batch") which is stable across schema changes.

**Stable vs volatile split.** The loop structure, tool discipline, and stop conditions are stable. The acceptance criteria and max rounds are task-specific — either inject them per-task or define a set of standard task templates, each with its own acceptance criteria. If acceptance criteria are stable for a task class (e.g. always: "file exists at output path" + "no error in WORKLOG"), move them into the stable section and cache them.

**Caching implications.** At ~85 tokens, this prompt sits below the caching threshold. For a persistent agent that handles many tasks of the same class, add a domain context block (system architecture, available tools summary, team conventions) to build the stable prefix into the caching range. For ephemeral single-task agents, caching is unlikely to apply — focus on keeping the prompt minimal instead.

**The WORKLOG pattern.** Limiting inline reasoning to 120 words prevents unbounded chain-of-thought accumulation in the context. If the agent requires longer reasoning chains (multi-step architectural planning), increase the WORKLOG limit explicitly and account for the additional tokens in your context budget.

**Max tool rounds as a safety valve.** The `STOPPED_MAX_ROUNDS` response signals the orchestrator that the agent ran out of budget. Handle this in your calling code: log the partial result, alert a human reviewer, and do not retry blindly (which would double the cost). Set `[M]` based on typical task complexity — 5–10 rounds for focused tasks, 20–30 for complex research or multi-file operations.

**When to expand.** For agents that modify persistent state (database writes, file system changes, API calls with side effects), add an explicit "Dry run first" step: generate a plan and confirm with the caller before executing. This prevents expensive rollbacks from incorrect execution.
