"""
gateway.py — LiteLLM Gateway core.

Orchestrates: guardrails → compression → token counting → LLM call → tracking.
All LLM calls go through litellm.completion() — swap the model string to
switch providers with zero other code changes.

LiteLLM features exercised:
  - litellm.completion()            unified API for 100+ models
  - litellm.token_counter()         per-model accurate token counts
  - litellm.completion_cost()       post-call cost in USD
  - litellm.cache                   in-memory response cache
  - litellm.callbacks               custom logging callback
  - litellm.get_model_info()        context window / pricing metadata
"""

from __future__ import annotations
import os
import time
import logging
from dataclasses import dataclass, field
from typing import Optional

import litellm
from litellm import Cache

from guardrails import GuardrailsChecker, GuardrailResult
from compressor import PromptCompressor
from token_tracker import TokenTracker, TokenCounts

logger = logging.getLogger(__name__)

# Enable LiteLLM in-memory response cache
litellm.cache = Cache(type="local")
litellm.set_verbose = False   # flip to True for raw request/response debugging


# ── Custom LiteLLM callback (logs every call) ────────────────────────────────
class _GatewayLogger(litellm.integrations.custom_logger.CustomLogger):
    def log_success_event(self, kwargs, response_obj, start_time, end_time):
        model = kwargs.get("model", "?")
        tokens = getattr(getattr(response_obj, "usage", None), "total_tokens", 0)
        logger.debug("litellm success | model=%s tokens=%d", model, tokens)

    def log_failure_event(self, kwargs, response_obj, start_time, end_time):
        logger.warning("litellm failure | model=%s error=%s", kwargs.get("model"), response_obj)


litellm.callbacks = [_GatewayLogger()]


# ── Data structures ──────────────────────────────────────────────────────────

@dataclass
class QueryResult:
    response: Optional[str]
    guardrails: GuardrailResult
    orig_tokens: int
    compressed_tokens: int
    tokens_saved: int
    compression_pct: float
    orig_compressed_input: str        # the compressed text sent to the model
    response_tokens: int
    total_tokens: int
    cost_usd: float
    cost_saved_usd: float
    latency_ms: float
    from_cache: bool
    context_utilization_pct: float


@dataclass
class ChatMessage:
    role: str
    content: str


# ── Gateway class ────────────────────────────────────────────────────────────

class LiteLLMGateway:
    def __init__(
        self,
        model: Optional[str] = None,
        max_history_turns: int = 8,
        daily_budget: float = 2.0,
        use_llmlingua: bool = False,   # set True if llmlingua is installed
    ):
        self.model = model or os.getenv("LITELLM_MODEL", "claude-haiku-4-5-20251001")
        self.max_history_turns = max_history_turns

        self.guardrails = GuardrailsChecker()
        self.compressor = PromptCompressor(use_llmlingua=use_llmlingua)
        self.tracker = TokenTracker(model=self.model, daily_budget=daily_budget)

        self.history: list[ChatMessage] = []
        self.system_prompt: str = (
            "You are a helpful, concise AI assistant. "
            "Provide clear, accurate answers. Be direct."
        )

    # ── Main entry point ─────────────────────────────────────────────────────

    def chat(self, user_input: str) -> QueryResult:
        """Process one user turn through the full gateway pipeline."""

        # ── 1. Guardrails ───────────────────────────────────────────────────
        gr = self.guardrails.check(user_input)
        if gr.blocked:
            self.tracker.record_blocked()
            return QueryResult(
                response=None,
                guardrails=gr,
                orig_tokens=self.tracker.count_text(user_input),
                compressed_tokens=0,
                tokens_saved=0,
                compression_pct=0.0,
                orig_compressed_input="",
                response_tokens=0,
                total_tokens=0,
                cost_usd=0.0,
                cost_saved_usd=0.0,
                latency_ms=0.0,
                from_cache=False,
                context_utilization_pct=0.0,
            )

        # ── 2. Build message list with history ──────────────────────────────
        messages_orig = self._build_messages(user_input)
        orig_tokens = self.tracker.count_messages(messages_orig)

        # ── 3. Compress user input ──────────────────────────────────────────
        compressed_input = self.compressor.compress(user_input)
        messages_compressed = self._build_messages(compressed_input)
        compressed_tokens = self.tracker.count_messages(messages_compressed)

        tokens_saved = max(0, orig_tokens - compressed_tokens)
        compression_pct = (tokens_saved / orig_tokens * 100) if orig_tokens > 0 else 0.0
        cost_saved = self.tracker.estimate_cost(tokens_saved)

        # ── 4. Call LiteLLM ─────────────────────────────────────────────────
        t0 = time.perf_counter()
        try:
            resp = litellm.completion(
                model=self.model,
                messages=messages_compressed,
                temperature=0.7,
                max_tokens=1024,
                caching=True,   # activates litellm.cache for identical requests
            )
        except litellm.exceptions.AuthenticationError as e:
            return self._error_result(gr, orig_tokens, compressed_tokens, tokens_saved,
                                      cost_saved, compression_pct, compressed_input,
                                      f"Auth error — check your API key: {e}")
        except litellm.exceptions.RateLimitError as e:
            return self._error_result(gr, orig_tokens, compressed_tokens, tokens_saved,
                                      cost_saved, compression_pct, compressed_input,
                                      f"Rate limit hit: {e}")
        except Exception as e:
            return self._error_result(gr, orig_tokens, compressed_tokens, tokens_saved,
                                      cost_saved, compression_pct, compressed_input,
                                      f"LiteLLM error: {e}")

        latency_ms = (time.perf_counter() - t0) * 1000

        # ── 5. Extract response ─────────────────────────────────────────────
        assistant_text = resp.choices[0].message.content or ""
        from_cache = getattr(resp, "_hidden_params", {}).get("cache_hit", False)

        if from_cache:
            self.tracker.record_cache_hit()

        counts: TokenCounts = self.tracker.record_call(
            resp,
            tokens_saved=tokens_saved,
            cost_saved=cost_saved,
            task_label="chat",
        )

        # ── 6. Update history with original (uncompressed) text ─────────────
        # We store original so context builds naturally across turns.
        self.history.append(ChatMessage("user", user_input))
        self.history.append(ChatMessage("assistant", assistant_text))

        return QueryResult(
            response=assistant_text,
            guardrails=gr,
            orig_tokens=orig_tokens,
            compressed_tokens=compressed_tokens,
            tokens_saved=tokens_saved,
            compression_pct=round(compression_pct, 1),
            orig_compressed_input=compressed_input,
            response_tokens=counts.output_tokens,
            total_tokens=counts.total_tokens,
            cost_usd=counts.cost_usd,
            cost_saved_usd=cost_saved,
            latency_ms=round(latency_ms, 1),
            from_cache=from_cache,
            context_utilization_pct=self.tracker.utilization_pct(compressed_tokens),
        )

    def clear_history(self):
        self.history.clear()

    @property
    def session(self):
        return self.tracker.session

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _build_messages(self, user_input: str) -> list[dict]:
        msgs: list[dict] = [{"role": "system", "content": self.system_prompt}]
        # Keep last N turns (each turn = 2 messages: user + assistant)
        recent = self.history[-(self.max_history_turns * 2):]
        for m in recent:
            msgs.append({"role": m.role, "content": m.content})
        msgs.append({"role": "user", "content": user_input})
        return msgs

    def _error_result(self, gr, orig_tokens, compressed_tokens, tokens_saved,
                      cost_saved, compression_pct, compressed_input, error_msg) -> QueryResult:
        return QueryResult(
            response=f"[Gateway Error] {error_msg}",
            guardrails=gr,
            orig_tokens=orig_tokens,
            compressed_tokens=compressed_tokens,
            tokens_saved=tokens_saved,
            compression_pct=round(compression_pct, 1),
            orig_compressed_input=compressed_input,
            response_tokens=0,
            total_tokens=0,
            cost_usd=0.0,
            cost_saved_usd=cost_saved,
            latency_ms=0.0,
            from_cache=False,
            context_utilization_pct=0.0,
        )
