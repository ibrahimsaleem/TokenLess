# Case studies and published patterns

> **Disclaimer:** The figures cited below are drawn from third-party community write-ups, vendor documentation, and practitioner reports cited in the TokenLess research corpus. They are self-reported or anecdotal and have not been independently audited. Treat them as directional benchmarks and validate against your own workloads. Your results will vary based on model choice, traffic shape, and baseline quality.

---

## 1. Dependency-aware prompting and graph-guided review

**Pattern:** Combine a short, decision-dense `CLAUDE.md` with a code-graph MCP that answers "which files are in the blast radius of this change?" before the agent reads anything.

**Reported outcome:** Community write-ups describe reductions of **~74%** in tokens per PR review session when replacing naive full-repo scans with graph-targeted file reads. Teams report the same or better answer quality because precision improves — the agent sees the right files, not every file.

**How to replicate:**

1. Install [tirth8205/code-review-graph](https://github.com/tirth8205/code-review-graph) and configure it as an MCP server.
2. Shorten `CLAUDE.md` to real project decisions (target: < 120 lines).
3. Run `scripts/audit-claude-md.sh` to confirm bloat is removed.
4. Measure tokens per PR review for two weeks (baseline) vs two weeks (post-change).

**Files:** `docs/04-mcp-guide.md`, `skills/enterprise_token_saver_skills_v2/docs/MCP_TOKEN_SAVERS.md`

---

## 2. Sub-task decomposition for agentic workflows

**Pattern:** Break a large feature request into explicit sub-tasks (defined in the prompt or in CLAUDE.md), execute each in a fresh session with a compact handoff summary, and assemble the results.

**Reported outcome:** Practitioner reports describe **~91% reduction** in tokens consumed per completed sub-task compared to running a monolithic session that accumulates full context. The mechanism is that each sub-task session starts with only the summary of prior work, not the full conversation history.

**How to replicate:**

1. Install the `compact-handoff` skill from `skills/token_optimization_skill_pack/`.
2. In CLAUDE.md, define sub-task boundaries and the handoff format.
3. At the end of each sub-task, trigger the compact-handoff skill before starting the next.

**Files:** `training/level-3-expert/01-architecture-patterns.md`, `skills/token_optimization_skill_pack/`

---

## 3. Hybrid model routing (cloud + local)

**Pattern:** Route easy steps (classification, extraction, simple summarization) to a small fast model or local model; escalate to frontier API only when multi-step reasoning is needed.

**Reported outcome:** Teams implementing a two-tier routing policy (small model for ~70% of requests) report **30–50% reduction** in cloud API spend without measurable quality regression on the routed tasks.

**How to replicate:**

1. Define task categories and assign each to a model tier (see `guidelines/MODEL-SELECTION-GUIDE.md`).
2. Implement routing in your request dispatcher. See the routing pseudocode in `docs/02-optimization-techniques.md`.
3. Log tier per request. Review mix weekly. Escalation rate above 40% suggests tiering definitions need adjustment.

---

## 4. Prompt caching at scale

**Pattern:** Keep a long static prefix (system prompt + tool definitions + stable reference material) byte-identical across requests. Provider caches the KV computation and bills a fraction of the input rate for cache hits.

**Reported outcome:** Providers document cache-hit savings of **up to 90%** on cached input tokens for high-traffic endpoints where the prefix exceeds ~1 000 tokens and requests arrive within the cache TTL. Savings are proportional to the fraction of input that is stable.

**Caveats:**

- Low-traffic endpoints may not sustain a warm cache. Measure hit rate.
- Any change to the cached prefix — even whitespace — invalidates the cache entry.
- TTLs vary by provider (Anthropic: ~5 minutes; verify current docs).

**How to replicate:**

1. Separate your prompt into a stable prefix and a volatile user section.
2. Review provider documentation for the specific caching API surface and markers.
3. Monitor cache-hit percentage in the usage response metadata.

---

## 5. Terminal output compression with RTK

**Pattern:** Before passing terminal output (test runner logs, build output, shell transcripts) to an agent, run it through [rtk-ai/rtk](https://github.com/rtk-ai/rtk), which strips repetition and noise while preserving actionable signal.

**Reported outcome:** Practitioners report **50–80% character reduction** on verbose tool output (e.g. npm install logs, pytest -v output), which directly reduces tokens when that output is pasted into a session.

**How to replicate:**

1. Install RTK: `pip install rtk` (verify current install method on the repo).
2. Pipe terminal output through RTK before inserting into agent context: `make build 2>&1 | rtk`.
3. Confirm no meaningful signal is lost by spot-checking the compressed output.

---

## 6. CLAUDE.md / AGENTS.md bloat audit (structural)

**Pattern:** Run [alexgreensh/token-optimizer](https://github.com/alexgreensh/token-optimizer) or `scripts/audit-claude-md.sh` against agent configuration files. Common findings: redundant safety rules, generic boilerplate inherited from templates, dead references to deprecated tools.

**Reported outcome:** Teams routinely find **20–40% of their CLAUDE.md content is redundant** on first audit. Removing it does not change agent behaviour but reduces every session's baseline overhead.

**How to replicate:**

1. Run `bash scripts/audit-claude-md.sh` from the repo root of your target project.
2. Review flagged lines. Remove generic boilerplate; keep project-specific decisions.
3. Re-run audit to confirm. Track character count over time.

---

## How to run your own pilot

Pick one pattern, one team, and a four-week window.

**Instrument before you start:**
- Run `scripts/estimate-cost.py` on a sample of representative requests for a baseline cost-per-task.
- Record the average number of files read per PR review or agent session.
- Record tokens per turn in a representative session.

**During the pilot:**
- Apply exactly one change (graph MCP, or RTK, or routing — not all three at once).
- Keep the instrumentation running.

**Retrospective:**
- Compare tokens-per-task and cost-per-task before and after.
- Survey developer satisfaction (did quality drop? Did speed improve?).
- Document findings in a `docs/pilots/YYYY-MM-<name>.md` file.

See the rollout template: [../skills/enterprise_token_saver_skills_v2/docs/ENTERPRISE_ROLLOUT.md](../skills/enterprise_token_saver_skills_v2/docs/ENTERPRISE_ROLLOUT.md).
