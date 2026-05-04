# IDE extensions (VS Code family): token-aware usage

Extensions such as **Cline**, **Continue**, and others attach context from your editor. Patterns mirror Copilot:

## Open tabs

- Fewer open files reduces accidental inclusion in context.
- If the extension shows a **token meter**, use it to decide when to summarize or start a new task.

## Indexing

- Allow or trigger **workspace indexing** where supported so retrieval replaces bulk reads.

## Prompt / instruction files

- Centralize repeated guidance in the extension’s **instructions** or project prompt file instead of pasting it in chat every time.

## Model selection

- Route trivial edits to **smaller** models (local or API) when quality remains acceptable.

## Privacy and noise

- Exclude secrets, dumps, and generated artifacts via `.gitignore`, `files.exclude`, and extension-specific ignore settings—this cuts both **risk** and **tokens**.
