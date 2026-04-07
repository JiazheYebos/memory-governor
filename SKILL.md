---
name: memory-governor
description: Memory compiler for Claude Code. Restructure knowledge into a 4-layer pyramid, then compile per-session context to minimum viable size. Zero dependencies.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
when_to_use: "Use when token consumption is high, CLAUDE.md is bloated, memory is disorganized, or starting a new project. Triggers: '/memory-governor', 'optimize memory', 'reduce tokens', 'clean up memory', 'memory audit', 'compile memory'"
argument-hint: "/memory-governor [audit|optimize|compile|capture|setup-hooks]"
arguments:
  - action
context: inline
---

# Memory Governor

A memory compiler for Claude Code. Like a code compiler transforms source into optimized machine code, Memory Governor compiles your full knowledge base (~50KB) into the minimum viable context (~2KB) for each session.

**No database. No vector store. No HTTP server. No API keys. Just organized Markdown.**

## Core Concept: Memory Compilation

```
Full Knowledge Base (Layer 2+3: 50KB, all your memory files + skills)
        ↓ compile
Session Context (Layer 0+1: ~2KB, only what THIS session needs)
```

Traditional approach: Load everything → waste tokens on irrelevant knowledge.
Our approach: Analyze intent → compile minimal context → inject only what's needed.

## The 4-Layer Knowledge Pyramid

```
Layer 0: CLAUDE.md          < 2KB     Always loaded. Eternal principles ONLY.
Layer 1: MEMORY.md index    < 15 entries  Always loaded. One-line pointers.
Layer 2: memory/*.md        On-demand    Detailed knowledge. Loaded when relevant.
Layer 3: skills/ + docs/    On-invoke    Templates & reference. Never auto-loaded.
```

**Layering rule: Content lives at the LOWEST layer where it's still accessible when needed.**

## Actions

### `/memory-governor audit`
Measure current state. Output token cost, layer violations, stale entries.

### `/memory-governor optimize`
Fix layer violations: move misplaced content down, merge duplicates, clean stale entries.

### `/memory-governor compile`
**The key differentiator.** Analyze current session intent, then build a minimal context payload.

### `/memory-governor capture`
Extract key knowledge from current conversation into appropriate memory layer.

### `/memory-governor setup-hooks`
Install session lifecycle hooks for automatic governance.

---

## Step-by-step: `audit`

### 1. Measure Current Cost
```bash
bash "$(dirname "$0" 2>/dev/null || echo ~/.claude/skills/memory-governor)/scripts/audit.sh"
```

### 2. Classify CLAUDE.md Content

Read CLAUDE.md. For each section, ask: **"Does this apply to EVERY conversation?"**

| If YES → Layer 0 (keep) | If NO → Layer 2 or 3 (move down) |
|---|---|

| Content Type | Correct Layer |
|-------------|--------------|
| Thinking principles, output format | 0 — Keep |
| API keys, credentials | 2 — Move down |
| Product/project specifics | 2 — Move down |
| Tool/model selection tables | 2 — Move down |
| Step-by-step workflows | 3 (skill) — Move down |
| Registered skills list | Delete (auto-detected) |
| Error history, anti-patterns | 2 — Move down |

**Target: CLAUDE.md < 2KB after optimization.**

### 3. Audit Memory Index

For each MEMORY.md entry:
- Still relevant? (read the file to verify)
- Entry < 120 chars? (it's a pointer, not content)
- Duplicate of another entry? → Merge
- Stale (> 60 days, facts changed)? → Update or remove
- Relative dates? → Convert to absolute

**Target: < 15 entries.**

### 4. Check Memory Files

- Any file > 5KB? → Split or summarize
- Total > 100KB? → Consolidate
- Multiple files on same topic? → Merge
- Referenced file paths still exist? → Verify

### 5. Output Report

```
## Memory Governor Audit

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| CLAUDE.md | X KB (~Y tokens) | < 2KB | ✅/⚠️ |
| Index entries | N | < 15 | ✅/⚠️ |
| Memory files | M files, Z KB | < 100KB | ✅/⚠️ |
| Per-session cost | ~T tokens | < 1000 | ✅/⚠️ |

Recommendations:
1. [specific actions]
```

---

## Step-by-step: `optimize`

Run audit first, then execute all recommendations:
1. Rewrite CLAUDE.md keeping only Layer 0 content
2. Create/update memory files for displaced content
3. Rebuild MEMORY.md index
4. Merge duplicate files
5. Remove stale index entries (preserve files)
6. Re-audit to confirm

**Human checkpoint**: Show before/after diff before writing.

---

## Step-by-step: `compile`

This is what makes Memory Governor different from every other tool.

### Phase 1: Intent Detection

Read the user's first message (or session topic) and classify the domain:

```
"Fix the login bug" → domain: backend, auth
"Write a blog post" → domain: content, writing
"Deploy to staging" → domain: infra, deployment
"Review this PR" → domain: code-review
```

### Phase 2: Relevance Scoring

Score each memory file against the detected domain:

```python
# Pseudo-logic (executed by Claude, not a script)
for each memory_file in memory/*.md:
    relevance = estimate_relevance(file.name, file.description, detected_domain)
    if relevance > threshold:
        include in compiled context
```

Scoring signals:
- Filename keywords matching domain
- MEMORY.md description matching intent
- Recency (state files always relevant, old decisions less so)
- Dependency (if file A references file B, include both)

### Phase 3: Compile Minimal Context

Build a single compiled block:

```markdown
## Compiled Context for This Session

### Active State
[from state_current.md — always included]

### Relevant Knowledge
[from scored memory files — domain-specific subset]

### Applicable Rules
[from feedback files — only matching rules]
```

### Phase 4: Inject

Append compiled context to the conversation as a single message, replacing the need to load all 15+ index entries.

**Result**: Instead of loading ~3000 tokens of generic context, load ~800 tokens of precisely relevant context.

### Compile Cache

If the same domain appears repeatedly (e.g., you always work on backend), cache the compiled output:

```
memory/.compiled/
  backend.md      # cached compile for backend sessions
  content.md      # cached compile for content sessions
  last_compiled: 2026-04-08
```

Cache invalidation: recompile if any source memory file was modified after `last_compiled`.

---

## Step-by-step: `capture`

Extract from current conversation:

| What | Where | Format |
|------|-------|--------|
| New decisions | memory/decisions.md | `- [DATE] Decision: X. Reason: Y` |
| Errors encountered | memory/errors.md | `- [DATE] Error: X. Fix: Y` |
| User preferences | memory/preferences.md | `- Preference: X` |
| State changes | memory/state.md | Update in-place |

**Rules**:
- Append, don't overwrite
- Absolute dates only (never "today", "yesterday")
- < 3 lines per entry
- Don't capture ephemeral task details

---

## Step-by-step: `setup-hooks`

Create/update `.claude/hooks.json`:

```json
{
  "hooks": {
    "SessionEnd": [{
      "command": "bash ~/.claude/skills/memory-governor/scripts/session-end-capture.sh",
      "description": "Check memory health, flag if governance needed"
    }]
  }
}
```

---

## Token Math

```
Per-session fixed tokens ≈ (CLAUDE.md bytes + MEMORY.md bytes) / 3

Without compile: ~3000 tokens (all index loaded)
With compile: ~800 tokens (only relevant subset)
Savings: 73%
```

| Rating | Tokens | Meaning |
|--------|--------|---------|
| ✅ Optimal | < 1000 | Lean and efficient |
| ⚠️ Acceptable | 1000-2000 | Run optimize |
| ❌ Bloated | > 2000 | Run compact immediately |

---

## Anti-Patterns This Fixes

1. **Knowledge Dump** — Everything in CLAUDE.md → Move to lower layers
2. **Index-as-Content** — MEMORY.md paragraphs → Shorten to pointers
3. **Zombie State** — "Working on X" from weeks ago → Update or archive
4. **Duplicate Facts** — Same info in 3 places → Single source of truth
5. **Skill Pollution** — Huge skills that false-trigger → Clear triggers, minimal content
6. **Date Decay** — "Yesterday decided..." → Absolute dates
7. **Shotgun Loading** — Load everything for every session → Compile per-intent
