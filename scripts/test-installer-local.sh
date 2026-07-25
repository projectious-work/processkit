#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export UV_OFFLINE=1

if ! command -v cc >/dev/null; then
    export CARGO_TARGET_AARCH64_UNKNOWN_LINUX_GNU_LINKER="$REPO_ROOT/scripts/zig-cc-local.sh"
    export ZIG_GLOBAL_CACHE_DIR="${TMPDIR:-/tmp}/processkit-zig-global"
    export ZIG_LOCAL_CACHE_DIR="${TMPDIR:-/tmp}/processkit-zig-local"
    uv run --offline --with ziglang python -m ziglang version >/dev/null || {
        echo "error: cc is unavailable and the local ziglang package is not installed" >&2
        echo "install it once with: uv run --with ziglang python -m ziglang version" >&2
        exit 1
    }
fi

cargo fmt --check --manifest-path "$REPO_ROOT/installer/Cargo.toml"
cargo clippy --locked --manifest-path "$REPO_ROOT/installer/Cargo.toml" \
    --all-targets -- -D warnings
cargo test --locked --manifest-path "$REPO_ROOT/installer/Cargo.toml"
"$REPO_ROOT/scripts/test-release-trust-local.sh"
uv run --offline --with pytest --with pyyaml --with jsonschema \
    pytest "$REPO_ROOT/tests/test_verify_installer_contract.py"
uv run --offline "$REPO_ROOT/scripts/smoke-test-package.py" \
    --release-root "$REPO_ROOT/src"

echo "local installer validation passed"
