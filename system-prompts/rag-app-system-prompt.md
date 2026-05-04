<!-- Token note: force cite-or-abstain to reduce hallucination retries. -->

You answer questions using **only** provided CONTEXT blocks from retrieval.

## CONTEXT rules

- Each CONTEXT block has id `[n]`. Reference ids in your answer like `[1][2]`.
- If CONTEXT is insufficient, reply: `INSUFFICIENT_CONTEXT` plus **one** query rewrite suggestion (≤20 words).

## Answer shape

1. Direct answer (≤ **[N]** sentences)
2. Bullets citing `[id]` for non-obvious claims
3. Optional: "Not covered by context" section left empty if nothing extra

## No outside knowledge

- Do not use training data for factual claims about this organization unless present in CONTEXT.

---

### Design notes (token and quality)

**Why cite-or-abstain.** The `INSUFFICIENT_CONTEXT` response pattern prevents the model from hallucinating plausible-sounding answers when the retrieved context does not actually contain the answer. The query rewrite suggestion provides immediate value to the user (they can adjust their search) without requiring a follow-up turn. This pattern saves the cost of re-prompting after a hallucinated answer.

**Stable vs volatile split.** The instructions above (the rules and answer shape) are fully stable. The CONTEXT blocks and the user question are volatile — they go in the user message. Structure: `system = [this prompt]` and `user = "CONTEXT [1]: ...\nCONTEXT [2]: ...\n\nQuestion: ..."`. This separation enables caching of the stable instruction block across all RAG requests to this endpoint.

**Caching implications.** At ~70 tokens, this system prompt alone sits below the caching minimum. If you serve a knowledge-intensive domain (legal, medical, technical documentation), consider adding a stable "domain authority" block listing which sources are authoritative, what to do with conflicting sources, and any mandatory disclaimers. This brings the stable prefix into the caching range and adds genuine guidance.

**Retrieved context token budget.** This prompt does not set a retrieval budget — that belongs in the retrieval pipeline code (see `training/level-3-expert/01-rag-pipelines.md`). However, the answer shape constrains the output: limiting the answer to `[N]` sentences prevents verbose completions that re-state everything in the context.

**When to shorten further.** For a pure Q&A endpoint with a fast-moving knowledge base, remove the "Not covered by context" optional section — it is only useful when you want the model to flag gaps explicitly. For a strict information retrieval application (no opinion, no synthesis), also add a rule: "Do not infer or combine information across context blocks unless explicitly asked."
