#!/usr/bin/env python3
"""Rough token estimate for a UTF-8 file or stdin (no third-party deps).

Uses chars/4 heuristic (~English average). For exact OpenAI counts install tiktoken separately.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, int(len(text) / 4))


def main() -> None:
    p = argparse.ArgumentParser(description="Rough token count estimate (len/4 heuristic).")
    p.add_argument("path", nargs="?", help="UTF-8 text file; omit to read stdin")
    p.add_argument("--json", action="store_true", help="print chars, est_tokens")
    args = p.parse_args()

    if args.path:
        raw = Path(args.path).read_text(encoding="utf-8", errors="replace")
    else:
        raw = sys.stdin.read()

    chars = len(raw)
    est = estimate_tokens(raw)
    if args.json:
        print(f'{{"chars": {chars}, "estimated_tokens": {est}}}')
    else:
        print(f"characters: {chars}")
        print(f"estimated_tokens (~chars/4): {est}")


if __name__ == "__main__":
    main()
