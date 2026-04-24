---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260423_2055-HappyFinch-skill-md-commands-metadata
  created: '2026-04-23T20:55:35+00:00'
  updated: '2026-04-24T00:24:55+00:00'
spec:
  title: 'SKILL.md commands: metadata uses stale &lt;skill&gt;-&lt;verb&gt; names
    — reconcile to /pk- namespace'
  state: done
  type: chore
  priority: medium
  assignee: TEAMMEMBER-cora
  description: '## Surfaced by


    New pk-doctor check `commands_consistency` (shipped in ToughMeadow, `BACK-20260423_1103`).
    Running it on the current tree produces **20 ERROR / 26 WARN** findings — broad
    pattern, not a single bug.


    ## Pattern


    Many processkit skills declare `metadata.processkit.commands:` entries with the
    legacy naming convention `<skill>-<verb>` (e.g. `status-briefing-generate`, `workitem-management-create`,
    `model-recommender-route`) but actually ship `commands/pk-<verb>.md` files in
    the `/pk-<verb>` namespace (e.g. `pk-resume.md`, `pk-work.md`, `pk-route.md`).


    Per the project''s `/pk-` command-namespace convention (owner preference memory),
    shipped files are correct; the SKILL.md metadata is stale.


    ## Affected skills (from running the check)


    status-briefing, workitem-management, model-recommender, note-management, owner-profiling,
    session-handover, skill-builder, skill-reviewer, standup-context, team-creator,
    skill-gate. Raw list of mismatches in the pk-doctor output attached at session-handover
    time.


    ## Scope


    1. Walk every `context/skills/processkit/*/SKILL.md` flagged by the check.

    2. Update each `commands:` metadata entry''s `name` to match the actually-shipped
    `commands/pk-*.md` filename stem.

    3. Re-verify: `uv run context/skills/processkit/pk-doctor/scripts/doctor.py --category=commands_consistency`
    should report 0 ERROR and 0 WARN.

    4. Mirror every SKILL.md change into `src/context/skills/processkit/*/SKILL.md`
    (dual-tree convention).

    5. Run `bash scripts/check-src-context-drift.sh` — must pass.


    ## Why not bundle into v0.19.2


    ToughMeadow''s goal is to ship the missing pk-doctor/commands file and prevent
    recurrence. The metadata cleanup is a separate cross-cutting rename that should
    be its own commit + its own review. Keeping scope tight lets v0.19.2 ship without
    this.


    ## Non-goals


    - No behavioural changes to any command.

    - No slash-command renames — the `/pk-*` names stay as-is.

    - Purely a metadata-naming reconciliation.


    ## Done criteria


    - `pk-doctor --category=commands_consistency` reports all-INFO in both trees.

    - `check-src-context-drift.sh` clean.

    - One commit: `chore: reconcile SKILL.md commands metadata to /pk- namespace`.'
  started_at: '2026-04-24T00:02:47+00:00'
  completed_at: '2026-04-24T00:24:55+00:00'
---

## Transition note (2026-04-24T00:09:55+00:00)

Applied: 11 renames (context-grooming, decision-record, model-recommender, note-management, owner-profiling, session-handover, skill-builder, skill-reviewer, standup-context, status-briefing, workitem-management), 2 insertions (discussion-management, skill-gate), 1 structural + rename (team-creator — commands block lifted out of provides: to metadata.processkit: and normalised to shipped entries). Both trees in sync. commands_consistency now reports 0 ERROR / 0 WARN / 1 INFO. Dropped entries for commands never shipped: model-recommender-profile, owner-profiling-refine, skill-reviewer-bulk-gotchas.


## Transition note (2026-04-24T00:24:55+00:00)

Shipped in 632d499. commands_consistency check reports 0/0/1 across both trees.
