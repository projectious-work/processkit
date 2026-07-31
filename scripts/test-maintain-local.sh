#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MAINTAIN="$ROOT/scripts/maintain.sh"

assert_eq() {
    [[ "$1" == "$2" ]] || {
        echo "expected '$2', got '$1'" >&2
        exit 1
    }
}

assert_eq "$("$MAINTAIN" release-branch v0.28.4)" "v0.x-release"
assert_eq "$("$MAINTAIN" release-branch v1.0.0-alpha.5)" \
    "v1.x-pre-release"
assert_eq "$("$MAINTAIN" release-branch v1.0.0)" "v1.x-release"

steps="$("$MAINTAIN" release v1.0.0-alpha.5 --list-steps)"
for required in state doctors audit test docs build publish verify; do
    grep -Fx "$required" <<<"$steps" >/dev/null
done

if "$MAINTAIN" release-branch invalid >/dev/null 2>&1; then
    echo "invalid version unexpectedly accepted" >&2
    exit 1
fi

if "$MAINTAIN" release-host v1.0.0-alpha.999 \
    "$(git -C "$ROOT" rev-parse HEAD)" >/dev/null 2>&1; then
    echo "host build unexpectedly accepted an untagged candidate" >&2
    exit 1
fi

echo "maintain.sh contract tests passed"
