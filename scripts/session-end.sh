#!/bin/bash
# Memory Governor - Session End Hook
# Checks memory health and flags issues for next session

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
    [ "$SIZE" -gt 3072 ] && echo "[$(date '+%m-%d %H:%M')] CLAUDE.md bloated: ${SIZE} bytes (> 3KB). Run /memory-governor optimize" >> "$ALERT_LOG"
    break
  fi
done

# Check index size
ENTRIES=$(grep -c "^-" "$MEMORY_DIR/MEMORY.md" 2>/dev/null || echo 0)
[ "$ENTRIES" -gt 20 ] && echo "[$(date '+%m-%d %H:%M')] Memory index: ${ENTRIES} entries (> 20). Run /memory-governor optimize" >> "$ALERT_LOG"

# Check for untagged memory files
UNTAGGED=0
for f in "$MEMORY_DIR"/*.md; do
  [ "$(basename "$f")" = "MEMORY.md" ] && continue
  grep -q "^tags:" "$f" 2>/dev/null || UNTAGGED=$((UNTAGGED + 1))
done
[ "$UNTAGGED" -gt 3 ] && echo "[$(date '+%m-%d %H:%M')] ${UNTAGGED} memory files missing tags. Run /memory-governor optimize" >> "$ALERT_LOG"

# Check total memory size
TOTAL_KB=$(du -sk "$MEMORY_DIR" 2>/dev/null | cut -f1)
[ "$TOTAL_KB" -gt 200 ] && echo "[$(date '+%m-%d %H:%M')] Memory dir: ${TOTAL_KB}KB (> 200KB). Run /memory-governor compact" >> "$ALERT_LOG"
