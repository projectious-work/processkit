---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260719_1430-HonestOak-use-manual-local-verification-instead-of
  created: '2026-07-19T14:30:50+00:00'
  updated: '2026-07-19T18:58:03+00:00'
spec:
  title: Use manual local verification instead of GitHub Actions
  state: superseded
  decision: Remove GitHub Actions workflows and repository-local GitHub actions from
    every maintained branch. Build, test, package, doctor, and documentation verification
    will be run manually with documented local commands.
  context: The owner explicitly does not want GitHub Actions and prefers manual local
    build and testing. The v1 branch currently contains an unpushed Native CI workflow,
    and other remote branches must be audited for deployed workflows.
  rationale: This makes the repository policy explicit and prevents workflow files
    from being reintroduced as an assumed release gate.
  alternatives:
  - option: Keep disabled workflow files
    rejected_because: They remain GitHub Actions configuration and can be re-enabled
      accidentally.
  - option: Keep Actions only on main
    rejected_because: The owner requested removal from every branch.
  consequences: GitHub will not automatically validate pushes or pull requests. Maintainers
    must run and report the local verification suite before merging or releasing.
  decided_at: '2026-07-19T14:30:50+00:00'
  supersedes: DEC-20260717_1431-FairLotus-make-processkit-core-ci-independent-of
  superseded_by: DEC-20260719_1857-KindGarnet-publish-documentation-to-gh-pages-from
---
