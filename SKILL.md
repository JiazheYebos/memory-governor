---
name: memory-governor
description: Safe memory enhancement for Claude Code. Never loses knowledge — procedural memory, metabolism, anti-amnesia. Strengthens recall while reducing waste. Zero dependencies.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
when_to_use: "Use when token consumption is high, memory is disorganized, or when Claude forgets proven methods. Triggers: '/memory-governor', 'optimize memory', 'compile memory', 'what did I do before'"
argument-hint: "/memory-governor [audit|optimize|compile|capture|metabolism|setup-hooks]"
arguments:
  - action
context: inline
---

# Memory Governor

Safe memory enhancement for Claude Code. Core principle:

> **NEVER lose existing knowledge. Enhance recall. Reduce waste as a side effect.**

Four capabilities:

1. **Procedural Memory** — Remembers HOW you solved problems, not just WHAT happened
2. **Memory Metabolism** — Hot memories auto-promote, cold memories auto-demote
3. **Anti-Amnesia** — Prevents re-exploring failed paths when a proven solution exists
4. **Safety-First Architecture** — Backup before any change, no silent deletions

Zero dependencies. Zero infrastructure. Just organized Markdown.

---

## ⚠️ Safety Guarantees (NON-NEGOTIABLE)

These rules override everything else in this skill:

1. **NEVER delete any file.** Move to `memory/.archive/` instead. Always recoverable.
2. **NEVER modify content without backup.** Before any optimize/compact, create `memory/.backup/{timestamp}/`
3. **NEVER remove from CLAUDE.md without confirming the content exists in a memory file first.** Moving content down layers ≠ deleting it.
4. **NEVER auto-execute optimize/compact.** Always show diff and require human confirmation.
5. **Files tagged `critical: true` are UNTOUCHABLE.** They are never moved, merged, archived, or modified by any automated action.
6. **Metabolism NEVER auto-archives.** Cold temperature is a recommendation, not an action. Only humans decide to archive.

### The Critical Tag

Any memory file with `critical: true` in frontmatter is permanently protected:
```yaml
---
name: trading_strategy_alpha
tags: [quant, strategy, trading]
critical: true
---
```
Memory Governor will:
- ✅ Include it in compile (always, regardless of temperature)
- ✅ Track its access temperature
- ❌ NEVER suggest moving, merging, archiving, or modifying it
- ❌ NEVER exclude it from context, even in aggressive compact mode

---

## The Problem This Solves (That Nobody Else Does)

Every memory system stores facts and events. None store **proven methods**.

Example: You successfully connect to an API after 30 minutes of debugging. The working code, the correct URL, the auth method — all lost next session. You start from scratch, try wrong approaches, waste time, and might even conclude "it can't be done" — when you literally did it yesterday.

This is **procedural amnesia**: forgetting skills you've already demonstrated.

Memory Governor fixes this with a dedicated procedural memory layer that captures every successful method and surfaces it before you try alternatives.

---

## Architecture: 5-Layer Knowledge Pyramid

```
Layer 0: CLAUDE.md            < 2KB     Eternal principles. Always loaded.
Layer 1: MEMORY.md index      < 15 entries  Tagged pointers. Always loaded.
Layer 2: memory/*.md           On-demand   Facts, decisions, state. Tag-indexed.
Layer 3: memory/procedures/*.md  On-demand   PROVEN METHODS. The "how I did it" layer.
Layer 4: skills/ + docs/       On-invoke   Templates & reference.
```

**Layer 3 is new.** It stores procedural knowledge — successful API integrations, working code patterns, solved problems — in a structured "recipe" format.

---

## Procedural Memory Format

```markdown
---
name: stripe_webhook_setup
tags: [api, stripe, payments, webhook]
proven: true
last_used: 2026-04-01
success_count: 3
---

# Stripe Webhook — Proven Working Method

## What
Set up Stripe webhook endpoint with signature verification

## Working Solution
- Endpoint: POST /api/webhooks/stripe
- Verify signature using `stripe.webhooks.constructEvent()`
- Must use raw body (not parsed JSON) for signature check

## Failed Approaches (never retry these)
- ❌ Using parsed JSON body → signature always fails
- ❌ express.json() middleware before webhook route → breaks raw body
- ❌ Webhook secret from dashboard test mode → doesn't work in live

## Code
\```python
import stripe
event = stripe.Webhook.construct_event(
    payload=request.body,  # RAW body, not JSON
    sig_header=request.headers['Stripe-Signature'],
    endpoint_secret=WEBHOOK_SECRET
)
\```
```

### Anti-Amnesia Rule

When Claude encounters a task, BEFORE trying any approach:
1. Check `memory/procedures/` for a matching procedure
2. If found and `proven: true` → **USE IT DIRECTLY**. Do NOT explore alternatives.
3. If not found → proceed normally, but capture the working method when done.

**This single rule prevents 90% of wasted time from re-exploration.**

---

## Memory Metabolism

Every memory file tracks access patterns:

```yaml
---
accessed: [2026-03-25, 2026-04-01, 2026-04-08]
temperature: hot    # auto-calculated
---
```

### Temperature Rules

| Temperature | Criteria | Compile Behavior |
|------------|---------|-----------------|
| 🔴 Hot | Accessed 3+ times in 14 days | Always include in compile |
| 🟡 Warm | Accessed 1-2 times in 14 days | Include if tags match |
| 🔵 Cool | Accessed in last 30 days | Include only if directly referenced |
| ⚪ Cold | Not accessed in 30+ days | Never auto-include, archive candidate |

### Metabolism Hook (session-end)

After each session, the hook:
1. Records which memory files were actually read
2. Updates `accessed` timestamps
3. Recalculates temperature
4. Flags cold files for review

This means the system **learns from actual usage** — no manual tagging needed for priority.

---

## Compile (v3 — Intent + Tags + Metabolism + Procedures)

### Phase 1: Intent Detection
```
"Fix the auth bug" → [backend, auth, debug]
```

### Phase 2: Procedure Check (FIRST)
Before loading any facts, check procedures:
```
Search memory/procedures/ for tags matching [backend, auth, debug]
If found → include proven solutions FIRST
```
This ensures Claude starts with "what worked before" not "let me figure it out."

### Phase 3: Temperature-Weighted Tag Match
```
For each memory file:
  relevance = tag_match_score × temperature_weight
  hot files get 2x weight
  cold files get 0.1x weight
```

### Phase 4: Link Following
If file A is included and contains `[[file_B]]` → include B (depth 1).

### Phase 5: Global Memory
`~/.claude/global-memory/` — credentials, preferences (cross-project).

### Phase 6: Build + Cache
Compiled output → `memory/.compiled/{domain}.md`
Procedures section always on top.

---

## Actions

### `/memory-governor audit`
Measure state + check for unrecorded procedures + find cold memories.

### `/memory-governor optimize`
Fix layers + add tags + add links + set up procedures directory.

### `/memory-governor compile`
Intent → procedures → temperature-weighted tags → links → build.

### `/memory-governor capture`
After solving a problem, capture:
- Facts → `memory/`
- **Working method → `memory/procedures/`** (the key differentiator)
- Credentials → `~/.claude/global-memory/`

### `/memory-governor metabolism`
Force recalculate all temperatures. Show hot/warm/cool/cold distribution.

### `/memory-governor setup-hooks`
Install 5 lifecycle hooks.

---

## The Anti-Amnesia Protocol

Embed in CLAUDE.md (one line, always loaded):

```
Before attempting any technical task, check memory/procedures/ for proven methods. Use them directly. Do not explore alternatives unless the proven method fails.
```

This line costs ~20 tokens but prevents hours of re-exploration.

---

## Capture: The "Never Forget a Win" Rule

When a task succeeds after significant effort, IMMEDIATELY write a procedure:

```markdown
---
name: [task_name]
tags: [relevant, tags]
proven: true
last_used: [today]
success_count: 1
---

# [Task] — Proven Working Method

## What
[One-line description]

## Working Solution
[Exact steps, URLs, code that worked]

## Failed Approaches
[What was tried and didn't work — so you never retry these]
```

**The "Failed Approaches" section is as valuable as the working solution.** It prevents the most common failure: trying the same wrong approach again.

---

## Determination Rules (Anti-Give-Up Protocol)

Also embed in CLAUDE.md:

```
When blocked on a task:
1. Search memory/procedures/ for prior solutions
2. Search the web for alternatives (at least 3 sources)
3. Try at least 2 different approaches before reporting failure
4. NEVER say "can't be done" if you haven't exhausted options
5. If still stuck, explain what was tried and suggest what the user could try
```

---

## Token Math

```
Without governor: ~3300 tokens (everything loaded)
After optimize:   ~900 tokens (layer cleanup)
After compile:    ~600 tokens (intent + temperature)
Procedure hit:    ~200 tokens extra (but saves 10-30 min of re-exploration)
```

The 200 tokens for a procedure file pays for itself thousands of times over in avoided re-work.

---

## vs. Competition

| | memory-governor v3 | Mem0 | claude-mem | MemGPT/Letta |
|---|---|---|---|---|
| Procedural memory | ✅ Dedicated layer | ❌ | ❌ | ❌ |
| Anti-amnesia | ✅ Check before explore | ❌ | ❌ | ❌ |
| Metabolism/decay | ✅ Access-based temp | ❌ | ❌ | ⚠️ RL-based |
| Failed path tracking | ✅ In procedure files | ❌ | ❌ | ❌ |
| Dependencies | Zero | Cloud API | Bun+SQLite | Agent framework |
| Token impact | -73% to -82% | -90% (cloud) | +500 | Variable |

**Our unique value: We're the only system that prevents AI from forgetting its own skills.**
