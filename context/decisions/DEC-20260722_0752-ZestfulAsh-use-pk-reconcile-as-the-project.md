---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260722_0752-ZestfulAsh-use-pk-reconcile-as-the-project
  created: '2026-07-22T07:52:43+00:00'
spec:
  title: Use pk-reconcile as the project-wide reconciliation command
  state: accepted
  decision: Add a project-reconciliation skill with the /pk-reconcile command. Its
    default all scope coordinates migration-management, pk-doctor, and repo-management.
    Make pk-resume delegate its session-start cleanup to pk-reconcile session-start,
    which resolves safe migrations and health work and inventories GitHub state without
    closing issues or merging pull requests.
  context: Users repeatedly request one combined action to resolve pending migrations,
    pk-doctor errors, warnings and actionable findings, GitHub issues, and open pull
    requests. Existing pk-resume and pk-repo-reconcile cover portions of that work
    but do not provide one coordinated command.
  rationale: A dedicated orchestrator removes repeated prompting while retaining specialist
    remediation and confirmation safeguards. Delegation from pk-resume eliminates
    duplicated migration, health, and GitHub instructions.
  alternatives:
  - option: Expand pk-repo-reconcile to include migrations and doctor findings
    rejected_because: Rejected because repository stewardship would become responsible
      for unrelated processkit state-machine and health remediation.
  - option: Make pk-resume execute every repository mutation by default
    rejected_because: Rejected because session start must not silently close external
      issues or merge protected pull requests.
  consequences: /pk-reconcile becomes the command for full cleanup; /pk-resume uses
    its session-start scope. External issue closure and PR merges remain evidence-
    and confirmation-gated.
  decided_at: '2026-07-22T07:52:43+00:00'
---
