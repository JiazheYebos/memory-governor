#!/bin/bash
# Memory Governor - Pre-Compact Hook
# Extracts key state before Claude Code compacts the conversation
# This preserves important context that might otherwise be lost

MEMORY_DIR=""
for d in $(find ~/.claude/projects -name "memory" -type d 2>/dev/null | head -3); do
  [ -f "$d/MEMORY.md" ] && MEMORY_DIR="$d" && break
done
[ -z "$MEMORY_DIR" ] && exit 0

# Touch a marker so the next session knows compaction happened
echo "[$(date '+%Y-%m-%d %H:%M')] Context compacted" >> "$MEMORY_DIR/.compaction_log"
