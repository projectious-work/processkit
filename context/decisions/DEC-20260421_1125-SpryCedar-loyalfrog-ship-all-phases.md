---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260421_1125-SpryCedar-loyalfrog-ship-all-phases
  created: '2026-04-21T11:25:59+00:00'
spec:
  title: LoyalFrog — ship all phases + Phase 0 rename for next release
  state: accepted
  decision: Implement /pk-retro (LoyalFrog) across Phase 0 (rename morning-briefing
    → status-briefing project-wide and in src/ deliverables), Phase 1 (base skill
    + 4 signals + dual-emit + proposed action items + 80-line cap), Phase 2 (--auto-workitems
    flag), and Phase 3 (--verbose flag) — all in the next release. Historical records
    (LogEntries, past DecisionRecords, applied migrations, past Artifacts/WorkItems)
    are NOT rewritten; they remain frozen records of what the skill was named at that
    time.
  context: Owner approved the /pk-retro plan and expanded scope to all phases + added
    a Phase 0 terminology rename so the skill directory, docs, and shipped src/ template
    reflect "status briefing" (provider-neutral) instead of "morning briefing".
  rationale: '"Morning" is time-of-day-specific and misleading for teams in other
    timezones or running mid-day catch-up. "Status briefing" is accurate and provider-neutral.
    Rolling it in with /pk-retro keeps the release thematic (session lifecycle: status-briefing
    at start, retro at close).'
  consequences: Downstream projects that pinned v0.18.x will see the skill dir renamed
    on next sync; a content migration will be emitted by the migration-management
    skill. Existing LogEntries/DRs that mention "morning-briefing" remain historically
    accurate and are not touched.
  deciders:
  - ACTOR-owner
  related_workitems:
  - BACK-20260420_1340-LoyalFrog-add-pk-retro-skill
  decided_at: '2026-04-21T11:25:59+00:00'
---
