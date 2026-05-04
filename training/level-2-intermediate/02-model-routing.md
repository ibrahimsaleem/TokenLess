# Lesson: model routing

## Decision pattern

1. Classify the task: extraction, rewrite, codegen, multi-file architecture, safety review.
2. Pick the **cheapest** tier that passes a small golden eval.
3. Escalate only on **failure signals** (unit tests, judge model, human spot-check).

## References

- [../../guidelines/MODEL-SELECTION-GUIDE.md](../../guidelines/MODEL-SELECTION-GUIDE.md)  
- Pricing table in `tokenwatch.py` (compare with live provider pages before budgeting).

## Read next

- [03-prompt-caching.md](03-prompt-caching.md)
