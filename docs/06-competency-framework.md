# Competency framework: token optimization

Use this to staff training and performance reviews for **AI builders**.

## Basic (novice)

- Explains what a **token** is and that models have **finite context**.
- Reads provider pricing tables and understands **input vs output** billing.
- Writes concise prompts; closes irrelevant editor context; starts fresh chats between unrelated tasks.
- Uses a token counter or IDE meter when prompted.

## Advanced (intermediate)

- Budgets prompts with **tiktoken**, `count_tokens`, or internal metrics.
- Maintains lean **`CLAUDE.md` / `AGENTS.md` / rules** files; moves detail into skills.
- Uses **summarization and compaction** deliberately; designs few-shot only when needed.
- **Routes models** by task risk; uses caching features where supported.
- Audits **MCP** footprint per project.

## Expert

- Performs **context breakdown** reviews (what is always-on vs on-demand).
- Builds **RAG** pipelines with evaluation for chunking and retrieval quality.
- Ships **custom MCP** or CLI tools that return minimal sufficient context.
- Runs org-wide **dashboards** (provider consoles + internal traces); sets budgets and alerts.
- Trains others; defines **lint rules** for prompts and agent configs.

## Mapping to TokenLess materials

- Basic: `training/level-1-beginner/`
- Advanced: `training/level-2-intermediate/` + `guidelines/`
- Expert: `training/level-3-expert/` + `docs/04-mcp-guide.md` + external graph/RTK/token-optimizer pilots
