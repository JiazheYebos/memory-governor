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

**Enhances memory for both AI and human.** Install → hooks auto-run → memory self-improves.

## Two Users, One System

This skill helps **two kinds of memory failure**:

### AI Amnesia (Claude forgets)
- Forgets proven API methods → re-explores, wastes time, says "can't do it"
- Fix: Procedural memory + anti-amnesia protocol

### Human Overload (you forget)
- Too many projects → lose track of progress, blockers, decisions
- Fix: Auto-briefing at session start + proactive state capture

## Engines (real code, auto-run via hooks)

| Component | File | Runs | Helps |
|-----------|------|------|-------|
| Compile engine | `scripts/compile.py` | SessionStart | AI recall |
| Metabolism engine | `scripts/metabolism.py` | SessionEnd | AI + Human |
| Briefing engine | `scripts/briefing.py` | SessionStart | **Human recall** |
| Backup engine | `scripts/backup.py` | Before optimize | Safety |
| Audit script | `scripts/audit.sh` | On demand | Both |

## Safety Guarantees

1. Files NEVER deleted — only archived to `.backup/`
2. `critical: true` files are permanently untouchable
3. Backup auto-created before any optimize
4. Metabolism recommends, never auto-archives

## Human Memory Support

### Auto-Briefing (SessionStart)
Every new conversation, Claude automatically:
1. Reads `memory/state_current.md`
2. Shows a short status summary before anything else:
```
📋 Current state:
- [In progress items]
- [Blocked items]
- [Decisions needed]
Suggested priority: [top 1-2 items]
```

### Auto-Capture (ongoing)
When the user makes an important decision or changes direction, Claude writes it to memory immediately — without being asked. The user never needs to say "remember this."

### State File Template (`memory/state_current.md`)
```yaml
---
name: state_current
tags: [state, critical]
critical: true
---
```
Sections: Urgent/Blocked → In Progress → Completed → Key TODOs → API Status

**Token cost: ~50 tokens/session (CLAUDE.md rules) + ~500 tokens once at session start (state read). Negligible vs the time saved.**

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
