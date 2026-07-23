---
title: Alpha Release Testing
description: Publish and consume an explicit v1 prerelease safely.
---

# Alpha Release Testing

## Release Policy

The first test release is an explicit prerelease such as
`v1.0.0-alpha.1`. It is merged from `v1.x-dev` into
`v1.x-pre-release`, validated there, and tagged there.

Prereleases never become the implicit `latest` version. `latest` remains the
highest stable release, currently from the supported v0 line. This prevents
existing aibox projects from crossing a major-version boundary without an
explicit pin. The matching aibox proposal is tracked in
[aibox issue #133](https://github.com/projectious-work/aibox/issues/133).

## Pre-tag Gate

Run from a clean `v1.x-pre-release` worktree:

```sh
uv run scripts/generate-v1-schemas.py --check
uv run scripts/smoke-test-servers.py
uv run scripts/smoke-test-package.py
npm --prefix docs-site run build
uv run scripts/generate-mcp-manifest.py --check
```

Also run `pk-doctor` and the release audit. The release build must validate
the committed MCP manifest and must not rewrite tracked release metadata.

## aibox Pilot

Use a disposable aibox project and pin the exact prerelease:

```toml
[processkit]
source = "https://github.com/projectious-work/processkit.git"
version = "v1.0.0-alpha.1"
```

Then:

1. run the aibox sync/apply operation for its v1 development line
2. confirm the lock file records the exact prerelease
3. confirm all processkit MCP servers and gateway tools are merged
4. run the v0-to-v1 migration planner before executing it
5. run `pk-doctor`
6. create and transition a WorkItem, Scope, Capability, and Skill
7. create a claim and a Risk
8. query by the Record, Actor, Capability, and Skill interfaces
9. export and validate an OKF v0.1 bundle
10. rebuild the container and repeat the read-only checks

Do not use `latest`, a floating branch name, or a moved tag for this pilot.
Record any aibox adapter failure against the exact processkit and aibox
versions.

## Promotion

Promote to `alpha.2` only from a new merge into `v1.x-pre-release`. Alpha
tags are immutable. Beta begins only after the alpha gate is green and the
planned ontology expansion remains within the recorded 60–70 percent target.
