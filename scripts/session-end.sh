#!/bin/bash
# Light health check — no file modification
CLAUDE_MD=""
for f in "./CLAUDE.md" "../CLAUDE.md" "../../CLAUDE.md"; do
  [ -f "$f" ] && CLAUDE_MD="$f" && break
done
if [ -n "$CLAUDE_MD" ]; then
  SIZE=$(wc -c < "$CLAUDE_MD" | tr -d ' ')
  [ "$SIZE" -gt 4096 ] && echo "[memory-governor] ⚠️ CLAUDE.md is ${SIZE} bytes. Consider running /memory-governor optimize"
fi
