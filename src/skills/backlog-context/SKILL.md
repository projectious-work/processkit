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
