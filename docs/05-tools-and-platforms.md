# Tools, monitoring, and open-source helpers

A note on scope: this guide covers tools for **local development and team governance**. It is not an exhaustive SaaS comparison — vendors change pricing and features frequently. Use these descriptions as a starting point and verify with each provider's current documentation.

---

## Token counting and local estimation

| Tool | What it does | When to use it |
|------|-------------|----------------|
| `tokenwatch.py` (this repo) | Local cost tracking, budgets, model comparison, dashboard | During development; CI checks; zero-cloud-data requirement |
| tiktoken | OpenAI BPE tokenizer; exact counts for GPT-family | Pre-call estimation for OpenAI endpoints |
| Anthropic SDK `count_tokens` | Exact count for Claude-shaped requests | Pre-call estimation for Anthropic endpoints |
| `scripts/check-context-size.py` | Rough character-to-token approximation, no API call | Quick check before pasting into a prompt |

### When a rough estimate is enough

Character count ÷ 3.5 gives a reasonable approximation for English prose with common LLMs. Use this when you want a quick sanity check without installing a tokenizer.

---

## Usage and cost monitoring — selection matrix

| Need | Local, zero-data | Cloud observability | CI gate |
|------|-----------------|--------------------|---------| 
| Per-call cost tracking | **TokenWatch** | Helicone, LangSmith | TokenWatch budget assertion |
| Multi-provider unified view | LiteLLM proxy | Helicone, OpenMeter | — |
| Prompt regression testing | PromptFoo (local) | PromptLayer, HumanLoop | PromptFoo CI mode |
| Authoritative billing | — | Anthropic Console, OpenAI Usage | — |
| Experiment A/B traces | — | LangSmith, Braintrust | — |

### TokenWatch vs SaaS monitoring

| Aspect | TokenWatch (local) | Helicone / LangSmith (cloud) |
|--------|-------------------|-----------------------------|
| Setup | pip install + one import | API key + SDK wrapper |
| Data leaves your infra | No | Yes |
| Real-time dashboard | Terminal / file | Web UI with history |
| Team aggregation | Manual (export JSON) | Built-in |
| Pricing / context comparison | Built-in | Varies |
| Free tier | Unlimited (MIT) | Typically limited |

**Recommendation:** Use TokenWatch locally during development and in CI. If your team needs aggregated dashboards across many engineers, introduce a cloud layer in a second phase.

---

## Proxy and privacy considerations

Several monitoring tools work as HTTP proxies sitting between your application and the LLM provider:

- **Benefit:** Capture every request and response without changing your application code.
- **Risk:** Every prompt, completion, and tool result passes through the proxy operator's infrastructure. Evaluate against your organization's data classification policy before enabling for production workloads involving customer data, PII, or regulated content.
- **Self-hosted proxies** (e.g. LiteLLM, Portkey in self-hosted mode): Resolve the data residency concern but add operational complexity.

If in doubt, start with local instrumentation (TokenWatch) and escalate to a proxy only when the observability gap is demonstrably costing optimization decisions.

---

## Prompt engineering and evaluation tools

- **LangChain** — chains, prompt templates, and some caching utilities. Pair with an observability layer for production.
- **DSPy** — programmatic prompt optimization. Best suited for research-grade systematic evaluation, not ad-hoc iteration.
- **PromptFoo** — open-source CLI for prompt regression testing. Supports CI runs.
- **HumanLoop** — collaborative prompt versioning and evaluation. SaaS.

---

## Open-source token optimization repositories

These go beyond counting tokens to **removing structural waste** from AI workflows:

### alexgreensh/token-optimizer

**Role:** Structural audit tool for Claude Code workflows. Scans CLAUDE.md, project memory, skills, and MCP configuration for common bloat patterns, runs compaction health checks, and reports on MCP overhead.

**When to pilot:** When `scripts/audit-claude-md.sh` flags file size concerns or when a team reports unexpectedly high tokens per agent session.

**Golden signals to check after adoption:** tokens per agent turn (before vs after audit), MCP server count, CLAUDE.md character count.

### rtk-ai/rtk

**Role:** Compresses noisy terminal output before it is inserted into agent context. Common sources of noise: test runner verbose output, `npm install` dependency trees, compiler warnings repeated across many files.

**When to pilot:** When your team frequently pastes terminal output into an agent session and the output is long.

**Golden signals:** Average characters of terminal output injected per turn; reduction ratio reported by RTK.

### tirth8205/code-review-graph

**Role:** Builds a dependency graph of the repository and exposes it via MCP, so an agent can query "which files are in the blast radius of this change?" instead of reading the full repository tree.

**When to pilot:** On large repos (>500 files) where PR review sessions reliably hit context ceiling.

**Golden signals:** Files read per PR review (before vs after graph MCP); context tokens per PR review.

---

## Golden signals dashboard

After instrumenting with TokenWatch, these are the five metrics to track consistently:

1. **Average input tokens per request** by route/endpoint.
2. **Average output tokens per request** by route/endpoint.
3. **Cost per active user-day** (daily spend ÷ unique users).
4. **Budget breach rate** (percentage of requests that exceed your configured per-request limit).
5. **Model tier mix** (percentage of calls going to each tier).

Record these weekly during development. Set a target line and treat regressions as bugs.

---

## Further reading

- [../training/level-2-intermediate/05-tokenwatch-integration.md](../training/level-2-intermediate/05-tokenwatch-integration.md) — hands-on TokenWatch setup.
- [../scripts/README.md](../scripts/README.md) — CLI wrappers for monitoring scripts.
- [../skills/enterprise_token_saver_skills_v2/docs/README_TOKEN_OPTIMIZATION_TOOLS.md](../skills/enterprise_token_saver_skills_v2/docs/README_TOKEN_OPTIMIZATION_TOOLS.md) — extended tool reference.
