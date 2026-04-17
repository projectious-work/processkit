---
apiVersion: processkit.projectious.work/v1
kind: Role
metadata:
  id: ROLE-senior-architect
  created: 2026-04-14T09:00:00Z
spec:
  name: senior-architect
  description: "Designs large new features and complex bug fixes; decomposes large work into implementation-sized tasks."
  primary_contact: false
  clone_cap: 5
  cap_escalation: "owner"
  responsibilities:
    - "Produce end-to-end design plans for large or cross-cutting features"
    - "Diagnose complex bugs where root cause is unclear or spans subsystems"
    - "Break large designs into developer-sized WorkItems with explicit success criteria"
    - "Record architectural decisions via decision-record before implementation begins"
    - "Review senior-sensitive PRs (schema, API contract, state-machine changes)"
  skills_required:
    - software-architecture
    - system-design
    - domain-driven-design
    - software-modularization
    - decision-record
    - threat-modeling
  default_scope: permanent
  model_tier: opus
  model_profiles:
    - { rank: 1, provider: anthropic, family: claude-opus, default_version: "4.7", default_effort: high,
        rationale: "Deep reasoning for large design; xhigh on multi-subsystem cases" }
    - { rank: 2, provider: openai, family: gpt-5, default_version: "5.4", default_effort: high,
        rationale: "Strong when Computer Use or OpenAI ecosystem integration required" }
    - { rank: 3, provider: xai, family: grok, default_version: "4.20", default_effort: high,
        rationale: "Pick when 2M-token context or multi-agent ensemble is the constraint" }
---
