# Lesson: prompt caching (provider-specific)

## When it helps

High **QPS** with identical long prefixes: policy, tool JSON, retrieved knowledge base preamble.

## Checklist

- Stable prefix is **byte-identical** across calls (watch hidden whitespace).
- Monitor cache hit metrics in responses and dashboards.
- Re-read provider docs quarterly—pricing and minimum lengths change.

## Read next

- [04-session-management.md](04-session-management.md)  
- Doc: [../../docs/03-tool-guides/api-usage.md](../../docs/03-tool-guides/api-usage.md)
