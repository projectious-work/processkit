---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260420_1729-SureTiger-groom-the-153-error
  created: '2026-04-20T17:29:14+00:00'
  updated: '2026-04-21T01:56:59+00:00'
spec:
  title: Groom the 153-ERROR baseline surfaced by first /pk-doctor run (Option A follow-up)
  state: done
  type: epic
  priority: medium
  description: 'First real `/pk-doctor` run against `/workspace` surfaced 153 ERROR
    / 17 WARN / 4 INFO (see `LOG-20260420_1720-GentleHill-doctor-report`). Owner chose
    Option A: ship doctor with honest baseline, pay down debt separately. This WorkItem
    tracks the sweep.


    ## Categories of ERROR (from doctor-report details)


    1. **WorkItem `type` enum violations** — entries using `research` / `feature`
    / `architecture` (v0.14 team-roster era); schema allows only `bug/chore/epic/spike/story/task`.
    Fix: transition to nearest valid type (`research` → `spike`, `feature` → `story`,
    `architecture` → `epic`) or re-issue as new WorkItems with correct type; note
    originals in the migration entry.


    2. **Null-coercion family** — `promotes_to: None` on notes, `supersedes: []` on
    decisions, etc. YAML parses `null` but JSON-Schema wants `object` or `string`.
    Fix: either remove the null/empty keys from the spec (omission ≡ absent) or extend
    schemas to accept `null` as a valid value for optional object/string fields. Schema
    extension is cleaner — one PR vs. dozens of file edits.


    3. **Backtick-in-block-scalar** — 7 WorkItems have markdown backticks in YAML
    block-scalar positions that break parsing. Fix: rewrite offending specs (they''re
    malformed YAML, not schema-valid-but-flagged).


    4. **11 CLI migrations at `context/migrations/` root** — flat files with no frontmatter
    (aibox-CLI-managed, not processkit-native). Two options: (a) move them to `applied/`
    once reviewed, (b) teach `checks/sharding.py` about the "CLI migration" filename
    pattern (`YYYYMMDD_HHMM_X.Y.Z-to-A.B.C.md`) as exempt from the state-bucket rule.
    Probably both — move the reviewed ones, exempt the pattern.


    5. **Schema reference mismatches** on some processes/ files.


    ## Acceptance


    - `/pk-doctor` run against `/workspace` returns 0 ERRORs.

    - WARNs reduced to <20 (down from 17 + whatever class 2 above re-classifies).

    - Grooming itself is audit-trailed — each fix either goes through an MCP write
    or is explicitly noted in a `grooming.applied` LogEntry.


    ## Dispatch shape


    Sub-tasks per category (break into separate WorkItems under this epic when scheduled):

    - Schema null-coercion refactor (extend schemas to accept null for optional fields)

    - WorkItem type-enum sweep (transition 15+ workitems)

    - YAML-breakage repair (7 WorkItems with backtick issues)

    - CLI migration sharding exemption + move

    - processes/ schema reconciliation'
  started_at: '2026-04-20T19:02:30+00:00'
  completed_at: '2026-04-21T01:56:59+00:00'
---

## Transition note (2026-04-20T19:02:30+00:00)

Dispatching worker for 5-track grooming sweep per DEC-20260420_XXXX-SureTigerGrooming. Strict-schema rewrite of legacy WorkItems (types + IDs), schema null/empty relaxation, CLI-migration sharding exemption, YAML hand-repairs, misplaced-log move.


## Transition note (2026-04-21T01:56:58+00:00)

All 5 tracks + backfill complete. 164 → 0 ERROR, 17 → 5 WARN (residual are Phase-2 filename renames). Drift guard PASS. Index clean. Collateral create_actor bug filed as separate WorkItem.


## Transition note (2026-04-21T01:56:59+00:00)

Shipped via the commit below.
