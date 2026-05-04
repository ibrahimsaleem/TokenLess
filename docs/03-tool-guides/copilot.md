# GitHub Copilot: token-aware usage

Copilot and Copilot Chat use **indexing and retrieval** (semantic search, grep, file tools) rather than dumping the whole workspace into every request. Your habits still change cost and quality.

## Open tabs and visible context

- **Open only relevant files.** Irrelevant visible code can leak into chat context.
- Use **explicit attachments** and `#` mentions when you know which file or symbol matters.

## Workspace indexing

- Keep the workspace index healthy (sign-in, permissions, large-repo settings per Microsoft docs).
- When the index is missing, tools fall back to slower search paths—still better than pasting megabytes manually.

## Prompt crafting

- Reference **symbols, paths, and error strings** instead of vague questions.
- Prefer one focused question per thread; split unrelated work across conversations.

## Inline completion

- Use **clear comments** and **good names** so the model infers intent with fewer extra tokens from surrounding noise.

## Model choice in Chat

When the product allows model selection, use **larger context / stronger models** only for refactors and multi-file work; use faster tiers for small edits.

## Official references

- [Workspace context (VS Code)](https://code.visualstudio.com/docs/copilot/reference/workspace-context)
- [Copilot best practices](https://docs.github.com/copilot/best-practices)
