---
name: memory-governor
description: Memory compiler for Claude Code. 4-layer pyramid + intent compilation + tag-based semantic index + auto-capture hooks + cross-project memory. Zero dependencies.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
when_to_use: "Use when token consumption is high, CLAUDE.md is bloated, memory is disorganized, or starting a new project. Triggers: '/memory-governor', 'optimize memory', 'reduce tokens', 'clean up memory', 'compile memory'"
argument-hint: "/memory-governor [audit|optimize|compile|capture|setup-hooks]"
arguments:
  - action
context: inline
---

# Memory Governor

A memory compiler for Claude Code. Compiles your full knowledge base (~50KB) into minimum viable session context (~2KB) through intent detection, tag-based indexing, and relationship-aware loading. Zero dependencies.

## Core Concept: Memory Compilation

```
Full Knowledge (50KB: memory files + skills + global memory)
        ↓ detect intent
        ↓ match tags
        ↓ follow links
        ↓ compile
Session Context (~2KB: only what THIS session needs)
```

## The 4-Layer Knowledge Pyramid

```
Layer 0: CLAUDE.md           < 2KB      Always loaded. Eternal principles ONLY.
Layer 1: MEMORY.md index     < 15 entries  Always loaded. Tagged pointers.
Layer 2: memory/*.md         On-demand   Detailed knowledge. Tag-indexed.
Layer 3: skills/ + docs/     On-invoke   Templates & reference.
```

**Layering rule: Content lives at the LOWEST layer where it's still accessible.**

## v2.1 Features

### Tag-Based Semantic Index (lightweight alternative to vector DB)
Every memory file uses frontmatter tags for domain matching:
```markdown
---
name: api_credentials
tags: [api, credentials, meta, kling, gemini]
---
```
Compile matches session intent against tags — no vector database needed.

### Relationship Links
Memory files reference each other with `[[links]]`:
```markdown
See also: [[decisions_product_specs]] for dimensions.
```
If file A is loaded and references file B, both are compiled into context.

### Auto-Capture Hooks
5 lifecycle hooks (shell scripts, no runtime dependencies):
- `SessionStart`: Load compiled context + check governance alerts
- `PreToolUse`: (reserved for future use)
- `PostToolUse`: (reserved for future use)
- `PreCompact`: Extract key state before context compaction
- `SessionEnd`: Capture decisions/errors, check memory health

### Cross-Project Global Memory
```
~/.claude/global-memory/
  credentials.md      # API keys shared across projects
  preferences.md      # User preferences (output style, language)
  tool-knowledge.md   # Cross-project tool expertise
```
Compile searches both project memory AND global memory.

---

## Actions

### `/memory-governor audit`
Measure current state. Output token cost, layer violations, missing tags, stale entries.

### `/memory-governor optimize`
Fix layer violations, add missing tags, merge duplicates, clean stale entries.

### `/memory-governor compile`
Detect session intent → match tags → follow links → build minimal context.

### `/memory-governor capture`
Extract key knowledge from current conversation into appropriate layer.

### `/memory-governor setup-hooks`
Install all 5 lifecycle hooks for automatic governance.

---

## Step-by-step: `audit`

### 1. Measure Cost
```bash
bash ~/.claude/skills/memory-governor/scripts/audit.sh
```

### 2. Classify CLAUDE.md
For each section: **"Does this apply to EVERY conversation?"**
- YES → Layer 0 (keep)
- NO → Move to Layer 2 or 3

| Content Type | Correct Layer |
|-------------|--------------|
| Thinking principles | 0 — Keep |
| API keys | 2 — Move |
| Project specifics | 2 — Move |
| Tool/model tables | 2 — Move |
| Workflows | 3 (skill) — Move |

**Target: CLAUDE.md < 2KB.**

### 3. Check Tags
```bash
# Find memory files missing tags
for f in memory/*.md; do
  grep -q "^tags:" "$f" || echo "MISSING TAGS: $f"
done
```

### 4. Check Links
```bash
# Find broken links
grep -roh '\[\[[^]]*\]\]' memory/*.md | sort -u | while read link; do
  name=$(echo "$link" | tr -d '[]')
  ls memory/*${name}* 2>/dev/null || echo "BROKEN LINK: $link"
done
```

### 5. Audit Index
- Entries < 15?
- Each < 120 chars?
- Stale entries (> 60 days)?
- Duplicates?

### 6. Check Global Memory
```bash
ls ~/.claude/global-memory/*.md 2>/dev/null || echo "No global memory (optional)"
```

### 7. Output Report
```
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| CLAUDE.md | X KB | < 2KB | ✅/⚠️ |
| Index entries | N | < 15 | ✅/⚠️ |
| Tagged files | X/Y | Y/Y | ✅/⚠️ |
| Linked files | X with links | — | ℹ️ |
| Global memory | exists/missing | — | ℹ️ |
| Per-session cost | ~T tokens | < 1000 | ✅/⚠️ |
```

---

## Step-by-step: `optimize`

1. Rewrite CLAUDE.md → Layer 0 content only
2. Move displaced content to memory files with proper tags
3. Add missing tags to all memory files (infer from filename + content)
4. Add `[[links]]` where files reference each other
5. Rebuild MEMORY.md index with tag hints
6. Merge duplicate files
7. Set up `~/.claude/global-memory/` if not exists
8. Move cross-project knowledge (credentials, preferences) to global
9. Re-audit to confirm

**Human checkpoint**: Show diff before writing.

---

## Step-by-step: `compile`

### Phase 1: Intent Detection
Read user's first message. Classify domain:
```
"Fix the login bug"       → [backend, auth, debug]
"Write a blog post"       → [content, writing]
"Deploy to staging"       → [infra, deployment]
"Set up Meta ads"         → [marketing, meta, ads]
"Make a product video"    → [visual, video, production]
```

### Phase 2: Tag Matching
Score each memory file:
```
For each memory file:
  score = count(file.tags ∩ detected_domains)
  if score > 0: candidate
```

Also always include:
- `state_current.md` (if exists) — always relevant
- Files tagged `[critical]` — always relevant

### Phase 3: Link Following
For each candidate file, scan for `[[links]]`:
```
If file A is included and contains [[file_B]]:
  also include file_B
```
Depth limit: 1 hop (prevent chain-loading entire memory).

### Phase 4: Global Memory Merge
Check `~/.claude/global-memory/`:
- `credentials.md` → include if session involves API calls
- `preferences.md` → always include (tiny, universal)

### Phase 5: Build Compiled Context
```markdown
## Compiled Context (auto-generated by memory-governor)

### State
[from state_current.md]

### Relevant Knowledge
[from tag-matched files]

### Global
[from global-memory, if relevant]
```

### Phase 6: Cache
Save to `memory/.compiled/{domain_hash}.md` with timestamp.
Next session with same domain → reuse if no source files changed.

---

## Step-by-step: `capture`

| What | Where | Tags |
|------|-------|------|
| Decisions | memory/decisions.md | [decision, {domain}] |
| Errors | memory/errors.md | [error, {domain}] |
| Preferences | ~/.claude/global-memory/preferences.md | [preference] |
| Credentials | ~/.claude/global-memory/credentials.md | [credential, {service}] |
| State changes | memory/state_current.md | [state, critical] |

Rules:
- Append, don't overwrite
- Absolute dates only
- < 3 lines per entry
- Add `[[links]]` to related files
- Add tags matching the domain

---

## Step-by-step: `setup-hooks`

Creates `.claude/hooks.json`:
```json
{
  "hooks": {
    "SessionStart": [{
      "command": "bash ~/.claude/skills/memory-governor/scripts/session-start.sh",
      "description": "Load governance alerts, compile context if cached"
    }],
    "PreCompact": [{
      "command": "bash ~/.claude/skills/memory-governor/scripts/pre-compact.sh",
      "description": "Extract key state before context compaction"
    }],
    "SessionEnd": [{
      "command": "bash ~/.claude/skills/memory-governor/scripts/session-end.sh",
      "description": "Capture knowledge, check memory health"
    }]
  }
}
```

---

## Token Math

```
Without compile: ~3000 tokens (full index + CLAUDE.md)
With compile:    ~800 tokens (tag-matched subset)
With cache:      ~600 tokens (pre-compiled)
Savings:         73-82%
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

## Anti-Patterns Fixed

1. **Knowledge Dump** — Everything in CLAUDE.md → Layer down
2. **Untagged Files** — Can't compile without tags → Auto-tag
3. **Island Files** — No links between related knowledge → Add links
4. **Project-Locked Knowledge** — Credentials repeated per-project → Global memory
5. **Shotgun Loading** — Load everything every session → Compile per-intent
6. **Zombie State** — Old "current" state → Update or archive
7. **Date Decay** — Relative dates → Absolute dates
