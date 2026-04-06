---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-decisions-adr
  name: decisions-adr
  version: "1.0.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Manages architectural decision records in context/DECISIONS.md. Records decisions with rationale, alternatives considered, and implications."
  category: process
  layer: 2
---

# Decision Tracking (ADR format)

## When to use

When the user makes a significant technical or process decision that should be recorded.

## Instructions

1. Read context/DECISIONS.md
2. Assign the next DEC-NNN number (inverse chronological order)
3. Each entry includes:
   - **Decision:** What was decided
   - **Rationale:** Why this option was chosen
   - **Alternatives:** What else was considered
4. Add the date in parentheses after the title
5. Place new decisions at the top, below the header
