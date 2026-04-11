---
apiVersion: processkit.projectious.work/v1
kind: Process
metadata:
  id: PROC-release
  version: "1.1.0"
  created: 2026-04-07T00:00:00Z
spec:
  name: release
  description: "Cut, tag, and publish a versioned processkit release."
  triggers:
    - release.requested
    - milestone.completed
  roles:
    - release-manager
    - developer
  steps:
    - name: breaking-change-audit
      role: release-manager
      description: >
        Confirm the version bump type (major/minor/patch) matches the
        changes. processkit's public API is: schema fields, state-machine
        transitions, and MCP tool signatures. Any removal or rename of
        these requires a MAJOR bump regardless of pre-1.0 status. When
        in doubt, major.
    - name: pre-release-tests
      role: developer
      description: "Run `uv run scripts/smoke-test-servers.py` — must be green."
      gates:
        - GATE-smoke-tests-green
    - name: update-changelog
      role: release-manager
      description: >
        Add a "What changed in vX.Y.Z" section to CHANGELOG.md with
        user-facing changes first. Also update the backlog Done section.
    - name: update-docs-site
      role: release-manager
      description: >
        Update docs-site for any user-visible changes (new primitives,
        new skills, MCP server changes). Version references, skill
        counts, and examples should reflect the new version.
    - name: stamp-provenance
      role: release-manager
      description: >
        Run `scripts/stamp-provenance.sh vX.Y.Z` to regenerate
        `src/PROVENANCE.toml` with the new version and timestamp.
    - name: commit-and-tag
      role: release-manager
      description: >
        Commit the version bump (CHANGELOG, PROVENANCE, version refs)
        in a single commit. Then create an annotated tag:
        `git tag -a vX.Y.Z -m "..."`.
    - name: push
      role: release-manager
      description: >
        Push both the commit and the tag:
        `git push origin main && git push origin vX.Y.Z`.
    - name: build-and-upload-release
      role: release-manager
      description: >
        Run `scripts/build-release-tarball.sh vX.Y.Z` to produce the
        release tarball and sha256 sidecar. Then:
        `gh release upload vX.Y.Z <tarball> <tarball>.sha256`.
        Verify the tarball downloads cleanly before proceeding.
      gates:
        - GATE-artifacts-verified
    - name: deploy-docs
      role: release-manager
      description: >
        Run `cd docs-site && npm run deploy` to publish the updated
        docs to GitHub Pages. Only after the tarball is verified.
        NOTE: the first public deploy is an open TODO — do NOT push
        to `gh-pages` directly until WildButter is unblocked.
  definition_of_done: >
    Smoke tests green; CHANGELOG updated; PROVENANCE stamped; version
    bumped; tag pushed; tarball uploaded to GitHub release with sha256;
    docs deployed.
  retryable: false
---

# Release Process (processkit)

This is the processkit-specific override of the generic `PROC-release`
process. It adds the `stamp-provenance`, tarball-build, and docs-deploy
steps specific to this repository.

## Why retryable: false

A failed release that has already pushed a tag and uploaded artifacts
cannot simply be re-run. Investigate what was done, then either:
- **Roll forward** — bump to the next patch and redo from
  `stamp-provenance`.
- **Roll back** — delete the remote tag (`git push origin --delete
  vX.Y.Z`) and re-do from scratch. Only safe if no consumers have
  downloaded the artifact yet.

## PROVENANCE.toml

`src/PROVENANCE.toml` records the version, commit SHA, and timestamp
for the release. `scripts/stamp-provenance.sh` regenerates it. Never
hand-edit it. Consumers (aibox) read this file to verify they are
consuming the right processkit version.

## Docs deploy blocker

`cd docs-site && npm run deploy` is blocked by aibox#42
(Docusaurus ProgressPlugin incompatibility). Track progress in
WildButter workitem. Do not push to `gh-pages` until the build
succeeds locally.
