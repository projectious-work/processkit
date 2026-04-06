# src/skills/

Multi-artifact skill packages. Each skill is a directory containing instructions
(SKILL.md), examples, templates, and optionally a Python MCP server.

See [FORMAT.md](FORMAT.md) for the complete skill package format spec.

## Status at v0.2.0

- **101 skill directories total.**
- **85 skills** migrated mechanically from the original aibox `templates/skills/`.
  Frontmatter upgraded to processkit v1 format. Bodies preserved as-is. Most
  already follow a "When to Use" + "Instructions" structure that roughly maps to
  Level 1 + Level 2 + Level 3 content, but they do not yet carry explicit
  `## Level 1/2/3` headings. A full explicit three-level rewrite is tracked as
  a follow-up (see context/BACKLOG.md in this repo).
- **16 new process-primitive skills** authored specifically for processkit.
  These DO use explicit `## Level 1/2/3` headings and serve as the reference
  style for future skills and for the three-level rewrite.

## The 16 new process-primitive skills

Layer 0 (foundation):
- `event-log` — append-only LogEntry, probabilistic

Layer 1 (primitive management):
- `actor-profile` — humans, agents, services
- `role-management` — named sets of responsibilities

Layer 2 (core entities):
- `workitem-management` — WorkItem lifecycle
- `decision-record` — DecisionRecord (ADR pattern)
- `scope-management` — Scope (sprints, milestones)
- `category-management` — classification axes
- `cross-reference-management` — lightweight frontmatter references
- `binding-management` — scoped/temporal many-to-many relationships

Layer 3 (process orchestration):
- `process-management` — Process definitions
- `state-machine-management` — StateMachine customization
- `gate-management` — validation checkpoints
- `schedule-management` — cadences and triggers
- `constraint-management` — rules and limits

Layer 4 (cross-cutting):
- `discussion-management` — multi-turn exploratory conversations
- `metrics-management` — quantified observations

## Skill package layout

```
<skill-name>/
  SKILL.md              ← three-level instructions
  examples/             ← example outputs
  templates/            ← YAML frontmatter entity scaffolds
  references/           ← optional deep-dive material (Level 3 extension)
  mcp/                  ← optional Python MCP server
```

## Skill hierarchy

Skills reference lower-layer skills via `uses:` in frontmatter. Strictly downward.

```
Layer 0: event-log (foundation)
Layer 1: role-management, actor-profile
Layer 2: workitem-management, decision-record, scope-management,
         category-management, cross-reference-management, binding-management
Layer 3: process-management, state-machine-management, gate-management,
         schedule-management, constraint-management
Layer 4: discussion-management, metrics-management
```

Technical and language skills (python-best-practices, rust-conventions,
fastapi-patterns, ...) are `layer: null` — the hierarchy only applies to
process-primitive skills.
