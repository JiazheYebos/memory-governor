# Memory Governor

**Automatically optimize Claude Code's memory architecture to cut token waste by 50-80%.**

After weeks of use, Claude Code's CLAUDE.md and memory files accumulate stale rules, duplicate content, and misplaced knowledge — silently consuming thousands of tokens every session. Memory Governor fixes this in one command.

## The Problem

```
Session start → Load CLAUDE.md (6KB = 2000 tokens)
             → Load MEMORY.md (4KB = 1300 tokens)
             → 3300 tokens WASTED before you even type anything
```

Most of that content doesn't need to be loaded every session.

## The Solution: 4-Layer Knowledge Pyramid

```
Layer 0: CLAUDE.md        < 2KB    ← Eternal principles (loaded always)
Layer 1: MEMORY.md index  < 15 entries ← Pointers only (loaded always)
Layer 2: memory/*.md      on-demand ← Detailed knowledge (loaded when relevant)
Layer 3: skills/          on-invoke ← Process templates (loaded only when called)
```

**Core rule: Push content to the lowest layer where it's still accessible.**

## Install

```bash
# Clone into your Claude Code skills directory
git clone https://github.com/YOUR_USERNAME/memory-governor.git ~/.claude/skills/memory-governor
```

That's it. No dependencies, no config, no API keys.

## Usage

```
/memory-governor audit     # Analyze without changing anything
/memory-governor optimize  # Fix issues automatically
/memory-governor compact   # Aggressive cleanup
/memory-governor report    # Show current stats
```

## What It Does

1. **Scans** CLAUDE.md, MEMORY.md, memory files, and skills
2. **Classifies** every piece of content by correct layer
3. **Moves** misplaced content down to the right layer
4. **Merges** duplicate/overlapping memory files
5. **Removes** stale entries from the index (files preserved)
6. **Reports** token savings

## What It Fixes

| Anti-Pattern | Before | After |
|-------------|--------|-------|
| CLAUDE.md as knowledge dump | 6KB, 2000 tokens/session | < 2KB, 500 tokens |
| 36 memory index entries | All loaded as pointers | < 15, most relevant only |
| API keys in CLAUDE.md | Loaded every session | In memory file, loaded on-demand |
| Stale project state | "Current: doing X" from 3 weeks ago | Updated or archived |
| Duplicate knowledge | Same fact in 3 places | Single source of truth |

## Real-World Results

Tested on a production project (Lukkey AG) with 6 months of accumulated memory:

```
Before: CLAUDE.md 6KB + MEMORY.md 4KB = ~3300 tokens/session
After:  CLAUDE.md 1.5KB + MEMORY.md 1.2KB = ~900 tokens/session
Savings: 73%
```

## How It Works (No Magic)

The skill follows one principle: **content should live at the lowest layer where it's still accessible when needed.**

- "Always use first principles" → Layer 0 (CLAUDE.md) ✓
- "Gemini API key is xyz" → Layer 2 (memory file) ✓
- "Product dimensions are 93.2x56.7mm" → Layer 2 (memory file) ✓
- "Step-by-step video production process" → Layer 3 (skill) ✓
- "Currently working on color wheel video" → Layer 2 (state file) ✓

If something is in Layer 0 but should be in Layer 2, you're paying tokens for it every single session even when it's irrelevant.

## Compatibility

- Claude Code (CLI, Desktop, Web, IDE extensions)
- Any project with CLAUDE.md
- Works alongside other skills and MCP servers

## Philosophy

Less is more. The best memory system isn't the one with the most features — it's the one that loads the least while losing nothing.

## License

MIT
