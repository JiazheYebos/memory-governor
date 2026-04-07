#!/bin/bash
# Memory Governor - Session End Auto-Capture Hook
# Runs automatically at end of each Claude Code session (if hooks enabled)
# Checks if memory needs governance and flags for next session

MEMORY_DIR=""
for d in $(find ~/.claude/projects -name "memory" -type d 2>/dev/null); do
  if [ -f "$d/MEMORY.md" ]; then
    MEMORY_DIR="$d"
    break
  fi
done

[ -z "$MEMORY_DIR" ] && exit 0

# Check CLAUDE.md size
CLAUDE_MD=""
for f in "./CLAUDE.md" "../CLAUDE.md"; do
  [ -f "$f" ] && CLAUDE_MD="$f" && break
done

if [ -n "$CLAUDE_MD" ]; then
  SIZE=$(wc -c < "$CLAUDE_MD" | tr -d ' ')
  if [ "$SIZE" -gt 3072 ]; then
    echo "[memory-governor] ⚠️ CLAUDE.md is ${SIZE} bytes (> 3KB). Run /memory-governor optimize" >> "$MEMORY_DIR/governance_alerts.log"
  fi
fi

# Check index size
ENTRIES=$(grep -c "^-" "$MEMORY_DIR/MEMORY.md" 2>/dev/null || echo 0)
if [ "$ENTRIES" -gt 20 ]; then
  echo "[memory-governor] ⚠️ Memory index has ${ENTRIES} entries (> 20). Run /memory-governor optimize" >> "$MEMORY_DIR/governance_alerts.log"
fi
