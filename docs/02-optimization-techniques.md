# General token optimization techniques

These patterns apply across APIs, agents, and IDE tools.

## Prompt compression and summarization

- Replace long prose with **bullet constraints** and **explicit output shape** (e.g. JSON keys).
- Move stable instructions to **one** system or policy block; do not repeat them every turn.
- Summarize long threads instead of appending full transcripts.

## Few-shot vs zero-shot

Few-shot examples improve accuracy but **cost tokens**. Use them when the task is unusual or format-critical; prefer tight instructions when the model already knows the domain.

## Chunking

For large documents or codebases: **chunk** input, process in windows, and aggregate results. Never assume “paste the whole repo” is viable.

## Retrieval-augmented generation (RAG)

Index knowledge (docs, tickets, code) and retrieve **top-k** chunks instead of sending everything. Teams have reported large reductions versus brute-force file reads when search is done well.

## Prompt / prefix caching (provider-specific)

Where the API supports caching a static prefix (e.g. long system prompt, tool definitions, repeated policy): structure requests so the **stable part is identical** across calls to maximize cache hits. Read the provider’s minimum block sizes and TTL rules.

## Structured outputs

Define **schemas** (JSON, tables) so the model stops cleanly and you avoid clarification rounds. Indirectly saves tokens by reducing retries.

## Model routing and tiering

Use **small/fast/cheap** models for classification, routing, extraction, and lint-level tasks. Reserve **large** models for multi-step reasoning, architecture, or high-stakes generation. Measure quality; do not over-tier.

## Session management

Trim history, **summarize** completed phases, and start **fresh sessions** for unrelated tasks. In CLI agents, compaction commands exist for the same purpose—use them with a written handoff (see skill packs).

## Next steps

- Tool-specific habits: [03-tool-guides/](03-tool-guides/)
- MCP patterns: [04-mcp-guide.md](04-mcp-guide.md)
- Monitoring and OSS helpers: [05-tools-and-platforms.md](05-tools-and-platforms.md)
