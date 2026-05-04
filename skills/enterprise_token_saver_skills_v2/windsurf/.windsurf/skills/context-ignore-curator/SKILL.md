---
name: context-ignore-curator
description: Create or improve .contextignore, .windsurfignore, .code-review-graphignore, and similar ignore files so agents avoid generated or low-value context.
---

# Context Ignore Curator

## Purpose
Prevent AI coding tools from reading files that are expensive and low-value.

## Always Consider Ignoring
```gitignore
node_modules/**
dist/**
build/**
coverage/**
target/**
.next/**
.nuxt/**
.venv/**
venv/**
__pycache__/**
*.pyc
*.min.js
*.min.css
*.map
*.lock
package-lock.json
yarn.lock
pnpm-lock.yaml
Cargo.lock
poetry.lock
vendor/**
generated/**
*.generated.*
*.snap
*.log
*.csv
*.parquet
*.sqlite
*.db
.env
.env.*
secrets/**
```

## Do Not Blindly Ignore
- lockfiles when dependency resolution is the task
- generated API clients when debugging generated behavior
- snapshots when snapshot tests fail
- logs when investigating production incidents

## Output Format
Return proposed ignore files:

```md
## .contextignore
...

## .code-review-graphignore
...

## .windsurfignore
...

## Reasoning
- ...
```
