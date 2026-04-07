---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-context-grooming
  name: context-grooming
  version: "1.0.0"
  created: 2026-04-07T00:00:00Z
spec:
  description: "Periodically review and prune the project context — archive completed work, summarize stale entries, propose disabling unused skills. Keeps the context lean so agents load less per session."
  category: process
  layer: 4
  uses: [event-log, context-archiving, index-management]
  provides:
    primitives: []
    templates: [grooming-report]
  when_to_use: "Run on a regular cadence (weekly or monthly) — or when the user notices session context bloat. Always proposes changes for human approval; never moves or deletes files silently."
---

# Context Grooming

## Level 1 — Intro

`context-grooming` is the periodic-cleanup skill. Once a week or once a
month, the agent walks the project's `context/` directory against a set
of rules and produces a report listing what could be archived, summarized,
or disabled. The user approves each item before any file moves. This is
how the project keeps its session context lean over time.

## Level 2 — Overview

### When to run

Triggered by:
- An explicit user request: "groom the context", "let's clean up"
- A cadence configured in `aibox.toml`:
  ```toml
  [context.grooming]
  cadence = "weekly"     # weekly | monthly | quarterly | never
  ```
  The agent checks the cadence at session start. If the last grooming was
  more than the cadence ago, it surfaces:
  > "Context grooming was last run 5 weeks ago. Want me to do a pass?"
- A noticeable session-context bloat: more than ~16k tokens loaded at
  session start (if the agent can detect this — depends on the runtime).

### What grooming does

Grooming is a **review-then-act** workflow:

1. **Walk** — agent walks `context/` against the ruleset (see Level 3).
2. **Report** — agent produces a `grooming-report.md` document listing
   proposed actions, organized by category.
3. **Review** — user reads the report and approves items individually
   (or in groups).
4. **Act** — agent moves/archives/disables only the approved items.
5. **Record** — appends a `LogEntry` (`event_type: context.groomed`) and
   updates the report's status field.

**Nothing is moved silently. Nothing is deleted, ever** — the worst that
can happen is "moved to `context/archive/`" which is reversible.

### The grooming report

The report lives at `context/grooming-reports/<date>.md`. Sample shape:

```markdown
---
apiVersion: processkit.projectious.work/v1
kind: Context
metadata:
  id: GROOM-2026-04-07
  privacy: project-private
spec:
  state: pending  # pending | approved | applied
  generated: 2026-04-07T10:00:00Z
---

# Grooming report — 2026-04-07

## Workitems eligible for archive (12)

| ID | Title | State | Last touched |
|---|---|---|---|
| BACK-foo | ... | done | 2026-02-01 |
| ... | ... | ... | ... |

[ ] Approve all
[ ] Approve individually: ...

## Standups eligible for summarization (8)

8 standup entries from Q1 2026 can be summarized into a single quarterly
summary:
- 2026-01-05.md → 2026-03-30.md

[ ] Approve summarization

## Unused skills (3)

These skills have not been invoked in any session for 60+ days:
- `pixijs-gamedev` (last used: 2026-01-12)
- `flutter-development` (last used: never since project init)
- `latex-authoring` (last used: 2026-02-08)

[ ] Approve disabling (move from .claude/skills/ to .claude/skills/.disabled/)
```

### The default ruleset

| Rule | Action proposed |
|---|---|
| WorkItem in terminal state (`done` / `cancelled`) for >30 days | Move to `context/archive/workitems/` |
| LogEntry older than 90 days, not referenced by any current entity | Move to `context/archive/logs/` |
| Standup entry older than current quarter | Summarize all entries from a quarter into one quarterly summary; archive originals |
| DecisionRecord superseded for >180 days | Move both the old and the new together to `context/archive/decisions/` |
| File over 500 lines that hasn't been edited in 30 days | Propose splitting or summarizing |
| Skill in `.claude/skills/` not invoked in any session for 60 days | Propose disabling (move to `.claude/skills/.disabled/`) |
| Migration in `applied/` older than 1 year | Archive (rare — kept for historical reference) |

These are defaults. Projects can override in `aibox.toml`:

```toml
[context.grooming.rules]
workitem_archive_age_days = 60       # default 30
log_archive_age_days = 180           # default 90
unused_skill_age_days = 90           # default 60
disable_skills_automatically = false # default false (always proposes, never auto-disables)
```

## Level 3 — Full reference

### Configuration

```toml
[context.grooming]
cadence = "monthly"           # weekly | monthly | quarterly | never (default: never)
report_dir = "context/grooming-reports"   # default

[context.grooming.rules]
# Override individual rules. All have safe defaults.
workitem_archive_age_days = 30
logentry_archive_age_days = 90
standup_archive_age_days = 90
decision_archive_age_days = 180
oversize_file_threshold_lines = 500
unused_skill_age_days = 60
```

### Interaction with `context-archiving`

`context-archiving` (the older skill) is the underlying "move file to
archive" capability. `context-grooming` is the periodic-review wrapper
that decides WHAT to move and proposes it. After approval, the actual
file moves are performed via `context-archiving`'s instructions. They
work together — `context-grooming` is the strategy; `context-archiving`
is the mechanism.

### What grooming will NOT touch

To stay safe and predictable, grooming explicitly skips:

- Anything in `context/owner/` (the personal context portfolio)
- Anything in any `private/` directory (user-private content)
- The current quarter's standups (only previous quarters get summarized)
- Currently in-progress work (Migration in `in-progress/`, WorkItem in
  `in-progress` state, etc.)
- Files less than 30 days old (regardless of size)
- The `context/migrations/` directory (migrations have their own lifecycle)

### When to override the cadence

Some projects benefit from rare grooming (long-running R&D where
historical context matters); some benefit from frequent grooming (fast-
moving sprints). The cadence config is per-project.

If the user repeatedly says "skip grooming" three sessions in a row, the
agent should propose:
> "You've skipped grooming three times. Do you want me to switch the
> cadence to a longer interval (or `never`)?"

### Relationship to context budget (in `agent-management`)

Grooming reduces the LIVE size of the context. The `[context.budget]`
section in `aibox.toml` (documented in `agent-management/SKILL.md`) tells
the agent how much context to load per session. The two work together:
grooming makes the corpus smaller; budget tells the agent how to load
selectively.

### Ideas for future versions

- **Ranking**: instead of binary "archive or not", rank files by
  "loading-cost vs information-value" and propose the bottom 10%.
- **Compaction**: instead of archive, the agent could rewrite a 500-line
  workitem-with-history into a 20-line summary + a link to the archived
  full version.
- **Auto-grooming for reversible moves only**: a low-risk subset of the
  rules could be applied automatically (still logged for review). v1
  ships with always-propose, never-auto.
