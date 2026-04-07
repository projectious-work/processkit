# AGENTS.md — {{PROJECT_NAME}}

This is the canonical entry point for any AI agent (or human) working on
this project. Agent harnesses that auto-load a provider-specific file
(`CLAUDE.md`, `CODEX.md`, `.cursor/rules`, etc.) should treat that file
as a **thin pointer** to this one.

This template ships with processkit under `src/scaffolding/AGENTS.md`.
Replace `{{PROJECT_NAME}}` and the project-specific notes section, then
keep the rest as-is — it encodes the always-on rules processkit-using
projects rely on.

## Read these first

If you are new to this project, in this exact order:

1. **`README.md`** — what {{PROJECT_NAME}} is and why
2. **`context/HANDOVER.md`** — current state, recent changes, next steps
3. **This file (`AGENTS.md`)** — the always-on rules below
4. **`context/BACKLOG.md`** — what's deferred, what's next

After those four, dig into specific files as the work demands.

## Always-on rules

### Use the index, not filesystem walks

This project uses processkit's `index-management` MCP server to discover
entities (work items, decisions, log entries, bindings, etc.). Call
`query_entities(kind=..., state=...)` instead of running `ls
context/workitems/` or grepping the filesystem. The index is faster,
context-cheaper, and reflects the canonical state.

### Lazy-load skills and references

Do not slurp `context/skills/`, `context/workitems/`, or any large
context directory at session start. Read `INDEX.md` files first (every
context directory should have one) and load specific files only when the
current task needs them. This is the three-level principle: start at
Level 1 (intro), drop to Level 2 (workflows) when the task is more
specific, drop to Level 3 (full reference) only for edge cases.

### Respect the configured context budget

Projects can declare a context budget in their processkit configuration
file (the location depends on how processkit was installed — see your
project's setup notes). The budget specifies which files are always
loaded vs. loaded on demand:

```toml
[context.budget]
target_tokens = 8000          # aim NOT to exceed this on initial load
max_tokens = 16000            # hard ceiling — must lazy-load above this

[context.budget.always_load]
files = [
  "AGENTS.md",
  "context/HANDOVER.md",
  "context/INDEX.md",
]

[context.budget.on_demand]
patterns = [
  "context/skills/**",
  "context/workitems/**",
  "context/logs/**",
]
```

If you're approaching the budget on a request, drop into lazy mode: read
INDEX files, then targeted files only.

### Write through the MCP servers

When creating, updating, or transitioning entities, use the relevant MCP
server tools (e.g. `create_workitem`, `transition_workitem`,
`record_decision`). Hand-editing entity files works, but bypasses the
index and the state-machine validation, so the index can go stale and
invalid transitions can slip through. Reserve hand edits for situations
the MCP tools genuinely don't cover.

## Project structure (typical)

A processkit-using project has approximately this layout:

```
{{PROJECT_NAME}}/
├── AGENTS.md               ← this file
├── README.md
├── context/                ← project-management artifacts
│   ├── HANDOVER.md         ← per-release agent briefing
│   ├── BACKLOG.md          ← deferred work
│   ├── INDEX.md            ← what lives in context/
│   ├── workitems/          ← WorkItem entities
│   ├── decisions/          ← DecisionRecord entities
│   ├── logs/               ← LogEntry entities (event log)
│   └── ...                 ← other entity-kind directories
└── ...                     ← project-specific source / docs / etc.
```

The exact directories depend on which processkit packages and skills are
installed. Run `query_entities` against the index to see what kinds are
in use.

## Project-specific notes

<!--
Add anything specific to {{PROJECT_NAME}} here:
- Bootstrap version pinning notes
- Special directory conventions
- Out-of-scope reminders
- Project-specific MCP servers
- Deployment quirks

Keep this section short — anything longer than a few paragraphs belongs
in context/HANDOVER.md.
-->

(none yet — fill in as the project grows)

## Where to find more

| Question | Where |
|---|---|
| What does this project do? | `README.md` |
| Current state and recent changes | `context/HANDOVER.md` |
| What's deferred / prioritized | `context/BACKLOG.md` |
| Entity file format | the processkit `primitives/FORMAT.md` shipped with your install |
| Skill format | the processkit `skills/FORMAT.md` shipped with your install |
| What MCP tools are available | the `mcp/README.md` of each installed skill |
