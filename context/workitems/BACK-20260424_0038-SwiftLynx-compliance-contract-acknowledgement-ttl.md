---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260424_0038-SwiftLynx-compliance-contract-acknowledgement-ttl
  created: '2026-04-24T00:38:15+00:00'
spec:
  title: Compliance-contract acknowledgement TTL — auto-renew or extend during active
    sessions
  state: backlog
  type: task
  priority: low
  assignee: TEAMMEMBER-cora
  description: '**Observed pattern (v0.19.2 retro):** the compliance-contract ack
    has a 12h TTL. During long sessions that span midnight (as happened in this cycle),
    the TTL silently expires mid-flow and the next context/ hand-edit is blocked with
    a cryptic "acknowledge_contract(version=''v1'')" error (note: the error text still
    says v1 even though on-disk contract is v2 — separate nit).


    **Proposed behaviour:**

    - Auto-renew the ack whenever a compliant write (`create_*`, `transition_*`, `record_*`,
    `log_event`) succeeds — the session is demonstrably still live.

    - OR extend the TTL to 24h to cover typical long sessions.

    - OR surface the "ack is about to expire" signal proactively (e.g., when there
    are <30 min left on the TTL, remind in the next tool result).


    **Also:** fix the error message text in `check_route_task_called.py` to reference
    the *current* on-disk contract version rather than hard-coding `v1`.


    **Target:** v0.20.0. **Owner:** cora.'
---
