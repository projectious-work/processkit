#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DIST_DIR="$PROJECT_ROOT/dist"
EVIDENCE_ROOT="$DIST_DIR/release-evidence"
GITHUB_REPO="${PROCESSKIT_GITHUB_REPO:-projectious-work/processkit}"

die() {
    echo "error: $*" >&2
    exit 1
}

info() {
    echo "==> $*"
}

usage() {
    cat <<'EOF'
Usage:
  scripts/maintain.sh test
  scripts/maintain.sh docs-deploy
  scripts/maintain.sh release-branch <version>
  scripts/maintain.sh release-check-state <version>
  scripts/maintain.sh release-doctors <version>
  scripts/maintain.sh release <version> [--steps <list>] [--list-steps]
  scripts/maintain.sh release-host <version>

Release step aliases:
  phase0   state,doctors
  checks   audit,test,docs
  build    build
  publish  publish
  verify   verify
  all      state,doctors,audit,test,docs,build,publish,verify
EOF
}

normalize_version() {
    local version="$1"
    [[ "$version" == v* ]] || version="v$version"
    [[ "$version" =~ ^v[0-9]+\.[0-9]+\.[0-9]+(-[0-9A-Za-z.-]+)?$ ]] ||
        die "invalid semantic version: $1"
    printf '%s\n' "$version"
}

release_branch_for() {
    local version
    version="$(normalize_version "$1")"
    case "$version" in
        v0.*-*) die "v0 prerelease branch policy is not defined" ;;
        v0.*) printf '%s\n' "v0.x-release" ;;
        v1.*-*) printf '%s\n' "v1.x-pre-release" ;;
        v1.*) printf '%s\n' "v1.x-release" ;;
        *) die "no release branch mapping for $version" ;;
    esac
}

candidate_sha() {
    git -C "$PROJECT_ROOT" rev-parse HEAD
}

evidence_dir() {
    local version="$1"
    printf '%s/%s/%s\n' "$EVIDENCE_ROOT" "$version" "$(candidate_sha)"
}

require_clean_candidate() {
    [[ -z "$(git -C "$PROJECT_ROOT" status --porcelain)" ]] ||
        die "release candidate worktree is dirty"
}

require_release_branch() {
    local version="$1" expected current
    expected="$(release_branch_for "$version")"
    current="$(git -C "$PROJECT_ROOT" branch --show-current)"
    [[ "$current" == "$expected" ]] ||
        die "$version must be released from $expected, not $current"
}

write_binding() {
    local version="$1" dir="$2" branch rustc_version python_version uv_version
    branch="$(git -C "$PROJECT_ROOT" branch --show-current)"
    rustc_version="$(rustc --version 2>/dev/null || echo unavailable)"
    python_version="$(python3 --version 2>&1 || echo unavailable)"
    uv_version="$(uv --version 2>&1 || echo unavailable)"
    mkdir -p "$dir/logs"
    jq -n --sort-keys \
        --arg version "$version" \
        --arg commit "$(candidate_sha)" \
        --arg branch "$branch" \
        --arg tree_state "clean" \
        --arg rustc "$rustc_version" \
        --arg python "$python_version" \
        --arg uv "$uv_version" \
        --arg host "$(rustc -vV 2>/dev/null |
            awk '/^host:/ {print $2}' || true)" \
        '{
          version: $version,
          commit: $commit,
          branch: $branch,
          treeState: $tree_state,
          toolchain: {rustc: $rustc, python: $python, uv: $uv},
          environment: {host: $host}
        }' >"$dir/binding.json"
}

ensure_binding() {
    local version="$1" dir
    require_clean_candidate
    dir="$(evidence_dir "$version")"
    if [[ ! -f "$dir/binding.json" ]]; then
        write_binding "$version" "$dir"
    fi
    jq -e \
        --arg version "$version" \
        --arg commit "$(candidate_sha)" \
        '.version == $version and .commit == $commit
         and .treeState == "clean"' \
        "$dir/binding.json" >/dev/null ||
        die "candidate evidence binding does not match"
    printf '%s\n' "$dir"
}

step_passed() {
    local dir="$1" step="$2"
    [[ -f "$dir/$step.passed" ]]
}

mark_passed() {
    local dir="$1" step="$2"
    date -u +'%Y-%m-%dT%H:%M:%SZ' >"$dir/$step.passed"
}

cmd_release_check_state() {
    local version dir report
    version="$(normalize_version "$1")"
    require_release_branch "$version"
    dir="$(ensure_binding "$version")"
    report="$dir/RELEASE-STATE.md"
    {
        echo "# Release state — $version"
        echo
        echo "- Candidate commit: \`$(candidate_sha)\`"
        echo "- Branch: \`$(git -C "$PROJECT_ROOT" branch --show-current)\`"
        echo "- Required branch: \`$(release_branch_for "$version")\`"
        echo "- Rust: \`$(rustc --version 2>/dev/null || echo unavailable)\`"
        echo "- Python: \`$(python3 --version 2>&1 || echo unavailable)\`"
        echo "- uv: \`$(uv --version 2>&1 || echo unavailable)\`"
        echo "- Cargo lock: \`$(sha256sum "$PROJECT_ROOT/installer/Cargo.lock" |
            awk '{print $1}')\`"
        echo "- MCP manifest: \`$(jq -r '.aggregate_sha256' \
            "$PROJECT_ROOT/src/context/.processkit-mcp-manifest.json")\`"
        echo "- Tracked release notes: \`release-notes/$version.md\`"
    } >"$report"
    cp "$report" "$DIST_DIR/RELEASE-STATE.md"
    mark_passed "$dir" state
    echo "$report"
}

cmd_release_doctors() {
    local version dir report log status=0
    version="$(normalize_version "$1")"
    require_release_branch "$version"
    dir="$(ensure_binding "$version")"
    report="$dir/RELEASE-DOCTORS.md"
    log="$dir/logs/doctors.log"
    {
        echo "# Release doctors — $version"
        echo
        echo '```text'
        uv run \
            "$PROJECT_ROOT/context/skills/processkit/pk-doctor/scripts/doctor.py" \
            --no-log || status=$?
        echo
        uv run \
            "$PROJECT_ROOT/context/skills/processkit/release-audit/scripts/release_audit.py" \
            --repo-root="$PROJECT_ROOT" --tree=both || status=$?
        echo '```'
    } >"$report" 2>"$log"
    cp "$report" "$DIST_DIR/RELEASE-DOCTORS.md"
    [[ "$status" -eq 0 ]] ||
        die "release doctors failed; see $report and $log"
    if grep -Eq '(^|[[:space:]])[1-9][0-9]* WARN|\\[W\\]|action_required' \
        "$report"; then
        [[ -s "$PROJECT_ROOT/release-deferrals/$version.md" ]] ||
            die "doctor warnings require tracked release-deferrals/$version.md"
    fi
    mark_passed "$dir" doctors
    echo "$report"
}

run_gate() {
    local dir="$1" name="$2"
    shift 2
    if step_passed "$dir" "$name"; then
        info "reusing candidate-bound evidence: $name"
        return
    fi
    info "running gate: $name"
    if "$@" >"$dir/logs/$name.log" 2>&1; then
        mark_passed "$dir" "$name"
    else
        die "$name failed; see $dir/logs/$name.log"
    fi
}

gate_audit() {
    uv run \
        "$PROJECT_ROOT/context/skills/processkit/release-audit/scripts/release_audit.py" \
        --repo-root="$PROJECT_ROOT" --tree=both
}

gate_test() {
    "$PROJECT_ROOT/scripts/test-installer-local.sh"
}

gate_docs() {
    local version="$1"
    [[ -s "$PROJECT_ROOT/release-notes/$version.md" ]] ||
        die "missing tracked release notes: release-notes/$version.md"
    for file in README.md CONTRIBUTING.md LICENSE SECURITY.md \
        CODE_OF_CONDUCT.md MAINTENANCE.md SUPPORT.md; do
        [[ -s "$PROJECT_ROOT/$file" ]] ||
            die "missing repository landing/support file: $file"
    done
    "$PROJECT_ROOT/scripts/check-docs-local.sh"
}

gate_build() {
    local version="$1" published_key
    [[ -n "${PROCESSKIT_RELEASE_PRIVATE_KEY:-}" ]] ||
        die "PROCESSKIT_RELEASE_PRIVATE_KEY is required"
    [[ -n "${PROCESSKIT_RELEASE_PUBLIC_KEY:-}" ]] ||
        die "PROCESSKIT_RELEASE_PUBLIC_KEY is required"
    "$PROJECT_ROOT/scripts/release-local.sh" "$version" \
        "$PROCESSKIT_RELEASE_PRIVATE_KEY" "$PROCESSKIT_RELEASE_PUBLIC_KEY"
    published_key="$PROJECT_ROOT/dist/processkit-$version-public.pem"
    cp "$PROCESSKIT_RELEASE_PUBLIC_KEY" "$published_key"
}

expand_steps() {
    local raw="$1" part result=()
    IFS=',' read -ra parts <<<"$raw"
    for part in "${parts[@]}"; do
        case "$part" in
            phase0) result+=(state doctors) ;;
            checks) result+=(audit test docs) ;;
            build) result+=(build) ;;
            publish) result+=(publish) ;;
            verify) result+=(verify) ;;
            all) result+=(state doctors audit test docs build publish verify) ;;
            state|doctors|audit|test|docs) result+=("$part") ;;
            *) die "unknown release step or alias: $part" ;;
        esac
    done
    printf '%s\n' "${result[@]}" | awk '!seen[$0]++'
}

publish_release() {
    local version="$1" dir="$2" notes prerelease=()
    require_release_branch "$version"
    for step in state doctors audit test docs build; do
        step_passed "$dir" "$step" ||
            die "publication requires current $step evidence"
    done
    notes="$PROJECT_ROOT/release-notes/$version.md"
    git -C "$PROJECT_ROOT" rev-parse -q --verify "refs/tags/$version" \
        >/dev/null && die "tag already exists: $version"
    git -C "$PROJECT_ROOT" tag -a "$version" -m "processkit $version"
    git -C "$PROJECT_ROOT" push origin "$version"
    [[ "$version" == *-* ]] && prerelease=(--prerelease)
    gh release create "$version" \
        "$PROJECT_ROOT/LICENSE" \
        "$PROJECT_ROOT/dist/processkit-$version"* \
        --repo "$GITHUB_REPO" --verify-tag "${prerelease[@]}" \
        --title "processkit $version" --notes-file "$notes"
    "$PROJECT_ROOT/scripts/publish-docs-gh-pages.sh"
    mark_passed "$dir" publish
}

verify_public_release() {
    local version="$1" dir="$2" verify_dir envelope signature public_key
    step_passed "$dir" publish ||
        die "public verification requires publication evidence"
    verify_dir="$(mktemp -d)"
    gh release download "$version" --repo "$GITHUB_REPO" --dir "$verify_dir"
    (
        cd "$verify_dir"
        local checksum_file
        while IFS= read -r checksum_file; do
            sha256sum -c "$(basename "$checksum_file")"
        done < <(find . -maxdepth 1 -type f -name '*.sha256' -print | sort)
    ) >"$dir/verify-checksums.log" 2>&1
    envelope="$verify_dir/processkit-$version.release.json"
    signature="$verify_dir/processkit-$version.release.sig"
    public_key="$verify_dir/processkit-$version-public.pem"
    [[ -f "$envelope" && -f "$signature" && -f "$public_key" ]] ||
        die "downloaded signed release envelope is incomplete"
    "$PROJECT_ROOT/scripts/verify-release-local.sh" \
        "$envelope" "$signature" "$public_key" \
        >"$dir/verify-signature.log" 2>&1
    gh release view "$version" --repo "$GITHUB_REPO" \
        --json tagName,isDraft,isPrerelease,assets,url \
        >"$dir/public-release.json"
    git -C "$PROJECT_ROOT" ls-remote origin \
        "refs/tags/$version^{}" >"$dir/public-tag.txt"
    mark_passed "$dir" verify
}

cmd_release() {
    local version="$1"
    shift
    local selected="all" list_only=false dir step status=0
    local -a steps=() check_pids=()
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --steps) selected="${2:-}"; shift 2 ;;
            --list-steps) list_only=true; shift ;;
            *) die "unknown release option: $1" ;;
        esac
    done
    if "$list_only"; then
        expand_steps all
        return
    fi
    version="$(normalize_version "$version")"
    require_release_branch "$version"
    dir="$(ensure_binding "$version")"
    mapfile -t steps < <(expand_steps "$selected")

    for step in "${steps[@]}"; do
        case "$step" in
            state) cmd_release_check_state "$version" >/dev/null ;;
            doctors) cmd_release_doctors "$version" >/dev/null ;;
        esac
    done

    # Independent validation gates run with bounded concurrency of three and
    # retain separate logs. Mutating build/publication steps remain serial.
    for step in "${steps[@]}"; do
        case "$step" in
            audit) (run_gate "$dir" audit gate_audit) & check_pids+=("$!") ;;
            test) (run_gate "$dir" test gate_test) & check_pids+=("$!") ;;
            docs) (run_gate "$dir" docs gate_docs "$version") &
                check_pids+=("$!") ;;
        esac
    done
    for pid in "${check_pids[@]}"; do
        wait "$pid" || status=1
    done
    [[ "$status" -eq 0 ]] || die "one or more candidate checks failed"

    for step in "${steps[@]}"; do
        case "$step" in
            build) run_gate "$dir" build gate_build "$version" ;;
            publish) publish_release "$version" "$dir" ;;
            verify) verify_public_release "$version" "$dir" ;;
        esac
    done
}

cmd_test() {
    "$PROJECT_ROOT/scripts/check-docs-local.sh"
    "$PROJECT_ROOT/scripts/test-installer-local.sh"
}

command="${1:-help}"
shift || true
case "$command" in
    help|-h|--help) usage ;;
    test) cmd_test ;;
    docs-deploy) "$PROJECT_ROOT/scripts/publish-docs-gh-pages.sh" ;;
    release-branch) release_branch_for "${1:?version required}" ;;
    release-check-state)
        cmd_release_check_state "${1:?version required}" ;;
    release-doctors) cmd_release_doctors "${1:?version required}" ;;
    release)
        [[ $# -gt 0 ]] || die "version required"
        cmd_release "$@" ;;
    release-host)
        version="$(normalize_version "${1:?version required}")"
        require_release_branch "$version"
        die "host-only artifact production is not implemented; candidate remains incomplete"
        ;;
    *) die "unknown command: $command" ;;
esac
