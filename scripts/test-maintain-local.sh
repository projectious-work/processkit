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

assert_eq "$("$MAINTAIN" release-branch v0.28.9)" "release/v0.28.9"
assert_eq "$("$MAINTAIN" release-branch 1.0.0-alpha.5)" \
    "release/v1.0.0-alpha.5"
assert_eq "$("$MAINTAIN" release-target v0.28.9)" "lts/v0"
assert_eq "$("$MAINTAIN" release-target v1.0.0-alpha.5)" "main"
assert_eq "$("$MAINTAIN" release-target v1.0.0)" "main"
assert_eq "$("$MAINTAIN" release-target v2.1.0)" "main"

steps="$("$MAINTAIN" release v1.0.0-alpha.5 --list-steps)"
for required in state doctors audit test docs build publish verify; do
    grep -Fx "$required" <<<"$steps" >/dev/null
done

# Off a release branch and off the target line, no release step may run.
if "$MAINTAIN" release v1.0.0-alpha.999 --steps state >/dev/null 2>&1; then
    echo "candidate step unexpectedly ran outside release/*" >&2
    exit 1
fi

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
