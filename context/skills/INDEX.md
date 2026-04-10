# skills/

Multi-artifact skill packages. Each skill is a directory containing instructions
(SKILL.md), examples, templates, and optionally a Python MCP server.

## Directory layout

Skills are organized into 7 category subdirectories.

```
skills/
  processkit/    — 30 skills for operating the processkit system
  engineering/   — 46 skills: software design, architecture, backend, languages
  devops/        — 15 skills: infrastructure, CI/CD, ops, monitoring
  data-ai/       — 11 skills: data science, ML, AI/LLM, embeddings
  product/       — 11 skills: product management, discovery, communication
  documents/     —  8 skills: document and content authoring
  design/        —  5 skills: visual, UI, and frontend design
  _lib/          — internal processkit Python library (not a skill)
```

## processkit skill hierarchy

The 30 processkit/ skills form a strict dependency hierarchy:

Layer 0 — foundation: `index-management`, `id-management`, `event-log`
Layer 1 — primitive management: `actor-profile`, `role-management`
Layer 2 — core entities: `workitem-management`, `decision-record`,
  `scope-management`, `category-management`, `cross-reference-management`,
  `binding-management`
Layer 3 — process orchestration: `process-management`, `state-machine-management`,
  `gate-management`, `schedule-management`, `constraint-management`,
  `migration-management`
Layer 4 — cross-cutting: `discussion-management`, `metrics-management`,
  `owner-profiling`, `context-grooming`, `note-management`, `morning-briefing`,
  `standup-context`, `status-update-writer`, `model-recommender`, `skill-finder`,
  `skill-builder`, `skill-reviewer`, `session-handover`, `agent-management`
