# Tools, monitoring, and open-source helpers

## Prompt engineering and evaluation

- **LangChain** — chains, some caching utilities; pair with observability.
- **DSPy** — programmatic prompt optimization research toolkit.
- **PromptLayer, PromptFoo, HumanLoop** — logging, evaluation, iteration workflows.

## Token counting

- **tiktoken** — OpenAI tokenizer for estimating GPT-family tokens.
- **Anthropic `count_tokens`** — exact counts for Claude-shaped requests (SDK/API).
- **LiteLLM** — unified proxy/wrapper with multi-provider usage metadata (verify license and deployment model for your org).

## Usage and cost monitoring

- **Helicone, LangSmith, OpenMeter** — tracing, dashboards, experiments.
- **Anthropic Console / OpenAI usage** — authoritative billing views.
- **TokenWatch (this repo)** — `tokenwatch.py` for **local** recording, budgets, and model comparison during app development.

## Open-source token optimization repositories

These go beyond “counting tokens” to **reduce waste**:

| Repository | Role | Pilot |
|------------|------|--------|
| [alexgreensh/token-optimizer](https://github.com/alexgreensh/token-optimizer) | Structural audit: CLAUDE.md, memory, skills, MCP bloat, compaction | Claude Code power users |
| [rtk-ai/rtk](https://github.com/rtk-ai/rtk) | Compress noisy **terminal output** before it hits the model | Terminal-heavy workflows |
| [tirth8205/code-review-graph](https://github.com/tirth8205/code-review-graph) | **Graph + MCP** for precise repo context | Large repos, PR review |

Details also in [../skills/enterprise_token_saver_skills_v2/docs/README_TOKEN_OPTIMIZATION_TOOLS.md](../skills/enterprise_token_saver_skills_v2/docs/README_TOKEN_OPTIMIZATION_TOOLS.md).

## Other references

- [LiteLLM on GitHub](https://github.com/BerriAI/litellm) — widely used gateway (verify you mean this org/repo when installing).
- Academic / Hugging Face **transformers** tokenizers for self-hosted models.
