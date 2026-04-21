---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260421_2036-SoundIvy-two-class-actor-ids
  created: '2026-04-21T20:36:22+00:00'
spec:
  title: Two-class actor IDs — role (fixed slug) vs identity (canonical timestamped)
  state: accepted
  decision: 'Formalize two distinct actor classes at the schema + validation layer:


    1. **Role actors**: `ACTOR-<kebab-slug>` where `<kebab-slug>` is in an approved
    allowlist. These are stable, human-readable identifiers for team roles (sr-architect,
    pm-claude, developer, etc.). Current 8 allowlist entries: assistant, developer,
    jr-architect, jr-developer, jr-researcher, pm-claude, sr-architect, sr-researcher.


    2. **Identity actors**: `ACTOR-<YYYYMMDD_HHMM>-<WordPair>-<slug>` — the canonical
    id-management format, used for dynamic/session/historical actors (owner, legacy-historical-backfill).


    Implementation:

    - `context/schemas/actor.yaml` gains a regex alternation on `metadata.id` accepting
    either shape, plus an `x-allowed-role-ids` field declaring the role-actor allowlist.

    - `context/skills/processkit/pk-doctor/scripts/checks/schema_filename.py` extended
    to enforce the pattern for `kind=Actor` entries; violations emit ERROR `schema.filename.invalid_actor_id_pattern`.

    - `context/skills/processkit/actor-profile/SKILL.md` documents the two classes,
    when to use each, and how to add a new approved role-id to the allowlist (requires
    a DecisionRecord).

    - The 8 existing role actors are LEFT UNCHANGED — renaming them would churn hundreds
    of cross-references (WorkItems, LogEntries, DRs) with zero semantic gain. They
    are the reason this class exists.


    Consequences:

    - Future hand-edit creation of an actor under `context/actors/` fails schema validation
    if the ID doesn''t match one of the two patterns.

    - Adding a new role actor requires amending the allowlist via a DR.

    - pk-doctor gains one more `kind`-specific check, following the existing pattern.'
  context: 'Owner noticed inconsistent actor filenames in context/actors/: 8 role
    actors (ACTOR-sr-architect etc., seeded 2026-04-14) use semantic-only slugs while
    2 newer actors (ACTOR-20260421_0144-ThriftyOtter-owner, AmberDawn-legacy-backfill)
    use the canonical datetime + word-pair + slug format that create_actor now emits.
    pk-doctor''s schema_filename check didn''t flag this because it validates filename-matches-id
    but not a per-kind ID pattern.'
  rationale: Role actors are conceptually different from session/identity actors —
    like POSIX root vs uid=1001. Keeping them fixed-slug is correct semantics AND
    zero-churn. Option A (rename everything to canonical) was rejected as high-churn
    with no semantic gain. Option C (migrate with aliases) was rejected as complexity
    without benefit.
  alternatives:
  - option: A — rename all to canonical
    rejected_because: breaks hundreds of cross-references for no semantic gain
  - option: C — migrate with alias mapping
    rejected_because: complexity without benefit
  deciders:
  - ACTOR-owner
  decided_at: '2026-04-21T20:36:22+00:00'
---
