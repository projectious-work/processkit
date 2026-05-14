#!/usr/bin/env bash
#
# processkit-diff.sh — generic diff between two processkit versions.
#
# Compares two tagged versions of processkit (or any fork) and prints a
# structured diff describing what changed: files added, removed, modified,
# plus a normalized affected_files list for Migration frontmatter.
# This is the consumer-facing entry point used by tools like aibox sync to
# generate Migration briefings.
#
# Usage:
#   scripts/processkit-diff.sh --from <tag> --to <tag> [--format <fmt>]
#
#   --from <tag>      The "old" version (e.g. v0.3.0). Required.
#   --to <tag>        The "new" version (e.g. v0.4.0). Required.
#   --format <fmt>    Output format: text (default) | toml | json
#   --src-path <p>    Subdirectory containing src/ (default: src)
#                     Use "" for repos that have no src/ wrapper.
#   --repo <path>     Path to the processkit checkout (default: current dir)
#
# Examples:
#
#   # Quick text diff between two upstream tags
#   scripts/processkit-diff.sh --from v0.3.0 --to v0.4.0
#
#   # Machine-readable TOML for tooling
#   scripts/processkit-diff.sh --from v0.3.0 --to v0.4.0 --format toml
#
#   # Diff between an ACME fork and upstream (run from a checkout that has both as remotes)
#   scripts/processkit-diff.sh --from upstream/v0.4.0 --to acme/v0.4.0-acme.1
#
# How it works:
#   1. Read PROVENANCE.toml at <to-tag> — gives the "new" file→version mapping
#   2. Read PROVENANCE.toml at <from-tag> — gives the "old" mapping
#   3. Compute set differences:
#        - added:    in new, not in old
#        - removed:  in old, not in new
#        - changed:  in both, but with a different version stamp
#                    (the version stamp changes when the file's content changed)
#        - unchanged: in both, same version stamp
#   4. Emit the diff in the requested format, including machine-readable
#      affected_files rows with Migration classifications
#
# This script is intentionally generic — it knows nothing about which fork
# you're running. The same script works for upstream processkit, ACME's
# fork, or any other downstream. The PROVENANCE.toml [source] block tells
# you which fork you're looking at; the [files] table tells you the
# version mapping.
#
# Exit codes:
#   0 — diff completed successfully
#   1 — usage error or missing arguments
#   2 — git error (e.g. tag not found, can't read PROVENANCE.toml at tag)

set -euo pipefail

REPO_PATH="."
SRC_PATH="src"
FROM_TAG=""
TO_TAG=""
FORMAT="text"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --from)         FROM_TAG="$2"; shift 2 ;;
        --to)           TO_TAG="$2"; shift 2 ;;
        --format)       FORMAT="$2"; shift 2 ;;
        --src-path)     SRC_PATH="$2"; shift 2 ;;
        --repo)         REPO_PATH="$2"; shift 2 ;;
        -h|--help)
            sed -n '3,40p' "$0" | sed 's/^# *//'
            exit 0
            ;;
        *)
            echo "Error: unknown argument '$1'" >&2
            echo "Run with --help for usage." >&2
            exit 1
            ;;
    esac
done

if [[ -z "$FROM_TAG" || -z "$TO_TAG" ]]; then
    echo "Error: --from and --to are required." >&2
    exit 1
fi

cd "$REPO_PATH"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "Error: '$REPO_PATH' is not a git repository." >&2
    exit 2
fi

# Read PROVENANCE.toml at a given tag. Output: lines of "path<TAB>version".
read_provenance_at_tag() {
    local tag="$1"
    local provenance_path
    if [[ -n "$SRC_PATH" ]]; then
        provenance_path="$SRC_PATH/PROVENANCE.toml"
    else
        provenance_path="PROVENANCE.toml"
    fi

    if ! git show "$tag:$provenance_path" >/dev/null 2>&1; then
        echo "Error: cannot read $provenance_path at tag $tag" >&2
        echo "       (does the tag exist? does PROVENANCE.toml exist at that tag?)" >&2
        return 2
    fi

    git show "$tag:$provenance_path" | awk '
        /^\[files\]/ { in_files = 1; next }
        /^\[/ { in_files = 0 }
        in_files && /^"/ {
            # Parse `"path" = "version"` lines without GNU awk-only
            # match(..., array), so this script works under mawk too.
            line = $0
            sub(/^[[:space:]]*"/, "", line)
            q = index(line, "\"")
            if (q <= 1) next
            path = substr(line, 1, q - 1)
            rest = substr(line, q + 1)
            sub(/^[[:space:]]*=[[:space:]]*"/, "", rest)
            q = index(rest, "\"")
            if (q <= 1) next
            version = substr(rest, 1, q - 1)
            if (path != "" && version != "") {
                printf "%s\t%s\n", path, version
            }
        }
    '
}

OLD_LIST=$(read_provenance_at_tag "$FROM_TAG") || exit 2
NEW_LIST=$(read_provenance_at_tag "$TO_TAG") || exit 2

# Build associative arrays in awk and emit the four sets.
# Output stable across runs by sorting at the end.
DIFF_OUTPUT=$(awk -v from="$FROM_TAG" -v to="$TO_TAG" '
    BEGIN { FS="\t" }
    NR == FNR {
        old[$1] = $2
        next
    }
    {
        new[$1] = $2
    }
    END {
        n_added = 0; n_removed = 0; n_changed = 0; n_unchanged = 0
        for (path in new) {
            if (!(path in old)) {
                added[++n_added] = path "\t" new[path]
            } else if (old[path] != new[path]) {
                changed[++n_changed] = path "\t" old[path] "\t" new[path]
            } else {
                n_unchanged++
            }
        }
        for (path in old) {
            if (!(path in new)) {
                removed[++n_removed] = path "\t" old[path]
            }
        }

        print "ADDED\t" n_added
        for (i = 1; i <= n_added; i++) print "ADDED\t" added[i]
        print "REMOVED\t" n_removed
        for (i = 1; i <= n_removed; i++) print "REMOVED\t" removed[i]
        print "CHANGED\t" n_changed
        for (i = 1; i <= n_changed; i++) print "CHANGED\t" changed[i]
        print "UNCHANGED\t" n_unchanged
    }
' <(echo "$OLD_LIST") <(echo "$NEW_LIST"))

cleanup_hints_py='
from __future__ import annotations

import json
import sys

diff_text = sys.argv[1]

SKILL_RENAMES = {
    "context/skills/processkit/morning-briefing":
        "context/skills/processkit/status-briefing",
    "context/skills/product/retrospective":
        "context/skills/product/sprint-retrospective",
}


def parse_diff(text: str):
    added, removed, changed = [], [], []
    n_unchanged = 0
    for line in text.splitlines():
        parts = line.split("\t")
        if parts[0] == "ADDED" and len(parts) == 3:
            added.append({"path": parts[1], "version": parts[2]})
        elif parts[0] == "REMOVED" and len(parts) == 3:
            removed.append({"path": parts[1], "version": parts[2]})
        elif parts[0] == "CHANGED" and len(parts) == 4:
            changed.append({
                "path": parts[1],
                "from_version": parts[2],
                "to_version": parts[3],
            })
        elif parts[0] == "UNCHANGED" and len(parts) == 2:
            n_unchanged = int(parts[1])
    return added, removed, changed, n_unchanged


def skill_dir(path: str) -> str | None:
    parts = path.split("/")
    if len(parts) < 4 or parts[0:2] != ["context", "skills"]:
        return None
    return "/".join(parts[:4])


def command_name(path: str) -> str | None:
    parts = path.split("/")
    if len(parts) == 6 and parts[4] == "commands" and path.endswith(".md"):
        return parts[5][:-3]
    return None


def generated_adapters(command: str) -> list[str]:
    return [
        f".agents/skills/{command}/",
        f".agents/skills/{command}.md",
        f".claude/commands/{command}.md",
        f".codex/commands/{command}.md",
        f".cursor/rules/{command}.mdc",
    ]


def cleanup_hints(removed: list[dict]) -> list[dict]:
    by_skill: dict[str, dict] = {}
    for item in removed:
        path = item["path"]
        sdir = skill_dir(path)
        if not sdir:
            continue
        entry = by_skill.setdefault(sdir, {
            "path": sdir,
            "classification": "removed-skill-files",
            "replacement_path": None,
            "remove_skill_directory": False,
            "removed_files": [],
            "removed_commands": [],
            "generated_adapters": [],
            "notes": "",
        })
        entry["removed_files"].append(path)
        if path == f"{sdir}/SKILL.md":
            entry["remove_skill_directory"] = True
        cmd = command_name(path)
        if cmd:
            entry["removed_commands"].append(cmd)
            entry["generated_adapters"].extend(generated_adapters(cmd))

    hints = []
    for sdir, entry in sorted(by_skill.items()):
        replacement = SKILL_RENAMES.get(sdir)
        if replacement:
            entry["classification"] = "renamed-skill"
            entry["replacement_path"] = replacement
            entry["remove_skill_directory"] = True
            entry["notes"] = (
                "Remove the old hot skill directory and generated adapters; "
                f"canonical replacement is {replacement}."
            )
        elif entry["remove_skill_directory"]:
            entry["classification"] = "removed-skill"
            entry["notes"] = (
                "Remove the old hot skill directory and generated adapters "
                "unless the downstream project intentionally forked it."
            )
        else:
            entry["notes"] = (
                "Remove the listed upstream-managed files and any generated "
                "adapters for removed command names; keep the skill directory "
                "when it still exists in the target template."
            )
        entry["removed_files"] = sorted(set(entry["removed_files"]))
        entry["removed_commands"] = sorted(set(entry["removed_commands"]))
        entry["generated_adapters"] = sorted(set(entry["generated_adapters"]))
        hints.append(entry)
    return hints


def affected_files(
    added: list[dict],
    removed: list[dict],
    changed: list[dict],
) -> list[dict]:
    rows: list[dict] = []
    for item in added:
        rows.append({
            "path": item["path"],
            "classification": "new-upstream",
            "to_version": item["version"],
        })
    for item in changed:
        rows.append({
            "path": item["path"],
            "classification": "changed-upstream-only",
            "from_version": item["from_version"],
            "to_version": item["to_version"],
        })
    for item in removed:
        rows.append({
            "path": item["path"],
            "classification": "removed-upstream",
            "from_version": item["version"],
        })
    return sorted(rows, key=lambda item: item["path"])


added, removed, changed, n_unchanged = parse_diff(diff_text)
print(json.dumps({
    "added": added,
    "removed": removed,
    "changed": changed,
    "n_unchanged": n_unchanged,
    "affected_files": affected_files(added, removed, changed),
    "cleanup_hints": cleanup_hints(removed),
}, indent=2))
'

cleanup_json() {
    python3 -c "$cleanup_hints_py" "$DIFF_OUTPUT"
}

# Emit in the requested format
emit_text() {
    local n_added n_removed n_changed n_unchanged
    n_added=$(echo "$DIFF_OUTPUT" | awk -F'\t' '$1=="ADDED" && NF==2 {print $2; exit}')
    n_removed=$(echo "$DIFF_OUTPUT" | awk -F'\t' '$1=="REMOVED" && NF==2 {print $2; exit}')
    n_changed=$(echo "$DIFF_OUTPUT" | awk -F'\t' '$1=="CHANGED" && NF==2 {print $2; exit}')
    n_unchanged=$(echo "$DIFF_OUTPUT" | awk -F'\t' '$1=="UNCHANGED" && NF==2 {print $2; exit}')

    cat <<EOF
processkit diff
  from: $FROM_TAG
  to:   $TO_TAG

Summary:
  added:     $n_added
  removed:   $n_removed
  changed:   $n_changed
  unchanged: $n_unchanged

EOF

    echo "Added files:"
    echo "$DIFF_OUTPUT" | awk -F'\t' '$1=="ADDED" && NF==3 {print "  + " $2 "  (first appears in " $3 ")"}' | sort
    echo
    echo "Removed files:"
    echo "$DIFF_OUTPUT" | awk -F'\t' '$1=="REMOVED" && NF==3 {print "  - " $2 "  (last in " $3 ")"}' | sort
    echo
    echo "Changed files:"
    echo "$DIFF_OUTPUT" | awk -F'\t' '$1=="CHANGED" && NF==4 {print "  M " $2 "  (" $3 " → " $4 ")"}' | sort

    local cleanup
    cleanup=$(cleanup_json)
    if echo "$cleanup" | python3 -c 'import json,sys; sys.exit(0 if json.load(sys.stdin)["cleanup_hints"] else 1)' >/dev/null; then
        echo
        echo "Cleanup hints:"
        echo "$cleanup" | python3 -c '
import json, sys
for item in json.load(sys.stdin)["cleanup_hints"]:
    repl = item.get("replacement_path") or "none"
    print("  - {} [{}] replacement: {}".format(
        item["path"], item["classification"], repl
    ))
    for adapter in item.get("generated_adapters", []):
        print("      remove generated adapter: {}".format(adapter))
'
    fi
}

emit_toml() {
    local n_added n_removed n_changed n_unchanged
    n_added=$(echo "$DIFF_OUTPUT" | awk -F'\t' '$1=="ADDED" && NF==2 {print $2; exit}')
    n_removed=$(echo "$DIFF_OUTPUT" | awk -F'\t' '$1=="REMOVED" && NF==2 {print $2; exit}')
    n_changed=$(echo "$DIFF_OUTPUT" | awk -F'\t' '$1=="CHANGED" && NF==2 {print $2; exit}')
    n_unchanged=$(echo "$DIFF_OUTPUT" | awk -F'\t' '$1=="UNCHANGED" && NF==2 {print $2; exit}')

    cat <<EOF
# processkit diff between $FROM_TAG and $TO_TAG

[diff]
from = "$FROM_TAG"
to = "$TO_TAG"
n_added = $n_added
n_removed = $n_removed
n_changed = $n_changed
n_unchanged = $n_unchanged

[diff.added]
EOF
    echo "$DIFF_OUTPUT" | awk -F'\t' '$1=="ADDED" && NF==3 {printf "\"%s\" = \"%s\"\n", $2, $3}' | sort
    echo
    echo "[diff.removed]"
    echo "$DIFF_OUTPUT" | awk -F'\t' '$1=="REMOVED" && NF==3 {printf "\"%s\" = \"%s\"\n", $2, $3}' | sort
    echo
    echo "[diff.changed]"
    echo "$DIFF_OUTPUT" | awk -F'\t' '$1=="CHANGED" && NF==4 {printf "\"%s\" = { from = \"%s\", to = \"%s\" }\n", $2, $3, $4}' | sort

    cleanup_json | python3 -c '
import json, sys
payload = json.load(sys.stdin)
for item in payload["affected_files"]:
    print()
    print("[[diff.affected_files]]")
    print(("path = {!r}").format(item["path"]).replace(chr(39), "\""))
    print(("classification = {!r}").format(item["classification"]).replace(chr(39), "\""))
    if item.get("from_version"):
        print(("from_version = {!r}").format(item["from_version"]).replace(chr(39), "\""))
    if item.get("to_version"):
        print(("to_version = {!r}").format(item["to_version"]).replace(chr(39), "\""))
for item in payload["cleanup_hints"]:
    print()
    print("[[diff.cleanup_hints]]")
    print(("path = {!r}").format(item["path"]).replace(chr(39), "\""))
    print(("classification = {!r}").format(item["classification"]).replace(chr(39), "\""))
    print(("remove_skill_directory = {}").format(str(item["remove_skill_directory"]).lower()))
    if item.get("replacement_path"):
        print(("replacement_path = {!r}").format(item["replacement_path"]).replace(chr(39), "\""))
    print("removed_files = [" + ", ".join(repr(x).replace(chr(39), "\"") for x in item["removed_files"]) + "]")
    print("removed_commands = [" + ", ".join(repr(x).replace(chr(39), "\"") for x in item["removed_commands"]) + "]")
    print("generated_adapters = [" + ", ".join(repr(x).replace(chr(39), "\"") for x in item["generated_adapters"]) + "]")
    print(("notes = {!r}").format(item["notes"]).replace(chr(39), "\""))
'
}

emit_json() {
    # Compact JSON for tooling. Uses python -c (universally available) for safe escaping.
    local cleanup
    cleanup=$(cleanup_json)
    python3 - <<'PYEOF' "$DIFF_OUTPUT" "$FROM_TAG" "$TO_TAG" "$cleanup"
import json, sys
diff_text = sys.argv[1]
from_tag = sys.argv[2]
to_tag = sys.argv[3]
cleanup_payload = json.loads(sys.argv[4])
added = []
removed = []
changed = []
n_unchanged = 0
for line in diff_text.splitlines():
    parts = line.split("\t")
    if parts[0] == "ADDED" and len(parts) == 3:
        added.append({"path": parts[1], "version": parts[2]})
    elif parts[0] == "REMOVED" and len(parts) == 3:
        removed.append({"path": parts[1], "version": parts[2]})
    elif parts[0] == "CHANGED" and len(parts) == 4:
        changed.append({"path": parts[1], "from_version": parts[2], "to_version": parts[3]})
    elif parts[0] == "UNCHANGED" and len(parts) == 2:
        n_unchanged = int(parts[1])
out = {
    "diff": {
        "from": from_tag,
        "to": to_tag,
        "n_added": len(added),
        "n_removed": len(removed),
        "n_changed": len(changed),
        "n_unchanged": n_unchanged,
        "added": sorted(added, key=lambda x: x["path"]),
        "removed": sorted(removed, key=lambda x: x["path"]),
        "changed": sorted(changed, key=lambda x: x["path"]),
        "affected_files": cleanup_payload["affected_files"],
        "cleanup_hints": cleanup_payload["cleanup_hints"],
    }
}
print(json.dumps(out, indent=2))
PYEOF
}

case "$FORMAT" in
    text) emit_text ;;
    toml) emit_toml ;;
    json) emit_json ;;
    *)
        echo "Error: unknown format '$FORMAT' (use text, toml, or json)" >&2
        exit 1
        ;;
esac
