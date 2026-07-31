# Install and Use the v1 Alpha

> Verify, install, and use processkit v1.0.0-alpha.5 step by step.

---

LLMS index: [llms.txt](/processkit/v1.x/llms.txt)

---

This tutorial installs the exact `v1.0.0-alpha.5` release into a new project.
Linux and macOS on x86_64 and arm64 are supported.

## 1. Check prerequisites

```sh
uname -m
python3 --version
uv --version
git --version
jq --version
```

Python 3.10 or newer, `uv`, Git, `curl`, `tar`, a SHA-256 utility, `openssl`,
and `jq` are required.

## 2. Download the exact release

```sh
mkdir -p "$PWD/.processkit-download/v1.0.0-alpha.5"
cd "$PWD/.processkit-download/v1.0.0-alpha.5"

release_url="https://github.com/projectious-work/processkit/releases/download/v1.0.0-alpha.5"
for asset in \
  processkit-v1.0.0-alpha.5.tar.gz \
  processkit-v1.0.0-alpha.5.tar.gz.sha256 \
  processkit-v1.0.0-alpha.5.release.json \
  processkit-v1.0.0-alpha.5.release.sig \
  processkit-v1.0.0-alpha.5-public.pem
do
  curl -fL "$release_url/$asset" -o "$asset"
done
```

The release is exact-pinned. Do not replace the tag with `latest`.

## 3. Verify checksums

```sh
sha256sum -c processkit-v1.0.0-alpha.5.tar.gz.sha256
```

The command must report `OK`.

## 4. Install the CLI locally

```sh
curl -fLO \
  https://raw.githubusercontent.com/projectious-work/processkit/v1.0.0-alpha.5/scripts/install-processkit.sh
chmod +x install-processkit.sh
./install-processkit.sh v1.0.0-alpha.5
export PATH="$HOME/.local/bin:$PATH"
processkit --version
```

No root access is required. Add `$HOME/.local/bin` to your shell `PATH` if
it is not already present.

## 5. Verify the signed release

```sh
mkdir -p "$PWD/trust"
key_id="d35516ccd7be9efad6579c5f6c2ab8ba1a59f18d563f339e62e1cef9a5f9a1eb"
cp processkit-v1.0.0-alpha.5-public.pem \
  "$PWD/trust/v1.pub.pem"

jq -n --arg key_id "$key_id" '{
  apiVersion: "processkit.projectious.work/local-trust/v1alpha1",
  kind: "TrustStore",
  keys: [{
    keyId: $key_id,
    algorithm: "Ed25519",
    publicKeyFile: "v1.pub.pem",
    status: "active"
  }]
}' >"$PWD/trust/trust-store.json"

processkit verify-release \
  --envelope "$PWD/processkit-v1.0.0-alpha.5.release.json" \
  --signature "$PWD/processkit-v1.0.0-alpha.5.release.sig" \
  --trust-store "$PWD/trust/trust-store.json"
```

For organizational use, obtain the public key through an independently
trusted channel. Publishing a key beside an artifact makes verification
reproducible but does not by itself establish publisher identity.

## 6. Extract the distribution

```sh
tar -xzf processkit-v1.0.0-alpha.5.tar.gz
distribution="$PWD/processkit-v1.0.0-alpha.5"
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
