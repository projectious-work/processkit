---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260723_1818-AstuteMoon-gate-processkit-v1-alpha-on-explicit
  created: '2026-07-23T18:18:54+00:00'
spec:
  title: Gate processkit v1 alpha on explicit prerelease adoption
  state: accepted
  decision: Publish processkit v1 prereleases only after aibox resolves `latest` to
    the newest stable processkit release by default. Explicit prerelease pins and
    branch overrides remain supported. Implement processkit v1 alpha through a v0.28.3
    reconciliation inventory, alpha MCP parity, representative migration, end-to-end
    scenario, minimum OKF export, release-artifact smoke testing, and an aibox adapter
    test.
  context: Processkit and aibox now both maintain supported v0.x and development v1.x
    lines. Aibox currently sorts all semver tags together, so a processkit v1 alpha
    tag could become the implicit latest version for v0 users.
  rationale: This preserves safe defaults for supported users while allowing intentional
    alpha testing, and turns the v1 alpha gate into executable evidence rather than
    a schema-only milestone.
  alternatives:
  - option: Publish the alpha immediately and rely on GitHub prerelease metadata
    rejected_because: Aibox uses git tags as the authoritative version list, so GitHub
      prerelease metadata does not protect `latest` resolution.
  - option: Avoid v1 tags and test only a moving branch
    rejected_because: This does not test the immutable release asset, checksum, provenance,
      or lockfile contract.
  consequences: 'The first processkit v1 alpha GitHub Release is blocked until aibox
    issue #133 is implemented on its supported v0.x line and forward-ported to v1.x.
    Processkit v1 work can proceed and can be tested through explicit branch/version
    pins in the meantime.'
  decided_at: '2026-07-23T18:18:54+00:00'
---
