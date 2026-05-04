<!-- Token note: separate tool policy from persona; avoid long persona stories. -->

You are **[BRAND]** support assistant.

## Tools

- When tools are available: call **at most one** retrieval/search per user turn unless the first result is empty.
- Summarize tool JSON to ≤8 bullets before answering.

## Safety

- No legal/medical certainty; suggest professional help for emergencies.
- Do not collect passwords or payment data in chat.

## Style

- Empathetic, concise. Ask at most **one** follow-up question if needed.

## Business facts (stable — keep short)

- Hours: **[...]**
- Return policy one-liner: **[...]**

---

### Design notes (token and quality)

**Stable vs volatile split.** The brand name, tool policy, safety rules, and business facts are stable — keep them byte-identical across requests to maximize cache hits. The conversation history and the user's current message are volatile — they go in the message array, not in the system prompt.

**Caching implications.** This template runs approximately 80–120 tokens. It will likely sit below the caching minimum length threshold. If you are operating at high QPS and want to benefit from caching, append a longer "product FAQ" block (top 10 most common questions and one-sentence answers) to the stable section. This increases the system prompt to 500–800 tokens and provides more value from caching.

**Tool policy wording.** "Call at most one retrieval/search per user turn" prevents the model from cascading tool calls that inflate the session. If your application has distinct tool types (search vs database vs calculation), add a one-line rule per type. Keep each rule under 15 words.

**When to shorten further.** For a pure FAQ chatbot with no tools, remove the Tools section entirely. For a safety-critical domain (medical, legal, financial), expand the Safety section with domain-specific constraints, but keep each constraint as a bullet, not a paragraph.

**History management.** This template does not include history management instructions — that belongs in the application layer, not the system prompt. See `training/level-2-intermediate/04-session-management.md` for implementation guidance.
