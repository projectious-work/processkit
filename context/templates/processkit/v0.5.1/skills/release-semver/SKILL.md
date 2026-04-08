---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-release-semver
  name: release-semver
  version: "1.1.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Semantic versioning releases — version bumps, changelogs, tags, publishing."
  category: process
  layer: 3
  when_to_use: "Use when preparing a new release: deciding the version bump, drafting the changelog, tagging the commit, and publishing to the project's distribution channel."
---

# Semantic Versioning Release Process

## Level 1 — Intro

Releases are routine, not heroic. Decide the version bump from the
nature of the changes, draft a changelog, update version files in
one commit, tag with `vX.Y.Z`, and publish. The goal is a release
anyone on the team can perform from the same checklist.

## Level 2 — Overview

### Determine the version bump

Semantic versioning has three numbers: MAJOR.MINOR.PATCH.

- **Patch** (0.1.0 → 0.1.1): bug fixes only, no API changes.
- **Minor** (0.1.0 → 0.2.0): new features, backward-compatible.
- **Major** (0.1.0 → 1.0.0): breaking changes.

Pre-1.0 projects bend the rules: minor bumps are allowed to break
compatibility, and patch bumps cover both features and fixes. Once
you ship 1.0, the rules become strict.

### Pre-release checklist

- All tests pass on the main branch.
- No uncommitted changes in the working tree.
- Dependencies reviewed and up to date where appropriate.
- CHANGELOG or release notes drafted.

### Draft the changelog

Group entries under **Added**, **Changed**, **Fixed**, and
**Removed**. Reference issue and PR numbers. Note breaking changes
prominently — call them out in their own section if a major bump
is involved.

### Bump, commit, tag, publish

Update the version in every relevant file (`Cargo.toml`,
`pyproject.toml`, `package.json`, lockfiles). Commit with a message
like `chore: bump version to vX.Y.Z`. Tag the commit `vX.Y.Z`.
Publish according to the project's distribution channel
(crates.io, PyPI, npm, GitHub Releases, container registry, etc.).

### Example

User says: "Let's release — we fixed two bugs and added a feature."
The agent recommends a minor bump (because of the new feature),
drafts changelog entries grouped Added/Fixed, updates version
files, creates the bump commit, and tags it.

## Level 3 — Full reference

### When pre-1.0 ends

Cut 1.0 when the public API is something you are willing to
support without breaking. Until then, keep the version below 1.0
honestly — there is no shame in 0.17.0, and it signals to users
that the surface may still move.

### Version bumps for special changes

| Change | Bump |
|---|---|
| Bug fix that does not change behavior contract | patch |
| Performance improvement, no API change | patch |
| New feature behind a feature flag | minor |
| New optional parameter with a default | minor |
| Removing or renaming a public symbol | major |
| Changing default behavior of an existing API | major |
| Tightening input validation that rejects previously valid input | major |
| Dependency bump that surfaces in your public API | major |

### Anti-patterns

- Bundling breaking changes into a patch release
- Skipping the changelog "because git log has it"
- Tagging a commit that was not built and tested
- Publishing from a developer machine without a clean checkout
- Re-tagging a published version to fix a mistake (cut a new
  patch instead)
- Pre-1.0 projects that promise stability they cannot keep
