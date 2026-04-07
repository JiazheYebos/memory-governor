# Memory Governor

**A memory compiler for Claude Code. Compile 50KB of knowledge into 2KB of session context.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## The Problem Everyone Solves Wrong

The Claude Code memory ecosystem has two camps:

**Camp 1: Add more infrastructure** (claude-mem, 46K⭐)
→ SQLite + Chroma vector DB + HTTP server + Bun runtime to manage your memory files.

**Camp 2: Add more skills** (everything-claude-code, 140K⭐)
→ 181 skills + 47 agents + hooks. Your context window is now 50% skill definitions.

**Camp 3: Compress output** (claude-token-efficient, 3.5K⭐)
→ Make Claude respond shorter. Doesn't touch the input side at all.

**What nobody does: optimize what gets loaded into the context window at session start.**

Every session, Claude Code loads CLAUDE.md + MEMORY.md before you type anything. After months of use, these files bloat to 6-10KB — that's 2000-3300 tokens of stale rules, duplicate entries, and knowledge that's irrelevant to the current session. Every. Single. Time.

## Our Approach: Compile, Don't Accumulate

Like a code compiler transforms source into optimized machine code:

```
Source (your full knowledge: 50KB of memory files)
  ↓ compile
Binary (this session's context: ~2KB of relevant knowledge)
```

Three innovations:

### 1. The 4-Layer Knowledge Pyramid

```
Layer 0: CLAUDE.md          < 2KB     Always loaded. Eternal principles ONLY.
Layer 1: MEMORY.md index    < 15 entries  Always loaded. One-line pointers.
Layer 2: memory/*.md        On-demand    Detailed knowledge.
Layer 3: skills/ + docs/    On-invoke    Templates & reference.
```

**Rule: Content lives at the LOWEST layer where it's still accessible.**

### 2. Intent-Driven Compilation

Instead of loading all knowledge every session:

```
User: "Fix the auth bug"
  → Detect domain: backend, auth
  → Score memory files by relevance
  → Compile: load only auth-related decisions + recent state
  → Result: 800 tokens instead of 3000
```

### 3. Compile Cache

Repeated domains reuse cached compilations. Cache invalidates when source files change.

## Install

```bash
git clone https://github.com/JiazheYebos/memory-governor.git ~/.claude/skills/memory-governor
```

No dependencies. No config. No API keys. No runtime. Done.

## Usage

```
/memory-governor audit        # Measure current token waste
/memory-governor optimize     # Fix layer violations automatically
/memory-governor compile      # Build minimal context for this session
/memory-governor capture      # Save knowledge from current conversation
/memory-governor setup-hooks  # Install auto-governance hooks
```

Quick standalone check:
```bash
bash ~/.claude/skills/memory-governor/scripts/audit.sh
```

## How `compile` Works

```
Phase 1: Intent Detection
  Read first message → classify domain (backend, frontend, infra, content...)

Phase 2: Relevance Scoring
  Score each memory file against detected domain
  Signals: filename keywords, description match, recency, dependencies

Phase 3: Build Minimal Context
  Include: active state (always) + relevant knowledge + applicable rules
  Exclude: everything else

Phase 4: Inject
  Single compiled block → ~800 tokens instead of ~3000
```

## What It Fixes

| Anti-Pattern | What Happens | Fix |
|-------------|-------------|-----|
| Knowledge dump CLAUDE.md | 6KB loaded every session | Move specifics to Layer 2 |
| Index-as-content | MEMORY.md entries are paragraphs | One-line pointers only |
| Zombie state | "Working on X" from weeks ago | Update or archive |
| Shotgun loading | All knowledge for every session | Compile per-intent |
| Duplicate facts | Same info in 3 places | Single source of truth |
| Date decay | "Yesterday decided..." | Absolute dates only |

## Benchmarks

Tested across multiple projects with 3-6 months of accumulated memory:

```
Before optimization:
  CLAUDE.md: 6KB + MEMORY.md: 4KB = ~3300 tokens/session

After optimize:
  CLAUDE.md: 1.5KB + MEMORY.md: 1.2KB = ~900 tokens/session (73% reduction)

After compile:
  Compiled context: ~800 tokens/session (76% reduction)
  With cache hit: ~600 tokens/session (82% reduction)
```

## Comparison

| | memory-governor | claude-mem (46K⭐) | everything-cc (140K⭐) | token-efficient (3.5K⭐) |
|---|---|---|---|---|
| Approach | Compile input | Capture & store | Add skills | Compress output |
| Dependencies | Zero | Bun+SQLite+Chroma | Plugin system | Zero |
| Install | git clone | npx + setup | Marketplace | Copy file |
| Token impact | **-73% to -82%** | +500 overhead | +significant | -63% output only |
| Intent-aware | ✅ Yes | ❌ No | ❌ No | ❌ No |
| Compile cache | ✅ Yes | N/A | N/A | N/A |
| Works offline | ✅ Yes | Partial | Yes | Yes |
| What it optimizes | Input context | Storage | Capabilities | Output verbosity |

**Key insight**: Others optimize the wrong side. Output compression saves tokens on responses. Input compilation saves tokens on _every message_ — including tool calls, which are the majority of Claude Code's token usage.

## Philosophy

> Adding a database, a vector store, and an HTTP server to manage 15 memory files is like buying a warehouse to organize a bookshelf.

> Adding 181 skills to reduce token waste is like hiring 181 employees to reduce payroll.

> Making responses shorter doesn't help when 3000 tokens of stale context are loaded before the conversation starts.

Just compile the bookshelf.

## Compatibility

- Claude Code (CLI, Desktop, Web, IDE extensions)
- Works alongside claude-mem, everything-claude-code, or any other tool
- Any project with CLAUDE.md

## License

MIT
