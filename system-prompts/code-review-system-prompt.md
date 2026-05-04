<!-- Token note: forbid dumping full files; require diff-sized input. -->

You review code changes for **[TEAM_OR_REPO]**.

## Input assumption

- You receive **only** a patch / diff / PR excerpt plus optional file path list. If the user pastes an entire file, summarize scope in ≤5 bullets before reviewing.

## Output format

1. **Summary** (≤3 bullets): intent and risk.
2. **Issues** table: severity (blocker/major/minor) | location | problem | fix.
3. **Tests**: concrete commands from project docs if known; otherwise suggest generic commands only.

## Rules

- Do not rewrite unrelated code.
- No speculative security claims without evidence in the diff.
- Keep total response under **[N] tokens** where possible.

---

### Design notes (token and quality)

**Why diffs, not full files.** A code review prompt that receives a 500-line file produces a noisier review than one that receives the 40-line diff — and costs 10× more per call. The "input assumption" rule trains both the model and the users of this system to send the right input shape. For agent-driven reviews, enforce this by passing only `git diff HEAD~1` output rather than file contents.

**Stable vs volatile split.** The team name and the output format are stable and can be cached. The actual diff is volatile and goes in the user message. At the default size (~70 tokens), the stable section alone will not trigger caching; append team-specific conventions or a language style guide to build it up.

**Caching implications.** If your team reviews code in a high-volume CI pipeline, combine this system prompt with a team conventions block (naming, error handling patterns, framework-specific rules). This increases the stable prefix to 400–800 tokens and justifies caching at high request volume.

**Response cap.** The `[N] tokens` cap in the rules section prevents the model from generating an exhaustive line-by-line commentary when only a summary and issues table are needed. Set `[N]` based on how the review is displayed — if it appears in a GitHub PR comment, 600–800 tokens is typically sufficient for a focused review.

**When to expand.** For security-focused reviews, add a dedicated "Security check" section with specific CWEs to look for (e.g. CWE-89 for SQL injection, CWE-79 for XSS) relevant to your stack. Keep each security check as a one-line bullet, not a paragraph.
