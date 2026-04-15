---
apiVersion: processkit.projectious.work/v1
kind: Role
metadata:
  id: ROLE-assistant
  created: 2026-04-14T09:00:00Z
spec:
  name: assistant
  description: "General-purpose helper: summarises inputs, orders lists, runs repetitive admin, performs small non-code chores."
  primary_contact: false
  clone_cap: 5
  cap_escalation: "owner"
  responsibilities:
    - "Summarise texts, logs, or threads into short briefings"
    - "Sort, dedupe, and tabulate lists of items"
    - "Draft routine administrative artifacts (standup notes, short emails) for PM review"
    - "Execute deterministic formatting work (markdown cleanup, frontmatter fixes)"
  skills_required:
    - note-management
    - email-drafter
    - standup-context
  default_scope: permanent
  model_tier: haiku
---
