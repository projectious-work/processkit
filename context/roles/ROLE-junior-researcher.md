---
apiVersion: processkit.projectious.work/v1
kind: Role
metadata:
  id: ROLE-junior-researcher
  created: 2026-04-14T09:00:00Z
spec:
  name: junior-researcher
  description: "Handles bounded research and analysis tasks of small-to-medium complexity."
  primary_contact: false
  clone_cap: 5
  cap_escalation: "owner"
  responsibilities:
    - "Answer focused research questions (one topic, a handful of sources)"
    - "Summarise documentation, blog posts, and specs into structured findings"
    - "Gather and tabulate comparison data (prices, versions, feature matrices)"
    - "Escalate to senior-researcher when the question opens up or stakes rise"
  skills_required:
    - research-with-confidence
    - prompt-engineering
  default_scope: permanent
  model_tier: sonnet
---
