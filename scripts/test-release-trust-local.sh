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

"$REPO_ROOT/scripts/processkit-keygen-local.sh" "$PRIVATE_KEY" "$PUBLIC_KEY" \
    >/dev/null
printf 'signed release fixture\n' >"$ARCHIVE"
printf 'native installer fixture\n' >"$INSTALLER"
ARCHIVE_SHA="$(sha256sum "$ARCHIVE" | awk '{print $1}')"
INSTALLER_SHA="$(sha256sum "$INSTALLER" | awk '{print $1}')"
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
    --arg installer_file "$(basename "$INSTALLER")" \
    --arg installer_sha256 "$INSTALLER_SHA" \
    --arg key_id "$KEY_ID" \
    '{
      apiVersion: "processkit.projectious.work/local-release/v1alpha1",
      kind: "LocalRelease",
      release: {name: "processkit", version: $version},
      archive: {file: $file, sha256: $sha256},
      installer: {
        file: $installer_file,
        sha256: $installer_sha256,
        target: "test-target"
      },
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

cargo run --quiet --offline --locked \
    --manifest-path "$REPO_ROOT/installer/Cargo.toml" -- \
    verify-release \
    --envelope "$ENVELOPE" \
    --signature "$SIGNATURE" \
    --trust-store "$TRUST_STORE" \
    --json >/dev/null

# Exercise the opaque request boundary with a real signed, safely extracted
# release archive.
tar -czf "$ARCHIVE" \
    -C "$REPO_ROOT/installer/crates/processkit/tests/fixtures/plans/empty" \
    distribution
ARCHIVE_SHA="$(sha256sum "$ARCHIVE" | awk '{print $1}')"
printf '%s  %s\n' "$ARCHIVE_SHA" "$(basename "$ARCHIVE")" \
    >"$ARCHIVE.sha256"
jq --arg sha256 "$ARCHIVE_SHA" '.archive.sha256 = $sha256' \
    "$ENVELOPE" >"$ENVELOPE.next"
mv "$ENVELOPE.next" "$ENVELOPE"
"$REPO_ROOT/scripts/sign-release-local.sh" \
    "$ENVELOPE" "$PRIVATE_KEY" "$SIGNATURE" >/dev/null
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
