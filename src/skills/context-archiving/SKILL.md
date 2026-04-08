---
name: context-archiving
description: |
  Moves completed backlog items, old decisions, finished projects, and stale session notes from active context files into context/archive/ counterparts. Use when active context files grow large, when closing out completed work, or during periodic context maintenance.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v1
    id: SKILL-context-archiving
    version: "1.1.0"
    created: 2026-04-06T00:00:00Z
    category: process
    layer: 2
---

# Context Archiving

## Intro

Archiving moves done work out of active context files into a
parallel `context/archive/` tree. Active files stay focused on
current work; archive files preserve full history. Items are never
deleted — only moved.

## Overview

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

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Deleting items instead of moving them.** Archiving is a move operation — the content goes to `context/archive/`, never disappears. Deletion destroys history that may be needed months later to understand why something was built or decided. If in doubt, archive; never delete.
- **Renumbering items during the archive move.** IDs like `DEC-042` or `BACK-007` are permanent identifiers referenced from code comments, PR descriptions, and other context files. Changing the ID during archiving breaks those references silently. IDs are stable across active and archive — the content moves, the ID stays the same.
- **Archiving an item that is still referenced by an open ticket or active context file.** A backlog item linked from an open GitHub issue should stay active even if it is marked `done`, until the issue closes. Before archiving, check whether the item is referenced from any live document or issue.
- **Reformatting content during the move.** A table row that archives as bullet points, or a section heading that becomes plain text, corrupts the document's structure and makes the archive harder to read and audit. Preserve the original format exactly: tables stay tables, headings stay headings.
- **Breaking bidirectional links.** Active files should link to their archive counterpart, and the archive should link back. Archiving without maintaining both directions means context becomes unreachable — a future reader may not know that a history of older decisions exists in the archive.
- **Archiving in-progress work because it "looks old."** The status of an item — not its age — determines archive eligibility. A decision from three years ago that is still actively referenced is not eligible for archiving. A workitem that has been in "in-progress" state for six months is also not eligible — it needs to be addressed or explicitly cancelled first.
- **Running archiving without first checking the invariants.** Before moving any item, verify: the active file's "Next ID" counter is unchanged, no open references will be broken, and the archive file exists (or needs to be created). Archiving without these checks leaves the context in a partially consistent state.

## Full reference

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
