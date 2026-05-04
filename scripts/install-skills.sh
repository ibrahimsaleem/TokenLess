#!/usr/bin/env bash
# Install both TokenLess skill packs into a target project directory.
# Usage: bash scripts/install-skills.sh [DEST_DIR]
# Default DEST_DIR is current directory.
set -euo pipefail

DEST="${1:-.}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SK="$ROOT/skills"

mkdir -p "$DEST/.claude/skills" "$DEST/.windsurf/skills" "$DEST/.windsurf/rules" "$DEST/.windsurf/workflows" "$DEST/.agents/skills"

echo "Installing enterprise_token_saver_skills_v2..."
cp -R "$SK/enterprise_token_saver_skills_v2/claude-code/.claude/skills/"* "$DEST/.claude/skills/" 2>/dev/null || true
cp -R "$SK/enterprise_token_saver_skills_v2/windsurf/.windsurf/skills/"* "$DEST/.windsurf/skills/" 2>/dev/null || true
cp -R "$SK/enterprise_token_saver_skills_v2/windsurf/.windsurf/rules/"* "$DEST/.windsurf/rules/" 2>/dev/null || true
cp -R "$SK/enterprise_token_saver_skills_v2/windsurf/.windsurf/workflows/"* "$DEST/.windsurf/workflows/" 2>/dev/null || true
cp -R "$SK/enterprise_token_saver_skills_v2/universal/.agents/skills/"* "$DEST/.agents/skills/" 2>/dev/null || true

echo "Installing token_optimization_skill_pack..."
cp -R "$SK/token_optimization_skill_pack/claude-code/.claude/skills/"* "$DEST/.claude/skills/" 2>/dev/null || true
cp -R "$SK/token_optimization_skill_pack/windsurf/.windsurf/skills/"* "$DEST/.windsurf/skills/" 2>/dev/null || true
cp -R "$SK/token_optimization_skill_pack/windsurf/.windsurf/rules/"* "$DEST/.windsurf/rules/" 2>/dev/null || true
cp -R "$SK/token_optimization_skill_pack/windsurf/.windsurf/workflows/"* "$DEST/.windsurf/workflows/" 2>/dev/null || true
cp -R "$SK/token_optimization_skill_pack/universal/.agents/skills/"* "$DEST/.agents/skills/" 2>/dev/null || true

echo "Done. Skills copied to: $DEST"
