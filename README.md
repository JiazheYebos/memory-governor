# Memory Governor

**A memory compiler for Claude Code. Compile 50KB of knowledge into 2KB of session context.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## The Problem Everyone Solves Wrong

The Claude Code memory ecosystem has two camps:

**Camp 1: Add infrastructure** (Mem0, Zep, claude-mem)
→ Vector databases, knowledge graphs, HTTP servers, cloud APIs. Your "memory optimizer" now needs its own DevOps.

**Camp 2: Add more skills** (everything-claude-code)
→ 181 skills + 47 agents. Your context window is now 50% skill definitions.

**Camp 3: Compress output** (claude-token-efficient, Caveman-Claude)
→ Shorter responses. Doesn't touch the input side — where the real waste is.

**What nobody does: compile the input context per session intent.**

Every session, Claude Code loads CLAUDE.md + MEMORY.md before you type anything. After months of use, these bloat to 6-10KB. That's 2000-3300 tokens of stale rules, duplicate entries, and knowledge irrelevant to the current session. Every. Single. Time.

## Our Approach: Compile, Don't Accumulate

```
Source (your full knowledge: 50KB of memory files)
  ↓ detect session intent
  ↓ match tags
  ↓ follow [[links]]
  ↓ merge global memory
  ↓ compile
Binary (this session's context: ~2KB)
```

## What's New in v2.1

### Tag-Based Semantic Index
Lightweight alternative to vector databases. Every memory file gets `tags:` in frontmatter. Compile matches intent against tags — zero infrastructure:
```yaml
---
name: api_credentials
tags: [api, credentials, meta, kling]
---
```

### Relationship Links
Files reference each other with `[[links]]`. If file A is loaded and references `[[file_B]]`, both compile into context:
```markdown
See also: [[product_specs]] for dimensions.
```

### Auto-Capture Hooks
5 lifecycle hooks (pure shell, no runtime):
- `SessionStart`: Load alerts, check compile cache
- `PreCompact`: Extract state before context compaction
- `SessionEnd`: Capture knowledge, check memory health

### Cross-Project Global Memory
```
~/.claude/global-memory/
  credentials.md      # API keys (shared across all projects)
  preferences.md      # Your output style, language, rules
  tool-knowledge.md   # Cross-project expertise
```

## Install

```bash
git clone https://github.com/JiazheYebos/memory-governor.git ~/.claude/skills/memory-governor
```

No dependencies. No config. No API keys. No runtime. Done.

## Usage

```
/memory-governor audit        # Measure current token waste
/memory-governor optimize     # Fix issues + add tags + add links
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
  "Fix the auth bug" → [backend, auth, debug]

Phase 2: Tag Matching
  Score memory files: count(file.tags ∩ detected_domains)
  Always include: state_current.md, files tagged [critical]

Phase 3: Link Following
  If file A included and contains [[file_B]] → also include B
  Depth limit: 1 hop

Phase 4: Global Memory Merge
  ~/.claude/global-memory/credentials.md → if API session
  ~/.claude/global-memory/preferences.md → always (tiny)

Phase 5: Build + Cache
  Compiled context → memory/.compiled/{domain}.md
  Reuse if source files unchanged
```

## Comparison

| | memory-governor | Mem0 | claude-mem (46K⭐) | everything-cc (140K⭐) | token-efficient (3.5K⭐) |
|---|---|---|---|---|---|
| Approach | **Compile input** | Cloud vector DB | Capture & store | Add skills | Compress output |
| Dependencies | **Zero** | API + cloud | Bun+SQLite+Chroma | Plugin system | Zero |
| Install | git clone | SDK setup | npx + runtime | Marketplace | Copy file |
| Token impact | **-73% to -82%** | -90% (cloud cost) | +500 overhead | +significant | -63% output only |
| Intent-aware | **✅** | ❌ | ❌ | ❌ | ❌ |
| Tag index | **✅** | Vector DB | SQLite FTS | ❌ | ❌ |
| Link following | **✅** | Knowledge graph | ❌ | ❌ | ❌ |
| Cross-project | **✅** | ✅ (cloud) | ❌ | ❌ | ❌ |
| Auto-hooks | **✅ (5 hooks)** | N/A | ✅ | ✅ | ❌ |
| Works offline | **✅** | ❌ | Partial | Yes | Yes |
| Privacy/GDPR | **✅ by design** | ❌ needs DPA | Partial | Yes | Yes |

**Key insight**: Mem0 achieves -90% through cloud infrastructure. We achieve -82% with zero infrastructure. The gap is 8%, the complexity gap is infinite.

## Benchmarks

```
Before optimization:
  CLAUDE.md: 6KB + MEMORY.md: 4KB = ~3300 tokens/session

After optimize (v2.0):
  CLAUDE.md: 1.5KB + MEMORY.md: 1.2KB = ~900 tokens/session → 73% reduction

After compile (v2.1):
  Tag-matched subset: ~800 tokens → 76% reduction

After compile + cache (v2.1):
  Cached domain: ~600 tokens → 82% reduction
```

## Memory File Template

```markdown
---
name: descriptive_name
description: One-line summary for index
tags: [domain1, domain2, keyword]
updated: 2026-04-08
---

# Title

Content here.

See also: [[related_file_name]]
```

## Philosophy

> Adding a vector database to manage 15 markdown files is like buying a data center to run a spreadsheet.

> Adding 181 skills to reduce token waste is like hiring 181 people to reduce payroll.

> Making responses shorter doesn't help when 3000 tokens of stale context load before the conversation starts.

Just compile the context.

## Contributors

<a href="https://github.com/JiazheYebos">
  <img src="https://github.com/JiazheYebos.png" width="60" style="border-radius:50%"/>
</a>

## Contributing

PRs welcome. Core principles:
- Zero dependencies (no databases, no servers, no API keys)
- Subtractive over additive (remove waste, don't add infrastructure)
- Works offline by default
- SKILL.md is the single source of truth

## License

MIT
