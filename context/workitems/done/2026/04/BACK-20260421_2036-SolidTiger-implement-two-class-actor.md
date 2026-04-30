---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260421_2036-SolidTiger-implement-two-class-actor
  created: '2026-04-21T20:36:31+00:00'
  updated: '2026-04-21T20:50:37+00:00'
spec:
  title: Implement two-class actor ID enforcement (schema + pk-doctor)
  state: done
  type: story
  priority: medium
  description: |
    Implements DEC-20260421_2043-<word-pair>-two-class-actor-ids. Scope:

    1. `context/schemas/actor.yaml` (+ `src/context/schemas/actor.yaml`) — add regex alternation on `metadata.id`:
       - `^ACTOR-\d{8}_\d{4}-[A-Z][a-z]+[A-Z][a-z]+-[a-z0-9-]+$` (identity class)
       - `^ACTOR-[a-z][a-z0-9-]*$` (role class, restricted by allowlist)
       - Add a schema-level `x-allowed-role-ids` list containing the 8 current role IDs.

    2. `context/skills/processkit/pk-doctor/scripts/checks/schema_filename.py` (+ src mirror) — for `kind=Actor`:
       - If filename matches identity-class regex → OK.
       - If filename matches role-class regex AND stem (without ACTOR-) is in allowlist → OK.
       - Otherwise → ERROR `schema.filename.invalid_actor_id_pattern`.
       - Keep existing filename↔metadata.id match check.

    3. `context/skills/processkit/actor-profile/SKILL.md` (+ src mirror) — add a section "Actor ID classes" documenting role vs identity, when to use each, and the allowlist-amendment process.

    4. Test coverage: extend existing schema_filename check tests (look for how other kind-specific validations are tested in pk-doctor) with cases for valid role, valid identity, invalid role (not in allowlist), invalid mixed form.

    5. Run pk-doctor after — must remain 0/0 (the 8 role actors and the 2 identity actors are all valid under the new rule).

    Dual-tree mirror is MANDATORY. Drift guard must pass.
  started_at: '2026-04-21T20:36:35+00:00'
  completed_at: '2026-04-21T20:50:37+00:00'
---

## Transition note (2026-04-21T20:36:35+00:00)

Dispatching Sonnet worker per DEC-20260421_2036-SoundIvy.


## Transition note (2026-04-21T20:50:32+00:00)

Schema regex + x-allowed-role-ids allowlist + pk-doctor check + SKILL.md docs + 8 new tests. 29/29 pass. Negative test confirmed: ACTOR-badname flagged as invalid_actor_id_pattern. Drift guard clean.


## Transition note (2026-04-21T20:50:37+00:00)

Shipping.
