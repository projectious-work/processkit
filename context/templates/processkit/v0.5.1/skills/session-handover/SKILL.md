---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-session-handover
  name: session-handover
  version: "1.1.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Generates a structured session handover note at the end of a work session."
  category: process
  layer: 2
  when_to_use: "Use when the user says \"handover\", \"wrap up\", \"end of session\", or asks to document progress so another agent can pick up. Trigger proactively when a session is ending and no handover note exists for today."
---

# Session Handover

## Level 1 — Intro

A session handover is a short, structured note that lets the next
agent (or the same human tomorrow) resume work without re-reading
the entire git history. Capture what was done, what is open, what
was decided, and what comes next.

## Level 2 — Overview

### Gather context

Run these commands to understand the current state:

```
git log --oneline -20          # recent commits
git status                     # any uncommitted changes
git diff --stat HEAD~1         # what changed in the last commit
```

Read `context/BACKLOG.md` to identify in-progress items, plus any
files that were edited recently (visible in the git log).

### Fill in the template

Use the template at `templates/managed/session-handover.md` (or
`templates/product/session-handover.md` for product process
projects). Fill in each section:

- **Summary** — one bullet per meaningful unit of work completed.
- **Open Threads** — anything started but not finished; each needs
  a next action.
- **Decisions Made** — key choices with rationale, so the next
  agent does not re-debate them.
- **Blockers** — concrete blockers with owner; write "None." if
  clear.
- **Next Steps** — ordered list, most important first.
- **Context for Next Agent** — branch, files changed, current
  state, gotchas.

### Save the file

Save to:

```
context/archive/sessions/session-handover-YYYY-MM-DD.md
```

Use today's date. If a file already exists for today, append `-2`
to the filename.

### Update BACKLOG.md

If any items changed status this session (todo → in-progress,
in-progress → done), update the backlog table now — not later.

### Example

```markdown
# Session Handover — 2026-03-26

## Summary

- Implemented BACK-012: session-handover template in managed and
  product templates
- Added session-handover skill to templates/skills/
- Updated context.rs to use the real template content for
  session_template_md

## Open Threads

- BACK-026 (skills quality review) — next action: audit
  context-archiving and standup-context skills first

## Decisions Made

- Decision: session-handover template is the same for managed and
  product. Rationale: handovers are session-level, not
  process-level — no meaningful difference between the two.

## Blockers

None.

## Next Steps

1. Run cargo clippy and cargo test to verify no regressions
2. Start BACK-026 skills quality review

## Context for Next Agent

**Branch / version:** main, v0.12.0
**Files changed this session:**
  templates/managed/session-handover.md (new)
  templates/product/session-handover.md (new)
  templates/skills/session-handover/SKILL.md (new)
  cli/src/context.rs (updated session_template_md content)
  context/BACKLOG.md (BACK-012 → done)
**Current state:** All tests passing, clippy clean.
**Gotchas:** The session_template_md key in context.rs seeds the
template into new projects via aibox init. The content must be a
valid fill-in-the-blanks document, not a filled example.
```

## Level 3 — Full reference

### What makes a handover useful

A handover is for someone with no memory of the session. Optimize
for: branch and commit they should check out, the single most
important thing to do next, and the gotchas that are not obvious
from the diff. Skip anything they can read from `git log`
themselves.

### Common failure modes

- **Summary that recaps the diff.** The diff is in git. The
  summary should explain *why* the changes were made.
- **Open threads with no next action.** "Still working on X" is
  not actionable. Write the literal next command.
- **Decisions without rationale.** Future agents will undo
  decisions whose reasoning is not captured.
- **Stale BACKLOG.md.** If the handover claims an item is done
  but the backlog still says in-progress, the next agent will
  start it again.
- **Skipping the handover when the session was short.** Even a
  three-bullet handover beats none.

### Triggering proactively

When a session is wrapping (user says goodbye, switches topics,
or there is a clear stopping point) and no handover exists for
today, offer to write one. Do not write it without permission;
some sessions are intentionally exploratory and do not warrant a
handover.
