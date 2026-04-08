---
name: backlog-context
description: |
  Manages a project backlog as a BACKLOG.md file in the context directory using a simple Markdown checkbox format. Use when adding, updating, prioritizing, or reviewing items in context/BACKLOG.md.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v1
    id: SKILL-backlog-context
    version: "1.1.0"
    created: 2026-04-06T00:00:00Z
    category: process
    layer: 2
---

# Backlog Management (Context-based)

## Intro

The backlog lives in `context/BACKLOG.md` as a checkbox-formatted
Markdown list. It is grouped by priority and references GitHub issues
where they exist. Edit it directly when work items change.

## Overview

### File location and format

Read and edit `context/BACKLOG.md`. Each work item uses the checkbox
format:

```
- [ ] **Title** — Description
```

Use `[x]` for completed items. Reference GitHub issues with `(#N)`
inline so links are easy to follow.

### Priority groups

Group items under priority headings, in order:

1. **Next Up** — actively staged for the current iteration
2. **Planned** — committed but not yet started
3. **Ideas** — speculative or unrefined

New items default to Ideas unless the user signals otherwise.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Adding items directly to "Next Up" without user confirmation.** The "Next Up" group represents actively staged work for the current iteration. Moving a speculative idea there without the user's explicit direction may displace or confuse the actual prioritized work. New items default to "Ideas" unless the user explicitly signals otherwise.
- **Duplicating an item instead of moving it between groups.** When an item's priority changes, the correct action is to move it from one group to another — not to create a second entry in the target group. Duplicates fragment the backlog, make status tracking unreliable, and require manual reconciliation later.
- **Marking items completed in the backlog instead of letting context-archiving handle removal.** This skill marks `[x]` in place; archiving completed items to `context/archive/` is the responsibility of the `context-archiving` skill. Don't conflate the two: mark done here, archive later through the separate skill.
- **Expanding item descriptions inline instead of linking to a workitem or issue.** A single line is the correct granularity for a backlog item. If the item requires a spec, acceptance criteria, or detailed notes, link to a tracked workitem or GitHub issue rather than expanding the backlog entry into a multi-paragraph description.
- **Letting the backlog grow without periodic grooming.** A backlog with 200 items in "Ideas" that haven't been touched in a year provides no signal about priorities. Stale backlogs erode trust in the document as an authoritative source. Periodically (via the `context-grooming` skill or manual review) prune ideas that are no longer viable and promote items that have become urgent.
- **Using the backlog as a task tracker for in-progress work.** The backlog tracks what exists and its priority tier, not who is working on it or what sub-tasks it entails. Detailed task decomposition and status tracking belong in a workitem, GitHub issue, or a project management system. The backlog is an inventory, not a project board.
- **Not updating the backlog at session end when items changed status.** The handover note becomes misleading if it claims an item is done while the backlog still shows it as in-progress, or vice versa. The rule is: update the backlog at the end of the session when any item's status changed — before writing the handover note.

## Full reference

### Editing rules

- Preserve the existing group ordering when adding items.
- Move items between groups as priority changes — do not duplicate.
- Mark items completed in place with `[x]`; archival of completed
  items is the job of the `context-archiving` skill, not this one.
- Keep the description on a single line; if more detail is needed,
  link to a workitem, issue, or doc instead of expanding inline.

### Cross-references

When a backlog item maps to a GitHub issue, append `(#N)` to the
title. When it maps to a tracked workitem, link the workitem id
(e.g. `WORK-042`) so the index MCP server can resolve it.
