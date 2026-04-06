---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-standup-context
  name: standup-context
  version: "1.0.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Manages session standup notes in context/STANDUPS.md. Records what was done, what is planned, and any blockers at the start or end of work sessions."
  category: process
  layer: 2
---

# Session Standup Notes (Context-based)

## When to use

At the start of a new session, or when the user asks to record progress.

## Instructions

1. Read context/STANDUPS.md
2. Add a new entry with today's date as heading
3. Each entry includes:
   - **Done:** What was completed since last session
   - **Next:** What is planned for this session
   - **Blockers:** Any issues preventing progress (or "None")
4. Place new entries at the top, below the header
5. Keep entries concise — one line per item
