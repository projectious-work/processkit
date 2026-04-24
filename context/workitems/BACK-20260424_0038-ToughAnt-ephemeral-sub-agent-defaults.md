---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260424_0038-ToughAnt-ephemeral-sub-agent-defaults
  created: '2026-04-24T00:38:05+00:00'
spec:
  title: Ephemeral sub-agent defaults — allow Write/mkdir under context/skills/ for
    scoped delegation
  state: backlog
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
---
