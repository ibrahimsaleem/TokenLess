"""
compressor.py — Multi-strategy prompt compressor for the TokenLess LiteLLM Gateway.

Pipeline (applied in order):
  1. Whitespace normalization
  2. Filler-phrase removal  (politeness preambles, AI meta-commentary)
  3. Verbose → concise word substitutions
  4. Extractive sentence scoring  (TF-based, for inputs >200 words)
  5. LLMLingua (optional — install: pip install llmlingua)

The goal is to reduce token count while keeping LLM response quality identical.
Typical savings: 15–40% heuristic, 50–80% with LLMLingua.
"""

from __future__ import annotations
import re
from typing import Optional


class PromptCompressor:
    # ── Filler phrases to strip ─────────────────────────────────────────────
    _FILLERS = [
        r"I\s+would\s+like\s+(?:you\s+)?to\s+",
        r"Could\s+you\s+(?:please\s+)?",
        r"Can\s+you\s+(?:please\s+)?",
        r"I\s+was\s+wondering\s+if\s+you\s+(?:could\s+)?",
        r"I\s+(?:am\s+)?need\s+you\s+to\s+",
        r"Please\s+help\s+me\s+(?:to\s+)?",
        r"I\s+want\s+you\s+to\s+",
        r"Could\s+you\s+kindly\s+",
        r"I\s+would\s+appreciate\s+(?:it\s+)?if\s+you\s+(?:could\s+)?",
        r"It\s+would\s+be\s+(?:really\s+)?(?:great|helpful|nice)\s+if\s+you\s+could\s+",
        r"If\s+you\s+don'?t\s+mind,?\s+",
        r"As\s+an\s+AI\s+(?:language\s+)?model,?\s*",
        r"As\s+an\s+AI,?\s*",
        r"Sure[,!]?\s+here(?:'s|\s+is)\s+",
        r"Certainly[,!]?\s+",
        r"Of\s+course[,!]?\s+",
        r"Absolutely[,!]?\s+",
        r"I'?m\s+happy\s+to\s+help\s+(?:you\s+)?(?:with\s+)?",
        r"Allow\s+me\s+to\s+",
        r"Let\s+me\s+help\s+you\s+(?:with\s+)?",
        r"I'll\s+(?:be\s+)?(?:do|try)\s+my\s+best\s+to\s+",
        r"Without\s+(?:further\s+)?ado,?\s+",
        r"To\s+answer\s+your\s+question,?\s+",
    ]

    # ── Verbose → concise substitutions ─────────────────────────────────────
    _SUBS: list[tuple[str, str]] = [
        (r"\bin\s+order\s+to\b", "to"),
        (r"\bdue\s+to\s+the\s+fact\s+that\b", "because"),
        (r"\bat\s+this\s+(?:point\s+in\s+time|moment\s+in\s+time)\b", "now"),
        (r"\bfor\s+the\s+purpose\s+of\b", "for"),
        (r"\bin\s+the\s+event\s+that\b", "if"),
        (r"\bwith\s+(?:regard|reference|respect)\s+to\b", "about"),
        (r"\bin\s+terms\s+of\b", "for"),
        (r"\ba\s+(?:large|significant|considerable)\s+number\s+of\b", "many"),
        (r"\bthe\s+majority\s+of\b", "most"),
        (r"\bprior\s+to\b", "before"),
        (r"\bsubsequent\s+to\b", "after"),
        (r"\bis\s+able\s+to\b", "can"),
        (r"\bare\s+able\s+to\b", "can"),
        (r"\bhas\s+the\s+ability\s+to\b", "can"),
        (r"\butilize[sd]?\b", "use"),
        (r"\bpurchase[sd]?\b", "buy"),
        (r"\bcommence[sd]?\b", "start"),
        (r"\bterminate[sd]?\b", "end"),
        (r"\bascertain[sd]?\b", "find out"),
        (r"\bdemonstrate[sd]?\b", "show"),
        (r"\binform[sd]?\b", "tell"),
        (r"\bmodify\b", "change"),
        (r"\bfacilitate[sd]?\b", "help"),
        (r"\binitiate[sd]?\b", "start"),
        (r"\bimplementati?on\b", "use"),
        (r"\bfunctionality\b", "feature"),
        (r"\badditionally,?\s*", "also, "),
        (r"\bfurthermore,?\s*", "also, "),
        (r"\bnevertheless,?\s*", "but "),
        (r"\bconsequently,?\s*", "so "),
        (r"\bsubsequently,?\s*", "then "),
    ]

    # ── Stopwords for sentence scoring ──────────────────────────────────────
    _STOP = frozenset({
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "must", "can", "to", "of", "in", "on",
        "at", "by", "for", "with", "about", "as", "into", "and", "or",
        "but", "not", "this", "that", "it", "its", "they", "their", "there",
        "then", "than", "so", "if", "from", "up", "out", "we", "you", "i",
        "he", "she", "my", "your", "our", "me", "him", "her", "us", "them",
    })

    def __init__(self, use_llmlingua: bool = True):
        self._lingua = None
        if use_llmlingua:
            self._lingua = self._try_load_lingua()

    def _try_load_lingua(self):
        try:
            from llmlingua import PromptCompressor as LinguaCompressor
            return LinguaCompressor(
                model_name="microsoft/llmlingua-2-xlm-roberta-large-meetingbank",
                use_llmlingua2=True,
                device_map="cpu",
            )
        except Exception:
            return None

    # ── Public API ──────────────────────────────────────────────────────────

    def compress(self, text: str, target_ratio: float = 0.6) -> str:
        """
        Apply full compression pipeline.
        target_ratio: fraction of original tokens to aim for (0.6 = keep 60%).
        """
        result = self._heuristic(text)

        # If LLMLingua is available and text is still long, apply neural compression
        if self._lingua and len(result.split()) > 80:
            try:
                compressed = self._lingua.compress_prompt(
                    result,
                    rate=target_ratio,
                    force_tokens=["\n", "?", "!", "."],
                )
                result = compressed.get("compressed_prompt", result)
            except Exception:
                pass   # fall back to heuristic result

        return result.strip()

    def stats(self, original: str, compressed: str) -> dict:
        orig_w = len(original.split())
        comp_w = len(compressed.split())
        saved = max(0, orig_w - comp_w)
        return {
            "original_words": orig_w,
            "compressed_words": comp_w,
            "words_saved": saved,
            "reduction_pct": round(saved / orig_w * 100, 1) if orig_w else 0.0,
            "using_llmlingua": self._lingua is not None,
        }

    # ── Internal pipeline ───────────────────────────────────────────────────

    def _heuristic(self, text: str) -> str:
        t = text

        # Step 1 — normalize whitespace
        t = re.sub(r"[ \t]+", " ", t)
        t = re.sub(r"\n{3,}", "\n\n", t)

        # Step 2 — strip filler phrases
        for pat in self._FILLERS:
            t = re.sub(pat, "", t, flags=re.IGNORECASE)

        # Step 3 — verbose → concise substitutions
        for pat, repl in self._SUBS:
            t = re.sub(pat, repl, t, flags=re.IGNORECASE)

        # Step 4 — clean up artefacts from stripping
        t = re.sub(r"\s+([.,!?;:])", r"\1", t)
        t = re.sub(r"\.{4,}", "...", t)
        t = re.sub(r"[ \t]+", " ", t)
        t = re.sub(r"\n[ \t]+", "\n", t)

        # Step 5 — extractive compression for long inputs
        if len(t.split()) > 200:
            t = self._extractive(t, keep_ratio=0.75)

        return t.strip()

    def _extractive(self, text: str, keep_ratio: float = 0.75) -> str:
        """Keep the highest-scoring sentences using TF-based importance."""
        # Split into sentences preserving paragraph breaks
        paragraphs = text.split("\n\n")
        result_parts: list[str] = []

        for para in paragraphs:
            sentences = re.split(r"(?<=[.!?])\s+", para.strip())
            if len(sentences) <= 2:
                result_parts.append(para)
                continue

            # Word frequency in this paragraph
            words = re.findall(r"\b\w+\b", para.lower())
            freq: dict[str, int] = {}
            for w in words:
                if w not in self._STOP and len(w) > 2:
                    freq[w] = freq.get(w, 0) + 1

            # Score each sentence
            scores: list[float] = []
            for sent in sentences:
                sent_words = re.findall(r"\b\w+\b", sent.lower())
                content_words = [w for w in sent_words if w not in self._STOP and len(w) > 2]
                if not content_words:
                    scores.append(0.0)
                    continue
                score = sum(freq.get(w, 0) for w in content_words) / len(content_words)
                scores.append(score)

            # Keep top-scoring sentences
            n_keep = max(2, round(len(sentences) * keep_ratio))
            threshold = sorted(scores, reverse=True)[min(n_keep - 1, len(scores) - 1)]
            kept = [s for s, sc in zip(sentences, scores) if sc >= threshold]
            result_parts.append(" ".join(kept))

        return "\n\n".join(result_parts)
