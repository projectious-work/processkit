# Install and Use the v1 Alpha

> Verify, install, and use processkit v1.0.0-alpha.4 step by step.

---

LLMS index: [llms.txt](/processkit/v1.x/llms.txt)

---

This tutorial installs the exact `v1.0.0-alpha.4` release into a new project.
It uses the only native target currently published:
`aarch64-unknown-linux-gnu`.

## 1. Check prerequisites

```sh
uname -m
python3 --version
uv --version
git --version
jq --version
```

Continue only when `uname -m` reports `aarch64` or `arm64`. Python 3.10 or
newer, `uv`, Git, `curl`, `tar`, `sha256sum`, and `jq` are required.

## 2. Download the exact release

```sh
mkdir -p "$PWD/.processkit-download/v1.0.0-alpha.4"
cd "$PWD/.processkit-download/v1.0.0-alpha.4"

release_url="https://github.com/projectious-work/processkit/releases/download/v1.0.0-alpha.4"
for asset in \
  processkit-v1.0.0-alpha.4.tar.gz \
  processkit-v1.0.0-alpha.4.tar.gz.sha256 \
  processkit-v1.0.0-alpha.4-aarch64-unknown-linux-gnu \
  processkit-v1.0.0-alpha.4-aarch64-unknown-linux-gnu.sha256 \
  processkit-v1.0.0-alpha.4.release.json \
  processkit-v1.0.0-alpha.4.release.sig \
  processkit-v1.0.0-alpha.4.release.pub.pem
do
  curl -fL "$release_url/$asset" -o "$asset"
done
```

The release is exact-pinned. Do not replace the tag with `latest`.

## 3. Verify checksums

```sh
sha256sum -c processkit-v1.0.0-alpha.4.tar.gz.sha256
sha256sum -c \
  processkit-v1.0.0-alpha.4-aarch64-unknown-linux-gnu.sha256
```

Both commands must report `OK`.

## 4. Install the CLI locally

```sh
install -d "$HOME/.local/bin"
install -m 0755 \
  processkit-v1.0.0-alpha.4-aarch64-unknown-linux-gnu \
  "$HOME/.local/bin/processkit"
export PATH="$HOME/.local/bin:$PATH"
processkit --version
```

No root access is required. Add `$HOME/.local/bin` to your shell `PATH` if
it is not already present.

## 5. Verify the signed release

```sh
mkdir -p "$PWD/trust"
key_id="035a31564b52ca7c6e0b7b4c4a37b4fcf94fb3dd178d98473af8a9242dafdeee"
cp processkit-v1.0.0-alpha.4.release.pub.pem \
  "$PWD/trust/alpha4.pub.pem"

jq -n --arg key_id "$key_id" '{
  apiVersion: "processkit.projectious.work/local-trust/v1alpha1",
  kind: "TrustStore",
  keys: [{
    keyId: $key_id,
    algorithm: "Ed25519",
    publicKeyFile: "alpha4.pub.pem",
    status: "active"
  }]
}' >"$PWD/trust/trust-store.json"

processkit verify-release \
  --envelope "$PWD/processkit-v1.0.0-alpha.4.release.json" \
  --signature "$PWD/processkit-v1.0.0-alpha.4.release.sig" \
  --trust-store "$PWD/trust/trust-store.json"
```

For organizational use, obtain the public key through an independently
trusted channel. Publishing a key beside an artifact makes verification
reproducible but does not by itself establish publisher identity.

## 6. Extract the distribution

```sh
tar -xzf processkit-v1.0.0-alpha.4.tar.gz
distribution="$PWD/processkit-v1.0.0-alpha.4"
```

The extracted directory is the required local `--distribution` input.

## 7. Create a project and review the plan

```sh
project_root="$PWD/../../../processkit-alpha-project"
mkdir -p "$project_root"
git -C "$project_root" init

processkit plan \
  --root "$project_root" \
  --distribution "$distribution" \
  --profile managed \
  --harness codex \
  --format human
```

`plan` is non-mutating. Review the selected profile, managed paths, and
harness projection before proceeding. Replace `codex` with `claude` when
that is your harness.

## 8. Install and verify

```sh
processkit install \
  --root "$project_root" \
  --distribution "$distribution" \
  --profile managed \
  --harness codex \
  --yes

processkit verify --root "$project_root"
git -C "$project_root" status --short
```

The installer owns only declared managed paths and harness keys. It records
ownership in `.processkit/state.json`; unrelated harness configuration and
project files are preserved.

## 9. Start using MCP

Restart the selected harness so it reads the installed projection. If you
need a direct development fallback, run the Python gateway from the project:

```sh
cd "$project_root"
uv run \
  context/skills/processkit/processkit-gateway/mcp/server.py \
  serve --transport stdio
```

In the harness, ask:

> Use processkit to create a medium-priority task WorkItem titled
> "Evaluate processkit v1 alpha", then read it back.

Continue with [Your First Entity](../first-entity/) for transitions,
decisions, relationships, and queries.

## 10. Update, recover, or uninstall

Preview a new exact distribution before updating:

```sh
processkit plan \
  --root "$project_root" \
  --distribution /path/to/new/exact/distribution \
  --profile managed \
  --harness codex

processkit update \
  --root "$project_root" \
  --distribution /path/to/new/exact/distribution \
  --yes
```

After an interrupted mutation:

```sh
processkit recover --root "$project_root" --yes
```

To remove only unchanged, provably managed content:

```sh
processkit uninstall --root "$project_root" --yes
```

Changed and user-owned files are preserved and reported.

## Alpha.4 limitations

- Only Linux ARM64 GNU has a published native executable.
- Release acquisition and trust-root distribution are manual.
- Human commands require a local distribution directory.
- Native `doctor`, `migrate`, `package`, `harness`, and `mcp` command groups
  are not implemented.
- Python and `uv` remain required for MCP.
- v0-to-v1 migration is evidence and compatibility inspection only; do not
  migrate an existing v0 project in place.

Track the exact status in the [issue #135 implementation
review](../../development/v1-version/issue-135-status/).
