---
name: decisions-adr
description: |
  Records architectural and process decisions in context/DECISIONS.md with rationale and alternatives, in inverse-chronological ADR format. Use when the user makes a significant technical or process decision that should be captured for future readers.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v1
    id: SKILL-decisions-adr
    version: "1.1.0"
    created: 2026-04-06T00:00:00Z
    category: process
    layer: 2
---

# Decision Tracking (ADR format)

## Intro

Decisions are recorded in `context/DECISIONS.md`, one entry per
choice, numbered `DEC-NNN` in inverse chronological order. Each
entry captures what was decided, why, and what else was on the
table.

## Overview

### Where decisions live

All entries go in `context/DECISIONS.md`. New decisions are added
at the top (just below the file header). Older decisions are
pushed down. The file's "Next ID" counter (if present) determines
the next number.

### Entry format

Each entry contains:

- **Decision** — what was chosen, in one sentence
- **Rationale** — why this option was picked
- **Alternatives** — what else was considered

Add the date in parentheses after the title:

```
## DEC-042: Use Postgres over MySQL (2026-04-07)

**Decision:** Standardize on Postgres for all new services.

**Rationale:** Better JSON support, stronger constraint system,
existing team familiarity.

**Alternatives:** MySQL (less expressive types), SQLite (won't
scale to multi-instance deploys).
```

## Full reference

### Numbering rules

- IDs are sequential and never reused.
- Inverse chronological in the file means newest at the top —
  but ID `DEC-042` is always `DEC-042`, regardless of where it
  sits relative to neighbors after later edits.
- If a decision is superseded, do not delete it. Add a new entry
  that references the superseded ID, and add a "Superseded by
  DEC-NNN" note to the original.

### What counts as a decision

Anything a future maintainer might reasonably ask "why did we do
it this way?" about. Examples:

- Choosing one library or framework over another
- Deciding on a coding convention that isn't enforced by tooling
- Setting a process rule (e.g. "all PRs require two reviewers")
- Rejecting a proposed approach (record the rejection so it
  doesn't get re-proposed)

What does *not* count: routine implementation choices, refactors,
bug fixes. These belong in commit messages, not decision records.

### Cross-referencing

Link decisions from code comments, PR descriptions, or other
context files when they explain the reasoning behind a choice.
A decision that isn't referenced from anywhere is at risk of
being forgotten.
