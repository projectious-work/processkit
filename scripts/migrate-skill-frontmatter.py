#!/usr/bin/env -S uv run --quiet
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "ruamel.yaml>=0.18",
# ]
# ///
"""Migrate processkit SKILL.md files from K8s-style frontmatter to Agent Skills standard.

Transformations:

  1. Frontmatter shape:
       OLD                                NEW
       apiVersion: ...               →    name: <skill-name>
       kind: Skill                        description: <spec.description + " " + spec.when_to_use>
       metadata:                          metadata:
         id: SKILL-...                      processkit:
         name: <skill-name>                   apiVersion: ...
         version: ...                         id: SKILL-...
         created: ...                         version: ...
       spec:                                  created: ...
         description: ...                     category: ...
         category: ...                        layer: ...
         layer: ...                           uses: [{skill, purpose}, ...]
         uses: [foo, bar]                     provides: ...
         provides: {...}
         when_to_use: ...

     - Top-level `name` lifts from metadata.name.
     - Top-level `description` concatenates spec.description + " " + spec.when_to_use.
     - `kind: Skill` is dropped (implied by location under src/skills/).
     - `uses:` flips from list-of-strings to list-of-objects with `skill` + `purpose`.
       Purposes are looked up from DEFAULT_PURPOSES; unknown deps get a TODO marker.
     - `when_to_use` is dropped from metadata (merged into description).

  2. Section headings in body:
       ## Level 1 — Intro          →   ## Intro
       ## Level 2 — Overview       →   ## Overview
       ## Level 3 — Full reference →   ## Full reference
       (any `## Level [123] — X`   →   ## X)

The script is idempotent: if a file's frontmatter already lacks top-level
apiVersion (i.e., it's already migrated), the script skips it.

Usage:
    scripts/migrate-skill-frontmatter.py [--dry-run] [--only <skill-name>]

In --dry-run mode, prints the planned transformation but writes nothing.
With --only, processes a single skill (useful for spot-checks).
"""
from __future__ import annotations

import argparse
import io
import re
import sys
from pathlib import Path

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString


# ---------------------------------------------------------------------------
# uses: → list-of-objects mapping. Generic purposes per dependency, suitable
# for any consuming skill. Skill-builder/skill-reviewer can refine these later.
# ---------------------------------------------------------------------------
DEFAULT_PURPOSES: dict[str, str] = {
    "event-log": "Log events to keep the audit trail accurate after every write.",
    "index-management": "Query existing entities and keep the SQLite index fresh after writes.",
    "id-management": "Allocate unique entity identifiers via central ID generation.",
    "actor-profile": "Resolve and validate Actor IDs referenced by this skill's entities.",
    "decision-record": "Record consequential decisions made during this skill's workflow.",
    "context-archiving": "Archive long-form context once it is no longer active.",
    "workitem-management": "Delegate WorkItem creation and state-machine handling.",
    "discussion-management": "Open structured multi-turn discussions when this skill needs to capture pre-decisional reasoning.",
    "scope-management": "Resolve and apply Scope identifiers when entities need scoping.",
    "role-management": "Resolve Role IDs when entities need role-based assignment.",
    "binding-management": "Express scoped or temporal relationships between entities (vs. simple cross-references).",
    "gate-management": "Evaluate gate conditions before allowing transitions.",
}


def purpose_for(parent_skill: str, dep: str) -> str:
    return DEFAULT_PURPOSES.get(
        dep,
        f"TODO: explain why {parent_skill} uses {dep}.",
    )


# ---------------------------------------------------------------------------
# Frontmatter splitting
# ---------------------------------------------------------------------------
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def split_frontmatter(text: str) -> tuple[str | None, str]:
    """Return (yaml_text, body_text). If no frontmatter, yaml_text is None."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, text
    return m.group(1), text[m.end() :]


# ---------------------------------------------------------------------------
# Section heading rename
# ---------------------------------------------------------------------------
LEVEL_HEADING_RE = re.compile(r"^## Level [123] — (.+)$", re.MULTILINE)


def rename_level_headings(body: str) -> str:
    return LEVEL_HEADING_RE.sub(r"## \1", body)


# ---------------------------------------------------------------------------
# Frontmatter migration
# ---------------------------------------------------------------------------
def is_old_format(fm: dict) -> bool:
    return "apiVersion" in fm and "spec" in fm and "metadata" in fm


def migrate_frontmatter(fm: dict, skill_name: str) -> dict:
    """Build the new flat frontmatter from the old K8s-style one."""
    metadata = fm.get("metadata", {}) or {}
    spec = fm.get("spec", {}) or {}

    # name lifts from metadata.name (must match directory name)
    name = metadata.get("name") or skill_name

    # description = spec.description + " " + spec.when_to_use (if both exist)
    description_what = (spec.get("description") or "").strip()
    description_when = (spec.get("when_to_use") or "").strip()
    if description_what and description_when:
        description = f"{description_what} {description_when}"
    elif description_what:
        description = description_what
    elif description_when:
        description = description_when
    else:
        description = f"TODO: write a description for {name}"

    # Length sanity check (Anthropic limit: 1024 chars)
    if len(description) > 1024:
        print(
            f"WARNING: {skill_name} description is {len(description)} chars (> 1024 limit)",
            file=sys.stderr,
        )

    # Use a literal block scalar for descriptions longer than ~80 chars so
    # the diff stays readable.
    if len(description) > 80:
        description_value: object = LiteralScalarString(description + "\n")
    else:
        description_value = description

    # processkit metadata sub-block — all the K8s-style fields land here
    processkit_meta: dict = {
        "apiVersion": fm.get("apiVersion"),
        "id": metadata.get("id"),
        "version": metadata.get("version"),
        "created": metadata.get("created"),
    }
    if "category" in spec:
        processkit_meta["category"] = spec["category"]
    if "layer" in spec:
        processkit_meta["layer"] = spec["layer"]

    # uses: list-of-strings → list-of-objects
    if "uses" in spec and spec["uses"] is not None:
        uses_list = spec["uses"]
        new_uses = []
        for entry in uses_list:
            if isinstance(entry, str):
                new_uses.append(
                    {"skill": entry, "purpose": purpose_for(skill_name, entry)}
                )
            elif isinstance(entry, dict):
                # Already in new shape — preserve
                new_uses.append(entry)
            else:
                print(
                    f"WARNING: {skill_name} has unknown uses entry: {entry!r}",
                    file=sys.stderr,
                )
        processkit_meta["uses"] = new_uses

    # provides: preserve as-is under processkit metadata
    if "provides" in spec and spec["provides"] is not None:
        processkit_meta["provides"] = spec["provides"]

    # replaces: rare; preserve under processkit metadata
    if "replaces" in spec:
        processkit_meta["replaces"] = spec["replaces"]

    # Drop None values to keep the frontmatter clean
    processkit_meta = {k: v for k, v in processkit_meta.items() if v is not None}

    new_fm: dict = {
        "name": name,
        "description": description_value,
        "metadata": {"processkit": processkit_meta},
    }
    return new_fm


# ---------------------------------------------------------------------------
# YAML round-trip
# ---------------------------------------------------------------------------
def make_yaml() -> YAML:
    y = YAML()
    y.preserve_quotes = True
    y.width = 100
    y.indent(mapping=2, sequence=4, offset=2)
    return y


def dump_frontmatter(new_fm: dict, yaml: YAML) -> str:
    buf = io.StringIO()
    yaml.dump(new_fm, buf)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Per-file driver
# ---------------------------------------------------------------------------
def migrate_file(path: Path, dry_run: bool, yaml: YAML) -> str:
    """Returns one of: 'migrated', 'skipped-already-new', 'skipped-no-frontmatter', 'error'."""
    text = path.read_text()
    yaml_text, body = split_frontmatter(text)
    if yaml_text is None:
        return "skipped-no-frontmatter"

    fm = yaml.load(yaml_text)
    if fm is None or not isinstance(fm, dict):
        return "error"

    if not is_old_format(fm):
        return "skipped-already-new"

    skill_name = path.parent.name
    new_fm = migrate_frontmatter(fm, skill_name)
    new_body = rename_level_headings(body)

    new_fm_text = dump_frontmatter(new_fm, yaml)
    new_text = f"---\n{new_fm_text}---\n{new_body}"

    if dry_run:
        print(f"--- {path} (dry-run) ---")
        print(new_text[:1500])
        if len(new_text) > 1500:
            print(f"... [{len(new_text) - 1500} more chars]")
        print()
    else:
        path.write_text(new_text)

    return "migrated"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Print transformations, don't write")
    parser.add_argument("--only", help="Process only the named skill (e.g. 'code-review')")
    parser.add_argument(
        "--root",
        default="src/skills",
        help="Root directory of skills (default: src/skills)",
    )
    args = parser.parse_args()

    root = Path(args.root)
    if not root.is_dir():
        print(f"ERROR: {root} is not a directory", file=sys.stderr)
        return 2

    yaml = make_yaml()

    files: list[Path] = []
    if args.only:
        candidate = root / args.only / "SKILL.md"
        if not candidate.is_file():
            print(f"ERROR: {candidate} not found", file=sys.stderr)
            return 2
        files = [candidate]
    else:
        for skill_dir in sorted(root.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if skill_md.is_file():
                files.append(skill_md)

    counts = {"migrated": 0, "skipped-already-new": 0, "skipped-no-frontmatter": 0, "error": 0}
    for f in files:
        result = migrate_file(f, args.dry_run, yaml)
        counts[result] += 1
        if result == "error":
            print(f"ERROR: failed to parse {f}", file=sys.stderr)

    print(
        f"\nResult: {counts['migrated']} migrated, "
        f"{counts['skipped-already-new']} already-new, "
        f"{counts['skipped-no-frontmatter']} no-frontmatter, "
        f"{counts['error']} errors "
        f"({'dry-run' if args.dry_run else 'applied'})"
    )
    return 0 if counts["error"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
