# Lesson: Dependency-aware prompting

**Level:** Expert — Level 3  
**Time:** 35 minutes  
**Prerequisites:** [02-custom-mcp-servers.md](02-custom-mcp-servers.md)

---

## Learning objectives

By the end of this lesson you will be able to:

1. Explain why dependency-aware prompting reduces tokens without reducing quality.
2. Configure a code-review-graph MCP server for a real repository.
3. Write a `CLAUDE.md` or `AGENTS.md` that uses graph context instead of full-repo instructions.
4. Measure the token reduction vs baseline (naive full-repo scan) for a PR review task.
5. Identify when graph context is insufficient and what to fall back to.

---

## The core idea

When an agent receives a task involving a codebase (bug fix, PR review, refactor), its instinct is to read broadly — exploring the repo tree, opening many files to understand context. This produces accurate results but at high token cost.

**Dependency-aware prompting** provides the agent with **structure** instead of content: a graph of which modules depend on which, which files are in the "blast radius" of a proposed change, and which tests cover those files. The agent can then make targeted reads of the 3–5 files that matter, instead of scanning 30–50.

---

## What the graph provides

A code dependency graph can answer questions like:

- "Which files import `auth/service.py`?" → scope for a change to that file.
- "What does `payments/processor.py` depend on?" → what to read before modifying it.
- "Which tests cover `api/routes/orders.py`?" → what to run to validate a change.
- "What is the blast radius of renaming `UserModel` to `User`?" → how many files need updating.

This information replaces the need to open and read each file. The agent queries the graph and gets a precise list, then reads only the files on that list.

---

## Setting up code-review-graph

Install the [tirth8205/code-review-graph](https://github.com/tirth8205/code-review-graph) server and register it as an MCP server:

```json
// .claude/mcp-servers.json (or equivalent for your agent)
{
  "mcpServers": {
    "code-graph": {
      "command": "python",
      "args": ["-m", "code_review_graph.server"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

Run the indexing step (typically a one-time operation per project, refreshed in CI):

```bash
python -m code_review_graph.index --root . --output .code-graph/
```

Verify the index by querying a known module:

```bash
python -m code_review_graph.cli dependents auth/service.py
```

Expected output: list of files that import `auth/service.py`. If this is accurate, the graph is ready.

---

## Writing the graph-aware CLAUDE.md

A naive `CLAUDE.md` says "read the auth module carefully when working on anything security-related." This prompts broad reads.

A graph-aware `CLAUDE.md` says:

```markdown
## Code navigation

Before reading any source file, query the code-graph MCP tool to identify:
- Direct dependents of the file you plan to change
- Test files covering those dependents

Read only the files returned by the graph query plus the target file itself.
Do not read the full repository tree or open files speculatively.

### Blast radius query
graph_tool.dependents(target_file) → files to review for impact
graph_tool.tests_for(target_file) → tests to run after the change
```

This explicit instruction replaces several thousand tokens of "read these directories" guidance with a 200-token policy that triggers dynamic, targeted reads.

---

## CI-generated ARCHITECTURE.md (lightweight alternative)

If installing an MCP server is not feasible, a CI-generated `ARCHITECTURE.md` provides a lighter version of the same idea:

```bash
# .github/workflows/update-architecture.yml
# Run after any merge to main
- name: Generate architecture summary
  run: python scripts/generate_architecture_md.py > ARCHITECTURE.md
```

The generated file contains short bullets per module: dependencies, size, team owner, and test coverage percentage. This is injected into context once per session (as a stable cacheable prefix) rather than the agent reading every file.

**Tradeoff:** Static architecture file vs dynamic graph query. The static file is simpler to set up; the dynamic graph is more precise because it answers the specific question for the specific file being changed.

---

## Measurement

**Baseline measurement:** Run 5 representative PR review sessions with full-repo access (no graph), record input tokens per session.

**Post-change measurement:** Run the same 5 sessions with graph MCP enabled and graph-aware `CLAUDE.md`, record input tokens per session.

**Expected result (based on community reports):** 50–75% reduction in input tokens per PR review session for repos with 200+ files. Quality should be equal or better because the agent reads the right files rather than many files.

**What to check if results are disappointing:**
- Confirm the graph index covers the changed files.
- Check whether the agent followed the graph-query instruction or fell back to broad reads.
- Verify the `CLAUDE.md` instruction is early and unambiguous.

---

## When graph context is insufficient

The graph approach works well for: file-level dependency queries, test coverage mapping, blast radius analysis.

It is insufficient for: understanding the internal logic of a function (you still need to read the file), resolving ambiguous type hierarchies that span multiple levels of indirection, or tasks that require reading prose documentation rather than code.

In these cases: use the graph to select the minimum set of files to read, then read them fully. The graph narrows the read set; it does not eliminate reading.

---

## Acceptance criteria

- [ ] Graph index is built for your target repository and covers at least 90% of source files.
- [ ] `CLAUDE.md` or `AGENTS.md` instructs the agent to query the graph before reading files.
- [ ] You have measured input token reduction vs baseline on at least 3 representative sessions.
- [ ] You can explain when graph context is sufficient vs when a full file read is still required.

---

## Read next

- [04-agent-architectures.md](04-agent-architectures.md)
- Case study: [../../docs/07-case-studies.md](../../docs/07-case-studies.md) — dependency-aware prompting section
