#!/usr/bin/env python3
"""
app.py — TokenLess LiteLLM Gateway Chat Demo

Terminal chat interface showcasing:
  ✦ LiteLLM unified gateway (swap model with one env var)
  ✦ Prompt injection & PII guardrails (pre-flight safety layer)
  ✦ Prompt compression (heuristic + optional LLMLingua)
  ✦ Accurate per-model token counting via litellm.token_counter()
  ✦ Real-time cost tracking via litellm.completion_cost()
  ✦ Response caching via litellm.cache
  ✦ Session budget integration via TokenWatch

Usage:
    python app.py
    python app.py --model gpt-4o-mini
    python app.py --model ollama/mistral          # free, no API key
    python app.py --model claude-haiku-4-5-20251001
"""

from __future__ import annotations
import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load .env from this directory
load_dotenv(Path(__file__).parent / ".env")

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich.rule import Rule
from rich.markup import escape
from rich import box

from gateway import LiteLLMGateway, QueryResult
from guardrails import CheckResult

console = Console()

# ── Colour palette ────────────────────────────────────────────────────────────
C_BRAND   = "bold cyan"
C_USER    = "bold white"
C_AI      = "green"
C_WARN    = "yellow"
C_ERROR   = "bold red"
C_PASS    = "green"
C_BLOCK   = "bold red"
C_DIM     = "dim"
C_GOLD    = "bold yellow"
C_HEADER  = "bold blue"


# ── UI helpers ────────────────────────────────────────────────────────────────

def print_banner(model: str):
    console.print()
    console.print(Panel(
        Text.from_markup(
            f"[{C_BRAND}]TokenLess LiteLLM Gateway[/{C_BRAND}]\n"
            f"[{C_DIM}]Prompt Safety · Token Compression · Cost Tracking · Smart Caching[/{C_DIM}]\n"
            f"[{C_DIM}]Model: [white]{model}[/white]  │  Type [bold]quit[/bold] to exit, "
            f"[bold]clear[/bold] to reset history[/{C_DIM}]"
        ),
        border_style="cyan",
        padding=(0, 2),
    ))
    console.print()


def _severity_icon(r: CheckResult) -> str:
    if r.severity == "block":
        return f"[{C_BLOCK}]✗ BLOCKED[/{C_BLOCK}]"
    if r.severity == "warn":
        return f"[{C_WARN}]⚠ WARN   [/{C_WARN}]"
    return f"[{C_PASS}]✓ OK     [/{C_PASS}]"


def print_metrics(result: QueryResult, query_num: int):
    """Render the metrics panels after each response."""

    # ── Guardrails panel ──────────────────────────────────────────────────
    gr_table = Table(show_header=False, box=None, padding=(0, 1))
    gr_table.add_column("icon",  no_wrap=True)
    gr_table.add_column("name",  style="bold", no_wrap=True)
    gr_table.add_column("msg",   style=C_DIM)

    for c in result.guardrails.checks:
        gr_table.add_row(_severity_icon(c), c.name, c.message)

    guardrail_panel = Panel(
        gr_table,
        title=f"[{C_HEADER}]GUARDRAILS[/{C_HEADER}]",
        border_style="blue",
        padding=(0, 1),
    )

    # ── Token / cost panel ────────────────────────────────────────────────
    tok_table = Table(show_header=False, box=None, padding=(0, 1))
    tok_table.add_column("label", style="bold", no_wrap=True)
    tok_table.add_column("value", no_wrap=True)

    def _fmt_cost(c: float) -> str:
        if c == 0:
            return "[dim]$0.000000[/dim]"
        return f"[green]${c:.6f}[/green]"

    cache_tag = " [bold cyan](CACHED — 0 tokens!)[/bold cyan]" if result.from_cache else ""

    tok_table.add_row("Original tokens",    f"[white]{result.orig_tokens:,}[/white]")
    tok_table.add_row("Compressed tokens",  f"[green]{result.compressed_tokens:,}[/green]")
    tok_table.add_row(
        "Tokens saved",
        f"[{C_GOLD}]{result.tokens_saved:,}  ({result.compression_pct}% reduction)[/{C_GOLD}]",
    )
    tok_table.add_row("─" * 18, "─" * 20)
    tok_table.add_row("Cost (orig est.)",   _fmt_cost(
        result.cost_usd + result.cost_saved_usd))
    tok_table.add_row("Actual cost",        _fmt_cost(result.cost_usd) + cache_tag)
    tok_table.add_row("Cost saved",         f"[{C_GOLD}]{_fmt_cost(result.cost_saved_usd)}[/{C_GOLD}]")
    tok_table.add_row("─" * 18, "─" * 20)
    tok_table.add_row("Response tokens",    f"[dim]{result.response_tokens:,}[/dim]")
    tok_table.add_row("Context usage",      f"[dim]{result.context_utilization_pct}% of window[/dim]")
    tok_table.add_row("Latency",            f"[dim]{result.latency_ms:.0f} ms[/dim]")

    token_panel = Panel(
        tok_table,
        title=f"[{C_HEADER}]TOKEN OPTIMIZATION[/{C_HEADER}]",
        border_style="blue",
        padding=(0, 1),
    )

    console.print(Columns([guardrail_panel, token_panel], equal=True, expand=True))


def print_session_bar(gw: LiteLLMGateway):
    s = gw.session
    parts: list[str] = [
        f"[{C_DIM}]Session #{s.queries}[/{C_DIM}]",
        f"Tokens used: [{C_GOLD}]{s.total_input + s.total_output:,}[/{C_GOLD}]",
        f"Saved: [{C_GOLD}]{s.tokens_saved:,}[/{C_GOLD}]",
        f"Total cost: [green]${s.total_cost:.6f}[/green]",
        f"Cost saved: [{C_GOLD}]${s.cost_saved:.6f}[/{C_GOLD}]",
    ]
    if s.cache_hits:
        parts.append(f"Cache hits: [cyan]{s.cache_hits}[/cyan]")
    if s.blocked:
        parts.append(f"Blocked: [{C_BLOCK}]{s.blocked}[/{C_BLOCK}]")

    budget = gw.tracker.budget_status()
    if budget:
        parts.append(f"[{C_WARN}]⚠ {budget}[/{C_WARN}]")

    console.print(Rule(" · ".join(parts), style="dim blue"))


def print_compressed_diff(original: str, compressed: str):
    """Show what the compressor changed (only when something actually changed)."""
    if original.strip() == compressed.strip():
        return
    console.print(Panel(
        Text.from_markup(
            f"[{C_DIM}]Compressed prompt sent to model:[/{C_DIM}]\n"
            f"[italic dim]{escape(compressed[:300])}{'…' if len(compressed) > 300 else ''}[/italic dim]"
        ),
        border_style="dim",
        padding=(0, 1),
    ))


def print_blocked(result: QueryResult):
    console.print()
    console.print(Panel(
        Text.from_markup(
            f"[{C_BLOCK}]Request blocked by gateway guardrails[/{C_BLOCK}]\n\n"
            + "\n".join(
                f"  [{C_BLOCK}]✗[/{C_BLOCK}] {c.name}: {c.message}"
                for c in result.guardrails.checks
                if c.severity == "block"
            )
        ),
        border_style="red",
        title="[bold red]GUARDRAIL BLOCK[/bold red]",
    ))
    console.print()


# ── Main loop ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="TokenLess LiteLLM Gateway Demo")
    parser.add_argument("--model", default=None,
                        help="LiteLLM model string (default: $LITELLM_MODEL or claude-haiku-4-5-20251001)")
    parser.add_argument("--budget", type=float, default=2.0,
                        help="Daily budget in USD for TokenWatch (default: $2.00)")
    parser.add_argument("--llmlingua", action="store_true",
                        help="Enable LLMLingua neural compression (requires: pip install llmlingua)")
    parser.add_argument("--debug", action="store_true",
                        help="Enable LiteLLM verbose logging")
    args = parser.parse_args()

    if args.debug:
        import litellm as _ll
        _ll.set_verbose = True

    gw = LiteLLMGateway(
        model=args.model,
        daily_budget=args.budget,
        use_llmlingua=args.llmlingua,
    )

    print_banner(gw.model)

    # Show model info
    try:
        import litellm as _ll
        info = _ll.get_model_info(gw.model)
        cw = info.get("max_input_tokens") or info.get("max_tokens", "?")
        console.print(f"[{C_DIM}]Context window: {cw:,} tokens  │  "
                      f"LLMLingua: {'enabled' if gw.compressor._lingua else 'disabled (install llmlingua)'}[/{C_DIM}]")
        console.print()
    except Exception:
        pass

    query_num = 0
    while True:
        try:
            user_input = console.input(f"[{C_USER}]You >[/{C_USER}] ").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            break
        if user_input.lower() == "clear":
            gw.clear_history()
            console.print(f"[{C_DIM}]History cleared.[/{C_DIM}]")
            continue
        if user_input.lower() == "stats":
            print_session_bar(gw)
            continue

        query_num += 1
        console.print()

        # Process through gateway
        result = gw.chat(user_input)

        if result.guardrails.blocked:
            print_blocked(result)
            print_session_bar(gw)
            continue

        # Show compressed diff if anything changed
        print_compressed_diff(user_input, result.orig_compressed_input)

        # Show AI response
        if result.response and not result.response.startswith("[Gateway Error]"):
            cache_badge = " [dim cyan][cached][/dim cyan]" if result.from_cache else ""
            console.print(Panel(
                Text.from_markup(escape(result.response)),
                title=f"[{C_AI}]Assistant[/{C_AI}]{cache_badge}",
                border_style="green",
                padding=(0, 1),
            ))
        else:
            console.print(Panel(
                Text.from_markup(f"[{C_ERROR}]{escape(result.response or 'No response')}[/{C_ERROR}]"),
                border_style="red",
            ))

        console.print()

        # Metrics panels
        print_metrics(result, query_num)
        console.print()

        # Session summary bar
        print_session_bar(gw)
        console.print()

    # Exit summary
    s = gw.session
    if s.queries > 0:
        console.print()
        console.print(Panel(
            Text.from_markup(
                f"[{C_BRAND}]Session complete[/{C_BRAND}]\n"
                f"Queries: [white]{s.queries}[/white]  │  "
                f"Tokens used: [{C_GOLD}]{s.total_input + s.total_output:,}[/{C_GOLD}]  │  "
                f"Tokens saved: [{C_GOLD}]{s.tokens_saved:,}[/{C_GOLD}]\n"
                f"Total cost: [green]${s.total_cost:.6f}[/green]  │  "
                f"Cost saved: [{C_GOLD}]${s.cost_saved:.6f}[/{C_GOLD}]  │  "
                f"Cache hits: [cyan]{s.cache_hits}[/cyan]"
            ),
            border_style="cyan",
        ))


if __name__ == "__main__":
    main()
