#!/bin/bash
# Memory Governor v4 — Session Start Hook
# Runs compile engine to generate minimal context

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Show alerts from previous session
MEMORY_DIR=""
for d in $(find ~/.claude/projects -name "memory" -type d 2>/dev/null | head -3); do
  [ -f "$d/MEMORY.md" ] && MEMORY_DIR="$d" && break
done

if [ -n "$MEMORY_DIR" ] && [ -f "$MEMORY_DIR/governance_alerts.log" ] && [ -s "$MEMORY_DIR/governance_alerts.log" ]; then
  echo "[memory-governor] ⚠️ Alerts:"
  cat "$MEMORY_DIR/governance_alerts.log"
  > "$MEMORY_DIR/governance_alerts.log"
fi

# Run compile (generates .compiled/context.md)
python3 "$SKILL_DIR/scripts/compile.py" 2>/dev/null || python3.12 "$SKILL_DIR/scripts/compile.py" 2>/dev/null
