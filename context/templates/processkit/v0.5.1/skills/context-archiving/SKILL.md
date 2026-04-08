---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-context-archiving
  name: context-archiving
  version: "1.1.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Moves completed backlog items, old decisions, finished projects, and stale session notes from active context files into context/archive/ counterparts."
  category: process
  layer: 2
  when_to_use: "Use when active context files grow large, when closing out completed work, or during periodic context maintenance."
---

# Context Archiving

## Level 1 — Intro

Archiving moves done work out of active context files into a
parallel `context/archive/` tree. Active files stay focused on
current work; archive files preserve full history. Items are never
deleted — only moved.

## Level 2 — Overview

### What gets archived

For each active file under `context/`, identify items eligible for
the archive:

- **Backlog** — items with status `done` or `archived`
- **Decisions** — older than the most recent ~6 entries, or
  explicitly superseded by a newer decision
- **Projects** — status `complete` or `archived`
- **Session notes** — older than the 3 most recent sessions

### The archive procedure

1. Read the active context file and its archive counterpart in
   `context/archive/`.
2. Identify the eligible items per the rules above.
3. Move them — preserve the original format (tables stay tables,
   headings stay headings).
4. Verify cross-references: each active file should link to its
   archive (`[archive/X.md](archive/X.md)`) and the archive should
   link back (`[../X.md](../X.md)`).
5. Confirm the active file's "Next ID" counter is unchanged
   (archiving must not renumber live items).

## Level 3 — Full reference

### Invariants

- **Never delete.** Move only. The archive is the canonical history.
- **Never renumber.** IDs are stable across active and archive.
- **Preserve format.** A row in a table stays a row; a heading
  stays a heading. Don't reformat in transit.
- **Bidirectional links.** Active <-> archive must always be
  reachable from both directions.

### Edge cases

- A decision that supersedes another: move the superseded one but
  leave a stub line in the active file referencing the new
  decision and the archive entry.
- A project that was archived but is being revived: move it back
  to active and note the revival in session notes; don't pretend
  it was never archived.
- A backlog item linked from an open issue: keep it active even
  if marked `done`, until the issue closes.

### Relationship to context-grooming

Archiving is mechanical movement based on status. `context-grooming`
is a broader review that may decide *what* should be done with
items (compress, summarize, drop entirely). Archiving runs more
often and with less judgment; grooming runs periodically and is
more opinionated.
