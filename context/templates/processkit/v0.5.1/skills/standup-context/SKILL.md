---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-standup-context
  name: standup-context
  version: "1.1.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Manages session standup notes in context/STANDUPS.md — done, next, blockers."
  category: process
  layer: 2
  when_to_use: "Use at the start of a new session, or when the user asks to record progress, log a standup, or add a daily check-in entry."
---

# Session Standup Notes (Context-based)

## Level 1 — Intro

A standup note is a one-screen log of what was just done, what is
about to happen, and what is blocked. Append a fresh entry to
`context/STANDUPS.md` at the top of each session so the team (and
future agents) have a continuous timeline of progress.

## Level 2 — Overview

### How to add an entry

1. Read `context/STANDUPS.md`.
2. Add a new entry with today's date as the heading.
3. Place the new entry at the top of the file, immediately below
   the header. Most recent first.

### Entry shape

Each entry contains three sections:

- **Done** — what was completed since the last session.
- **Next** — what is planned for this session.
- **Blockers** — any issues preventing progress, or "None".

Keep entries concise: one line per item, no paragraphs.

### Example

```markdown
## 2026-04-07

**Done:**
- BACK-014: rewrote 9 process skills to three-level format
- Verified line wrapping with awk

**Next:**
- BACK-015: smoke-test the rewritten skills

**Blockers:**
- None
```

## Level 3 — Full reference

### Why standups belong in context, not a chat tool

Putting standups in `context/STANDUPS.md` makes them part of the
project's persistent memory. A chat-tool standup is gone when the
channel scrolls; a context-file standup is in git, indexable, and
visible to every agent that opens the project.

### Anti-patterns

- Long paragraphs instead of bullets
- Backfilling missed days with invented activity (just skip them)
- Vague "next" entries like "continue work" — name the item
- Treating "blockers: none" as filler — if there really is a
  blocker, surface it loudly
- Letting the file grow forever without archival; rotate to
  `context/archive/standups/` when it gets long
