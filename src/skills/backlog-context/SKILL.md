---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-backlog-context
  name: backlog-context
  version: "1.0.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Manages project backlog as a BACKLOG.md file in the context directory. Creates, prioritizes, and tracks work items in Markdown format."
  category: process
  layer: 2
---

# Backlog Management (Context-based)

## When to use

When the user asks to add, update, or review backlog items.

## Instructions

1. Read context/BACKLOG.md
2. Work items use checkbox format: `- [ ] **Title** — Description`
3. Group by priority: Next Up, Planned, Ideas
4. Reference GitHub issues where they exist: (#N)
5. Mark completed items with [x]
