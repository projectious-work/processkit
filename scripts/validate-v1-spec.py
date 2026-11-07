#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "jsonschema>=4.0",
#   "pyyaml>=6.0",
# ]
# ///

"""Validate the processkit v1 specifications' executable contracts.

Specifications follow the company layout standard (`spec/<slug>/v<N>/`).
Layout, SPEC.toml, freeze, and CHANGES.md rules are checked by
`python3 .standards/standards.py check-specs`; this script checks the
processkit-specific contracts: the roadmap, requirement IDs, interface
catalogs, and local links.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "docs/roadmap.schema.json"
ROADMAP_PATH = ROOT / "roadmap.yaml"
SPEC_ROOT = ROOT / "spec"
DOC_ROOT = ROOT / "docs/v1"
INVALID_ROADMAP_ROOT = ROOT / "tests/roadmap"
REQUIREMENT_RE = re.compile(r"\*\*(PK-[A-Z]+-[0-9]{3}):\*\*")
CITED_RE = re.compile(r"\b(PK-[A-Z]+-[0-9]{3})\b")
MARKDOWN_LINK_RE = re.compile(r"\[[^]]+\]\(([^)]+)\)")
SPEC_REF_RE = re.compile(r"^([a-z0-9]+(?:-[a-z0-9]+)*)@v([1-9][0-9]*)$")


def validate_roadmap(
    roadmap: dict[str, object],
    validator: jsonschema.Draft202012Validator,
    *,
    check_paths: bool,
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

    if not check_paths:
        return
    for item in items:
        if item["status"] == "released" or "devNote" in item:
            note = ROOT / item["devNote"]
            if not note.is_file():
                raise ValueError(
                    f"{item['id']} references absent development note: "
                    f"{note}"
                )
        for ref in item.get("specs", []):
            match = SPEC_REF_RE.match(ref)
            version_dir = SPEC_ROOT / match[1] / f"v{match[2]}"
            if not (version_dir / "SPEC.toml").is_file():
                raise ValueError(
                    f"{item['id']} references absent specification: {ref}"
                )


def check_links(document: Path) -> None:
    text = document.read_text(encoding="utf-8")
    for target in MARKDOWN_LINK_RE.findall(text):
        if "://" in target or target.startswith(("#", "mailto:")):
            continue
        path_part = target.split("#", 1)[0]
        if path_part and not (document.parent / path_part).resolve().exists():
            raise ValueError(
                f"broken local link in {document.relative_to(ROOT)}: {target}"
            )


def known_requirement_ids() -> set[str]:
    """IDs defined by any specification or kept in v1 documentation."""
    known: set[str] = set()
    for requirements in SPEC_ROOT.glob("*/v*/requirements.md"):
        known.update(REQUIREMENT_RE.findall(requirements.read_text("utf-8")))
    for document in DOC_ROOT.glob("*.md"):
        known.update(REQUIREMENT_RE.findall(document.read_text("utf-8")))
        known.update(
            re.findall(
                r"^- `(PK-[A-Z]+-[0-9]{3})`",
                document.read_text("utf-8"),
                re.M,
            )
        )
    return known


def check_specifications() -> int:
    """Return the number of requirement IDs in the latest versions."""
    known = known_requirement_ids()
    owners: dict[str, str] = {}
    latest_total = 0
    for slug_dir in sorted(p for p in SPEC_ROOT.iterdir() if p.is_dir()):
        versions = sorted(
            (
                p
                for p in slug_dir.iterdir()
                if re.fullmatch(r"v[1-9]\d*", p.name)
            ),
            key=lambda p: int(p.name[1:]),
        )
        for version_dir in versions:
            requirements = version_dir / "requirements.md"
            text = requirements.read_text(encoding="utf-8")
            defined = REQUIREMENT_RE.findall(text)
            repeated = sorted({i for i in defined if defined.count(i) > 1})
            if repeated:
                raise ValueError(
                    f"{requirements.relative_to(ROOT)} defines IDs twice: "
                    f"{repeated}"
                )
            for requirement_id in defined:
                owner = owners.setdefault(requirement_id, slug_dir.name)
                if owner != slug_dir.name:
                    raise ValueError(
                        f"{requirement_id} is defined by both {owner} and "
                        f"{slug_dir.name}"
                    )

            catalog = yaml.safe_load(
                (version_dir / "interfaces.yaml").read_text(encoding="utf-8")
            )
            if (catalog.get("slug"), catalog.get("version")) != (
                slug_dir.name, int(version_dir.name[1:])
            ):
                raise ValueError(
                    f"{version_dir.relative_to(ROOT)}/interfaces.yaml: "
                    "slug/version do not match the directory"
                )
            unknown = sorted(
                set(CITED_RE.findall(json.dumps(catalog))) - known
            )
            if unknown:
                raise ValueError(
                    f"{version_dir.relative_to(ROOT)}/interfaces.yaml cites "
                    f"unknown requirements: {unknown}"
                )
            for schema_path in sorted(version_dir.glob("schemas/*.json")):
                jsonschema.Draft202012Validator.check_schema(
                    json.loads(schema_path.read_text(encoding="utf-8"))
                )
            for document in sorted(version_dir.glob("*.md")):
                check_links(document)
        if versions:
            latest_total += len(
                REQUIREMENT_RE.findall(
                    (versions[-1] / "requirements.md").read_text(
                        encoding="utf-8"
                    )
                )
            )
    return latest_total


def main() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    roadmap = yaml.safe_load(ROADMAP_PATH.read_text(encoding="utf-8"))

    jsonschema.Draft202012Validator.check_schema(schema)
    validator = jsonschema.Draft202012Validator(
        schema,
        format_checker=jsonschema.Draft202012Validator.FORMAT_CHECKER,
    )
    validate_roadmap(roadmap, validator, check_paths=True)

    for invalid_path in sorted(INVALID_ROADMAP_ROOT.glob("invalid-*.yaml")):
        invalid = yaml.safe_load(invalid_path.read_text(encoding="utf-8"))
        try:
            validate_roadmap(invalid, validator, check_paths=False)
        except (jsonschema.ValidationError, ValueError):
            continue
        raise ValueError(
            f"expected roadmap validation to fail: {invalid_path}"
        )

    total = check_specifications()
    for document in sorted(DOC_ROOT.glob("*.md")):
        check_links(document)

    if total < 100:
        raise ValueError(
            f"unexpectedly small normative requirement inventory: {total}"
        )

    print(
        "processkit v1 specification contracts are valid "
        f"({total} normative requirements)"
    )


if __name__ == "__main__":
    main()
