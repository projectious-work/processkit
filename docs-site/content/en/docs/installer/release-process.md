---
title: "Evidence-bound Release Process"
description: "Repository-owned, resumable release orchestration for processkit maintainers."
weight: 35
---

Issue
[#151](https://github.com/projectious-work/processkit/issues/151)
defines the aibox-style release ritual adopted by processkit.

## Release branch and target line

Releases follow the company GitHub Flow standard. The candidate is prepared
on `release/vX.Y.Z`, which holds only the `chore(release): vX.Y.Z` commit.
After owner approval it is squash-merged into its target line, and the tag
is created on the squash commit:

| Version | Release branch | Target line and tag |
| --- | --- | --- |
| v0.x | `release/v0.Y.Z` from `lts/v0` | `lts/v0` |
| v1.x and later, including prereleases | `release/vX.Y.Z` from `main` | `main` |

Resolve both without mutation:

```sh
scripts/maintain.sh release-branch v1.0.0-alpha.5
scripts/maintain.sh release-target v1.0.0-alpha.5
```

The candidate steps (`state`, `doctors`, `audit`, `test`, `docs`, `build`)
run only on the release branch. `publish` and `verify` run only on the target
line, at its fetched tip, after the squash merge. If the release finds a
defect, close the release pull request, fix it through `fix/*`, and cut a new
release branch. Never force-push `main` or `lts/v0`.

## Candidate evidence

Evidence belongs to an exact candidate:

```text
dist/release-evidence/<version>/<tree>/
├── binding.json
├── RELEASE-STATE.md
├── RELEASE-DOCTORS.md
├── logs/
└── <step>.passed
```

The binding records version, commit, source tree, clean state, branch, Rust,
Python, `uv`, and host target. Evidence is keyed by the source tree, because
the squash commit on the target line has a new commit id but the same tree as
the release branch. A step marker is reused only within that binding.

## Phase zero

```sh
scripts/maintain.sh release vX.Y.Z --steps phase0
```

This writes dependency/toolchain state and runs `pk-doctor` plus the release
audit. Errors block. Warnings and actionable findings require a tracked
`release-deferrals/vX.Y.Z.md` with rationale, owner, issue, and expiry.

## Candidate checks

```sh
scripts/maintain.sh release vX.Y.Z --steps checks
```

Independent audit, installer, and production-documentation gates run with
bounded concurrency and retain separate logs. The documentation gate requires:

- `release-notes/vX.Y.Z.md`;
- README, contribution, license, security, conduct, maintenance, and support
  files; and
- a complete Hugo build, generated-link check, and contrast check.

## Build and signing

Set absolute paths to the private and public Ed25519 keys:

```sh
export PROCESSKIT_RELEASE_PRIVATE_KEY=/secure/release.pem
export PROCESSKIT_RELEASE_PUBLIC_KEY=/secure/release.pub.pem
scripts/maintain.sh release vX.Y.Z --steps build
```

The build delegates to the existing local release pipeline and stops on any
test, artifact, checksum, signature, or package-acceptance failure.

## Publication and verification

After reviewing the evidence:

```sh
scripts/maintain.sh release vX.Y.Z --steps publish,verify
```

Publication:

1. rechecks the designated release branch and clean candidate;
2. requires all prerequisite evidence;
3. creates and pushes an annotated tag;
4. creates a GitHub release from tracked curated notes with all matching
   archive, checksum, signature, key, and native assets; and
5. deploys the production documentation.

Final verification downloads the public assets, checks archive digests,
records GitHub release metadata, and records the remote peeled tag.

## Recovery and resumption

Rerun the same command on the same candidate. Passed step markers are reused.
Changing the commit creates a new evidence directory and reruns the selected
steps. Publication is deliberately not inferred from a local green run.

If a tag or release was partially published, inspect remote state before
continuing. The orchestrator fails closed when the tag already exists instead
of overwriting public history.

## Host-only phase

`release-host` verifies the exact tag, full source commit, and clean checkout
before building and natively running `processkit --version`. It emits the
binary, checksum, and local-host provenance. Maintainers run that contract on
local x86_64 and arm64 Linux and macOS hosts, then copy the outputs into the
finalization workspace. Collected assets are signed into one release envelope;
a release must not claim a target without its native smoke evidence.
