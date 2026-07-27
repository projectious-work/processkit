#!/usr/bin/env bash
set -euo pipefail
exec uv run --offline --with ziglang python -m ziglang cc "$@"
