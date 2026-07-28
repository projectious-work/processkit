#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Generate the release-owned Python/uv runtime manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tomllib
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPO_ROOT / "src"
SKILLS_ROOT = SOURCE_ROOT / "context" / "skills"
OUTPUT = SOURCE_ROOT / ".processkit" / "installer" / "runtime" / "python-uv.json"
API_VERSION = "processkit.projectious.work/python-runtime/v1alpha1"


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _header(path: Path) -> tuple[str, dict[str, Any]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    block: list[str] = []
    in_block = False
    for line in lines:
        stripped = line.strip()
        if not in_block:
            if stripped == "# /// script":
                in_block = True
            continue
        if stripped == "# ///":
            if not block:
                raise ValueError(f"empty PEP 723 block: {path}")
            raw = "\n".join(block) + "\n"
            return raw, tomllib.loads(raw)
        if not line.startswith("#"):
            raise ValueError(f"invalid PEP 723 line: {path}: {line!r}")
        content = line[1:]
        if content.startswith(" "):
            content = content[1:]
        block.append(content)
    raise ValueError(f"missing or unclosed PEP 723 block: {path}")


def build_manifest(source_root: Path = SOURCE_ROOT) -> dict[str, Any]:
    skills_root = source_root / "context" / "skills"
    servers: list[dict[str, Any]] = []
    profiles: dict[str, dict[str, Any]] = {}
    paths = sorted(skills_root.glob("*/*/mcp/server.py"))
    if not paths:
        raise ValueError(f"no shipped MCP servers found under {skills_root}")
    for path in paths:
        raw, metadata = _header(path)
        requires_python = metadata.get("requires-python")
        dependencies = metadata.get("dependencies")
        if not isinstance(requires_python, str) or not requires_python:
            raise ValueError(f"missing requires-python in {path}")
        if not isinstance(dependencies, list) or not all(
            isinstance(item, str) and item for item in dependencies
        ):
            raise ValueError(f"invalid dependencies in {path}")
        dependencies = sorted(dependencies)
        relative = path.relative_to(source_root).as_posix()
        profile_data = {
            "requiresPython": requires_python,
            "dependencies": dependencies,
        }
        profile_sha256 = hashlib.sha256(_canonical(profile_data)).hexdigest()
        servers.append(
            {
                "path": relative,
                "headerSha256": hashlib.sha256(
                    raw.encode("utf-8")
                ).hexdigest(),
                "profileSha256": profile_sha256,
                **profile_data,
            }
        )
        profile = profiles.setdefault(
            profile_sha256,
            {
                "sha256": profile_sha256,
                **profile_data,
                "serverPaths": [],
            },
        )
        profile["serverPaths"].append(relative)
    dependency_profiles = sorted(profiles.values(), key=lambda item: item["sha256"])
    manifest_core = {
        "apiVersion": API_VERSION,
        "kind": "PythonRuntimePolicy",
        "source": {
            "root": "context/skills",
            "scope": "shipped-release",
        },
        "python": {
            "requires": ">=3.10",
        },
        "uv": {
            "command": "uv",
            "requiredFeatures": ["pep-723-script-metadata"],
        },
        "dependencyResolution": {
            "coldOfflineSupported": False,
            "requiresPreparedCache": True,
            "resolvedVersionsLocked": False,
        },
        "servers": servers,
        "dependencyProfiles": dependency_profiles,
    }
    return {
        **manifest_core,
        "aggregateSha256": hashlib.sha256(_canonical(manifest_core)).hexdigest(),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    try:
        manifest = build_manifest()
    except (OSError, ValueError, tomllib.TOMLDecodeError) as error:
        print(f"runtime manifest generation failed: {error}", file=sys.stderr)
        return 1
    payload = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != payload:
            print(f"stale Python runtime manifest: {OUTPUT}", file=sys.stderr)
            return 1
        print(f"Python runtime manifest is current: {OUTPUT}")
        return 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(payload, encoding="utf-8")
    print(f"wrote Python runtime manifest: {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
