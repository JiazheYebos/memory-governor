# Memory Governor

**Zero-dependency memory optimizer for Claude Code. Cut per-session token waste by 50-80%.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

After weeks of use, Claude Code's CLAUDE.md and memory files accumulate stale rules, duplicate content, and misplaced knowledge — silently consuming thousands of tokens every session. Memory Governor fixes this in one command.

## The Problem

```
Session start → Load CLAUDE.md (6KB = 2000 tokens)
             → Load MEMORY.md (4KB = 1300 tokens)
             → 3300 tokens GONE before you even type anything
```

Most of that content doesn't need to be loaded every session. But it does — every single time.

## The Solution: 4-Layer Knowledge Pyramid

```
Layer 0: CLAUDE.md        < 2KB     ← Eternal principles (loaded always)
Layer 1: MEMORY.md index  < 15 entries ← Pointers only (loaded always)
Layer 2: memory/*.md      on-demand  ← Detailed knowledge (loaded when relevant)
Layer 3: skills/          on-invoke  ← Process templates (loaded only when called)
```

**Core rule: Push content to the lowest layer where it's still accessible.**

Examples:
- "Always use first principles thinking" → Layer 0 (CLAUDE.md) ✓
- "API key is abc123" → Layer 2 (memory file) ✓
- "Step-by-step deployment process" → Layer 3 (skill) ✓
- "Currently working on feature X" → Layer 2 (state file) ✓

If something is in Layer 0 but should be in Layer 2, you're paying tokens for it every session — even when it's irrelevant.

## Install

```bash
git clone https://github.com/JiazheYebos/memory-governor.git ~/.claude/skills/memory-governor
```

No dependencies. No config. No API keys. Done.

## Usage

```
/memory-governor audit      # Analyze without changing anything
/memory-governor optimize   # Fix issues automatically
/memory-governor compact    # Aggressive cleanup
/memory-governor capture    # Extract knowledge from current session
/memory-governor setup-hooks # Install auto-governance hooks
```

Or run the standalone audit script:
```bash
bash ~/.claude/skills/memory-governor/scripts/audit.sh
```

## What It Does

1. **Scans** CLAUDE.md, MEMORY.md, memory files, and skills
2. **Classifies** every piece of content by its correct layer
3. **Moves** misplaced content down to the right layer
4. **Merges** duplicate and overlapping memory files
5. **Cleans** stale entries from the index (original files preserved)
6. **Reports** exact token savings

## What It Fixes

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Knowledge dump CLAUDE.md | Everything in one file, loaded every session | Move specifics to Layer 2/3 |
| Index-as-content | MEMORY.md entries that are paragraphs | Shorten to one-line pointers |
| Zombie entries | "Current task: X" from 3 weeks ago | Update or archive |
| Duplicate facts | Same info in CLAUDE.md AND memory AND skill | Single source of truth |
| Skill pollution | Skills with huge rule blocks that false-trigger | Clear triggers, minimal content |
| Date decay | "Yesterday we decided..." | Convert to absolute dates |

## Real Results

Tested on a production project with 6 months of accumulated memory:

```
Before: CLAUDE.md 6KB + MEMORY.md 4KB = ~3300 tokens/session
After:  CLAUDE.md 1.5KB + MEMORY.md 1.2KB = ~900 tokens/session
Savings: 73%
```

## How It Compares

| Feature | memory-governor | claude-mem (46K⭐) | everything-claude-code (140K⭐) |
|---------|----------------|-------------------|-------------------------------|
| Dependencies | None | Bun + SQLite + Chroma | Heavy plugin system |
| Install | 1 line git clone | `npx` + runtime setup | Plugin marketplace |
| Approach | Subtractive (reduce load) | Additive (capture more) | Additive (181 skills) |
| Auto-capture | Via hooks (optional) | Built-in hooks | Built-in hooks |
| Vector search | No (not needed at < 15 entries) | Yes (Chroma) | No |
| Web UI | No | Yes | No |
| Offline | Yes | Partially | Yes |
| Token impact | Reduces 50-80% | Adds ~500 tokens overhead | Adds significant overhead |

**Philosophy difference**: Others add infrastructure to manage growing context. We shrink the context so it doesn't need managing.

## Token Budget Guide

```
Per-session tokens ≈ (CLAUDE.md bytes + MEMORY.md bytes) / 3
```

| Rating | Tokens | Action |
|--------|--------|--------|
| ✅ Optimal | < 1000 | You're good |
| ⚠️ Acceptable | 1000-2000 | Run `/memory-governor optimize` |
| ❌ Bloated | > 2000 | Run `/memory-governor compact` immediately |

## Compatibility

- Claude Code (CLI, Desktop, Web, IDE extensions)
- Any project with CLAUDE.md
- Works alongside other skills, MCP servers, and hooks
- No conflict with claude-mem or other memory systems

## Philosophy

The best memory system isn't the one with the most features — it's the one that loads the least while losing nothing.

Adding a database, a vector store, and an HTTP server to manage 15 memory files is like buying a warehouse to organize a bookshelf. Just organize the bookshelf.

## License

MIT
