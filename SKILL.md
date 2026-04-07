---
name: memory-governor
description: Safe memory enhancement with auto-running engines. Procedural memory, metabolism, anti-amnesia. Install → hooks auto-run → memory self-improves. Zero dependencies.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
when_to_use: "Use when memory needs governance, or when Claude forgets proven methods. Triggers: '/memory-governor', 'optimize memory', 'compile memory'"
argument-hint: "/memory-governor [audit|optimize|compile|capture|metabolism|setup-hooks]"
arguments:
  - action
context: inline
---

# Memory Governor v4

**Install → hooks auto-run → memory self-improves.** No manual intervention needed.

## What's Different in v4

v1-v3 were "instruction manuals" — Claude had to read the SKILL.md and pretend to execute.
v4 has **real code** that runs automatically via hooks:

| Component | File | Runs |
|-----------|------|------|
| Compile engine | `scripts/compile.py` | Auto at SessionStart |
| Metabolism engine | `scripts/metabolism.py` | Auto at SessionEnd |
| Backup engine | `scripts/backup.py` | Before any optimize |
| Audit script | `scripts/audit.sh` | On demand |

## Safety Guarantees

1. Files NEVER deleted — only archived to `.backup/`
2. `critical: true` files are permanently untouchable
3. Backup auto-created before any optimize
4. Metabolism recommends, never auto-archives

## Quick Start

```bash
# Install
git clone https://github.com/JiazheYebos/memory-governor.git ~/.claude/skills/memory-governor

# Activate hooks (one-time)
/memory-governor setup-hooks

# That's it. Hooks handle everything automatically.
```

## Actions

### `/memory-governor setup-hooks`
Create `.claude/hooks.json` with SessionStart + SessionEnd hooks.
**This is the only action most users need to run.**

### `/memory-governor audit`
```bash
bash ~/.claude/skills/memory-governor/scripts/audit.sh
```

### `/memory-governor compile [topic]`
```bash
python3 ~/.claude/skills/memory-governor/scripts/compile.py "fix auth bug"
```
Generates `memory/.compiled/context.md` — read this instead of all memory files.

### `/memory-governor metabolism`
```bash
python3 ~/.claude/skills/memory-governor/scripts/metabolism.py
```

### `/memory-governor capture`
After solving a hard problem, write a procedure file:
```
memory/procedures/{name}.md
```
Format:
```yaml
---
name: descriptive_name
tags: [relevant, tags]
critical: true  # if vital
proven: true
---
# Title
## Working Solution
[exact steps/code]
## Failed Approaches
[what didn't work]
```

### `/memory-governor optimize`
Runs backup first, then:
1. Check CLAUDE.md for layer violations
2. Move misplaced content to memory files
3. Merge duplicates
4. Add missing tags
5. Rebuild index

**Always shows diff and asks for confirmation.**
