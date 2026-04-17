---
apiVersion: processkit.projectious.work/v1
kind: Role
metadata:
  id: ROLE-junior-architect
  created: 2026-04-14T09:00:00Z
spec:
  name: junior-architect
  description: "Handles small-to-medium design work, focused architectural questions, and moderate-complexity bug fixes."
  primary_contact: false
  clone_cap: 5
  cap_escalation: "owner"
  responsibilities:
    - "Design single-module features and moderate refactors"
    - "Answer architectural questions that do not require cross-subsystem reasoning"
    - "Diagnose bugs with a known-ish failure surface (single service, single module)"
    - "Escalate to senior-architect when scope, uncertainty, or blast radius grows mid-task"
  skills_required:
    - software-architecture
    - system-design
    - software-modularization
    - decision-record
  default_scope: permanent
  model_tier: sonnet
  model_profiles:
    - { rank: 1, provider: anthropic, family: claude-sonnet, default_version: "4.6", default_effort: medium,
        rationale: "Daily design workhorse; 256K output window for long design docs" }
    - { rank: 2, provider: openai, family: gpt-5, default_version: "5.4", default_effort: medium,
        rationale: "Fallback; cost-comparable to Sonnet" }
---
