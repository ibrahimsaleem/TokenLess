# Lesson: context windows

The **context window** is the maximum tokens the model can use in one shot for input + tools + history (and the provider’s reserved output budget).

## Failure modes

- Truncation drops early instructions.
- The model attends poorly to “middle” content in very long contexts (known phenomenon—still assume discipline).

## Product rule of thumb

Design so **typical** requests sit at **well below** the advertised limit; keep headroom for tools, retries, and user growth.

## Read next

- [03-billing-basics.md](03-billing-basics.md)  
- Reference: [../../guidelines/CONTEXT-WINDOW-GUIDE.md](../../guidelines/CONTEXT-WINDOW-GUIDE.md)
