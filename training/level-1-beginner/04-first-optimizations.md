# Lesson 4: First optimizations (do these today)

**Level:** Beginner — Level 1  
**Time:** 25 minutes  
**Prerequisites:** [03-billing-basics.md](03-billing-basics.md)

---

## Learning objectives

By the end of this lesson you will be able to:

1. Apply five immediate prompt optimizations to any existing project.
2. Use `scripts/check-context-size.py` to measure the before/after impact.
3. Establish a personal review checklist for prompt commits.
4. Know which optimizations to tackle next at Level 2.

---

## The five first optimizations

These require no library changes, no infrastructure, and no provider-specific features. You can apply every one of them today with a text editor.

### 1. Delete fluff from system prompts

**What it is:** Mission statements, "As a helpful AI…" framing, restated company values, duplicated safety rules.

**How to find it:** Read your system prompt line by line and ask: "If I removed this, would the model behave differently?" If the answer is no, it is a candidate for removal.

**Example:**

Before:
```
You are a highly capable, helpful, and friendly AI assistant created by Acme Corp to assist our valued customers with their questions and needs. You should always be kind, empathetic, and professional. Safety is our top priority.
```

After:
```
You assist Acme Corp customers with product and support questions. Be direct and factual.
```

Before: ~50 tokens. After: ~15 tokens. Same effective behaviour.

### 2. Stop repeating the same instructions every turn

**What it is:** Instructions that appear in the system prompt and are then repeated in each user message, or that appear in both `CLAUDE.md` and a separate instructions file.

**How to fix it:** Pick one canonical location (the system prompt) and remove duplicates everywhere else.

### 3. Clear history between unrelated tasks

**What it is:** Conversation history from a prior task (e.g. debugging a payment module) that persists into a new unrelated task (e.g. writing a blog post).

**How to fix it:**

- In chat UIs: start a new conversation explicitly. Do not rely on summarization of a session that has already wandered off-topic.
- In CLI agents (Claude Code, etc.): use `/compact` after completing a distinct unit of work, or `/clear` for a fully fresh session.
- In code: implement a `clear_history()` path in your session manager for task boundaries.

### 4. Close irrelevant files in IDE tools

**What it is:** Open editor tabs that IDE AI extensions auto-attach to context, even though they are not relevant to the current task.

**How to fix it:** Before starting an AI-assisted session, close all files unrelated to the immediate task. If your extension shows a context file list, review it before sending a long prompt.

### 5. Cap output with max_tokens

**What it is:** Not setting `max_tokens` (or setting it very high "to be safe") allows the model to generate long completions at 3–5× the input token rate.

**How to fix it:** Set `max_tokens` deliberately based on the expected output length for each request type. For a classification endpoint: 10–20 tokens. For a code-review endpoint: 500–1 500 tokens. Revisit the cap periodically as you see real output distributions.

---

## Before-and-after measurement

Before applying any optimization, record the baseline using `scripts/check-context-size.py`:

```bash
python scripts/check-context-size.py --file system_prompt.txt
```

Then apply the optimization and re-run. Record:

- Character count before and after.
- Estimated token count before and after.
- Behaviour test: run your standard evaluation cases and confirm no quality regression.

Target on a first pass: 25–40% reduction in system prompt tokens. This is almost always achievable without touching any meaningful constraint.

---

## Personal review checklist (add to your PR template)

Copy this into your team's pull request template for any prompt change:

```
Token hygiene:
- [ ] System prompt reviewed for fluff and duplicated rules
- [ ] History management strategy defined (rolling window, summarize, or clear)
- [ ] max_tokens set intentionally for each request type
- [ ] Estimated input tokens per request documented (rough)
- [ ] No secrets or PII in the prompt
```

---

## Common misconceptions

**"These changes will hurt quality."** Removing fluff and redundancy does not remove information — it removes tokens that carry no new information. A model that receives a concise, unambiguous prompt often outperforms one given a verbose prompt, because it has less noise to attend to.

**"I only need to do this once."** Prompts accumulate clutter over time as requirements change. Budget a prompt review into every major feature release or sprint.

**"max_tokens is a safety limit, not a cost control."** It is both. Setting it appropriately also prevents unexpected long completions from inflating output spend.

---

## 2-minute exercise

Pick any system prompt in your current project (or use one from `system-prompts/` in this repo):

1. Run `check-context-size.py` on it.
2. Apply optimization #1 (delete fluff) and re-run.
3. Apply optimization #2 (remove duplicates) and re-run.
4. Record the token reduction. Did behaviour change? (If you do not have an automated eval, read the prompt aloud — does it still constrain the same behaviours?)

---

## You know this lesson when…

- You have applied at least three of the five optimizations to a real prompt in your project.
- You can articulate why each optimization reduces tokens without reducing useful information.
- Your PR template or personal checklist includes at least three of the five items above.

---

## What is next

These five tactics represent the quick wins. Level 2 covers techniques that require code changes: prompt compression strategies, model routing, prompt caching, and session management.

- Continue to: [../level-2-intermediate/README.md](../level-2-intermediate/README.md)
- Reference: [../../guidelines/QUICK-REFERENCE-CHEATSHEET.md](../../guidelines/QUICK-REFERENCE-CHEATSHEET.md)
- Tool habits: [../../docs/03-tool-guides/](../../docs/03-tool-guides/)
