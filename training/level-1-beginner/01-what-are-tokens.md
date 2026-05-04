# Lesson: what are tokens?

Tokens are how models **chunk text** for processing and billing. They are not always whole words.

## Why engineers should care

- APIs charge per **input** and **output** tokens.
- Latency often grows with **input** size.
- Very long inputs can cause **lost instructions** or truncation.

## Practical intuition

- English averages roughly **3–4 characters per token** (rough estimate only).
- Code with many symbols can differ.

## Read next

- [02-context-windows.md](02-context-windows.md)  
- Deep dive: [../../docs/01-core-concepts.md](../../docs/01-core-concepts.md)
