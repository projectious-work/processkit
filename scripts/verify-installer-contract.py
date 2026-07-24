#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6.0", "jsonschema>=4.0"]
# ///
"""Validate the release-owned installer contract without mutating it."""

from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import sys

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = Path(".processkit/installer")
REQUIRED = (
    "distribution.yaml", "release-descriptor.json", "operations.yaml",
    "ownership-matrix.yaml", "catalogs/mcp.yaml", "adapters/codex.yaml",
    "adapters/claude.yaml",
)
SCHEMAS = (
    "distribution", "release-descriptor", "installer-request",
    "installer-result", "mcp-catalog", "harness-adapter",
    "installation-state", "compatibility", "variables",
)


def _safe_relative(value: str) -> bool:
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def validate(release_root: Path) -> list[str]:
    base = release_root / CONTRACT
    failures = [f"missing installer contract: {name}" for name in REQUIRED
                if not (base / name).is_file()]
    failures.extend(
        f"missing installer schema: {name}" for name in SCHEMAS
        if not (base / "schemas" / f"{name}.schema.json").is_file()
    )
    if failures:
        return failures
    try:
        distribution = yaml.safe_load((base / "distribution.yaml").read_text())
        descriptor = json.loads((base / "release-descriptor.json").read_text())
        schema = json.loads((base / "schemas/distribution.schema.json").read_text())
        descriptor_schema = json.loads(
            (base / "schemas/release-descriptor.schema.json").read_text()
        )
        jsonschema.validate(distribution, schema)
        jsonschema.validate(descriptor, descriptor_schema)
    except (OSError, ValueError, yaml.YAMLError, jsonschema.ValidationError) as exc:
        return [f"invalid installer contract: {exc}"]

    spec = distribution["spec"]
    operations = yaml.safe_load((base / "operations.yaml").read_text())
    available = set(operations.get("operations", {}))
    component_ids: set[str] = set()
    destinations: set[str] = set()
    for component in spec["components"]:
        ident = component.get("id")
        destination = component.get("destination", "")
        operation = component.get("operation")
        if not ident or ident in component_ids:
            failures.append(f"duplicate or missing component id: {ident!r}")
        component_ids.add(ident)
        if not isinstance(destination, str) or not _safe_relative(destination):
            failures.append(f"unsafe destination for {ident}: {destination!r}")
        if destination in destinations and destination != ".":
            failures.append(f"duplicate destination: {destination}")
        destinations.add(destination)
        if operation not in available:
            failures.append(f"unsupported operation for {ident}: {operation!r}")
        source = component.get("source", {})
        candidates = [source.get("file"), *(source.get("include") or [])]
        for candidate in candidates:
            if candidate is None:
                continue
            if not isinstance(candidate, str) or not _safe_relative(candidate):
                failures.append(f"unsafe source for {ident}: {candidate!r}")
    for name, profile in spec["profiles"].items():
        unknown = set(profile.get("include", [])) - component_ids
        if unknown:
            failures.append(f"profile {name} references unknown components: {sorted(unknown)}")
    manifest = descriptor["distribution"].get("manifest")
    if not isinstance(manifest, str) or not _safe_relative(manifest):
        failures.append("descriptor manifest path is unsafe")
    elif not (release_root / manifest).is_file():
        failures.append(f"descriptor manifest is missing: {manifest}")
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("release_root", nargs="?", type=Path,
                        default=ROOT / "src")
    args = parser.parse_args(argv)
    failures = validate(args.release_root.resolve())
    if failures:
        print("installer contract validation failed:", file=sys.stderr)
        print("\n".join(f"  - {item}" for item in failures), file=sys.stderr)
        return 1
    print(f"installer contract is valid: {args.release_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
