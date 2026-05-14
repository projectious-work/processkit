---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260514_0223-AbleShell-expanded-agents-md-hygiene-scope
  created: '2026-05-14T02:23:14+00:00'
spec:
  title: Expanded AGENTS.md Hygiene Scope
  state: accepted
  decision: The AGENTS.md hygiene work must check the full set of processkit-owned
    or processkit-dependent guidance, not only observed team/model anti-patterns.
    The check should emit reconciliation briefings that tell the project agent what
    to replace, merge, rehome, or explicitly fork.
  context: After approving managed AGENTS.md blocks and a pk-doctor hygiene check,
    the owner explicitly broadened the required scope. The check must analyze what
    processkit regulates and whether AGENTS.md contains the references needed for
    current processkit operation.
  rationale: 'Derived project AGENTS.md drift can break processkit operation in many
    ways: stale compliance rules, stale entity IO instructions, stale migration flow,
    stale MCP topology, stale command references, missing managed blocks, and local
    content mixed into processkit-owned guidance. Focusing only on concrete provider
    model anti-patterns would miss other high-impact drift classes.'
  consequences: Implementation should include deterministic managed-block checks,
    semantic stale-guidance checks, processkit reference coverage checks, and actionable
    briefing text suitable for a project agent to reconcile the file safely.
  decided_at: '2026-05-14T02:23:14+00:00'
---
