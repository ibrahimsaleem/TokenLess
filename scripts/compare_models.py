#!/usr/bin/env python3
"""CLI wrapper for TokenWatch.compare_models."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tokenwatch import TokenWatch  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description="Compare model costs for fixed token counts.")
    ap.add_argument("--in", dest="inp", type=int, required=True, help="input tokens")
    ap.add_argument("--out", dest="outp", type=int, required=True, help="output tokens")
    ap.add_argument("--top", type=int, default=15, help="show N cheapest models")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    m = TokenWatch(storage_path=str(ROOT / ".tokenwatch_scripts"))
    rows = m.compare_models(args.inp, args.outp)[: args.top]
    if args.json:
        print(json.dumps(rows, indent=2))
        return
    w = max(len(r["model"]) for r in rows)
    for r in rows:
        print(f"{r['model']:<{w}}  ${r['cost_usd']:.8f}  ({r['provider']})")


if __name__ == "__main__":
    main()
