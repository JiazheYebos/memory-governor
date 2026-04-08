#!/bin/bash
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PY="python3"
command -v python3.12 >/dev/null 2>&1 && PY="python3.12"
$PY "$SKILL_DIR/scripts/briefing.py" 2>/dev/null
