# Alpha Release Testing

> Publish and consume an explicit v1 prerelease safely.

---

LLMS index: [llms.txt](/processkit/v1.x/llms.txt)

---

> **Alpha.4 documentation review:** This page records design or historical
> planning. For shipped behavior and current gaps, use the
> [issue #135 implementation review](./issue-135-status.md).

## Release Policy

The current test release is the explicit prerelease
`v1.0.0-alpha.4`. It is merged from `v1.x-dev` into
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
  v1.0.0-alpha.4 release.pem release.pub.pem
```

The signed envelope binds the archive, native installer executable, target
triple, version, and trusted key. Verify it independently:

```sh
scripts/verify-release-local.sh \
  dist/processkit-v1.0.0-alpha.4.release.json \
  dist/processkit-v1.0.0-alpha.4.release.sig \
  release.pub.pem
```

Run the native executable against a disposable project through its opaque
request contract. The local installer suite covers install, verify, update,
recovery, user-drift handling, and uninstall. It neither invokes aibox nor
uses GitHub Actions.

An aibox pilot may consume the exact signed prerelease afterward. That is a
downstream compatibility check and never blocks or defines processkit
release correctness.

## Promotion

Promote to `alpha.3` only from a new merge into `v1.x-pre-release`. Alpha
tags are immutable. The supported v0 line remains the default until the
complete ontology and final CLI have passed joint processkit/aibox testing.
