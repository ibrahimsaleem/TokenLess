# Context window guide

Context window = maximum tokens the model can attend to in **one** request, including system instructions, tools, retrieved documents, conversation history, and the provider’s reserved space for the answer.

## Why tables drift

Providers ship new **snapshots** and context lengths frequently. Treat numbers below as **order-of-magnitude planning** only. Before launch, copy limits from the official model card for **your** exact model string.

## Planning ranges (verify externally)

| Family | Typical planning range | Notes |
|--------|------------------------|-------|
| Frontier Claude (Sonnet-class) | ~200k context common; some SKUs advertise 1M | Tool + history eat the same budget |
| Claude Haiku | Often lower than largest Sonnet | Good for high-volume |
| GPT-4.1 / GPT-5 class | High context variants exist | Check per deployment |
| Gemini Flash / Pro | Flash cheaper; verify input pricing for long prompts | Great for batch summarization |
| Local / OSS 7B–13B | 8k–32k typical | Harder limits; tighter prompts |

## Engineering rules

1. **Reserve output budget**: if the window is 200k but you need 8k tokens of answer, stop accumulating input at ~192k (plus provider overhead—measure).
2. **Tool definitions count**: large JSON schemas are tokens.
3. **Prefer retrieval** over “just increase context”.
4. **Test truncation behavior**: what does your SDK do when you exceed limits?

## Links

- Anthropic model docs: https://platform.claude.com/docs/en/about-claude/models/overview  
- OpenAI model docs: https://platform.openai.com/docs/models  
- Google Gemini docs: https://ai.google.dev/gemini-api/docs  

## Related

- [01-core-concepts.md](../docs/01-core-concepts.md)  
- [SYSTEM-PROMPT-GUIDE.md](SYSTEM-PROMPT-GUIDE.md)
