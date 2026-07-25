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
scripts/release-local.sh v1.0.0-alpha.3 \
  "$HOME/.config/processkit/keys/release.pem" \
  "$HOME/.config/processkit/trust.d/release.pub.pem"
```

The command runs the complete local validation suite, builds a reproducible
archive, creates an integrity envelope, signs it with Ed25519, and verifies the
result. It produces archive, checksum, release JSON, and signature files under
`dist/`.

## Verify after copying

```sh
scripts/verify-release-local.sh \
  dist/processkit-v1.0.0-alpha.3.release.json \
  dist/processkit-v1.0.0-alpha.3.release.sig \
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

## Current alpha boundary

The shell verifier is the local release-side verifier. The Rust installer must
gain native trust-store verification before signed releases become mandatory
for install and update. Until that lands, the installer commands remain alpha
and must not be presented as authenticity-enforcing.
