#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "jsonschema>=4.0",
#   "pyyaml>=6.0",
# ]
# ///

"""Validate the processkit v1 specification's executable contracts."""

from __future__ import annotations

import json
import re
from pathlib import Path

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "spec/schemas/v1/roadmap.schema.json"
ROADMAP_PATH = ROOT / "spec/doc/v1/roadmap.yaml"
DOC_ROOT = ROOT / "spec/doc/v1"
REQUIREMENT_RE = re.compile(r"\b(PK-[A-Z]+-[0-9]{3})\b")
MARKDOWN_LINK_RE = re.compile(r"\[[^]]+\]\(([^)]+)\)")
INVALID_ROADMAP_ROOT = ROOT / "spec/tests/v1/roadmap"


def validate_roadmap(
    roadmap: dict[str, object],
    validator: jsonschema.Draft202012Validator,
    *,
    check_note_paths: bool,
) -> None:
    validator.validate(roadmap)

    groups = roadmap["groups"]
    group_ids = [group["id"] for group in groups]
    duplicate_groups = sorted(
        group_id
        for group_id in set(group_ids)
        if group_ids.count(group_id) > 1
    )
    if duplicate_groups:
        raise ValueError(f"duplicate roadmap group IDs: {duplicate_groups}")

    items = [item for group in groups for item in group["items"]]
    item_ids = [item["id"] for item in items]
    duplicates = sorted(
        item_id for item_id in set(item_ids) if item_ids.count(item_id) > 1
    )
    if duplicates:
        raise ValueError(f"duplicate roadmap IDs: {duplicates}")

    known = set(item_ids)
    broken = sorted(
        (item["id"], dependency)
        for item in items
        for dependency in item["dependencies"]
        if dependency not in known
    )
    if broken:
        raise ValueError(f"unknown roadmap dependencies: {broken}")

    dependencies = {
        item["id"]: set(item["dependencies"])
        for item in items
    }
    pending = set(known)
    while pending:
        ready = {
            item_id
            for item_id in pending
            if not (dependencies[item_id] & pending)
        }
        if not ready:
            raise ValueError(
                f"cyclic roadmap dependencies: {sorted(pending)}"
            )
        pending -= ready

    if check_note_paths:
        for item in items:
            if item["status"] == "shipped":
                note = ROOT / item["devNote"]
                if not note.is_file():
                    raise ValueError(
                        f"{item['id']} references absent development note: "
                        f"{note}"
                    )


def main() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    roadmap = yaml.safe_load(ROADMAP_PATH.read_text(encoding="utf-8"))

    jsonschema.Draft202012Validator.check_schema(schema)
    validator = jsonschema.Draft202012Validator(
        schema,
        format_checker=jsonschema.Draft202012Validator.FORMAT_CHECKER,
    )
    validate_roadmap(roadmap, validator, check_note_paths=True)

    for invalid_path in sorted(INVALID_ROADMAP_ROOT.glob("invalid-*.yaml")):
        invalid = yaml.safe_load(invalid_path.read_text(encoding="utf-8"))
        try:
            validate_roadmap(invalid, validator, check_note_paths=False)
        except (jsonschema.ValidationError, ValueError):
            continue
        raise ValueError(
            f"expected roadmap validation to fail: {invalid_path}"
        )

    requirement_sources: dict[str, list[str]] = {}
    for document in sorted(DOC_ROOT.glob("*.md")):
        text = document.read_text(encoding="utf-8")
        for requirement_id in REQUIREMENT_RE.findall(text):
            requirement_sources.setdefault(requirement_id, []).append(
                document.name
            )

        for target in MARKDOWN_LINK_RE.findall(text):
            if "://" in target or target.startswith("#"):
                continue
            path_part = target.split("#", 1)[0]
            linked_path = (document.parent / path_part).resolve()
            if path_part and not linked_path.exists():
                raise ValueError(
                    f"broken local link in {document.name}: {target}"
                )

    duplicates = {
        requirement_id: sources
        for requirement_id, sources in requirement_sources.items()
        if len(sources) > 1
    }
    if duplicates:
        raise ValueError(f"duplicate normative requirement IDs: {duplicates}")

    if len(requirement_sources) < 100:
        raise ValueError(
            "unexpectedly small normative requirement inventory: "
            f"{len(requirement_sources)}"
        )

    print(
        "processkit v1 specification contracts are valid "
        f"({len(requirement_sources)} normative requirements)"
    )


if __name__ == "__main__":
    main()
