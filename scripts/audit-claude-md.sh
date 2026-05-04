#!/usr/bin/env bash
# Warn if CLAUDE.md or AGENTS.md exceed soft word-count budgets.
set -euo pipefail

WARN_WORDS="${WARN_WORDS:-600}"
FAIL_WORDS="${FAIL_WORDS:-1200}"

check_file() {
  local f="$1"
  [[ -f "$f" ]] || return 0
  local words
  words="$(wc -w < "$f" | tr -d ' ')"
  if (( words > FAIL_WORDS )); then
    echo "FAIL: $f has $words words (>${FAIL_WORDS}). Trim or move content to skills." >&2
    return 2
  fi
  if (( words > WARN_WORDS )); then
    echo "WARN: $f has $words words (>${WARN_WORDS}). Consider splitting." >&2
  fi
  echo "OK: $f ($words words)"
}

check_file "CLAUDE.md"
check_file "AGENTS.md"
