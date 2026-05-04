# Lesson: Custom MCP servers

**Level:** Expert — Level 3  
**Time:** 45 minutes  
**Prerequisites:** [01-rag-pipelines.md](01-rag-pipelines.md); familiarity with MCP protocol basics

---

## Learning objectives

By the end of this lesson you will be able to:

1. Decide when building a custom MCP server is justified vs alternatives (CLI, direct API call, static injection).
2. Design a tool schema that minimizes per-call token overhead.
3. Implement a tool that returns identifiers for follow-up rather than bulk payloads.
4. Apply the three-step security review for any new MCP server.
5. Write an acceptance test for a new MCP tool that validates both token efficiency and correctness.

---

## When to build a custom MCP server

A custom MCP server is justified when:

1. The data source is internal (your database, internal API, custom knowledge base) and no off-the-shelf server covers it.
2. The response needs to be **deterministic and small** — a well-designed internal tool returns exactly what the model needs, while a generic web search might return thousands of tokens of irrelevant content.
3. The same query will recur frequently across agent sessions (cache value is high).
4. Existing options (CLI scripts, direct file reads) would produce response payloads too large for reliable in-context use.

**Do not build a custom MCP server when:**
- A simple CLI command or Python function achieves the same result without registering a schema in the agent.
- The tool would be called rarely (the schema overhead per session outweighs the benefit).
- The same data could be injected as a static block in `CLAUDE.md` or `AGENTS.md` (no runtime call needed).

---

## Schema design for minimal token overhead

The tool description in your server schema is injected into every request as prose. Write it defensively short:

**Verbose (costly) schema description:**
```json
{
  "name": "get_customer_data",
  "description": "Retrieves comprehensive customer data from the internal CRM system including account details, contact information, subscription status, billing history, support ticket references, and custom attributes. Returns a complete JSON object with all available fields."
}
```

**Lean schema description:**
```json
{
  "name": "get_customer",
  "description": "Fetch CRM customer record by customer_id. Returns: account, subscription, support_ticket_ids.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "customer_id": {"type": "string", "description": "CRM customer UUID"}
    },
    "required": ["customer_id"]
  }
}
```

Rules:
- Description: one sentence maximum. State what it returns, not why it exists.
- Parameter descriptions: 5–8 words each.
- Remove all padding ("This tool allows you to…", "Use this when…").

---

## Returning identifiers instead of payloads

The most important design pattern for token-efficient MCP tools: **return references, not bulk data**.

**Anti-pattern (returns full data in one call):**
```python
@tool
def search_documents(query: str, top_k: int = 5) -> list[dict]:
    results = vector_store.search(query, top_k)
    return [{"id": r.id, "title": r.title, "content": r.full_text} for r in results]
    # Returns 5 × 3000 tokens = 15 000 tokens per call
```

**Better pattern (returns IDs; agent fetches only what it needs):**
```python
@tool
def search_documents(query: str, top_k: int = 5) -> list[dict]:
    results = vector_store.search(query, top_k)
    return [{"id": r.id, "title": r.title, "score": r.score} for r in results]
    # Returns ~200 tokens per call

@tool
def get_document(doc_id: str) -> dict:
    doc = vector_store.get(doc_id)
    return {"id": doc.id, "title": doc.title, "content": doc.text[:3000]}
    # Agent fetches only the 1–2 documents it actually needs
```

This two-call pattern reduces average retrieval cost dramatically when top_k is large and only a subset of results are actually used.

---

## Mandatory parameters

Every MCP tool that returns a list or collection should support:

- `top_k` or `limit` — capped in the implementation, not just accepted.
- `max_chars` or `max_tokens` — enforced hard limit on the payload size.
- `timeout` — do not let slow back-ends stall the agent.

```python
@tool
def search_logs(query: str, limit: int = 10, max_chars: int = 8000) -> dict:
    raw_results = log_backend.search(query, limit=min(limit, 50))  # cap at 50
    payload = format_results(raw_results)
    return {"results": payload[:max_chars], "truncated": len(payload) > max_chars}
```

---

## Security review checklist

Before deploying any custom MCP server, answer these three questions:

**1. What data can this tool expose?**

Map every tool to the data classes it can access. For each class: Is this data PII? Is it regulated (HIPAA, GDPR, PCI)? Can the tool be queried in a way that returns data the requesting user is not authorized to see? If yes to any of these: add authorization checks inside the tool implementation, not just at registration.

**2. What can this tool modify?**

Read-only tools have a lower risk profile than write tools. For write tools: add a confirmation step (return a preview and require an `execute=true` parameter), log every write with the requesting agent session ID, and require explicit approval from a team lead before production deployment.

**3. What does the result flow through?**

Tool results flow into the agent's context and may be included in logging, session exports, or summarizations. Ensure the result does not contain credentials, private keys, or tokens that could be exfiltrated through the agent's normal output channels.

---

## Acceptance criteria for a new MCP tool

Before merging a new MCP server implementation:

- [ ] Schema description is ≤ 1 sentence, parameters ≤ 8 words each.
- [ ] All list-returning tools accept `limit` and `max_chars`; both are enforced in code.
- [ ] Unit test: call the tool with a query that would return a large payload; assert `len(response_json) < MAX_CHARS`.
- [ ] Security review checklist completed and signed off.
- [ ] Tool is registered in the team's approved server list.
- [ ] At least one session test: agent can complete the target task using the tool with measured token overhead below the defined budget.

---

## Failure modes

**Schema bloat creep.** Tool descriptions grow over time as documentation improves. Audit schema token count quarterly using the weekly MCP audit checklist in `docs/04-mcp-guide.md`.

**Tool result caching not implemented.** Repeated identical queries hit the data source every time. For read-only tools with stable data, add an in-memory or Redis cache with a short TTL.

**Unbounded list responses.** The `limit` parameter is accepted but not enforced; a query returns 10 000 items. Add a hard cap inside the tool implementation.

**Authorization bypass.** Tool returns data based on what the agent asks for, not on what the requesting user is authorized to see. Add authorization inside the tool, not as a pre-filter at the agent layer.

---

## Read next

- [03-dependency-aware-prompting.md](03-dependency-aware-prompting.md)
- Doc: [../../docs/04-mcp-guide.md](../../docs/04-mcp-guide.md)
- Security baseline: [../../guidelines/DEVELOPER-GUIDELINES.md](../../guidelines/DEVELOPER-GUIDELINES.md) (Rule 6)
