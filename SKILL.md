---
name: memory-governor
description: Automatically scan, optimize, and restructure Claude Code memory architecture to minimize token consumption while preserving all knowledge. Works on any project.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
when_to_use: "Use when starting a new project, when token consumption feels high, when CLAUDE.md is bloated, or when memory files are disorganized. Triggers: '/memory-governor', 'optimize memory', 'reduce tokens', 'clean up memory', 'memory audit'"
argument-hint: "/memory-governor [audit|optimize|compact|report]"
arguments:
  - action
context: inline
---

# Memory Governor

Automatically audit and optimize Claude Code's memory architecture to minimize per-session token consumption while preserving all knowledge.

## Problem This Solves

Every Claude Code session loads CLAUDE.md + MEMORY.md into context. When these files grow unchecked (common after weeks of use), each session wastes thousands of tokens on stale rules, duplicate entries, and content that belongs in lower layers. This skill fixes that automatically.

## Inputs
- `$action`: `audit` (analyze only) | `optimize` (fix issues) | `compact` (aggressive cleanup) | `report` (show stats)

## Architecture: The 4-Layer Knowledge Pyramid

```
Layer 0: CLAUDE.md (< 2KB)
  → Eternal principles only. Loaded EVERY session.
  → If it doesn't apply to EVERY conversation, it doesn't belong here.

Layer 1: MEMORY.md index (< 15 entries)
  → One-line pointers to Layer 2 files. Loaded every session.
  → Each entry < 120 chars. It's an INDEX, not content.

Layer 2: memory/*.md files
  → Detailed knowledge. Loaded ON DEMAND when relevant.
  → Decisions, credentials, project state, feedback rules.

Layer 3: skills/*.md + external files
  → Process templates and reference data. Loaded ONLY when invoked.
  → Never auto-loaded into context.
```

**Core rule: Content must live at the LOWEST layer where it's still accessible when needed.**

## Steps

### 1. Scan Current State
Run diagnostics:
```bash
# CLAUDE.md size
wc -c $(find . -name "CLAUDE.md" -maxdepth 1 2>/dev/null || echo "CLAUDE.md")

# Memory index entries
MEMORY_DIR=$(find ~/.claude/projects -path "*/memory/MEMORY.md" 2>/dev/null | head -1)
if [ -n "$MEMORY_DIR" ]; then
  echo "Index entries: $(grep -c '^-' "$MEMORY_DIR")"
  echo "Memory dir size: $(du -sh "$(dirname "$MEMORY_DIR")")"
  echo "Memory files: $(ls "$(dirname "$MEMORY_DIR")"/*.md 2>/dev/null | wc -l)"
fi

# Skills loaded
find ~/.claude/skills -name "SKILL.md" 2>/dev/null | wc -l
```

**Success criteria**: Output current sizes and counts

### 2. Audit CLAUDE.md (Layer 0)

Read CLAUDE.md and classify every section:

| Content Type | Correct Layer | Action |
|-------------|---------------|--------|
| Core thinking principles | 0 (CLAUDE.md) | Keep |
| Output format rules | 0 | Keep |
| Troubleshooting principles | 0 | Keep |
| API keys / credentials | 2 (memory file) | **Move down** |
| Product specs / details | 2 | **Move down** |
| Tool routing tables | 2 or 3 | **Move down** |
| Model selection rules | 2 | **Move down** |
| Project-specific state | 2 | **Move down** |
| Workflow procedures | 3 (skill) | **Move down** |
| Anti-patterns / error lists | 2 | **Move down** |
| Registered skills list | Remove (auto-detected) | **Delete** |

**Rules**:
- CLAUDE.md MUST be < 2KB after optimization
- Every line must pass the test: "Does this apply to EVERY conversation?"
- If no → move it to Layer 2 or 3

**Success criteria**: CLAUDE.md < 2KB, only eternal principles remain

### 3. Audit MEMORY.md Index (Layer 1)

Check each index entry:
- [ ] Is the linked file still relevant? (read it to verify)
- [ ] Is the entry < 120 characters?
- [ ] Is there a duplicate or near-duplicate entry?
- [ ] Has the linked content become stale? (check dates, verify facts)
- [ ] Can multiple entries be merged into one file?

**Rules**:
- Index MUST have < 15 entries
- Remove entries for completed/abandoned projects
- Merge related entries (e.g., 5 separate "feedback_*" → 1 "feedback_consolidated.md")
- NEVER delete the actual .md files — only remove from index
- Convert relative dates to absolute dates in memory files

**Success criteria**: Index < 15 entries, each < 120 chars, no stale pointers

### 4. Consolidate Memory Files (Layer 2)

Scan all memory/*.md files:

**Merge candidates** (files covering similar topics):
```bash
# Find similar filenames
ls memory/ | sort | uniq -d
# Find files with overlapping content
grep -l "keyword" memory/*.md
```

**Stale content check**:
- Files with dates > 30 days old → verify if still accurate
- Files referencing specific file paths → verify paths still exist
- Files with "TODO" or "待完成" → check if done

**Size check**:
- Any file > 5KB → consider splitting or summarizing
- Total memory dir > 100KB → needs aggressive consolidation

**Success criteria**: No duplicate files, no stale content, total < 100KB

### 5. Validate Skills (Layer 3)

Check installed skills:
- Are any skills auto-loading content into context? (they shouldn't)
- Are any skills duplicating knowledge already in memory?
- Do skills have clear `when_to_use` triggers? (prevents false activation)

**Success criteria**: Skills are lazy-loaded only, no context pollution

### 6. Output Report

```markdown
## Memory Governor Report

### Before
- CLAUDE.md: X KB (~Y tokens)
- Memory index: N entries
- Memory files: M files, Z KB total
- Skills: S installed
- Estimated per-session fixed cost: T tokens

### After
- CLAUDE.md: X KB (~Y tokens)
- Memory index: N entries
- Memory files: M files, Z KB total
- Estimated per-session fixed cost: T tokens

### Changes Made
- [list of specific changes]

### Savings
- Token reduction: XX%
```

## Token Estimation Formula

```
Per-session tokens ≈ (CLAUDE.md bytes / 3) + (MEMORY.md bytes / 3)
```

Rough guide:
- 1KB text ≈ 330 tokens
- Target: < 1000 tokens fixed cost per session
- Max acceptable: 2000 tokens

## Common Anti-Patterns This Fixes

1. **CLAUDE.md as knowledge dump** — People add every rule, API key, and project detail to CLAUDE.md. Fix: move to Layer 2.
2. **Memory index as content** — Index entries that are paragraphs instead of pointers. Fix: one-line summaries only.
3. **Duplicate knowledge** — Same fact in CLAUDE.md AND a memory file AND a skill. Fix: single source of truth at lowest viable layer.
4. **Stale state** — "Current task: doing X" from 3 weeks ago. Fix: update or remove.
5. **Skill over-specification** — Skills with 5KB of rules that get loaded on false triggers. Fix: clear `when_to_use` and minimal content.
