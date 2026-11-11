---
title: "Release Production"
description: "Build, sign, verify, and publish processkit releases with bound host evidence."
weight: 30
---

The v1 release path is agent-first, human-operable, and entirely local.
Maintainer-controlled machines invoke the same repository scripts and bind
their native results to one tagged commit. No GitHub Actions or hosted build
service participates.

## One-time key setup

Keep the private key outside the repository. The public key may be copied to
the local trust store of every machine that installs official releases.

```sh
scripts/processkit-keygen-local.sh \
  "$HOME/.config/processkit/keys/release.pem" \
  "$HOME/.config/processkit/trust.d/release.pub.pem"
```

Back up the private key securely. Losing it prevents producing a release under
that identity. Disclosing it requires creating a new key identity and removing
the compromised public key from local trust stores.

## Validate and create a release

```sh
scripts/release-local.sh v1.0.0-alpha.5 \
  "$HOME/.config/processkit/keys/release.pem" \
  "$HOME/.config/processkit/trust.d/release.pub.pem"
```

The command runs the complete local validation suite, builds a reproducible
archive, creates an integrity envelope, signs it with Ed25519, and verifies the
result. It produces the archive, native installer executable, checksum
sidecars, release JSON, and signature under `dist/`. The signed envelope
contains a required `installerAssets` matrix. A local alpha or beta release
contains the current Rust host target. Multi-host production uses local Linux
and macOS machines to build each executable independently, copies their
outputs into one trusted finalization workspace, and then binds the matrix:

```sh
scripts/finalize-release-local.sh v1.0.0-alpha.5 \
  /secure/release.pem \
  /secure/release.pub.pem \
  aarch64-unknown-linux-gnu \
  x86_64-unknown-linux-gnu \
  aarch64-apple-darwin \
  x86_64-apple-darwin
```

Finalization fails if any named asset is absent, duplicated, symlinked, or
unsafe. The resulting signature binds every target, filename, digest, and byte
size. Each local host executes `scripts/build-host-artifact.sh`, verifies tag
and commit provenance, and natively smoke-tests its binary. Merely naming a
target never manufactures or validates it.

On each host, check out the release tag and run:

```sh
scripts/maintain.sh release-host v1.0.0-alpha.5
```

Before building, the host checks the following:

- The checkout is exactly the tagged commit.
- The tag points to that commit.
- The commit is on `origin/main`, the v1 release line.
- The worktree is clean.
- The Rust host target matches the requested target.

The provenance file records the version, target, source SHA, release line,
and host details.

## Recovering from a failed host build

A host build never changes the tag or the release line, so recovery is local:

1. Read the error. A provenance error (`checkout does not match source SHA`,
   `tag does not match source SHA`, `source SHA is not on origin/main`, or
   `host checkout is dirty`) means the host has the wrong source. Run
   `git fetch --tags origin`, check out the tag, and remove local changes.
   Never move or recreate a published tag to make a host pass.
2. A toolchain or smoke-test error means the host itself is broken. Fix the
   Rust toolchain, delete that host's `dist/processkit-<version>-<target>*`
   files, and run the host build again.
3. If a target cannot be built at all, do not finalize a matrix that names
   it. The prerelease is finalized only with the targets that were actually
   built and verified, and the missing target is tracked in an issue.
4. If the fix needs a source change, the tag is not reused. Merge the fix to
   `main` and cut the next prerelease version.

## Exact-version bootstrap

The non-root bootstrap installs a native executable only after checking its
checksum, signed-envelope membership, signature, and the canonical Ed25519 key
fingerprint published in `release/processkit-v1-signing-public.pem`:

```sh
scripts/install-processkit.sh v1.0.0-alpha.5
```

It detects Linux x86_64/ARM64 and macOS x86_64/ARM64, installs to
`$HOME/.local/bin` by default, and refuses floating versions. Supplying the
Operators may override the fingerprint only when intentionally selecting a
different trusted release identity.

## Verify after copying

```sh
scripts/verify-release-local.sh \
  dist/processkit-v1.0.0-alpha.5.release.json \
  dist/processkit-v1.0.0-alpha.5.release.sig \
  "$HOME/.config/processkit/trust.d/release.pub.pem"
```

Copying or publishing these files is a separate operation. Any filesystem,
server, removable medium, or artifact host may be used. Publication does not
confer trust; the signature and local public key do.

## Agent operation

Agents should use explicit absolute key paths, capture exit status, retain the
complete stderr log, and report the generated file paths and public-key
fingerprint. They must never print or copy private-key contents. A failed local
gate stops release creation.

## Native consumer verification

The shell verifier remains the human-operable release-side check. The Rust
installer also verifies releases against the versioned JSON trust store:

```sh
processkit verify-release \
  --envelope dist/processkit-v1.0.0-alpha.5.release.json \
  --signature dist/processkit-v1.0.0-alpha.5.release.sig \
  --trust-store "$HOME/.config/processkit/trust-store.json"
```

Both verifiers bind the exact envelope bytes, Ed25519 key identity, semantic
version, archive filename, byte size, SHA-256, and top-level directory. They
also bind every installer target, filename, byte size, and SHA-256, rejecting
duplicate targets or files. The envelope separately binds the release
descriptor and `PROVENANCE.toml` inside the archive; extraction verifies both
digests and requires the provenance tag to match the release version.

Legacy trees can be inspected independently before installation. See
[v0 to v1 compatibility inspection](./v0-compatibility.md).
