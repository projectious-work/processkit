---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260820_0812-CuriousQuail-apply-pending-content-sync-migration
  created: '2026-08-20T08:12:53+00:00'
spec:
  title: Apply pending content-sync migration
  state: accepted
  decision: Apply MIG-20260820_0729-ContentSync-processkit-content-sync despite its
    one reported conflict, as explicitly confirmed by the user.
  context: The reconciliation run found a pending upstream content-sync migration
    from v0.27.0 to v0.28.8 with 15 new upstream files, 145 local-only files, and
    one conflict in supply-chain-audit/mcp/server.py.
  rationale: The user explicitly confirmed the migration should be applied.
  consequences: The migration-management state machine will record the application
    and preserve its audit trail.
  decided_at: '2026-08-20T08:12:53+00:00'
---
