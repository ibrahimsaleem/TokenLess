"""
token_tracker.py — Token counting and cost tracking via LiteLLM.

Uses litellm.token_counter() for model-accurate counts and integrates with
the TokenWatch library from this repo for session budget tracking.
"""

from __future__ import annotations
import sys
import os
from dataclasses import dataclass, field
from typing import Optional

import litellm

# Try to import TokenWatch from parent repo
_REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

try:
    from tokenwatch import TokenWatch
    _HAS_TOKENWATCH = True
except ImportError:
    _HAS_TOKENWATCH = False


@dataclass
class TokenCounts:
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost_usd: float
    model: str


@dataclass
class SessionStats:
    total_input: int = 0
    total_output: int = 0
    total_cost: float = 0.0
    tokens_saved: int = 0
    cost_saved: float = 0.0
    queries: int = 0
    cache_hits: int = 0
    blocked: int = 0


class TokenTracker:
    """
    LiteLLM-powered token counting with optional TokenWatch budget integration.

    Key LiteLLM APIs used:
      - litellm.token_counter(model, text | messages)  — per-model accurate counts
      - litellm.completion_cost(completion_response)    — actual post-call cost
      - litellm.get_model_info(model)                  — context window, pricing
    """

    # Fallback pricing ($/1M input tokens) if litellm doesn't know the model
    _PRICING_FALLBACK: dict[str, float] = {
        "gpt-3.5-turbo": 0.50,
        "gpt-4": 30.00,
        "gpt-4-turbo": 10.00,
        "gpt-4o": 2.50,
        "gpt-4o-mini": 0.15,
        "claude-3-haiku-20240307": 0.25,
        "claude-haiku-4-5-20251001": 0.80,
        "claude-3-sonnet-20240229": 3.00,
        "claude-3-5-sonnet-20241022": 3.00,
        "claude-sonnet-4-6": 3.00,
        "claude-3-opus-20240229": 15.00,
        "gemini-pro": 0.50,
        "gemini-1.5-flash": 0.075,
        "ollama/mistral": 0.00,
        "ollama/llama3": 0.00,
    }

    def __init__(self, model: str = "claude-haiku-4-5-20251001", daily_budget: float = 1.0):
        self.model = model
        self.session = SessionStats()

        # Wire up TokenWatch if available
        self._tw: Optional[object] = None
        if _HAS_TOKENWATCH:
            try:
                self._tw = TokenWatch()
                self._tw.set_budget(daily_usd=daily_budget)
            except Exception:
                self._tw = None

    # ── Token counting ──────────────────────────────────────────────────────

    def count_text(self, text: str) -> int:
        """Count tokens for a plain string (model-accurate via LiteLLM)."""
        try:
            return litellm.token_counter(model=self.model, text=text)
        except Exception:
            return max(1, len(text) // 4)  # ~4 chars/token fallback

    def count_messages(self, messages: list[dict]) -> int:
        """Count tokens for a full messages list (includes role overhead)."""
        try:
            return litellm.token_counter(model=self.model, messages=messages)
        except Exception:
            return sum(max(1, len(m.get("content", "")) // 4) for m in messages)

    # ── Cost estimation ─────────────────────────────────────────────────────

    def estimate_cost(self, input_tokens: int, output_tokens: int = 0) -> float:
        """Pre-call cost estimate in USD."""
        try:
            # litellm.cost_per_token returns (prompt_cost, completion_cost)
            p_cost, c_cost = litellm.cost_per_token(
                model=self.model,
                prompt_tokens=input_tokens,
                completion_tokens=output_tokens,
            )
            return p_cost + c_cost
        except Exception:
            rate = self._PRICING_FALLBACK.get(self.model, 1.0)
            return ((input_tokens + output_tokens) / 1_000_000) * rate

    def actual_cost(self, completion_response) -> float:
        """Extract actual cost from a completed litellm response."""
        try:
            return litellm.completion_cost(completion_response=completion_response)
        except Exception:
            usage = getattr(completion_response, "usage", None)
            if usage:
                return self.estimate_cost(
                    getattr(usage, "prompt_tokens", 0),
                    getattr(usage, "completion_tokens", 0),
                )
            return 0.0

    # ── Context window info ─────────────────────────────────────────────────

    def context_window(self) -> int:
        try:
            info = litellm.get_model_info(self.model)
            return info.get("max_input_tokens") or info.get("max_tokens", 4096)
        except Exception:
            return 4096

    def utilization_pct(self, token_count: int) -> float:
        cw = self.context_window()
        return round(token_count / cw * 100, 1) if cw else 0.0

    # ── Session tracking ────────────────────────────────────────────────────

    def record_call(
        self,
        completion_response,
        tokens_saved: int = 0,
        cost_saved: float = 0.0,
        task_label: str = "",
    ) -> TokenCounts:
        usage = getattr(completion_response, "usage", None)
        inp = getattr(usage, "prompt_tokens", 0) if usage else 0
        out = getattr(usage, "completion_tokens", 0) if usage else 0
        cost = self.actual_cost(completion_response)

        self.session.total_input += inp
        self.session.total_output += out
        self.session.total_cost += cost
        self.session.tokens_saved += tokens_saved
        self.session.cost_saved += cost_saved
        self.session.queries += 1

        # Forward to TokenWatch for persistent budget tracking
        if self._tw:
            try:
                self._tw.record_usage(
                    model=self.model,
                    input_tokens=inp,
                    output_tokens=out,
                    task_label=task_label or "chat",
                )
            except Exception:
                pass

        return TokenCounts(
            input_tokens=inp,
            output_tokens=out,
            total_tokens=inp + out,
            cost_usd=cost,
            model=self.model,
        )

    def record_blocked(self):
        self.session.blocked += 1

    def record_cache_hit(self):
        self.session.cache_hits += 1

    def budget_status(self) -> Optional[str]:
        """Return TokenWatch budget alert string if over budget."""
        if not self._tw:
            return None
        try:
            alerts = self._tw.check_budget_alerts()
            return alerts if alerts else None
        except Exception:
            return None
