---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260422_0232-CuriousOwl-v0-19-0-phase
  created: '2026-04-22T02:32:27+00:00'
  updated: '2026-04-22T08:03:28+00:00'
spec:
  title: v0.19.0 Phase 6 — Migration, pk-doctor team_consistency, and end-to-end dogfood
  state: done
  type: task
  priority: high
  assignee: ACTOR-developer
  description: |
    Cut the project over to v0.19.0 and verify end-to-end.

    **Migration of existing entities**
    - Migrate `ACTOR-20260421_0144-ThriftyOtter-owner` → `context/team-members/<chosen-slug>/` (human type): team-member.yaml, persona.md (seed from current actor profile), card.json (A2A), empty tiered memory tree, `private/` subdirectory.
    - Remove `ACTOR-20260421_0144-AmberDawn-legacy-historical-backfill` (not meaningful per user).
    - Delete 8 role-class actors (ACTOR-developer, ACTOR-assistant, ACTOR-sr-architect, ACTOR-sr-researcher, ACTOR-pm-claude, ACTOR-jr-architect, ACTOR-jr-developer, ACTOR-jr-researcher) — roles are now enough.
    - Seed a few named AI team-members (from name pool) to replace the role-class personas where still needed.

    **pk-doctor integration — 5th check category `team_consistency`**
    Checks (from team-manager.check_all_consistency):
    1. YAML frontmatter drift (team-member.yaml schema)
    2. Memory tier directory structure
    3. Binding reference resolution
    4. Name uniqueness
    5. Name-pool compliance (AI team-members)
    6. Orphaned memory files
    7. Sensitivity misplacement (confidential/pii in shared path)
    8. private/ gitignore presence
    9. Memory file header required fields
    10. Card ↔ team-member parity

    pk-doctor report surfaces all with the existing error/warning pipeline.

    **Dogfood**
    - Regenerate `context/team/roster.md` for new model.
    - Run `pk-retro` on v0.19.0.
    - Dispatch a routed task end-to-end, verifying resolve_bindings_for returns the expected model.
    - Full pk-doctor sweep: 0 errors, clean drift.

    **Done when**
    - Only the new team-member entities exist.
    - pk-doctor reports 0 errors across all 5 categories.
    - Migration is reproducible via script.
    - CHANGELOG and AGENTS.md updated; docs-site reflects new taxonomy.
  started_at: '2026-04-22T06:09:01+00:00'
  completed_at: '2026-04-22T08:03:28+00:00'
---

## Transition note (2026-04-22T06:09:01+00:00)

Starting Phase 6 partial migration in parallel with Phase 5 agent: ThriftyOtter → team-member, remove AmberDawn + 8 role-class actors + 7 legacy role files. pk-doctor wiring + dogfood wait for Phase 5.


## Transition note (2026-04-22T08:03:24+00:00)

Phase 6 complete: ThriftyOtter migrated to TEAMMEMBER-thrifty-otter (persona + card + 6 memory tiers); AmberDawn + 8 role-class actors + 7 legacy roles + 8 legacy role-assignment bindings deleted; 30 default bindings materialized from MANIFEST.yaml; pk-doctor gained 5th check category team_consistency; roster regenerated for v0.19.0; AGENTS.md Team section updated; CHANGELOG v0.19.0 section written. Final pk-doctor: 0 ERROR / 0 WARN / 5 INFO. Dogfood: resolve(software-engineer@senior)→sonnet 4.6, resolve(ai-research-scientist@principal)→opus 4.6 extra-high, resolve(assistant@junior)→haiku 4.5 — all Layer 5.
