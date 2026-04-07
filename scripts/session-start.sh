#!/bin/bash
# Memory Governor - Session Start Hook
# Checks for governance alerts and loads cached compile if available

MEMORY_DIR=""
for d in $(find ~/.claude/projects -name "memory" -type d 2>/dev/null | head -3); do
  [ -f "$d/MEMORY.md" ] && MEMORY_DIR="$d" && break
done
[ -z "$MEMORY_DIR" ] && exit 0

# Check governance alerts from previous session
ALERT_LOG="$MEMORY_DIR/governance_alerts.log"
if [ -f "$ALERT_LOG" ] && [ -s "$ALERT_LOG" ]; then
  echo "[memory-governor] Alerts from previous session:"
  cat "$ALERT_LOG"
  > "$ALERT_LOG"  # Clear after showing
fi
