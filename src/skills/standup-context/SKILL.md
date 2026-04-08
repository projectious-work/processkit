---
name: standup-context
description: |
  Manages session standup notes in context/STANDUPS.md — done, next, blockers. Use at the start of a new session, or when the user asks to record progress, log a standup, or add a daily check-in entry.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v1
    id: SKILL-standup-context
    version: "1.1.0"
    created: 2026-04-06T00:00:00Z
    category: process
    layer: 2
---

# Session Standup Notes (Context-based)

## Intro

A standup note is a one-screen log of what was just done, what is
about to happen, and what is blocked. Append a fresh entry to
`context/STANDUPS.md` at the top of each session so the team (and
future agents) have a continuous timeline of progress.

## Overview

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

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Appending the new entry at the bottom instead of the top.** The skill requires most-recent-first ordering. An entry appended at the end requires scrolling the entire file to find today's standup. Always insert immediately below the file header, not at the bottom.
- **Writing Done in future tense.** Done is for what was actually completed since the last session, not plans. "Will fix the login bug" in the Done section is wrong — future intentions belong in Next. If nothing was completed, write "None" rather than inventing done items.
- **Conflating slow progress with blockers.** "It's taking longer than expected" is not a blocker. A blocker is a specific external dependency or obstacle that cannot be resolved without another person or decision. Vague blockers provide no actionable information.
- **Writing multi-paragraph standup entries.** Standups are one line per item, not prose. Detailed explanations belong in workitems, decision records, or code comments. Multi-paragraph entries dilute the signal for readers scanning recent activity.
- **Skipping the standup when there is nothing visible to report.** A session with no commits still has a standup: what was read, what was investigated, what was ruled out. Gaps in the standup log make the project timeline harder to reconstruct.
- **Back-filling standups with invented entries for missed sessions.** If a session was missed, leave the gap visible rather than manufacturing an entry with a past date. An invented entry misrepresents the project timeline and creates confusion if audited.
- **Not reading STANDUPS.md before appending.** Failing to read the file first risks duplicating the most recent date heading or inserting the new entry in the wrong location. Always read the file before adding an entry.

## Full reference

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
