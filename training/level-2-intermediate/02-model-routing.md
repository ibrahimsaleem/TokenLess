# Lesson: Model routing

**Level:** Intermediate — Level 2  
**Time:** 30 minutes  
**Prerequisites:** [01-prompt-compression.md](01-prompt-compression.md)

---

## Learning objectives

By the end of this lesson you will be able to:

1. Define a task taxonomy for your application and assign each task type to a model tier.
2. Implement a basic routing function in Python.
3. Choose an escalation signal (test result, judge model, or human spot-check).
4. Measure model tier mix in production using TokenWatch task labels.

---

## Why routing reduces cost (and often improves quality)

Not every task needs the most capable model. A classification request ("Is this message spam or not?") is structurally simpler than a multi-file refactor ("Refactor the auth module to use JWT, update all callers, and write tests"). Sending the classification to a frontier model wastes money; sending the refactor to a small model likely produces poor output.

The key insight: **quality is task-specific, not model-specific in absolute terms.** A small model can match a large model on simple tasks and be 10–30× cheaper per token.

---

## Define a task taxonomy

Start by listing the distinct request types your application handles. Map each to a tier:

| Task type | Characteristics | Suggested tier |
|-----------|----------------|----------------|
| Classification / routing | Short input, enumerated output, no reasoning chain | Fast/small |
| Extraction | Structured output from a defined schema | Fast/small |
| Short summarization (<2 pages) | Prose input, prose output, no cross-document reasoning | Fast/small |
| Code completion (single function) | Code context, local scope | Mid |
| Code review (file or PR) | Code context, broader scope, judgment required | Mid |
| Q&A with retrieved context | Retrieval + reasoning | Mid |
| Multi-file architecture / refactor | Broad context, cross-file dependencies | Large only on escalation |
| Safety review / high-stakes output | Alignment and judgment requirements | Large |

Your taxonomy will differ based on your application. Start with 3 tiers (small, mid, large) and refine.

---

## Implementation sketch

```python
SMALL  = "claude-haiku-4-5-20251001"   # or gpt-4.1-nano, gemini-flash
MID    = "claude-sonnet-4-5-20251015"  # or gpt-4.1, gemini-pro
LARGE  = "claude-opus-4-5-20251101"    # or gpt-5, gemini-ultra

SMALL_TASKS  = {"classify", "extract", "route", "summarize_short"}
MID_TASKS    = {"codegen", "review", "qa", "summarize_long"}
# Everything else → escalate to large, but only after mid attempt

def route(task_type: str, escalation: bool = False) -> str:
    if task_type in SMALL_TASKS:
        return SMALL
    if task_type in MID_TASKS or not escalation:
        return MID
    return LARGE

def call_with_routing(task_type: str, prompt: str, evaluator=None) -> str:
    model = route(task_type)
    response = call_llm(model, prompt)
    if evaluator and not evaluator(response):
        # Escalate once
        model = route(task_type, escalation=True)
        response = call_llm(model, prompt)
    return response
```

Label each call with `task_label=task_type` when recording to TokenWatch. This makes the tier mix visible in the dashboard.

---

## Choosing an escalation signal

Escalation should be triggered by **objective failure**, not by "I feel uncertain":

1. **Test / schema validation** — the output failed to parse as valid JSON, or failed a unit test. Objective and automatable.
2. **Judge model (LLM-as-evaluator)** — a fast cheap model grades the response against a rubric. Returns pass/fail. Adds one small-model call.
3. **Human spot-check** — sampled asynchronously. Provides ground truth but is not fast enough to gate synchronous requests.

Avoid escalating by default "to be safe." Track your escalation rate; above 15–20% for a given task type, consider recalibrating the tier assignment rather than escalating more.

---

## Measurement

Add `task_label` to every `record_usage` call in TokenWatch:

```python
monitor.record_usage(model, input_tokens, output_tokens, task_label=task_type)
```

After a week, run the dashboard and review the model tier mix per task type. Questions to answer:
- What fraction of `classify` tasks are still going to MID or LARGE? (Should be near zero.)
- What is the escalation rate for `codegen`?
- Which task type has the highest cost per call? Is it appropriate?

---

## Common misconceptions

**"I should default to the largest model for anything complex."** "Complex" is not the same as "requires the largest model." Most multi-step problems can be decomposed into subtasks most of which are simple.

**"Routing adds latency."** A routing lookup or classification step takes milliseconds. The latency savings from routing to a faster model vastly outweigh any classification overhead.

**"Small models are not good enough."** Small models have improved dramatically. Run an evaluation before dismissing them. Many teams discover that small models pass evaluation on 80%+ of their task types.

---

## You know this lesson when…

- You have defined a task taxonomy for at least one feature in your application.
- You have a routing function (even a simple if/else) in code.
- You track model tier mix per task type using TokenWatch labels and review it weekly.

---

## Read next

- [03-prompt-caching.md](03-prompt-caching.md)
- Guidelines: [../../guidelines/MODEL-SELECTION-GUIDE.md](../../guidelines/MODEL-SELECTION-GUIDE.md)
