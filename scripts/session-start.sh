#!/bin/bash
# Memory Governor v4 — Session Start Hook
# 1. Show human briefing (status summary)
# 2. Run compile engine (AI context)

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PY="python3"
command -v python3.12 >/dev/null 2>&1 && PY="python3.12"

# Human briefing
$PY "$SKILL_DIR/scripts/briefing.py" 2>/dev/null

# AI compile
$PY "$SKILL_DIR/scripts/compile.py" 2>/dev/null
