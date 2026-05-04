# Lesson: Prompt compression

**Level:** Intermediate — Level 2  
**Time:** 30 minutes  
**Prerequisites:** Level 1 complete

---

## Learning objectives

By the end of this lesson you will be able to:

1. Apply three compression patterns (bulletization, collapse, de-duplication) to any prose prompt.
2. Compress a real system prompt to ≤40% of its original token estimate without breaking the target behaviour.
3. Identify when compression will hurt quality and stop before it does.
4. Measure the result with `scripts/check-context-size.py` and record the delta.

---

## Why prompt compression matters at Level 2

In Level 1 you removed obvious fluff. Compression at this level is more systematic: you are applying explicit rewriting patterns, not just deleting lines. The goal is to preserve every meaningful constraint while eliminating the prose scaffolding those constraints are buried in.

---

## Pattern 1: Bulletization

Convert narrative paragraphs into constraint bullets. Each bullet carries exactly one rule or decision.

**Before (narrative, ~80 tokens):**
```
When the user asks a question about billing, you should look up the relevant policy
in the documents provided and give a clear answer. If the policy does not cover the
question, you should tell the user that you do not have the information and recommend
they contact support. Always be polite and avoid technical jargon.
```

**After (bullets, ~30 tokens):**
```
Billing questions:
- Answer from provided policy documents only.
- If not covered → "I don't have that info; contact support."
- Plain language; no jargon.
```

Same behaviour. 62% token reduction.

---

## Pattern 2: Collapse multi-message history

When conversation history accumulates, collapse the oldest turns into a summary block before the most recent N turns.

**Structure:**
```
[Summary of session so far: ~100 tokens]
[Turn N-2: ~80 tokens]
[Turn N-1: ~80 tokens]
[Turn N (current): user message]
```

Replace the full rolling history. The model retains necessary context; old details are compressed into a summary it can reference.

When to trigger: after every 10–15 turns, or whenever the context meter shows history consuming >40% of the window.

---

## Pattern 3: De-duplicate error stacks

When debugging sessions attach stack traces, only the first occurrence of each unique stack frame is meaningful. Repeated identical stacks are common when tests fail on multiple inputs.

**Before:** 12 copies of the same stack trace pasted into one session (8 000+ tokens).  
**After:** 1 copy + a note "same stack repeated 11 more times" (700 tokens).

De-duplication is lossless for the model's reasoning — it does not gain new information from the 12th copy of the same error.

---

## Pattern 4: Collapse multi-step conversation to a handoff note

After completing a distinct sub-task in an agent session, write a compact handoff note and start fresh.

**Handoff note format:**
```
## Session handoff
Task completed: [one sentence]
Decisions made: [2–5 bullets]
Files changed: [list]
Outstanding: [1–3 items]
```

This note, compressed into 80–120 tokens, replaces tens of thousands of tokens of prior conversation. The `compact-handoff` skill in `skills/token_optimization_skill_pack/` automates this.

---

## Anti-patterns

- **Over-compressing genuinely load-bearing constraints.** If a safety rule is removed "for brevity" and the model produces unsafe output, the optimization was wrong. Test after every compression pass.
- **Pasting entire JSON logs into the user message.** A 5 MB JSON blob is many hundreds of thousands of tokens. Extract only the relevant key-value pairs.
- **Pasting the entire company handbook as context.** Use RAG (Level 3) to retrieve only the relevant policy sections at query time.
- **Compressing into ambiguity.** "Be helpful" is vaguer than "answer factual questions only; do not generate code." The shorter constraint is fine because it is specific; do not go shorter than specific.

---

## Worked practice exercise

1. Find a system prompt in your project that is over 500 tokens (estimate using the character ÷ 4 rule).
2. Copy it into `system_prompt_v1.txt`.
3. Apply patterns 1–3 in a new file `system_prompt_v2.txt`.
4. Run `python ../../scripts/check-context-size.py --file system_prompt_v1.txt` and record the result.
5. Run the same command on `system_prompt_v2.txt` and record the result.
6. Test both versions against your standard evaluation cases (even a manual 5-query smoke test works for this exercise).

Target: ≤40% of v1 token count in v2, with no regression on the smoke test.

---

## Measurement

- Token delta: `(v1_tokens - v2_tokens) / v1_tokens × 100%`
- Quality check: smoke test pass rate on your evaluation cases (count of failures / total).
- Monthly cost delta: plug the token delta into `scripts/estimate-cost.py` at your expected request volume.

---

## You know this lesson when…

- You can describe all four compression patterns without looking at notes.
- You have compressed a real system prompt to ≤40% of original tokens with no smoke-test regression.
- You know at least two situations where you should stop compressing.

---

## Read next

- [02-model-routing.md](02-model-routing.md)
- Doc: [../../docs/02-optimization-techniques.md](../../docs/02-optimization-techniques.md)
