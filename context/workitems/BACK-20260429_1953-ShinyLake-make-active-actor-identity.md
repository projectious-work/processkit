---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260429_1953-ShinyLake-make-active-actor-identity
  created: '2026-04-29T19:53:06+00:00'
  labels:
    area: team
    release: next
    source: user-request
spec:
  title: Make active actor identity visible in harness sessions
  state: backlog
  type: story
  priority: high
  description: Define how a project chooses a main interlocutor actor/team-member
    at harness startup and how responses identify whether the active speaker is the
    main interlocutor, a delegated role, or a specialist actor. The design should
    cover AGENTS.md/session briefing conventions, TeamMember defaults, role/model
    routing, and provider-neutral transcript markers without hard-coding Claude, Codex,
    or any vendor.
---
