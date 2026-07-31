---
title: "Evidence-bound Release Process"
description: "Repository-owned, resumable release orchestration for processkit maintainers."
weight: 35
---

Issue
[#151](https://github.com/projectious-work/processkit/issues/151)
defines the aibox-style release ritual adopted by processkit.

## Version-line authority

The requested semantic version determines the only branch permitted to tag:

| Version | Required branch |
| --- | --- |
| stable v0 | `v0.x-release` |
| v1 alpha, beta, or RC | `v1.x-pre-release` |
| stable v1 | `v1.x-release` |

Resolve the mapping without mutation:

```sh
scripts/maintain.sh release-branch v1.0.0-alpha.5
```

Promotion into protected branches happens through pull requests. Never
force-push a release branch.

## Candidate evidence

Evidence belongs to an exact candidate:

```text
dist/release-evidence/<version>/<commit>/
├── binding.json
├── RELEASE-STATE.md
├── RELEASE-DOCTORS.md
├── logs/
└── <step>.passed
```

The binding records version, commit, clean tree, branch, Rust, Python, `uv`,
and host target. A step marker is reused only within that binding.

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
binary, checksum, and runner provenance. The
`v1-native-artifacts.yml` workflow runs that contract on x86_64 and arm64 Linux
and macOS hosts. Collected assets are signed into one release envelope; a
release must not claim a target without its native smoke evidence.
