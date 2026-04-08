# Memory Governor

**Procedural memory + auto-briefing for Claude Code.**

Claude Code remembers facts and preferences. It doesn't remember *how it solved problems*. After a hard debugging session, the working solution vanishes. Next time, it re-explores from scratch — or worse, retries the exact approach that already failed.

Memory Governor adds a `procedures/` directory that stores proven methods with failed approaches. One rule in CLAUDE.md makes Claude check it before attempting anything.

## Install

```bash
git clone https://github.com/JiazheYebos/memory-governor.git ~/.claude/skills/memory-governor
```

Then run `/memory-governor setup-hooks` once.

## What It Adds

### 1. Procedural Memory

`memory/procedures/` stores what worked and what didn't:

```markdown
# memory/procedures/stripe_webhook.md
## Working Solution
- Use raw body for signature verification (NOT parsed JSON)
- Webhook route BEFORE express.json() middleware
## Failed Approaches
- ❌ Parsed JSON body → signature always fails
- ❌ express.json() before webhook route → breaks verification
```

One rule in CLAUDE.md: *"Before any task, check procedures first. If found, use directly."*

### 2. Auto-Briefing

A Python script runs at session start and prints your current status:

```
📋 Session Briefing
🚨 Blocked: API key expired
🔄 In Progress: Feature branch deployment
📚 8 proven procedures available
```

You don't need to remember where you left off. Claude tells you.

### 3. Five Behavioral Rules (~100 tokens in CLAUDE.md)

```
- Check procedures before attempting any task
- Try 3+ approaches before reporting failure
- Verify output yourself before reporting done
- Tasks > 3 days old: ask if still relevant
- Write working solutions to procedures immediately
```

## What It Doesn't Do

- No database, no vector store, no HTTP server
- No automatic "memory compilation" (Claude's built-in selection works fine)
- No 181 skills or 47 agents
- Doesn't modify your existing memory files
- Doesn't add complexity to a working system

## Architecture

```
memory/
  procedures/       ← NEW: proven methods + failed approaches
  state_current.md  ← NEW: human-readable status for auto-briefing
  *.md              ← your existing memory files (untouched)
```

## Token Cost

| Item | Cost | When |
|------|------|------|
| 5 rules in CLAUDE.md | ~100 tokens | Every message |
| Briefing output | ~100 tokens | Session start (once) |
| **Total overhead** | **~100 tokens/message** | |

## When To Use This

**Good fit:**
- You work on complex projects across multiple sessions
- You've wasted time re-solving problems Claude already solved
- You lose track of project state between sessions

**Not needed:**
- Simple single-session tasks
- You already have a mature memory system with your own procedures

## Contributors

<a href="https://github.com/JiazheYebos">
  <img src="https://github.com/JiazheYebos.png" width="60" style="border-radius:50%"/>
</a>

## License

MIT
