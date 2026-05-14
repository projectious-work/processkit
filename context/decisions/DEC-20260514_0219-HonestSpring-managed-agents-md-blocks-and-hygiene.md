---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260514_0219-HonestSpring-managed-agents-md-blocks-and-hygiene
  created: '2026-05-14T02:19:57+00:00'
spec:
  title: Managed AGENTS.md Blocks And Hygiene Briefings
  state: accepted
  decision: Use managed AGENTS.md blocks for processkit-owned guidance, and add a
    pk-doctor AGENTS.md hygiene check that emits a reconciliation briefing for the
    project agent when drift or anti-patterns are detected.
  context: The owner approved the managed-block approach and an added pk-doctor check
    with a project-agent briefing as the outcome while reviewing derived-project AGENTS.md
    drift.
  rationale: AGENTS.md is customized in derived projects, so full-file overwrite is
    too destructive, but unmanaged full-file preservation lets processkit-owned instructions
    drift across releases. Managed blocks allow deterministic replacement of processkit-owned
    material while preserving local project content. A doctor check and briefing gives
    existing derived projects a migration path without requiring unsafe automatic
    rewrites.
  alternatives:
  - option: Continue manual AGENTS.md review during migrations
    tradeoff: Preserves local customization but has already produced inconsistent
      derived files and stale processkit guidance.
  - option: Overwrite AGENTS.md on every sync
    tradeoff: Keeps upstream guidance current but destroys project-specific instructions
      and would be unacceptable for mature derived projects.
  consequences: Future implementation should define processkit-owned AGENTS.md block
    boundaries, add drift and anti-pattern detection, and generate actionable reconciliation
    briefings during processkit/aibox migration or doctor runs. The check set should
    cover the broader processkit contract, not only provider-model/team anti-patterns.
  decided_at: '2026-05-14T02:19:57+00:00'
---
