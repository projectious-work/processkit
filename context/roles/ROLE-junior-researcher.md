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
  model_profiles:
    - { rank: 1, provider: anthropic, family: claude-sonnet, default_version: "4.6", default_effort: low,
        rationale: "Bounded one-topic research; low effort keeps cost predictable" }
    - { rank: 2, provider: google, family: gemini-flash, default_version: "2.5", default_effort: medium,
        rationale: "Free tier / low cost for high-volume summarization" }
---
