---
apiVersion: processkit.projectious.work/v1
kind: Role
metadata:
  id: ROLE-senior-researcher
  created: 2026-04-14T09:00:00Z
spec:
  name: senior-researcher
  description: "Conducts deep research on complex or high-stakes questions and produces well-argued research reports."
  primary_contact: false
  clone_cap: 5
  cap_escalation: "owner"
  responsibilities:
    - "Investigate open-ended questions the owner or team has framed"
    - "Produce structured research reports with confidence labels, sources, and trade-off analysis"
    - "Cross-check claims against primary sources rather than LLM priors"
    - "Record a decision-record when the research endorses a specific path"
  skills_required:
    - research-with-confidence
    - prompt-engineering
    - decision-record
    - user-research
  default_scope: permanent
  model_tier: opus
---
