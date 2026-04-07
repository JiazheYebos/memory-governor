#!/bin/bash
# Memory Governor - Quick Audit Script
# Run standalone: bash ~/.claude/skills/memory-governor/scripts/audit.sh

echo "================================"
echo "Memory Governor - Quick Audit"
echo "================================"

# Find CLAUDE.md
CLAUDE_MD=""
for f in "./CLAUDE.md" "../CLAUDE.md" "../../CLAUDE.md"; do
  if [ -f "$f" ]; then CLAUDE_MD="$f"; break; fi
done

if [ -n "$CLAUDE_MD" ]; then
  SIZE=$(wc -c < "$CLAUDE_MD" | tr -d ' ')
  TOKENS=$((SIZE / 3))
  if [ "$SIZE" -gt 2048 ]; then
    echo "⚠️  CLAUDE.md: ${SIZE} bytes (~${TOKENS} tokens) — TOO LARGE (> 2KB)"
  else
    echo "✅ CLAUDE.md: ${SIZE} bytes (~${TOKENS} tokens)"
  fi
else
  echo "ℹ️  No CLAUDE.md found"
fi

# Find memory index
MEMORY_MD=$(find ~/.claude/projects -name "MEMORY.md" -path "*/memory/*" 2>/dev/null | head -1)
if [ -n "$MEMORY_MD" ]; then
  ENTRIES=$(grep -c "^-" "$MEMORY_MD" 2>/dev/null || echo 0)
  MEM_SIZE=$(wc -c < "$MEMORY_MD" | tr -d ' ')
  MEM_TOKENS=$((MEM_SIZE / 3))

  if [ "$ENTRIES" -gt 15 ]; then
    echo "⚠️  Memory index: ${ENTRIES} entries (~${MEM_TOKENS} tokens) — TOO MANY (> 15)"
  else
    echo "✅ Memory index: ${ENTRIES} entries (~${MEM_TOKENS} tokens)"
  fi

  MEM_DIR=$(dirname "$MEMORY_MD")
  FILE_COUNT=$(ls "$MEM_DIR"/*.md 2>/dev/null | wc -l | tr -d ' ')
  DIR_SIZE=$(du -sh "$MEM_DIR" 2>/dev/null | cut -f1)
  echo "   Memory files: ${FILE_COUNT} files, ${DIR_SIZE}"
else
  echo "ℹ️  No memory index found"
fi

# Skills
SKILL_COUNT=$(find ~/.claude/skills -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
echo "   Skills installed: ${SKILL_COUNT}"

# Total estimate
TOTAL_TOKENS=$(( ${TOKENS:-0} + ${MEM_TOKENS:-0} ))
echo ""
echo "📊 Estimated per-session fixed cost: ~${TOTAL_TOKENS} tokens"
if [ "$TOTAL_TOKENS" -gt 2000 ]; then
  echo "⚠️  Above recommended maximum (2000). Run: /memory-governor optimize"
elif [ "$TOTAL_TOKENS" -gt 1000 ]; then
  echo "ℹ️  Acceptable but could be improved. Run: /memory-governor optimize"
else
  echo "✅ Within optimal range (< 1000)"
fi
