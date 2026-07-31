---
title: Alpha Release Testing
description: Publish and consume an explicit v1 prerelease safely.
---

> **Alpha.5 documentation review:** This page records design or historical
> planning. For shipped behavior and current gaps, use the
> [issue #135 implementation review](./issue-135-status.md).

## Release Policy

The current test release is the explicit prerelease
`v1.0.0-alpha.5`. It is merged from `v1.x-dev` into
`v1.x-pre-release`, validated there, and tagged there.

Prereleases never become the implicit `latest` version. `latest` remains the
highest stable release, currently from the supported v0 line. Downstream
installers must opt in to an exact prerelease.

## Pre-tag Gate

Run from a clean `v1.x-pre-release` worktree:

```sh
uv run scripts/generate-v1-schemas.py --check
uv run scripts/smoke-test-servers.py
uv run scripts/smoke-test-package.py
scripts/check-docs-local.sh
uv run scripts/generate-mcp-manifest.py --check
scripts/test-installer-local.sh
```

Also run `pk-doctor` and the release audit. The release build must validate
the committed MCP manifest and must not rewrite tracked release metadata.

## Standalone Pilot

Create a local signing key once, then build the complete release set:

```sh
scripts/processkit-keygen-local.sh release.pem release.pub.pem
scripts/release-local.sh \
  v1.0.0-alpha.5 release.pem release.pub.pem
```

The signed envelope binds the archive, native installer executable, target
triple, version, and trusted key. Verify it independently:

```sh
scripts/verify-release-local.sh \
  dist/processkit-v1.0.0-alpha.5.release.json \
  dist/processkit-v1.0.0-alpha.5.release.sig \
  release.pub.pem
```

Run the native executable against a disposable project through its opaque
request contract. The local installer suite covers install, verify, update,
recovery, user-drift handling, and uninstall. It neither invokes aibox nor
uses GitHub Actions.

The suite includes two complementary recovery signals:

- the full shipped distribution completes install/update/uninstall lifecycle
  acceptance; and
- a compact signed-layout fixture sets
  `PROCESSKIT_INSTALLER_FAIL_AFTER_ACTION=0`, proves exit 75 and a durable
  journal, runs native recovery, verifies the exact old state and project-owned
  file, retries the update, and verifies the new provenance.

Run that focused acceptance independently with:

```sh
scripts/test-update-recovery-local.sh
```

An aibox pilot may consume the exact signed prerelease afterward. That is a
downstream compatibility check and never blocks or defines processkit
release correctness.

## Promotion

Promote the next alpha only from a new merge into `v1.x-pre-release`. Alpha
tags are immutable. The supported v0 line remains the default until the final
CLI and migration path have passed joint processkit/aibox testing.
