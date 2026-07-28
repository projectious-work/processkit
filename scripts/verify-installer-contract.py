#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "pyyaml>=6.0",
#   "jsonschema>=4.0",
#   "tomli>=2.0; python_version < '3.11'",
# ]
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
try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = Path(".processkit/installer")
REQUIRED = (
    "distribution.yaml", "release-descriptor.json", "operations.yaml",
    "ownership-matrix.yaml", "catalogs/mcp.yaml", "adapters/codex.yaml",
    "adapters/claude.yaml", "runtime/python-uv.json",
)
SCHEMAS = (
    "distribution", "release-descriptor", "installer-request",
    "installer-result", "mcp-catalog", "harness-adapter",
    "installation-state", "compatibility", "variables",
    "local-release-envelope", "local-trust-store",
    "transaction-action", "transaction-journal",
    "recovery-result", "managed-adapter-state", "python-runtime-policy",
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


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _pep723_payload(path: Path) -> str | None:
    in_block = False
    block: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not in_block:
            if stripped == "# /// script":
                in_block = True
            continue
        if stripped == "# ///":
            return "\n".join(block) + "\n" if block else None
        if not line.startswith("#"):
            return None
        content = line[1:]
        block.append(content[1:] if content.startswith(" ") else content)
    return None


def _validate_runtime_policy(
    release_root: Path,
    runtime_policy: dict,
) -> list[str]:
    failures: list[str] = []
    servers = runtime_policy.get("servers", [])
    entries = {
        server.get("path"): server
        for server in servers
        if isinstance(server, dict) and isinstance(server.get("path"), str)
    }
    if len(entries) != len(servers):
        failures.append("runtime policy has duplicate or invalid server paths")
        return failures
    shipped_paths = sorted(
        path.relative_to(release_root).as_posix()
        for path in (
            release_root / "context" / "skills"
        ).glob("*/*/mcp/server.py")
    )
    if sorted(entries) != shipped_paths:
        failures.append("runtime policy server inventory differs from release")
    expected_profiles: dict[str, dict] = {}
    for relative, entry in entries.items():
        if not _safe_relative(relative):
            failures.append(f"unsafe runtime policy server path: {relative!r}")
            continue
        path = release_root / relative
        if not path.is_file():
            failures.append(f"runtime policy server is missing: {relative}")
            continue
        payload = _pep723_payload(path)
        if payload is None:
            failures.append(f"invalid PEP 723 header: {relative}")
            continue
        try:
            metadata = tomllib.loads(payload)
        except tomllib.TOMLDecodeError:
            failures.append(f"invalid PEP 723 header: {relative}")
            continue
        requires_python = metadata.get("requires-python")
        dependencies = metadata.get("dependencies")
        if not isinstance(requires_python, str) or not requires_python:
            failures.append(f"invalid PEP 723 metadata: {relative}")
            continue
        if not isinstance(dependencies, list) or not all(
            isinstance(item, str) and item for item in dependencies
        ):
            failures.append(f"invalid PEP 723 metadata: {relative}")
            continue
        actual_profile_data = {
            "requiresPython": requires_python,
            "dependencies": sorted(dependencies),
        }
        actual_header = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        if entry.get("headerSha256") != actual_header:
            failures.append(f"runtime policy header digest differs: {relative}")
        profile_data = {
            "requiresPython": entry.get("requiresPython"),
            "dependencies": entry.get("dependencies"),
        }
        if profile_data != actual_profile_data:
            failures.append(f"runtime policy profile data differs: {relative}")
        profile_sha256 = hashlib.sha256(
            _canonical_json(actual_profile_data)
        ).hexdigest()
        if entry.get("profileSha256") != profile_sha256:
            failures.append(f"runtime policy profile digest differs: {relative}")
        profile = expected_profiles.setdefault(
            profile_sha256,
            {
                "sha256": profile_sha256,
                **actual_profile_data,
                "serverPaths": [],
            },
        )
        profile["serverPaths"].append(relative)
    expected = sorted(
        expected_profiles.values(),
        key=lambda profile: profile["sha256"],
    )
    if runtime_policy.get("dependencyProfiles") != expected:
        failures.append("runtime policy dependency profiles are inconsistent")
    core = {
        key: value
        for key, value in runtime_policy.items()
        if key != "aggregateSha256"
    }
    aggregate = hashlib.sha256(_canonical_json(core)).hexdigest()
    if runtime_policy.get("aggregateSha256") != aggregate:
        failures.append("runtime policy aggregate digest differs")
    return failures


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
        compatibility_schema = json.loads(
            (base / "schemas/compatibility.schema.json").read_text()
        )
        runtime_policy = json.loads(
            (base / "runtime/python-uv.json").read_text()
        )
        runtime_schema = json.loads(
            (base / "schemas/python-runtime-policy.schema.json").read_text()
        )
        jsonschema.validate(runtime_policy, runtime_schema)
    except (OSError, ValueError, yaml.YAMLError, jsonschema.ValidationError) as exc:
        return [f"invalid installer contract: {exc}"]

    spec = distribution["spec"]
    failures.extend(_validate_runtime_policy(release_root, runtime_policy))
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
    runtime_components = [
        component
        for component in spec["components"]
        if component.get("id") == "python-runtime-policy"
    ]
    if len(runtime_components) != 1:
        failures.append("distribution must define one python-runtime-policy component")
    else:
        runtime_component = runtime_components[0]
        if runtime_component.get("source", {}).get("file") != (
            ".processkit/installer/runtime/python-uv.json"
        ):
            failures.append("python-runtime-policy source is incorrect")
        if runtime_component.get("destination") != (
            ".processkit/runtime/python-uv.json"
        ):
            failures.append("python-runtime-policy destination is incorrect")
        if runtime_component.get("operation") != "copy/v1":
            failures.append("python-runtime-policy operation is incorrect")
        if runtime_component.get("ownership") != "managed-three-way":
            failures.append("python-runtime-policy ownership is incorrect")
        for name, profile in spec["profiles"].items():
            if "python-runtime-policy" not in profile.get("include", []):
                failures.append(
                    f"profile {name} omits python-runtime-policy"
                )
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
    compatibility_ids: set[str] = set()
    compatibility_versions: set[str] = set()
    for manifest_path in spec.get("compatibility", []):
        if not isinstance(manifest_path, str) or not _safe_relative(manifest_path):
            failures.append(f"unsafe compatibility manifest: {manifest_path!r}")
            continue
        path = release_root / manifest_path
        if not path.is_file():
            failures.append(f"compatibility manifest is missing: {manifest_path}")
            continue
        try:
            manifest = yaml.safe_load(path.read_text())
            jsonschema.validate(manifest, compatibility_schema)
        except (OSError, yaml.YAMLError, jsonschema.ValidationError) as exc:
            failures.append(f"invalid compatibility manifest {manifest_path}: {exc}")
            continue
        ident = manifest["id"]
        version = manifest["source"]["releaseVersion"]
        if ident in compatibility_ids or version in compatibility_versions:
            failures.append(f"duplicate compatibility identity: {ident} / {version}")
        compatibility_ids.add(ident)
        compatibility_versions.add(version)
        anchors = manifest["detection"]["anchors"]
        anchor_paths = [anchor["path"] for anchor in anchors]
        if len(anchor_paths) != len(set(anchor_paths)):
            failures.append(f"duplicate compatibility anchor in {ident}")
        for anchor in anchors:
            if not _safe_relative(anchor["path"]):
                failures.append(f"unsafe compatibility anchor in {ident}")
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
