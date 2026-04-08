---
name: memory-governor
description: Procedural memory + auto-briefing for Claude Code. Remember what works, forget nothing important. Zero dependencies.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
when_to_use: "Triggers: '/memory-governor', 'optimize memory', 'compile memory'"
argument-hint: "/memory-governor [audit|optimize|capture|setup-hooks]"
arguments:
  - action
context: inline
---

# Memory Governor

Two things Claude Code doesn't do well:
1. **Remember how it solved problems** (procedural memory)
2. **Keep the human oriented** across sessions (auto-briefing)

This skill adds both. Nothing else.

---

## Behavioral Rules (added to CLAUDE.md on setup, ~100 tokens)

```
- Before any task, check memory/procedures/ for proven methods. Use directly if found.
- When blocked, try 3+ approaches. Don't push problems to user.
- Verify output yourself before reporting done.
- Tasks in state_current.md > 3 days: ask user if still relevant.
- User decisions and working solutions: write to memory/procedures/ immediately.
```

---

## Procedural Memory

`memory/procedures/` stores proven methods with failed approaches:

```yaml
---
name: stripe_webhook
tags: [api, stripe]
proven: true
---
# Stripe Webhook
## Working Solution
- Use raw body for signature (NOT parsed JSON)
## Failed Approaches
- ❌ express.json() before webhook → breaks signature
```

**Anti-amnesia rule**: Before attempting any technical task, check procedures first. If a proven method exists, use it directly. Don't re-explore.

---

## Auto-Briefing

`scripts/briefing.py` runs at session start (via hook). Reads `memory/state_current.md` and prints:

```
📋 Session Briefing
🚨 Blocked: [items]
🔄 In Progress: [items]
📚 N proven procedures available
```

---

## Setup

```bash
git clone https://github.com/JiazheYebos/memory-governor.git ~/.claude/skills/memory-governor
/memory-governor setup-hooks
```

`setup-hooks` does:
1. Adds behavioral rules to CLAUDE.md (~100 tokens)
2. Creates `memory/procedures/` directory
3. Creates `memory/state_current.md` template
4. Installs SessionStart hook (briefing) and SessionEnd hook (health check)

---

## Actions

### `/memory-governor audit`
Measure CLAUDE.md size, index entries, procedure count.

### `/memory-governor optimize`
Move misplaced content from CLAUDE.md to memory files. Backup first, confirm before writing.

### `/memory-governor capture`
Write current conversation's working solutions to `memory/procedures/`.

### `/memory-governor setup-hooks`
One-time hook installation.

---

## What This Doesn't Do

- No vector database, no SQLite, no HTTP server
- No automatic context compilation (Claude's built-in memory selection is good enough)
- No metabolism engine (simple is better than clever)
- No 47 agents or 181 skills
- Doesn't modify your existing memory files

---

## Safety

- Files NEVER deleted, only archived
- `critical: true` tag protects files from any modification
- All optimize changes require human confirmation
