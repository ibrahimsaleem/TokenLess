# Lesson: RAG pipelines that save tokens

## Design checklist

- Chunking strategy matches document type (code vs prose).
- Embedding model and dimensionality chosen for **recall** targets.
- **Top-k** and **max chars** per retrieval enforced in code.
- Re-ranking only when measured lift justifies cost.

## Evaluation

- Offline: hit rate on labeled questions.
- Online: answer correctness + **tokens retrieved** distribution.

## Read next

- [02-custom-mcp-servers.md](02-custom-mcp-servers.md)  
- Doc: [../../docs/02-optimization-techniques.md](../../docs/02-optimization-techniques.md)
