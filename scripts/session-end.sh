#!/bin/bash
# Memory Governor v4 — Session End Hook
# Runs metabolism engine + health checks

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Run metabolism (update temperatures)
python3 "$SKILL_DIR/scripts/metabolism.py" 2>/dev/null || python3.12 "$SKILL_DIR/scripts/metabolism.py" 2>/dev/null

# Health checks
MEMORY_DIR=""
for d in $(find ~/.claude/projects -name "memory" -type d 2>/dev/null | head -3); do
  [ -f "$d/MEMORY.md" ] && MEMORY_DIR="$d" && break
done
[ -z "$MEMORY_DIR" ] && exit 0

ALERT_LOG="$MEMORY_DIR/governance_alerts.log"

# Check CLAUDE.md size
for f in "./CLAUDE.md" "../CLAUDE.md" "../../CLAUDE.md"; do
  if [ -f "$f" ]; then
    SIZE=$(wc -c < "$f" | tr -d ' ')
    [ "$SIZE" -gt 3072 ] && echo "[$(date '+%m-%d %H:%M')] CLAUDE.md: ${SIZE} bytes (> 3KB)" >> "$ALERT_LOG"
    break
  fi
done

# Check index size
ENTRIES=$(grep -c "^-" "$MEMORY_DIR/MEMORY.md" 2>/dev/null || echo 0)
[ "$ENTRIES" -gt 20 ] && echo "[$(date '+%m-%d %H:%M')] Index: ${ENTRIES} entries (> 20)" >> "$ALERT_LOG"

# Check for procedures without recent access
if [ -d "$MEMORY_DIR/procedures" ]; then
  PROC_COUNT=$(ls "$MEMORY_DIR/procedures/"*.md 2>/dev/null | wc -l | tr -d ' ')
  echo "[memory-governor] ${PROC_COUNT} procedures tracked"
fi
