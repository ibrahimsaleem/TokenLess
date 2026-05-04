# IDE extensions (VS Code family): token-aware usage

Extensions such as **Cline**, **Continue**, **Roo**, and similar tools attach context from your editor and submit it to an LLM API on your behalf. Because they operate with real API keys and may send large amounts of context automatically, disciplined configuration has a direct cost impact.

---

## Open-tab hygiene

Every open file is a potential context injection, whether the extension picks it up automatically or the model infers relevance from the tab list.

**Checklist:**

- [ ] Close files unrelated to the current task before starting an AI-assisted session.
- [ ] Keep at most 5–8 tabs open when using context-auto-inclusion extensions.
- [ ] Use your editor's tab groups or workspaces to separate concerns (e.g. `frontend` vs `backend` workspace).
- [ ] Check whether the extension has a **"context files" panel** — review it before sending a long prompt.

**Anti-pattern:** Leaving a 3 000-line legacy file open that gets auto-attached because it was recently edited.

---

## Token meters and context indicators

Several extensions (Continue, Cline with some providers) display an approximation of how many tokens are loaded in the current context.

**Checklist:**

- [ ] Enable the token meter / context indicator in extension settings if available.
- [ ] Set a personal threshold (e.g. alert yourself at 40 000 tokens) and treat it as a prompt to summarize or start a fresh session.
- [ ] If the extension does not offer a meter, run `scripts/check-context-size.py` on the files you plan to reference before starting a long task.
- [ ] After summarizing or compacting, verify the estimated token count dropped before continuing.

---

## Workspace indexing and retrieval

Some extensions can index the workspace and retrieve relevant sections on demand rather than injecting full files.

**Checklist:**

- [ ] Enable workspace indexing in the extension settings if offered (Continue: `"indexing.enabled": true`).
- [ ] Allow the index to complete before starting context-heavy tasks.
- [ ] Prefer retrieval-mode prompts ("look up the auth module") over explicit file inclusion ("read `src/auth/service.ts`") when the extension supports both.
- [ ] Set the retrieval depth or top-k to a sensible value (3–8 results) rather than the maximum.
- [ ] Exclude generated files and `node_modules` from the index (see `.contextignore.template`).

---

## Instruction and prompt files

**Checklist:**

- [ ] Centralize repeated guidance in the extension's project instruction file (e.g. `.continue/config.json` system prompt, or `.cline/instructions.md`).
- [ ] Apply the same compression rules as you would to a system prompt: bullets over prose, remove motivational framing.
- [ ] Review the instruction file at the start of each sprint. Remove stale rules.
- [ ] Keep the instruction file under 2 000 tokens unless caching is confirmed.
- [ ] Do not paste the same instruction in both the project file and the chat — pick one source.

---

## Model selection per task

Most extensions allow choosing the model per session or per message.

**Checklist:**

- [ ] Maintain a personal routing policy (small model for completions, search, and short refactors; large model for multi-file architecture and review). Pin this in the project instruction file.
- [ ] Use local models (Ollama, LM Studio) for tasks that do not require frontier capability: simple completions, variable renames, formatting.
- [ ] When using a local model, be aware that context-window limits may be smaller than cloud equivalents — check the model card.
- [ ] Review extension telemetry or logs weekly to see which model handled the most tokens. Adjust routing if the small model never runs.

---

## Privacy, noise, and secrets

**Checklist:**

- [ ] Add a `.contextignore` or equivalent file to the project root. Use `templates/.contextignore.template` as a starting point.
- [ ] Confirm that `.env`, `*.pem`, `*.key`, secrets files, and credential JSON files are excluded.
- [ ] Exclude generated artifact directories (`dist/`, `build/`, `.next/`, `__pycache__/`) — they add tokens without adding information.
- [ ] Audit the extension's "allow list" or "deny list" settings at least once per project. Check what it would include by default.
- [ ] Never paste raw API keys or tokens in chat even as examples — redact them.

---

## Summary checklist (print and post)

| Category | Action |
|----------|--------|
| Open tabs | Close unrelated files; keep < 8 tabs |
| Context meter | Enable it; treat 40k tokens as a summarize-or-restart signal |
| Workspace index | Enable retrieval mode; set top-k 3–8; exclude generated files |
| Instruction file | Keep under 2k tokens; bullets only; review each sprint |
| Model choice | Small model for simple tasks; escalate explicitly |
| Secrets and noise | `.contextignore` in every project; no raw keys in chat |

---

## Related resources

- `.contextignore` template: `templates/.contextignore.template`
- Context size estimator: `scripts/check-context-size.py`
- Copilot-specific tab and model habits: `docs/03-tool-guides/claude-code.md` (patterns transfer)
- Skill install for any project: `skills/README.md`
