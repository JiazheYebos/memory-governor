---
name: memory-governor
description: Zero-dependency memory optimizer for Claude Code. Audit, compact, and restructure memory to cut token waste 50-80%. 4-layer knowledge pyramid with auto-capture hooks.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
when_to_use: "Use when token consumption is high, CLAUDE.md is bloated, memory is disorganized, or starting a new project. Triggers: '/memory-governor', 'optimize memory', 'reduce tokens', 'clean up memory', 'memory audit', 'token太多'"
argument-hint: "/memory-governor [audit|optimize|compact|capture|setup-hooks]"
arguments:
  - action
context: inline
---

# Memory Governor

Zero-dependency memory optimizer for Claude Code. Audit, compact, and restructure your memory architecture to minimize per-session token consumption while preserving all knowledge.

**What makes this different from claude-mem, everything-claude-code, etc.:**
- No runtime dependencies (no Bun, no SQLite, no Chroma, no HTTP server)
- Subtractive philosophy: reduce context load, don't add 181 skills
- One `git clone`, immediately functional
- Works offline, no API keys needed

## The 4-Layer Knowledge Pyramid

```
Layer 0: CLAUDE.md          < 2KB    Always loaded. Eternal principles ONLY.
Layer 1: MEMORY.md index    < 15 entries  Always loaded. One-line pointers.
Layer 2: memory/*.md        On-demand    Detailed knowledge. Loaded when relevant.
Layer 3: skills/ + docs/    On-invoke    Templates & reference. Never auto-loaded.
```

**Core rule: Every piece of content must live at the LOWEST layer where it's still accessible when needed. Anything higher wastes tokens every session.**

## Actions

### `/memory-governor audit`
Analyze without changing anything. Output current state + recommendations.

### `/memory-governor optimize`
Automatically fix issues: move misplaced content down layers, merge duplicates, clean stale entries.

### `/memory-governor compact`
Aggressive mode: consolidate all memory files, rewrite CLAUDE.md to minimum, rebuild index.

### `/memory-governor capture`
Extract key knowledge from current conversation and write to appropriate memory layer.

### `/memory-governor setup-hooks`
Install session lifecycle hooks for automatic memory management.

## Steps for `audit`

### 1. Measure Current Cost
```bash
SKILL_ROOT="$(dirname "$(readlink -f "$0")" 2>/dev/null || echo ~/.claude/skills/memory-governor)"
bash "$SKILL_ROOT/scripts/audit.sh"
```

Report: CLAUDE.md size, index entries, memory file count/size, estimated tokens.

### 2. Classify CLAUDE.md Content

Read CLAUDE.md line by line. For each section ask: **"Does this apply to EVERY conversation?"**

| If YES → | Keep in Layer 0 |
| If NO → | Recommend move to Layer 2 or 3 |

Specific classification rules:

| Content | Correct Layer | Move? |
|---------|--------------|-------|
| Thinking principles, output format | 0 | Stay |
| API keys, credentials | 2 | ↓ Move |
| Product/project specifics | 2 | ↓ Move |
| Tool/model selection tables | 2 | ↓ Move |
| Step-by-step workflows | 3 (skill) | ↓ Move |
| Registered skills list | Delete (auto-detected) | ✗ Remove |
| Error history, anti-patterns | 2 | ↓ Move |

### 3. Audit Memory Index

For each entry in MEMORY.md:
- Still relevant? → Keep
- Stale (> 60 days, facts changed)? → Update or remove from index
- Duplicate of another entry? → Merge
- Entry > 120 chars? → Shorten to pointer

Target: < 15 entries, each < 120 characters.

### 4. Check Memory Files

- Any file > 5KB? → Consider splitting
- Total > 100KB? → Needs consolidation
- Relative dates ("yesterday", "last week")? → Convert to absolute
- File paths cited? → Verify they still exist
- Multiple files on same topic? → Merge

### 5. Output Report

```
## Memory Governor Audit

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| CLAUDE.md | X KB (~Y tokens) | < 2KB (~660 tokens) | ✅/⚠️ |
| Index entries | N | < 15 | ✅/⚠️ |
| Memory files | M files, Z KB | < 100KB | ✅/⚠️ |
| Per-session cost | ~T tokens | < 1000 | ✅/⚠️ |

### Recommendations
1. [specific action items]
```

## Steps for `optimize`

Run `audit` first, then automatically execute all recommendations:
1. Rewrite CLAUDE.md keeping only Layer 0 content
2. Move displaced content to new/existing memory files
3. Rebuild MEMORY.md index
4. Merge duplicate memory files
5. Remove stale index entries (preserve files)
6. Re-run audit to confirm improvement

**Human checkpoint**: Show before/after diff, ask for confirmation before writing.

## Steps for `capture`

Extract from current conversation:
1. New decisions made → `memory/decisions.md`
2. Errors encountered → `memory/errors.md`
3. User preferences learned → `memory/preferences.md`
4. Project state changes → `memory/state.md`

**Rules**:
- Append, don't overwrite
- Convert relative dates to absolute
- Keep entries concise (< 3 lines each)
- Don't capture ephemeral task details

## Steps for `setup-hooks`

Create `.claude/hooks.json` with:
```json
{
  "hooks": {
    "SessionEnd": [{
      "command": "bash ~/.claude/skills/memory-governor/scripts/session-end-capture.sh",
      "description": "Auto-capture key knowledge at session end"
    }]
  }
}
```

This enables automatic memory governance without manual intervention.

## Token Estimation

```
Per-session tokens ≈ (CLAUDE.md bytes + MEMORY.md bytes) / 3
```

| Rating | Tokens | Meaning |
|--------|--------|---------|
| ✅ Optimal | < 1000 | Lean and efficient |
| ⚠️ Acceptable | 1000-2000 | Room to improve |
| ❌ Bloated | > 2000 | Immediate optimization needed |

## Anti-Patterns This Fixes

1. **Knowledge Dump CLAUDE.md** — Everything crammed into one file that loads every session
2. **Index-as-Content** — MEMORY.md entries that are paragraphs instead of pointers
3. **Zombie Entries** — "Current task: X" from weeks ago, never updated
4. **Duplicate Facts** — Same information in CLAUDE.md AND memory AND skill
5. **Skill Pollution** — Skills with huge rule blocks that false-trigger and load unnecessarily
6. **Date Decay** — "Yesterday we decided..." becomes meaningless after a week
