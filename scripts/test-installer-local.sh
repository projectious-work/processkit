#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

cargo fmt --check --manifest-path "$REPO_ROOT/installer/Cargo.toml"
cargo clippy --locked --manifest-path "$REPO_ROOT/installer/Cargo.toml" \
    --all-targets -- -D warnings
cargo test --locked --manifest-path "$REPO_ROOT/installer/Cargo.toml"
uv run --with pytest --with pyyaml --with jsonschema \
    pytest "$REPO_ROOT/tests/test_verify_installer_contract.py"
uv run "$REPO_ROOT/scripts/smoke-test-package.py" --release-root "$REPO_ROOT/src"

echo "local installer validation passed"
