"""
guardrails.py — Prompt safety layer for the TokenLess LiteLLM Gateway.

Checks every user message before it hits the LLM:
  1. Prompt injection detection (regex)
  2. PII scanner (email, SSN, phone, credit card)
  3. Content policy (harmful keyword filter)
  4. Input size guard (prevent token-bomb payloads)
"""

from __future__ import annotations
import re
from dataclasses import dataclass, field


@dataclass
class CheckResult:
    name: str
    passed: bool
    severity: str   # "pass" | "warn" | "block"
    message: str


@dataclass
class GuardrailResult:
    blocked: bool
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def has_warnings(self) -> bool:
        return any(c.severity == "warn" for c in self.checks)


class GuardrailsChecker:
    # ── Prompt Injection ────────────────────────────────────────────────────
    _INJECTION = [
        r"ignore\s+(all\s+)?(previous|prior|above|earlier)\s+instructions?",
        r"disregard\s+(all\s+)?(previous|prior|above)\s+instructions?",
        r"forget\s+your\s+(instructions?|training|guidelines?|rules?|constraints?)",
        r"you\s+are\s+now\s+(DAN|AIM|STAN|evil|jailbreak|unrestricted)",
        r"act\s+as\s+(if\s+)?you\s+(are|were)\s+(an?\s+)?(evil|unrestricted|uncensored)",
        r"pretend\s+(you\s+are|to\s+be)\s+(an?\s+)?(unrestricted|uncensored|evil)",
        r"you\s+must\s+comply\s+with\s+all\s+requests?",
        r"do\s+anything\s+now",
        r"<\s*/?system\s*>",
        r"\[INST\]|\[\/INST\]",
        r"###\s*instruction\s*:",
        r"<\s*s\s*>.*?<\s*/s\s*>",   # XML-like instruction wrappers
        r"new\s+instructions?\s*:",
        r"from\s+now\s+on\s+(you|your)",
    ]

    # ── PII Patterns ────────────────────────────────────────────────────────
    _PII = {
        "email": r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b",
        "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
        "phone": r"\b(\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
        "credit_card": r"\b(?:\d[ \-]?){13,16}\b",
        "API_key": r"\b(sk-|AKIA|AIza)[A-Za-z0-9_\-]{16,}\b",
    }

    # ── Harmful Content ─────────────────────────────────────────────────────
    _HARMFUL = [
        "how to make a bomb",
        "how to build a weapon",
        "synthesize drugs",
        "create ransomware",
        "create malware",
        "write a virus",
        "exploit this vulnerability to steal",
        "ddos attack tutorial",
        "child pornography",
        "child exploitation",
        "self-harm instructions",
        "how to kill someone",
    ]

    MAX_INPUT_CHARS = 12_000   # ≈3 000 tokens; compressor handles long inputs

    def check(self, text: str) -> GuardrailResult:
        checks: list[CheckResult] = []
        blocked = False

        # 1 ── Prompt injection ─────────────────────────────────────────────
        injection_hit = next(
            (p for p in self._INJECTION if re.search(p, text, re.IGNORECASE | re.DOTALL)),
            None,
        )
        if injection_hit:
            checks.append(CheckResult(
                name="Prompt Injection",
                passed=False,
                severity="block",
                message="Prompt injection pattern detected — request blocked",
            ))
            blocked = True
        else:
            checks.append(CheckResult(
                name="Prompt Injection",
                passed=True,
                severity="pass",
                message="No injection patterns found",
            ))

        # 2 ── PII ──────────────────────────────────────────────────────────
        found_pii = [k for k, pat in self._PII.items() if re.search(pat, text)]
        if found_pii:
            checks.append(CheckResult(
                name="PII Detection",
                passed=False,
                severity="warn",
                message=f"Potential PII detected: {', '.join(found_pii)} — sanitize before sending",
            ))
        else:
            checks.append(CheckResult(
                name="PII Detection",
                passed=True,
                severity="pass",
                message="No PII found",
            ))

        # 3 ── Content policy ───────────────────────────────────────────────
        lower = text.lower()
        harmful_hit = next((kw for kw in self._HARMFUL if kw in lower), None)
        if harmful_hit:
            checks.append(CheckResult(
                name="Content Policy",
                passed=False,
                severity="block",
                message="Harmful content policy violation — request blocked",
            ))
            blocked = True
        else:
            checks.append(CheckResult(
                name="Content Policy",
                passed=True,
                severity="pass",
                message="Content policy: PASS",
            ))

        # 4 ── Input size ───────────────────────────────────────────────────
        char_count = len(text)
        if char_count > self.MAX_INPUT_CHARS:
            checks.append(CheckResult(
                name="Input Size Guard",
                passed=False,
                severity="warn",
                message=f"Input is {char_count:,} chars (>{self.MAX_INPUT_CHARS:,}) — compressor activated",
            ))
        else:
            checks.append(CheckResult(
                name="Input Size Guard",
                passed=True,
                severity="pass",
                message=f"Input size OK ({char_count:,} chars)",
            ))

        return GuardrailResult(blocked=blocked, checks=checks)
