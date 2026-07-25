#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6.0", "jsonschema>=4.0"]
# ///
"""Validate the release-owned installer contract without mutating it."""

from __future__ import annotations

import argparse
import hashlib
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
    "local-release-envelope", "local-trust-store",
    "transaction-action", "transaction-journal",
    "recovery-result", "managed-adapter-state",
)


def _safe_relative(value: str) -> bool:
    if "\\" in value or "\x00" in value:
        return False
    path = PurePosixPath(value)
    return bool(value) and not path.is_absolute() and ".." not in path.parts


def _normalized_relative(value: str) -> str | None:
    if not _safe_relative(value):
        return None
    return PurePosixPath(value).as_posix()


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
        for name in SCHEMAS:
            json.loads(
                (base / "schemas" / f"{name}.schema.json").read_text()
            )
        distribution_path = base / "distribution.yaml"
        distribution = yaml.safe_load(distribution_path.read_text())
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
    ownership = yaml.safe_load((base / "ownership-matrix.yaml").read_text())
    catalog = yaml.safe_load((base / "catalogs/mcp.yaml").read_text())
    available = set(operations.get("operations", {}))
    policies = set(ownership.get("policies", {}))
    component_ids: set[str] = set()
    destinations: set[str] = set()
    for component in spec["components"]:
        ident = component.get("id")
        destination = component.get("destination", "")
        operation = component.get("operation")
        if not ident or ident in component_ids:
            failures.append(f"duplicate or missing component id: {ident!r}")
        component_ids.add(ident)
        normalized_destination = (
            _normalized_relative(destination)
            if isinstance(destination, str) else None
        )
        if normalized_destination is None:
            failures.append(f"unsafe destination for {ident}: {destination!r}")
        elif normalized_destination in destinations and normalized_destination != ".":
            failures.append(f"duplicate destination: {normalized_destination}")
        elif normalized_destination is not None:
            destinations.add(normalized_destination)
        if operation not in available:
            failures.append(f"unsupported operation for {ident}: {operation!r}")
        if component.get("ownership") not in policies:
            failures.append(
                f"unknown ownership for {ident}: {component.get('ownership')!r}"
            )
        source = component.get("source", {})
        file_source = source.get("file")
        include_sources = source.get("include")
        if bool(file_source) == bool(include_sources):
            failures.append(
                f"component {ident} must declare exactly one source form"
            )
            continue
        candidates = [file_source, *(include_sources or [])]
        for candidate in candidates:
            if candidate is None:
                continue
            if not isinstance(candidate, str) or not _safe_relative(candidate):
                failures.append(f"unsafe source for {ident}: {candidate!r}")
                continue
            if candidate.endswith("/**"):
                if not (release_root / candidate[:-3]).is_dir():
                    failures.append(f"include source is missing for {ident}: {candidate}")
            elif not (release_root / candidate).is_file():
                failures.append(f"file source is missing for {ident}: {candidate}")
    for name, profile in spec["profiles"].items():
        unknown = set(profile.get("include", [])) - component_ids
        if unknown:
            failures.append(f"profile {name} references unknown components: {sorted(unknown)}")
    manifest = descriptor["distribution"].get("manifest")
    if not isinstance(manifest, str) or not _safe_relative(manifest):
        failures.append("descriptor manifest path is unsafe")
    elif not (release_root / manifest).is_file():
        failures.append(f"descriptor manifest is missing: {manifest}")
    elif descriptor["distribution"].get("manifestSha256") != hashlib.sha256(
        (release_root / manifest).read_bytes()
    ).hexdigest():
        failures.append("descriptor manifest digest does not match")
    if descriptor["distribution"].get("protocol") != spec["installer"].get("protocol"):
        failures.append("descriptor and manifest installer protocols differ")
    catalog_source = catalog.get("source_of_truth", {})
    for key in ("manifest", "preauth"):
        path = catalog_source.get(key)
        if not isinstance(path, str) or not _safe_relative(path):
            failures.append(f"unsafe MCP catalog source {key}: {path!r}")
        elif not (release_root / path).is_file():
            failures.append(f"MCP catalog source is missing: {path}")
    for adapter in spec.get("harnessAdapters", {}).values():
        if not isinstance(adapter, str) or not _safe_relative(adapter):
            failures.append(f"unsafe adapter path: {adapter!r}")
        elif not (release_root / adapter).is_file():
            failures.append(f"adapter is missing: {adapter}")
        else:
            adapter_data = yaml.safe_load((release_root / adapter).read_text())
            if adapter_data.get("catalog") != spec["catalogs"].get("mcp"):
                failures.append(f"adapter catalog differs from distribution: {adapter}")
            destination = adapter_data.get("destination")
            if not isinstance(destination, str) or not _safe_relative(destination):
                failures.append(f"unsafe adapter destination: {adapter}")
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
