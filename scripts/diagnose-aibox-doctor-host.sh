#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/diagnose-aibox-doctor-host.sh [--output FILE]

Runs read-only host diagnostics for aibox doctor and writes a report file.

Options:
  -o, --output FILE   Report path. Defaults to diagnostics/aibox-doctor-host-<timestamp>.txt
  -h, --help          Show this help.
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 2
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
repo_root="$(cd "${script_dir}/.." && pwd -P)"
invocation_dir="$(pwd -P)"
stamp="$(date '+%Y%m%d-%H%M%S')"
output="${repo_root}/diagnostics/aibox-doctor-host-${stamp}.txt"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -o | --output)
      [[ $# -ge 2 ]] || die "$1 requires a file path"
      output="$2"
      shift 2
      ;;
    -h | --help)
      usage
      exit 0
      ;;
    *)
      die "unknown argument: $1"
      ;;
  esac
done

if [[ "$output" != /* ]]; then
  output="${invocation_dir}/${output}"
fi

mkdir -p "$(dirname "$output")"

print_command() {
  local arg

  printf '$'
  for arg in "$@"; do
    printf ' %q' "$arg"
  done
  printf '\n'
}

LAST_RC=0

run_section() {
  local title="$1"
  local rc
  shift

  {
    printf '\n## %s\n\n' "$title"
    print_command "$@"
  } >>"$output"

  set +e
  "$@" >>"$output" 2>&1
  rc=$?
  set -e

  {
    printf '\n[exit_code=%d]\n' "$rc"
  } >>"$output"

  LAST_RC="$rc"
}

write_selected_env() {
  local line name value

  printf '\n## selected environment\n\n' >>"$output"
  while IFS= read -r line; do
    name="${line%%=*}"
    value="${line#*=}"
    case "$name" in
      AIBOX* | PROCESSKIT* | PK_* | MCP* | CODEX* | CLAUDE* | OPENAI* | \
        ANTHROPIC* | DEEPSEEK* | GEMINI* | GOOGLE*)
        case "$name" in
          *KEY* | *TOKEN* | *SECRET* | *PASSWORD* | *CREDENTIAL*)
            printf '%s=<redacted>\n' "$name" >>"$output"
            ;;
          *)
            printf '%s=%s\n' "$name" "$value" >>"$output"
            ;;
        esac
        ;;
    esac
  done < <(env | LC_ALL=C sort)
}

{
  printf '# aibox host doctor diagnostic\n\n'
  printf 'generated_at_local=%s\n' "$(date '+%Y-%m-%dT%H:%M:%S%z')"
  printf 'generated_at_utc=%s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  printf 'script=%s\n' "$0"
  printf 'script_dir=%s\n' "$script_dir"
  printf 'repo_root=%s\n' "$repo_root"
  printf 'invocation_dir=%s\n' "$invocation_dir"
  printf 'user=%s\n' "${USER:-unknown}"
  printf 'shell=%s\n' "${SHELL:-unknown}"
  printf 'path=%s\n' "${PATH:-}"
} >"$output"

if command -v hostname >/dev/null 2>&1; then
  printf 'hostname=%s\n' "$(hostname)" >>"$output"
fi

if command -v aibox >/dev/null 2>&1; then
  printf 'aibox_path=%s\n' "$(command -v aibox)" >>"$output"
else
  printf 'aibox_path=<not found>\n' >>"$output"
fi

write_selected_env

run_section "platform: uname" uname -a

if command -v git >/dev/null 2>&1; then
  run_section "git: rev-parse" git rev-parse --show-toplevel
  run_section "git: status short" git status --short
else
  printf '\n## git\n\nnot found on PATH\n' >>"$output"
fi

run_section "project files: expected host config presence" \
  find "$repo_root" -maxdepth 2 \
  \( -name AGENTS.md -o -name .mcp.json -o -name aibox.toml \
  -o -name aibox.yaml -o -name .aibox -o -name .agents \
  -o -name .codex -o -name .claude -o -name .cursor \) \
  -print

if command -v aibox >/dev/null 2>&1; then
  run_section "aibox: version" aibox --version
  run_section "aibox: help" aibox --help
  run_section "aibox doctor: help" aibox doctor --help

  run_section "aibox doctor" aibox doctor
  doctor_rc="$LAST_RC"

  run_section "aibox doctor: integrity table" aibox doctor --integrity
  run_section "aibox doctor: integrity json" aibox doctor --integrity -o json
  run_section "aibox doctor: integrity yaml" aibox doctor --integrity -o yaml
else
  doctor_rc=127
  {
    printf '\n## aibox\n\n'
    printf 'aibox was not found on PATH, so aibox doctor could not be run.\n'
  } >>"$output"
fi

{
  printf '\n## summary\n\n'
  printf 'report=%s\n' "$output"
  printf 'aibox_doctor_exit_code=%s\n' "$doctor_rc"
} >>"$output"

printf 'wrote %s\n' "$output"
exit "$doctor_rc"
