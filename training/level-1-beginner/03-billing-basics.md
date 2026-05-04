# Lesson: billing basics

## Input vs output

Almost all cloud LLM APIs bill **prompt tokens** and **completion tokens** separately. Output is often more expensive per token.

## Caching (where available)

Some providers discount **repeated static prefixes**. You must structure requests deliberately—read the current pricing page.

## Subscriptions vs metered APIs

- IDE assistants may bundle usage differently than raw APIs.
- Still: **smaller context → faster → cheaper feeling → fewer errors**.

## Read next

- [04-first-optimizations.md](04-first-optimizations.md)  
- Optional: run `python ../scripts/compare_models.py --help` after Level 2 setup.
