# Memory Governor

**The memory system that remembers what works. Procedural memory + metabolism + anti-amnesia for Claude Code.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## The Problem Nobody Talks About

You spend 30 minutes connecting to an API. It works. Next session, Claude tries a completely different approach, fails, and says "can't be done." **You literally did it yesterday.**

This is **procedural amnesia** — AI forgetting its own proven skills.

Every memory system stores facts (Mem0), events (claude-mem), or relationships (Zep). **None store "how I successfully did X."** Meanwhile, CLAUDE.md bloats to 6KB over months — 2000+ tokens of stale rules loaded every session, while actually useful knowledge (working API calls, solved bugs, proven methods) is lost.

Every session, Claude Code loads CLAUDE.md + MEMORY.md before you type anything. After months of use, these bloat to 6-10KB. That's 2000-3300 tokens of stale rules, duplicate entries, and knowledge irrelevant to the current session. Every. Single. Time.

## Three Innovations (That No Other System Has)

### 1. Procedural Memory — "How I Did It" Layer
```markdown
# memory/procedures/stripe_webhook.md
## Working Solution
- Use raw body for signature verification (NOT parsed JSON)
- Webhook route BEFORE express.json() middleware
## Failed Approaches (never retry these)
- ❌ Parsed JSON body → signature always fails
- ❌ express.json() before webhook route → breaks verification
```
Before trying ANY approach, Claude checks procedures first. If a proven method exists, use it directly. No re-exploration.

### 2. Memory Metabolism — Auto Temperature
```
🔴 Hot (3+ accesses in 14 days)   → always compiled into context
🟡 Warm (1-2 accesses in 14 days) → compiled if tags match
🔵 Cool (accessed in 30 days)     → compiled only if directly referenced
⚪ Cold (30+ days untouched)      → archive candidate
```
No manual tagging needed. The system learns what matters from actual usage.

### 3. Anti-Amnesia Protocol
One line in CLAUDE.md that prevents hours of wasted re-exploration:
> "Before attempting any technical task, check memory/procedures/ for proven methods. Use them directly. Do not explore alternatives unless the proven method fails."

## Architecture

```
Source (50KB: facts + procedures + skills)
  ↓ check procedures FIRST
  ↓ detect intent
  ↓ temperature-weighted tag match
  ↓ follow [[links]]
  ↓ merge global memory
  ↓ compile
Context (~2KB: proven methods + relevant facts)
```

## Also Includes (from v2.x)

### Tag-Based Semantic Index
Lightweight alternative to vector databases. Every memory file gets `tags:` in frontmatter. Compile matches intent against tags — zero infrastructure:
```yaml
---
name: api_credentials
tags: [api, credentials, stripe, aws]
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

| | memory-governor v3 | Mem0 | claude-mem (46K⭐) | everything-cc (140K⭐) | MemGPT/Letta |
|---|---|---|---|---|---|
| **Procedural memory** | **✅ Dedicated layer** | ❌ | ❌ | ❌ | ❌ |
| **Anti-amnesia** | **✅ Check before explore** | ❌ | ❌ | ❌ | ❌ |
| **Failed path tracking** | **✅ In procedures** | ❌ | ❌ | ❌ | ❌ |
| **Memory metabolism** | **✅ Access-based** | ❌ | ❌ | ❌ | ⚠️ RL-based |
| Intent compilation | ✅ | ❌ | ❌ | ❌ | ❌ |
| Dependencies | **Zero** | Cloud API | Bun+SQLite+Chroma | Plugin system | Agent framework |
| Token impact | -73% to -82% | -90% (cloud) | +500 overhead | +significant | Variable |
| Works offline | **✅** | ❌ | Partial | Yes | ❌ |
| Privacy/GDPR | **✅ by design** | ❌ | Partial | Yes | ❌ |

**Our unique position: The only system that prevents AI from forgetting its own skills.**

Mem0 achieves -90% token reduction through cloud infrastructure. We achieve -82% with zero infrastructure. But we solve a problem they don't even address: procedural amnesia.

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
