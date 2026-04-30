---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260421_0156-WarmGrove-fix-create-actor-mcp
  created: '2026-04-21T01:56:55+00:00'
  updated: '2026-04-21T07:25:55+00:00'
spec:
  title: Fix create_actor MCP tool — emits LogEntry without required actor field (self-referential
    bug)
  state: done
  type: bug
  priority: low
  description: |
    Found during SureTiger grooming sweep (BACK-20260420_1729). When `mcp__processkit-actor-profile__create_actor` is called, it auto-emits an `actor.created` LogEntry — but the emitted LogEntry is missing the required `spec.actor` field. Reproduced today: the 2 actors created during SureTiger closeout (ACTOR-20260421_0144-AmberDawn-legacy-historical-backfill and ACTOR-20260421_0144-ThriftyOtter-owner) both produced schema-invalid LogEntries (LOG-20260421_0144-AmberFjord-actor-created, LOG-20260421_0144-LoyalSpruce-actor-created).

    Likely self-referential cause: the actor doesn't exist yet at the moment the log_event is emitted, so the server has no actor ID to attribute. Two fixes possible:
    (a) Emit the LogEntry AFTER the actor is persisted, using the newly-created actor's ID.
    (b) Allow the LogEntry to reference a system actor (e.g., ACTOR-system) for actor.created events, or make `actor` optional for this specific event_type.

    Option (a) is cleaner — the actor that was just created IS logically the subject, and self-attribution is fine ("ACTOR-foo was created by ACTOR-foo" — the tool acted in the actor's name). Alternative: use a module-level ACTOR-system placeholder for bootstrap events.

    Acceptance: create_actor emits an `actor.created` LogEntry that passes schema validation without manual backfill.
  started_at: '2026-04-21T02:09:18+00:00'
  completed_at: '2026-04-21T07:25:55+00:00'
---

## Transition note (2026-04-21T02:09:18+00:00)

Dispatching worker — emit-after-persist with self-attribution shape.


## Transition note (2026-04-21T07:25:51+00:00)

Expanded fix shipped: not just create_actor, but all 18 auto-log sites across 10 servers. 6 session LogEntries backfilled. Drift allowlist extended.


## Transition note (2026-04-21T07:25:55+00:00)

Shipped in commit below.
