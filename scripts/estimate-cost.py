#!/usr/bin/env python3
"""CLI wrapper for TokenWatch.estimate_cost."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Repo root: scripts/ -> parent
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tokenwatch import TokenWatch  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description="Estimate USD cost for a hypothetical call.")
    ap.add_argument("model", help="Model id as in tokenwatch.PROVIDER_PRICING")
    ap.add_argument("--in", dest="inp", type=int, required=True, help="input tokens")
    ap.add_argument("--out", dest="outp", type=int, required=True, help="output tokens")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    m = TokenWatch(storage_path=str(ROOT / ".tokenwatch_scripts"))
    res = m.estimate_cost(args.model, args.inp, args.outp)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        if "error" in res:
            print(res["error"], file=sys.stderr)
            sys.exit(1)
        print(f"model: {res['model']}")
        print(f"provider: {res['provider']}")
        print(f"estimated_cost_usd: {res['estimated_cost_usd']}")


if __name__ == "__main__":
    main()
