# Local release operation

The v1 release path is local, agent-first, and human-operable. It does not
require GitHub Actions, a hosted CI service, or a publication provider.
Agents and humans invoke the same repository scripts.

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
scripts/release-local.sh v1.0.0-alpha.2 \
  "$HOME/.config/processkit/keys/release.pem" \
  "$HOME/.config/processkit/trust.d/release.pub.pem"
```

The command runs the complete local validation suite, builds a reproducible
archive, creates an integrity envelope, signs it with Ed25519, and verifies the
result. It produces the archive, native installer executable, checksum
sidecars, release JSON, and signature under `dist/`. The signed envelope
contains a required `installerAssets` matrix. A local alpha or beta release
contains the current Rust host target; later multi-platform releases can add
one unique entry per target after building each executable locally.

## Verify after copying

```sh
scripts/verify-release-local.sh \
  dist/processkit-v1.0.0-alpha.2.release.json \
  dist/processkit-v1.0.0-alpha.2.release.sig \
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
  --envelope dist/processkit-v1.0.0-alpha.2.release.json \
  --signature dist/processkit-v1.0.0-alpha.2.release.sig \
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
