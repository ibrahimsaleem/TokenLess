# MCP: token-saving patterns and policy

The Model Context Protocol (MCP) lets agents call tools at runtime. Every connected MCP server injects a set of **tool definitions** into the agent's context before the first turn. These definitions are prose-heavy JSON schemas — a moderately configured setup can add 2 000–8 000 tokens of overhead before the user's first word arrives.

This guide explains where the cost comes from, how to govern it, and how to use MCP intentionally as a token-saving mechanism rather than a source of hidden inflation.

---

## Where MCP tokens come from

When an agent lists available tools, the provider receives a JSON array of tool objects — one per registered tool. Each entry includes a name, description paragraph, and a parameter schema (input_schema). A minimal tool definition typically costs 150–400 tokens. A well-documented server with eight complex tools can contribute 3 000+ tokens per request.

The overhead compounds across three sources:

1. **Tool definitions** — every server contributes its full schema every call.
2. **Tool invocation records** — every tool call and its result is added to the running conversation.
3. **Idle servers** — a server loaded but never called still injects its full schema every turn.

---

## Categories that usually save tokens

MCP servers in the following categories tend to **return more value than they cost** when used deliberately:

1. **Code graph / AST MCP** — answers "which files matter?" before wide reads. Example: [code-review-graph](https://github.com/tirth8205/code-review-graph). Replaces a broad repo scan with a targeted 3–5 file selection.
2. **Documentation retrieval** — returns **top-k** chunks from an indexed knowledge base instead of pasting entire manuals into the user message. Requires an accurate index and a well-tuned top-k value (start at 3–5).
3. **Memory MCP** — stores durable notes outside the chat window so the model does not need to re-derive context at the start of each session. Requires hygiene (TTL, size cap per entry).
4. **Issue or PR MCP** — fetches **one** ticket or pull request by id when a user references it, instead of pasting the full ticket body manually.
5. **Log or search MCP** — returns **filtered slices** (by time, level, query) rather than full log files. Pair with a hard character limit on the returned slice.

---

## Defer vs eager tool listing

MCP frameworks differ in when tool schemas are sent to the model:

- **Eager (default in most frameworks):** All tool definitions are included in every request, whether or not the agent will call them.
- **Deferred / on-demand:** Tools are listed only when the agent explicitly queries them, or when a tool is first invoked. Substantially lower overhead for large toolsets.

Prefer deferred listing where the framework supports it. In Claude Code, this is controlled by how you configure the MCP server registration. In agent code, review whether your orchestration library sends `tools=[]` by default or attaches everything.

---

## Per-environment configuration

### Claude Code

Open the project-level MCP configuration (`.claude/mcp-servers.json` or the Settings panel). Review the active server list before each session type:

- **Writing code** — enable only the code graph and version-control servers.
- **Answering questions** — enable only documentation retrieval and memory.
- **PR review** — enable code graph, issue/PR, and memory; disable unrelated services.

### Windsurf (Cascade)

MCP servers are configured in `.windsurf/mcp.json`. Apply the same session-type principle. Windsurf Cascade sessions are billed per context unit, so unused servers have a direct cost.

### Custom agent code

When building with the provider SDK directly, only pass the tools array for servers relevant to the current task. Use routing logic to select a subset:

```python
def tool_set_for_task(task_type: str) -> list:
    if task_type == "codegen":
        return [code_graph_tools, file_system_tools]
    elif task_type == "qa":
        return [docs_retrieval_tools, memory_tools]
    else:
        return []  # no tools — cheaper for pure-text tasks
```

---

## Weekly MCP audit checklist

Run this review at the start of each sprint or after any new server is added:

- [ ] List all registered MCP servers. Is each one referenced in at least one CLAUDE.md, workflow, or team session in the past week?
- [ ] For each active server: what is the tool count? Does every tool have a use case this team actually hits?
- [ ] Is any server returning results larger than 4 000 tokens in practice? Check tool invocation logs or ask the model to report tool result sizes.
- [ ] Do retrieval tools have explicit `top_k` or `max_chars` limits configured?
- [ ] Are any secrets, API keys, or personal data flowing through tool results? (Audit at least monthly.)
- [ ] Are memory entries older than 30 days? Prune entries that no longer apply.

---

## Security considerations

MCP tools can surface sensitive data if not governed. Enforce the following:

- **Scope tools to minimum privilege.** A documentation retrieval tool should have read-only access to the docs index only.
- **Never route secrets through tool results.** If a tool returns an API key or credential even temporarily, rotate it.
- **Set size limits.** Unbounded tool output can exfiltrate large data payloads and inflate cost simultaneously.
- **Log tool calls.** Record which tool was called, by which agent session, and with what arguments — at a minimum for audit-grade systems.

---

## When MCP is the wrong tool

Prefer ordinary CLI commands and local scripts when:

- The operation is a one-off read (e.g. reading a single file by known path) — just pass the text directly.
- The tool schema would cost more tokens than the result saves.
- The same information is already available in the conversation context.
- A local script could run in milliseconds without a network call.

---

## Further reading

- [Model Context Protocol](https://modelcontextprotocol.io) — official specification.
- Enterprise skill doc: [../skills/enterprise_token_saver_skills_v2/docs/MCP_TOKEN_SAVERS.md](../skills/enterprise_token_saver_skills_v2/docs/MCP_TOKEN_SAVERS.md)
- Training: [../training/level-3-expert/02-custom-mcp-servers.md](../training/level-3-expert/02-custom-mcp-servers.md)
- Guidelines: [../guidelines/DEVELOPER-GUIDELINES.md](../guidelines/DEVELOPER-GUIDELINES.md) (Rule 4: MCP discipline)
