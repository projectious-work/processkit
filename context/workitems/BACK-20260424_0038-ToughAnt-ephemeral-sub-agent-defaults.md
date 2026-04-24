---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260424_0038-ToughAnt-ephemeral-sub-agent-defaults
  created: '2026-04-24T00:38:05+00:00'
  updated: '2026-04-24T01:10:28+00:00'
spec:
  title: Ephemeral sub-agent defaults — allow Write/mkdir under context/skills/ for
    scoped delegation
  state: done
  type: task
  priority: medium
  assignee: TEAMMEMBER-cora
  description: '**Observed pattern (v0.19.2 retro):** dispatching an ephemeral subagent
    for ToughMeadow (create `commands/pk-doctor.md` + new check module) hit a permission
    block — the subagent could not `Write` new files or `mkdir` new directories, even
    with `dangerouslyDisableSandbox=true`. Cost ~10 min to diagnose and forced the
    main session to do the file creation itself, negating the parallelization benefit.


    **Scope to investigate:**

    - Harness-level permission defaults for spawned subagents: are they inheriting
    a stricter set than the main session?

    - Whether there is a documented allowlist path for scoped writes under `context/skills/<skill>/`
    when the task is explicitly that kind.

    - If the block is intentional (safety), document it in AGENTS.md so delegation
    prompts avoid set-up-for-failure tasks.


    **Done criteria:**

    - Either (a) subagents can create files under `context/skills/processkit/*/commands/`
    and `context/skills/processkit/*/scripts/checks/` when dispatched for scoped tasks,
    OR (b) AGENTS.md documents the restriction with a clear "delegate X to agents,
    do Y yourself" rule.


    **Target:** next session. **Owner:** cora.'
  started_at: '2026-04-24T01:01:54+00:00'
  completed_at: '2026-04-24T01:10:28+00:00'
---

## Transition note (2026-04-24T01:01:54+00:00)

Picked up for v0.20.0 per DEC-SolidBadger.


## Transition note (2026-04-24T01:03:19+00:00)

Fix: option (b) — added "Sub-agent delegation" section to AGENTS.md and src/AGENTS.md documenting the read-only / mutating split and the "don't broaden the allowlist, move the write back to main" rule. Option (a) deferred: harness-level permission propagation is out of scope for processkit (belongs to the consuming harness).


## Transition note (2026-04-24T01:10:28+00:00)

Shipped in e3b7b3c for v0.20.0.
