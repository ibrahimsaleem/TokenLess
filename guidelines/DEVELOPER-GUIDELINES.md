# Developer guidelines — AI applications with LLM APIs

These rules apply to **every** service that calls a hosted LLM with an API key. Each rule includes the definition-of-done criteria and the corresponding PR checklist line item, so they can be enforced during code review without subjective debate.

---

## Rule 1: Instrument before optimizing

**What it means:** Before changing a prompt, a model, or an integration, measure the current token and cost distribution. Optimizations without baselines cannot be validated and tend to be repeated unnecessarily.

**How to implement:**

Log at minimum: model id, input tokens, output tokens, latency (ms), task label (feature name), and optionally session id and tenant id. In development, use `tokenwatch.py` to record to local disk. In production, use the provider's usage API or a proxy layer.

```python
from tokenwatch import TokenWatch
monitor = TokenWatch(storage_path=".tokenwatch")
# After each call:
monitor.record_from_anthropic_response(response, task_label="summarize")
```

**Definition of done:** The feature's average input tokens, output tokens, and cost-per-request appear in the TokenWatch dashboard or an equivalent monitoring view before the PR is merged.

**PR checklist item:** `[ ] Token metrics instrumented and baseline documented in PR description`

---

## Rule 2: Always-on context is expensive

**What it means:** Root `AGENTS.md`, `CLAUDE.md`, global IDE rules, and default system prompts are loaded on every turn. A 4 000-token always-on context costs 4 000 tokens of input on every single request, regardless of whether that request needs the information.

**How to implement:**

- Keep root `CLAUDE.md` and `AGENTS.md` under 120 lines (aim for < 60 lines for most projects).
- Move detailed procedures into skills or internal docs. Reference them with a single line: `"See coding-standards skill for detailed style rules."`
- Run `bash scripts/audit-claude-md.sh` on any PR that modifies `CLAUDE.md`, `AGENTS.md`, or agent configuration files.

**Definition of done:** `CLAUDE.md` and `AGENTS.md` are < 120 lines and pass the audit script with no critical flags.

**PR checklist item:** `[ ] CLAUDE.md / AGENTS.md under 120 lines; audit script run and output attached`

---

## Rule 3: Retrieval beats bulk paste

**What it means:** Attaching entire files, logs, or repositories to a prompt is almost always the wrong choice. Use retrieval — RAG, symbol search, code graph, or server-side search — to inject only the relevant portion.

**How to implement:**

- For document knowledge: configure a RAG pipeline with `top_k ≤ 5` and `max_chars ≤ 8000` hard limits in code.
- For codebase context: use [code-review-graph](https://github.com/tirth8205/code-review-graph) or a similar graph MCP to identify which files are relevant before reading any of them.
- For logs: use a search/filter MCP or CLI command to extract the relevant slice before injecting.

**Definition of done:** No route injects more than 10 000 tokens of retrieved content per request by default. Large injection is only permitted with an explicit override and a documented justification.

**PR checklist item:** `[ ] Retrieved context per request capped at ≤ 10k tokens; RAG top_k and max_chars enforced in code`

---

## Rule 4: Model routing is mandatory

**What it means:** Every service that calls LLM APIs must have a documented routing policy: which task types use which model tier, and what the escalation path is. "Use the best model for everything" is not a routing policy — it is the absence of one.

**How to implement:**

Define a task taxonomy (simple: 3 tiers; complex: as many as your use case needs). Implement routing logic. Document the policy in the service README or in `CLAUDE.md` / `AGENTS.md`. Review the tier mix weekly using TokenWatch task labels.

**Definition of done:** The routing policy is documented, implemented in code, and the tier mix per task type is visible in the monitoring dashboard.

**PR checklist item:** `[ ] Model routing policy documented; task taxonomy defined; routing implemented in code`

**Reference:** [MODEL-SELECTION-GUIDE.md](MODEL-SELECTION-GUIDE.md)

---

## Rule 5: Monitor usage — treat cost regressions as bugs

**What it means:** A 30% increase in average input tokens for a route is a bug, not expected variation. Treat it as one: investigate, find the root cause, and fix or document it explicitly.

**How to implement:**

- Set a budget alert at 80% of the monthly budget expectation in TokenWatch.
- Review the top-5 most expensive task labels weekly.
- When average input tokens for any route increase > 20% week-over-week, open an investigation ticket.

**Telemetry fields to log per request:**

| Field | Why |
|-------|-----|
| `model` | Identifies the tier |
| `input_tokens` | Primary cost driver |
| `output_tokens` | Secondary cost driver (often 3–5× more expensive) |
| `latency_ms` | Correlates with input size |
| `task_label` | Routes monitoring to the right feature |
| `cache_hit` | Validates caching is working |
| `session_id` | For session-level rollups |

**Definition of done:** All mandatory telemetry fields are logged. Budget alert is configured.

**PR checklist item:** `[ ] All telemetry fields present; budget alert configured and tested`

---

## Rule 6: MCP and tools are part of the prompt

**What it means:** Each MCP tool definition consumes context tokens on every request, whether or not the tool is called. An unused MCP server with 8 tools may add 3 000+ tokens of overhead silently.

**How to implement:**

- Disable MCP servers not needed for the current session type.
- Apply the weekly MCP audit checklist from `docs/04-mcp-guide.md`.
- Enforce `top_k`, `max_bytes`, and timeouts on custom MCP tools.
- Keep tool description text under 1 sentence; parameter descriptions under 8 words.

**Definition of done:** Active MCP servers are listed and justified in the session configuration. Custom tools have hard limits in their implementation code.

**PR checklist item:** `[ ] MCP server list reviewed; unused servers disabled; tool descriptions ≤ 1 sentence`

---

## Rule 7: Secrets and PII

**What it means:** Secrets (API keys, passwords, tokens) and personally identifiable information (names, emails, health data, financial data) must not flow through third-party LLM APIs unless contractually permitted.

**How to implement:**

- Add a `.contextignore` (or equivalent) to every project that excludes `.env`, `*.key`, `*.pem`, credential files, and personal data files. Use `templates/.contextignore.template` as a starting point.
- Redact logs before injecting them as model input. Use a PII detection step if operating in a regulated domain.
- Review system prompts for any hardcoded values that should not be exposed (internal URLs, keys, personal names).

**Definition of done:** `.contextignore` exists in the project root. No secrets or PII present in system prompts or injected context in code review.

**PR checklist item:** `[ ] .contextignore present; no secrets or PII in prompts or injected context`

---

## Rule 8: Output caps

**What it means:** `max_tokens` must be set explicitly for every request type. The default (provider maximum) is almost never the right value. Open-ended generation is both a cost risk (verbose completions at 3–5× input rate) and a quality risk (the model continues generating beyond where a concise answer would end).

**How to implement:**

Define `max_tokens` per route based on the expected response shape. Review actual output token distributions after 1 000 requests and adjust.

| Route type | Suggested max_tokens |
|------------|---------------------|
| Classification / routing | 10–20 |
| Extraction (short fields) | 50–150 |
| Summarization | 200–500 |
| Code generation (function) | 500–1 500 |
| Multi-file analysis / review | 1 500–3 000 |

**Definition of done:** Every `client.create` / `client.chat.completions.create` / equivalent call in the codebase has an explicit `max_tokens` value.

**PR checklist item:** `[ ] max_tokens set explicitly for each API call; value justified by expected response shape`

---

## Rule 9: History policy

**What it means:** Every conversational or agentic feature must have a documented and implemented history management strategy. "We don't manage history" is a strategy, but it is the most expensive one and typically not intentional.

**Options:**

- **Sliding window (N turns):** Keep the last N message pairs. Drop older ones. Simple; appropriate for short-session apps.
- **Summarize and continue:** After N turns, summarize accumulated history into a compact block and start fresh. Preserves cross-session context without accumulation.
- **Archive and reference:** Archive session transcripts for retrieval by id; do not keep them in the active context. Suitable for long-lived relationships with sparse reference patterns.

**Definition of done:** The history strategy is documented in the service README or the agent configuration. The implementation is visible in the session management layer.

**PR checklist item:** `[ ] History management strategy documented and implemented; strategy name recorded in README`

---

## Rule 10: Prompt changes are code changes

**What it means:** System prompts, user message templates, and agent instructions are code. They deserve versioning, review, testing, and a changelog.

**How to implement:**

- Store prompts in `prompts/` with version-numbered filenames.
- Include a `PROMPT_CHANGELOG.md` updated with every change (see [SYSTEM-PROMPT-GUIDE.md](SYSTEM-PROMPT-GUIDE.md) Section 6).
- Pair prompt diffs with token delta estimates (`scripts/estimate-cost.py` or `scripts/check-context-size.py`).
- Run a regression test suite (smoke test minimum) before merging any prompt change.

**Definition of done:** Prompt files are versioned in git. PROMPT_CHANGELOG.md is current. Regression test attached to the PR.

**PR checklist item:** `[ ] Prompt versioned; PROMPT_CHANGELOG.md updated; regression test run; token delta documented`

---

## Rule 11: Start new projects from templates

**What it means:** Every new project that uses LLM APIs should start from the lean templates in this repo, not from scratch or from a copy of a larger project's configuration.

**How to implement:**

```bash
# Copy lean starter templates into your project root
cp templates/CLAUDE.md.template ./CLAUDE.md
cp templates/AGENTS.md.template ./AGENTS.md
cp templates/.contextignore.template ./.contextignore
```

Remove only what is inapplicable. Add only what is project-specific. Keep additions minimal.

**Definition of done:** New LLM projects reference the template files in their setup instructions and start from them.

**PR checklist item:** `[ ] New project started from templates/; no extraneous content carried over from copy-paste`

---

## Quick reference

- [QUICK-REFERENCE-CHEATSHEET.md](QUICK-REFERENCE-CHEATSHEET.md) — one-page summary of all rules
- [SYSTEM-PROMPT-GUIDE.md](SYSTEM-PROMPT-GUIDE.md) — detailed prompt engineering guidance
- [MODEL-SELECTION-GUIDE.md](MODEL-SELECTION-GUIDE.md) — tier decision tree with pricing reference
- [CONTEXT-WINDOW-GUIDE.md](CONTEXT-WINDOW-GUIDE.md) — context planning by model and pattern
