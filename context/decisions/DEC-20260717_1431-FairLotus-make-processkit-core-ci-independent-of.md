---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260717_1431-FairLotus-make-processkit-core-ci-independent-of
  created: '2026-07-17T14:31:22+00:00'
  updated: '2026-07-19T14:30:50+00:00'
spec:
  title: Make processkit core CI independent of aibox
  state: superseded
  decision: Processkit core CI will run native MCP, staged-package, regression, and
    documentation checks without installing or invoking aibox. Aibox integration remains
    a separate adapter test boundary.
  context: The v1.0 test strategy requires clear failure ownership and repeatable
    validation from the processkit repository. The existing smoke test did not invoke
    aibox but still used an aibox.toml fixture marker and imported directly from the
    checkout.
  rationale: Provider-neutral fixtures and staged-distribution tests prove processkit
    behavior and package completeness directly. Separating the aibox adapter prevents
    installer or host-runtime failures from blocking diagnosis of processkit core
    failures.
  alternatives:
  - option: Keep manual aibox-derived-project dogfooding as the primary test
    rejected_because: It is not repeatable in repository CI and conflates installer
      failures with processkit failures.
  - option: Run the release builder on every pull request
    rejected_because: The builder mutates generated metadata and enforces tag-specific
      provenance, so it is unsuitable for ordinary branch validation.
  consequences: GitHub Actions must maintain native, staged-package, and docs jobs.
    Release validation can reuse the package smoke test against a built archive. Aibox
    coverage remains necessary, but as a separately owned adapter suite.
  decided_at: '2026-07-17T14:31:22+00:00'
  superseded_by: DEC-20260719_1430-HonestOak-use-manual-local-verification-instead-of
---
