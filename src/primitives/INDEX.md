# primitives/

The 18 universal process primitives. Framework-agnostic building blocks that appear
in every process methodology (SAFe, PMBOK, CMMI, Scrum, Kanban). processkit provides
them as schemas and state machines; it does not impose a workflow.

## Contents

- **FORMAT.md** — entity file format spec (apiVersion/kind/metadata/spec YAML frontmatter)
- **schemas/** — one YAML schema file per primitive type
- **state-machines/** — default state machine definitions (extended per process template)

## The 18 primitives

1. **WorkItem** — unit of work (task/story/issue/ticket)
2. **LogEntry** — immutable record of something that happened
3. **DecisionRecord** — a choice with rationale
4. **Artifact** — any produced output
5. **Role** — a named set of responsibilities
6. **Process** — sequence of steps with decision points
7. **StateMachine** — set of states with allowed transitions
8. **Category** — classification/taxonomy
9. **CrossReference** — typed link between entities (lightweight, frontmatter-level)
10. **Gate** — validation point
11. **Metric** — quantified observation
12. **Schedule** — time-based trigger / cadence
13. **Scope** — boundary grouping related items (project, sprint, quarter, ...)
14. **Constraint** — rule or limit
15. **Context** — ambient knowledge and environment
16. **Discussion** — structured conversation producing decisions
17. **Actor** — person or agent (preferences, expertise, working style)
18. **Binding** — assignment of one entity to another with optional scope/time/conditions (generalized RoleBinding)

See [FORMAT.md](FORMAT.md) for how these are expressed as files.
