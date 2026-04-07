---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-agent-management
  name: agent-management
  version: "1.0.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Multi-agent workflow coordination including task delegation, context sharing, handoff protocols, and quality gates. Use when orchestrating multiple AI agents, designing agent pipelines, or managing agent-to-agent communication."
  category: process
  layer: 4
---

# Agent Management

## When to Use

When the user asks to:
- Coordinate multiple AI agents on a shared task
- Decompose a large task into agent-assignable subtasks
- Design an agent pipeline (research, implement, review)
- Set up handoff protocols between agents
- Define quality gates for multi-agent workflows
- Recover from agent failures or stalled tasks

## Instructions

### 1. Task Decomposition

Break work into agent-sized units. Each subtask must have:

1. **Clear scope** -- one well-defined outcome, not "do everything"
2. **Input specification** -- exactly what files, context, or prior outputs the agent needs
3. **Output specification** -- what artifact the agent produces (file, diff, structured answer)
4. **Success criteria** -- how to verify the subtask is done correctly
5. **Estimated complexity** -- small (single file), medium (module), large (cross-cutting)

Rules of thumb:
- If a subtask requires more than 3 files of context, split it further
- If a subtask has no verifiable output, redefine it
- Prefer depth-first (finish one subtask fully) over breadth-first (start many in parallel)

### 2. Agent Role Definitions

Assign roles based on the task, not on agent identity:

| Role | Responsibility | Input | Output |
|---|---|---|---|
| **Planner** | Decomposes task, defines subtask order and dependencies | User request, codebase overview | Task plan with ordered subtasks |
| **Researcher** | Gathers information, reads code, finds patterns | Specific questions, file paths | Structured findings with citations |
| **Coder** | Implements changes, writes code | Task spec, relevant files, findings | Code changes (diff or files) |
| **Reviewer** | Validates correctness, style, completeness | Code changes, task spec, success criteria | Approval or rejection with reasons |

Guidelines:
- A single agent can fill multiple roles sequentially (plan, then code, then self-review)
- Never skip the reviewer role -- even self-review catches errors
- The planner role is mandatory for tasks touching more than 2 files

### 3. Context Sharing Strategies

Agents lose context between sessions. Use explicit context transfer:

**File-based (preferred for Claude Code):**
- Write findings to a scratch file (e.g., `_agent_notes.md`) that the next agent reads
- Use structured formats: headings, bullet points, file paths with line numbers
- Delete scratch files when the workflow completes

**Structured handoff messages:**
- Summarize what was done, what remains, and what blockers exist
- Include exact file paths and line numbers, not vague descriptions
- List assumptions made and decisions taken

**Shared memory (project files):**
- Use `DECISIONS.md` or `HANDOVER.md` for persistent cross-session context
- Keep entries timestamped and concise
- Reference specific commits or file versions

### 4. Handoff Protocols

Every handoff between agent roles must include:

1. **Status** -- what is complete and what is not
2. **Artifacts** -- list of files created or modified, with paths
3. **Verification** -- what was checked and how (tests run, manual review, linting)
4. **Blockers** -- anything that prevents the next step
5. **Next action** -- explicit instruction for the receiving agent

Format for handoff:
```
## Handoff: [Role] -> [Role]
**Status:** [complete | partial | blocked]
**Changes:** [list of file paths]
**Verified:** [tests passed | linted | reviewed]
**Blockers:** [none | description]
**Next:** [specific instruction]
```

### 5. Quality Gates

Insert verification checkpoints between stages:

- **After planning:** Does the plan cover all requirements? Are subtasks independent?
- **After research:** Are findings specific (file paths, line numbers) not vague?
- **After coding:** Do tests pass? Does `cargo clippy` / linter pass? Does the change match the spec?
- **After review:** Are all must-fix items addressed? Is the reviewer satisfied?

A quality gate fails the workflow forward -- do not proceed until the gate passes. If a gate fails twice on the same issue, escalate to the user.

### 6. Error Recovery and Fallbacks

When an agent step fails:

1. **Capture the failure** -- save error output, not just "it failed"
2. **Diagnose** -- is it a context issue (missing info), a capability issue (wrong approach), or an environment issue (tool error)?
3. **Retry with adjustment** -- provide missing context, try alternative approach, or fix environment
4. **Escalate** -- if two retries fail, stop and report to the user with full context

Fallback strategies:
- If a coder agent is stuck, switch to researcher role first to gather more context
- If review finds fundamental issues, return to planner role to re-scope
- If context is too large, split the task into smaller independent pieces

### 7. Progress Tracking

For multi-step workflows, maintain a checklist:

```
## Agent Workflow: [Task Name]
- [x] Plan: decomposed into N subtasks
- [x] Research: gathered context for subtask 1
- [ ] Code: implement subtask 1
- [ ] Review: verify subtask 1
- [ ] Code: implement subtask 2
...
```

Update the checklist after each step. This serves as both progress tracking and handoff context.

## Examples

**User:** "Add authentication to this API -- use multiple agents to plan, implement, and review."
**Agent:** Creates a task plan: (1) Researcher reads existing route handlers and middleware patterns, writes findings to `_auth_notes.md`. (2) Coder implements auth middleware, JWT validation, and protected route decorators based on findings. (3) Reviewer checks the implementation against OWASP guidelines, verifies tests pass, and confirms no hardcoded secrets. Each handoff includes the structured handoff block with status, artifacts, and next action.

**User:** "Set up a code review pipeline for incoming changes."
**Agent:** Defines a three-stage pipeline: (1) Researcher reads the diff and gathers context about affected modules. (2) Reviewer evaluates correctness, security, performance, and style using the code-review skill checklist. (3) Planner summarizes findings into must-fix, should-fix, and nit categories with specific line references. Quality gate: all must-fix items require a re-review cycle before approval. See `references/coordination-patterns.md` for the pipeline pattern.

**User:** "Research the best caching strategy, then implement it."
**Agent:** Runs a research-then-implement workflow: (1) Researcher examines current data access patterns, identifies hot paths, checks existing caching (if any), and writes structured findings with measured or estimated latencies. (2) Planner reviews findings and selects a caching approach, documenting the decision. (3) Coder implements the cache layer following the plan. (4) Reviewer verifies cache invalidation logic, checks for stale data risks, and confirms tests cover cache hit/miss paths. Handoff between research and planning includes specific file paths and quantified findings.

## Context budget and lazy loading

processkit projects can grow to dozens of skills, hundreds of workitems,
and many years of decision history. Loading all of this every session is
wasteful — most files have no relevance to the current request. The agent
must load context **selectively**.

### Read INDEX files first, not full directories

Every directory under `context/` should have an `INDEX.md` (Level 0 per
the three-level principle). At session start, the agent reads:

1. `CLAUDE.md` (root)
2. `context/AIBOX.md` (project baseline)
3. `context/owner/identity.md` and `context/owner/working-style.md` (the
   highest-leverage owner files)
4. `context/INDEX.md` and any `context/*/INDEX.md` files
5. `context/migrations/INDEX.md` (always loaded — the migration state
   summary)

These are short, dense, and tell the agent what exists. The agent does
NOT slurp `context/skills/`, `context/workitems/`, etc. on session start.

### Use the index MCP server, not filesystem walks

The `index-management` MCP server is the right way to discover entities.
Instead of `ls context/skills/`, the agent calls
`query_entities(kind="Skill", category="process")` and gets back a list
of just the skills that match. Same for workitems, decisions, bindings,
events. Filesystem walking is the slow, context-expensive fallback.

### Load skills on demand, not upfront

When the agent needs a specific skill (e.g. `code-review`), it reads
`context/skills/code-review/SKILL.md` at that moment — not at session
start. If the SKILL.md references a deeper file (`references/...`), only
read that when the agent's task actually needs it. This is the
three-level principle in action: start at Level 1, drop to Level 2 when
the user's request is more specific, drop to Level 3 only for edge cases.

### Respect the configured context budget

Projects can declare a budget in `aibox.toml`:

```toml
[context.budget]
target_tokens = 8000          # aim NOT to exceed this on initial load
max_tokens = 16000            # hard ceiling — must use lazy loading above this

[context.budget.always_load]
files = [
  "CLAUDE.md",
  "context/AIBOX.md",
  "context/owner/identity.md",
  "context/owner/working-style.md",
  "context/INDEX.md",
  "context/migrations/INDEX.md",
]

[context.budget.on_demand]
patterns = [
  "context/skills/**",
  "context/workitems/**",
  "context/logs/**",
  "context/decisions/**",
]
```

The agent reads `[context.budget]` at session start (it's part of the
`always_load` set if not overridden) and follows the rules:

- `always_load.files` are loaded into the first turn unconditionally
- `on_demand.patterns` are loaded only when needed, via the index MCP
  server or direct file reads
- The agent estimates the total token count of `always_load` and warns
  the user if it exceeds `target_tokens`

The values are advisory — there is no runtime enforcement. The agent
honors them as instructions.

### When context is still too big

If even the always-load set is too large, the agent should:
1. Surface this to the user: "Loading 24k tokens of context, target is
   8k. Want me to run `context-grooming`?"
2. Suggest specific candidates for archival or summarization based on
   the `context-grooming` ruleset
3. Offer to update the `[context.budget]` config to a higher target if
   the project genuinely needs more
4. Never silently truncate or drop files

### Relationship to `context-grooming`

`agent-management` says HOW to load context efficiently per session.
`context-grooming` runs periodically to make the corpus smaller. Both
work together: grooming reduces the live size; lazy loading reduces what
gets loaded from that smaller corpus.
