#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export CARGO_NET_OFFLINE=true
if ! command -v cc >/dev/null; then
    export CARGO_TARGET_AARCH64_UNKNOWN_LINUX_GNU_LINKER="$REPO_ROOT/scripts/zig-cc-local.sh"
    export ZIG_GLOBAL_CACHE_DIR="${TMPDIR:-/tmp}/processkit-zig-global"
    export ZIG_LOCAL_CACHE_DIR="${TMPDIR:-/tmp}/processkit-zig-local"
fi
TEST_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/processkit-trust-test.XXXXXX")"
trap 'rm -rf "$TEST_ROOT"' EXIT

PRIVATE_KEY="$TEST_ROOT/release.pem"
PUBLIC_KEY="$TEST_ROOT/release.pub.pem"
TRUST_STORE="$TEST_ROOT/trust-store.json"
VERSION="v1.0.0-alpha.0"
ARCHIVE="$TEST_ROOT/processkit-$VERSION.tar.gz"
ENVELOPE="$TEST_ROOT/processkit-$VERSION.release.json"
SIGNATURE="$TEST_ROOT/processkit-$VERSION.release.sig"
INSTALLER="$TEST_ROOT/processkit-$VERSION-test-target"
ARCHIVE_ROOT="$TEST_ROOT/processkit-$VERSION"
DESCRIPTOR="$ARCHIVE_ROOT/.processkit/installer/release-descriptor.json"
PROVENANCE="$ARCHIVE_ROOT/PROVENANCE.toml"

"$REPO_ROOT/scripts/processkit-keygen-local.sh" "$PRIVATE_KEY" "$PUBLIC_KEY" \
    >/dev/null
mkdir -p "$ARCHIVE_ROOT"
cp -a \
    "$REPO_ROOT/installer/crates/processkit/tests/fixtures/plans/empty/distribution/." \
    "$ARCHIVE_ROOT/"
printf '[source]\ngenerated_for_tag = "%s"\n' "$VERSION" >"$PROVENANCE"
tar -czf "$ARCHIVE" -C "$TEST_ROOT" "processkit-$VERSION"
printf 'native installer fixture\n' >"$INSTALLER"
ARCHIVE_SHA="$(sha256sum "$ARCHIVE" | awk '{print $1}')"
ARCHIVE_SIZE="$(stat -c %s "$ARCHIVE")"
INSTALLER_SHA="$(sha256sum "$INSTALLER" | awk '{print $1}')"
INSTALLER_SIZE="$(stat -c %s "$INSTALLER")"
DESCRIPTOR_SHA="$(sha256sum "$DESCRIPTOR" | awk '{print $1}')"
PROVENANCE_SHA="$(sha256sum "$PROVENANCE" | awk '{print $1}')"
printf '%s  %s\n' "$ARCHIVE_SHA" "$(basename "$ARCHIVE")" \
    >"$ARCHIVE.sha256"
KEY_ID="$(
    openssl pkey -pubin -in "$PUBLIC_KEY" -outform DER |
        sha256sum | awk '{print $1}'
)"
jq -n --sort-keys \
    --arg key_id "$KEY_ID" \
    --arg public_key "$(basename "$PUBLIC_KEY")" \
    '{
      apiVersion: "processkit.projectious.work/local-trust/v1alpha1",
      kind: "TrustStore",
      keys: [{
        keyId: $key_id,
        algorithm: "Ed25519",
        publicKeyFile: $public_key,
        status: "active"
      }]
    }' >"$TRUST_STORE"
jq -n --sort-keys \
    --arg version "$VERSION" \
    --arg file "$(basename "$ARCHIVE")" \
    --arg sha256 "$ARCHIVE_SHA" \
    --argjson archive_size "$ARCHIVE_SIZE" \
    --arg descriptor_sha256 "$DESCRIPTOR_SHA" \
    --arg provenance_sha256 "$PROVENANCE_SHA" \
    --arg installer_file "$(basename "$INSTALLER")" \
    --arg installer_sha256 "$INSTALLER_SHA" \
    --argjson installer_size "$INSTALLER_SIZE" \
    --arg key_id "$KEY_ID" \
    '{
      apiVersion: "processkit.projectious.work/local-release/v1alpha1",
      kind: "LocalRelease",
      release: {name: "processkit", version: $version},
      archive: {
        file: $file,
        sha256: $sha256,
        size: $archive_size,
        topLevelDirectory: ("processkit-" + $version)
      },
      descriptor: {
        file: ".processkit/installer/release-descriptor.json",
        sha256: $descriptor_sha256
      },
      provenance: {
        file: "PROVENANCE.toml",
        sha256: $provenance_sha256,
        generatedForTag: $version
      },
      installerAssets: [{
        file: $installer_file,
        sha256: $installer_sha256,
        target: "test-target",
        size: $installer_size
      }],
      signing: {algorithm: "Ed25519", keyId: $key_id}
    }' >"$ENVELOPE"
"$REPO_ROOT/scripts/sign-release-local.sh" \
    "$ENVELOPE" "$PRIVATE_KEY" "$SIGNATURE" >/dev/null
"$REPO_ROOT/scripts/verify-release-local.sh" \
    "$ENVELOPE" "$SIGNATURE" "$TEST_ROOT" >/dev/null

printf 'tampered\n' >>"$INSTALLER"
if "$REPO_ROOT/scripts/verify-release-local.sh" \
    "$ENVELOPE" "$SIGNATURE" "$TEST_ROOT" >/dev/null 2>&1; then
    echo "error: shell verifier accepted a tampered installer asset" >&2
    exit 1
fi
printf 'native installer fixture\n' >"$INSTALLER"

jq '.installerAssets[0].size += 1' "$ENVELOPE" >"$ENVELOPE.next"
mv "$ENVELOPE.next" "$ENVELOPE"
"$REPO_ROOT/scripts/sign-release-local.sh" \
    "$ENVELOPE" "$PRIVATE_KEY" "$SIGNATURE" >/dev/null
if "$REPO_ROOT/scripts/verify-release-local.sh" \
    "$ENVELOPE" "$SIGNATURE" "$TEST_ROOT" >/dev/null 2>&1; then
    echo "error: shell verifier accepted an installer size mismatch" >&2
    exit 1
fi
jq --argjson size "$INSTALLER_SIZE" \
    '.installerAssets[0].size = $size' \
    "$ENVELOPE" >"$ENVELOPE.next"
mv "$ENVELOPE.next" "$ENVELOPE"

jq '.installerAssets += [.installerAssets[0]]' \
    "$ENVELOPE" >"$ENVELOPE.next"
mv "$ENVELOPE.next" "$ENVELOPE"
"$REPO_ROOT/scripts/sign-release-local.sh" \
    "$ENVELOPE" "$PRIVATE_KEY" "$SIGNATURE" >/dev/null
if cargo run --quiet --offline --locked \
    --manifest-path "$REPO_ROOT/installer/Cargo.toml" -- \
    verify-release \
    --envelope "$ENVELOPE" \
    --signature "$SIGNATURE" \
    --trust-store "$TRUST_STORE" >/dev/null 2>&1; then
    echo "error: native verifier accepted duplicate installer assets" >&2
    exit 1
fi
jq '.installerAssets = [.installerAssets[0]]' \
    "$ENVELOPE" >"$ENVELOPE.next"
mv "$ENVELOPE.next" "$ENVELOPE"
"$REPO_ROOT/scripts/sign-release-local.sh" \
    "$ENVELOPE" "$PRIVATE_KEY" "$SIGNATURE" >/dev/null

cargo run --quiet --offline --locked \
    --manifest-path "$REPO_ROOT/installer/Cargo.toml" -- \
    verify-release \
    --envelope "$ENVELOPE" \
    --signature "$SIGNATURE" \
    --trust-store "$TRUST_STORE" \
    --json >/dev/null

# Exercise the opaque request boundary with the signed, safely extracted
# release archive.
jq -n \
    --arg root "$TEST_ROOT/project" \
    --arg envelope "$ENVELOPE" \
    --arg signature "$SIGNATURE" \
    --arg trust_store "$TRUST_STORE" \
    '{
      apiVersion: "processkit.projectious.work/installer/v1alpha1",
      operation: "plan",
      root: $root,
      envelopePath: $envelope,
      signaturePath: $signature,
      trustStorePath: $trust_store,
      profiles: ["managed"]
    }' >"$TEST_ROOT/request.json"
SIGNED_RESULT="$(
    cargo run --quiet --offline --locked \
        --manifest-path "$REPO_ROOT/installer/Cargo.toml" -- \
        execute --request "$TEST_ROOT/request.json"
)"
jq -e '.status == "planned"' <<<"$SIGNED_RESULT" >/dev/null || {
    echo "$SIGNED_RESULT" >&2
    exit 1
}

printf 'tampered\n' >>"$ENVELOPE"
if cargo run --quiet --offline --locked --manifest-path \
    "$REPO_ROOT/installer/Cargo.toml" -- verify-release \
    --envelope "$ENVELOPE" \
    --signature "$SIGNATURE" \
    --trust-store "$TRUST_STORE" >/dev/null 2>&1; then
    echo "error: native verifier accepted a tampered envelope" >&2
    exit 1
fi

echo "local release trust validation passed"
