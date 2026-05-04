# Lesson: RAG pipelines that save tokens

**Level:** Expert — Level 3  
**Time:** 40 minutes  
**Prerequisites:** Level 2 complete; familiarity with vector databases or embedding APIs

---

## Learning objectives

By the end of this lesson you will be able to:

1. Design a RAG pipeline that enforces hard token limits on retrieved context.
2. Choose a chunking strategy appropriate to the document type.
3. Identify and mitigate the three most common RAG failure modes (lost recall, injection inflation, stale index).
4. Instrument a RAG pipeline to measure tokens retrieved per query at p50 and p95.
5. Justify when to add re-ranking and when it is not worth the cost.

---

## Why RAG is a token optimization strategy

Naive knowledge injection pastes entire documents into the prompt. A 50-page policy document = 50 000+ tokens per request, every request. RAG replaces this with a retrieval step that selects the most relevant 1 000–4 000 tokens for each specific query. Done well, this is the single largest context reduction available for knowledge-intensive applications.

The trap: poorly configured RAG can actually increase token cost (over-retrieval) or hurt quality (wrong chunks returned) worse than naively injecting the whole document.

---

## Chunking strategy by document type

The right chunking strategy depends on the document structure:

| Document type | Strategy | Chunk size | Overlap |
|---------------|----------|------------|---------|
| Prose / policy docs | Paragraph | 200–400 tokens | 50 tokens |
| Technical reference | Section (header-delimited) | 400–800 tokens | 100 tokens |
| Source code | Function / class boundary (AST) | Variable — one unit | None |
| Conversation transcripts | Speaker turn | 100–200 tokens | 1 turn |
| Structured data (tables) | Row batch + header | 10–20 rows | Header row only |

**Anchor chunk approach for prose:** Always include the first paragraph of a document section as a prefix in every chunk from that section. This preserves topic context even when the retrieved chunk is from deep in the section.

**Fixed-size with overlap (fallback):** When document structure is not parseable, chunk at a fixed character count with a 10–15% overlap to avoid cutting mid-sentence. This is the least precise approach; prefer structural chunking when possible.

---

## Hard token limits in code

Never rely on "top-k should be small enough." Enforce a hard cap on retrieved bytes in code:

```python
MAX_RETRIEVAL_TOKENS = 6000  # hard ceiling per request

def retrieve_with_cap(query: str, top_k: int = 5) -> str:
    results = vector_store.search(query, top_k=top_k)
    chunks = []
    total = 0
    for chunk in results:
        estimated_tokens = len(chunk.text) // 4
        if total + estimated_tokens > MAX_RETRIEVAL_TOKENS:
            break  # hard stop
        chunks.append(chunk.text)
        total += estimated_tokens
    return "\n\n---\n\n".join(chunks)
```

Instrument the `total` value per request to track p50 and p95 retrieval token counts. If p95 is close to `MAX_RETRIEVAL_TOKENS`, your cap is biting frequently — investigate whether k or chunk size needs adjustment.

---

## Failure modes and mitigations

### 1. Lost recall

**What it is:** The relevant chunk exists in the index but the retrieval query does not surface it (embedding space miss).

**Mitigation:**
- **Hybrid search:** combine BM25 lexical search with vector search, then deduplicate. BM25 catches exact keyword matches that semantic search may miss.
- **Query expansion:** generate 2–3 paraphrases of the user query and retrieve for each.
- **Offline evaluation:** build a small labeled dataset (query → expected chunk) and measure hit rate before deploying changes.

### 2. Injection inflation

**What it is:** top_k is set too high, or chunks are too large, causing the retrieval block to consume the majority of the context window even when most returned chunks are irrelevant.

**Mitigation:**
- Start with `top_k=3` and measure answer quality. Only increase if evaluation shows quality gaps.
- Apply the hard token cap (above) as a safety net.
- Track "useful chunk ratio" in evaluation: what fraction of retrieved chunks were referenced in the response?

### 3. Stale index

**What it is:** Source documents are updated but the embedding index is not re-computed, causing the model to answer from outdated information.

**Mitigation:**
- Implement incremental re-indexing triggered by document update events (webhook, CI step, or scheduled job).
- Store a document hash alongside each chunk. On retrieval, optionally validate freshness.
- For frequently changing documents, consider reducing the RAG chunk cache TTL.

---

## Re-ranking: when to add it

Re-ranking applies a cross-encoder model after initial retrieval to score the candidate chunks more precisely than cosine similarity alone. It improves quality but adds latency and cost (one inference call for re-ranking).

**Add re-ranking when:**
- Offline evaluation shows retrieval precision below ~60% hit rate.
- Queries are long and nuanced (the bi-encoder embedding misses subtlety).
- The incremental quality improvement justifies the latency and cost.

**Skip re-ranking when:**
- Top-k is small (≤3) and queries are short — cosine similarity is usually sufficient.
- Latency is a hard constraint.
- The primary problem is stale index or lost recall — re-ranking does not fix these.

---

## Instrumentation

Record these per RAG-backed request:

```python
monitor.record_usage(
    model, input_tokens, output_tokens,
    task_label="qa_rag",
    metadata={
        "retrieval_tokens": retrieval_token_count,
        "chunks_returned": len(results),
        "top_k": top_k,
    }
)
```

Review `retrieval_tokens` at p50 and p95 weekly. A rising p95 without a corresponding quality improvement suggests over-retrieval is creeping in.

---

## Acceptance criteria (you know this lesson when…)

- Your RAG pipeline has a hard token cap enforced in code, not just a top_k suggestion.
- You have measured hit rate on at least 20 labeled queries.
- You can explain lost recall vs injection inflation vs stale index — and the mitigation for each — without notes.
- The p95 retrieval token count for your pipeline is known and sits below 60% of your context budget.

---

## Read next

- [02-custom-mcp-servers.md](02-custom-mcp-servers.md)
- Doc: [../../docs/02-optimization-techniques.md](../../docs/02-optimization-techniques.md) — RAG section
