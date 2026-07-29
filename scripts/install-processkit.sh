#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'EOF'
Usage:
  install-processkit.sh <exact-version> --key-sha256 <sha256> [options]

Options:
  --bin-dir <path>     Install directory (default: $HOME/.local/bin)
  --repo <url>         Release repository URL
  --target <triple>    Override detected target
  --key-sha256 <hash>  Trusted Ed25519 public-key fingerprint

The version must be exact (for example v1.0.0-alpha.5). The installer never
uses sudo and never resolves a floating "latest" release.
EOF
}

die() {
    echo "error: $*" >&2
    exit 1
}

[[ $# -gt 0 ]] || {
    usage
    exit 2
}
VERSION="$1"
shift
BIN_DIR="${HOME:?HOME is required}/.local/bin"
REPO_URL="https://github.com/projectious-work/processkit"
TARGET=""
KEY_SHA256="${PROCESSKIT_TRUSTED_KEY_SHA256:-}"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --bin-dir) BIN_DIR="${2:?path required}"; shift 2 ;;
        --repo) REPO_URL="${2:?URL required}"; shift 2 ;;
        --target) TARGET="${2:?target required}"; shift 2 ;;
        --key-sha256) KEY_SHA256="${2:?hash required}"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) die "unknown option: $1" ;;
    esac
done

[[ "$VERSION" =~ ^v[0-9]+\.[0-9]+\.[0-9]+(-[0-9A-Za-z.-]+)?$ ]] ||
    die "an exact semantic version is required"
[[ "$KEY_SHA256" =~ ^[a-f0-9]{64}$ ]] ||
    die "--key-sha256 must be a lowercase SHA-256 fingerprint"
[[ "$BIN_DIR" == /* ]] || die "--bin-dir must be absolute"

if [[ -z "$TARGET" ]]; then
    machine="$(uname -m)"
    case "$(uname -s):$machine" in
        Linux:x86_64) TARGET="x86_64-unknown-linux-gnu" ;;
        Linux:aarch64|Linux:arm64) TARGET="aarch64-unknown-linux-gnu" ;;
        Darwin:x86_64) TARGET="x86_64-apple-darwin" ;;
        Darwin:arm64|Darwin:aarch64) TARGET="aarch64-apple-darwin" ;;
        *) die "unsupported platform: $(uname -s) $machine" ;;
    esac
fi
case "$TARGET" in
    x86_64-unknown-linux-gnu|aarch64-unknown-linux-gnu|\
    x86_64-apple-darwin|aarch64-apple-darwin) ;;
    *) die "unsupported target: $TARGET" ;;
esac

for command in curl jq openssl mktemp; do
    command -v "$command" >/dev/null || die "required command missing: $command"
done
if command -v sha256sum >/dev/null; then
    sha256_file() {
        sha256sum "$1" | awk '{print $1}'
    }
    sha256_stdin() {
        sha256sum | awk '{print $1}'
    }
elif command -v shasum >/dev/null; then
    sha256_file() {
        shasum -a 256 "$1" | awk '{print $1}'
    }
    sha256_stdin() {
        shasum -a 256 | awk '{print $1}'
    }
else
    die "required SHA-256 command missing: sha256sum or shasum"
fi

tmp_dir="$(mktemp -d)"
staged=""
trap 'rm -rf "$tmp_dir"; [[ -z "$staged" ]] || rm -f "$staged"' EXIT
base_url="${REPO_URL%/}/releases/download/$VERSION"
asset="processkit-$VERSION-$TARGET"
envelope="processkit-$VERSION.release.json"
signature="processkit-$VERSION.release.sig"
public_key="processkit-$VERSION-public.pem"

for file in "$asset" "$asset.sha256" "$envelope" "$signature" "$public_key"; do
    curl --fail --location --silent --show-error \
        "$base_url/$file" --output "$tmp_dir/$file"
done

actual_key_sha="$(
    openssl pkey -pubin -in "$tmp_dir/$public_key" -outform DER |
        sha256_stdin
)"
[[ "$actual_key_sha" == "$KEY_SHA256" ]] ||
    die "published key does not match the trusted fingerprint"
[[ "$(jq -er '.signing.keyId' "$tmp_dir/$envelope")" == "$KEY_SHA256" ]] ||
    die "release envelope names a different signing key"
jq -e \
    --arg version "$VERSION" \
    '.apiVersion == "processkit.projectious.work/local-release/v1alpha1"
     and .kind == "LocalRelease"
     and .release.name == "processkit"
     and .release.version == $version
     and .signing.algorithm == "Ed25519"' \
    "$tmp_dir/$envelope" >/dev/null ||
    die "release envelope identity does not match the request"
openssl pkeyutl -verify -rawin -pubin \
    -inkey "$tmp_dir/$public_key" \
    -in "$tmp_dir/$envelope" \
    -sigfile "$tmp_dir/$signature" >/dev/null ||
    die "release envelope signature verification failed"

expected_sha="$(
    jq -er --arg target "$TARGET" --arg file "$asset" \
        '.installerAssets[]
         | select(.target == $target and .file == $file)
         | .sha256' "$tmp_dir/$envelope"
)"
expected_size="$(
    jq -er --arg target "$TARGET" --arg file "$asset" \
        '.installerAssets[]
         | select(.target == $target and .file == $file)
         | .size' "$tmp_dir/$envelope"
)"
[[ "$expected_sha" =~ ^[a-f0-9]{64}$ ]] ||
    die "release envelope does not contain the requested target"
actual_size="$(wc -c <"$tmp_dir/$asset" | tr -d '[:space:]')"
[[ "$actual_size" == "$expected_size" ]] ||
    die "installer asset size mismatch"
sidecar_sha="$(awk 'NF >= 1 {print $1; exit}' "$tmp_dir/$asset.sha256")"
actual_sha="$(sha256_file "$tmp_dir/$asset")"
[[ "$sidecar_sha" == "$actual_sha" ]] ||
    die "installer asset digest does not match its checksum sidecar"
[[ "$actual_sha" == "$expected_sha" ]] ||
    die "installer asset digest does not match the signed envelope"

mkdir -p "$BIN_DIR"
destination="$BIN_DIR/processkit"
[[ ! -e "$destination" && ! -L "$destination" ]] ||
    die "destination already exists: $destination"
staged="$(mktemp "$BIN_DIR/.processkit.install.XXXXXX")"
cp "$tmp_dir/$asset" "$staged"
chmod 755 "$staged"
"$staged" --version >/dev/null
if ! ln "$staged" "$destination"; then
    die "destination appeared during installation: $destination"
fi
rm -f "$staged"
staged=""
trap - EXIT
rm -rf "$tmp_dir"

echo "installed processkit $VERSION for $TARGET to $destination"
