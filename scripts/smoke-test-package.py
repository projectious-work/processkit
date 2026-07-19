#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "mcp[cli]>=1.0",
#   "pyyaml>=6.0",
#   "jsonschema>=4.0",
#   "jinja2>=3.1",
#   "httpx>=0.27",
#   "sqlite-vec>=0.1.0",
# ]
# ///
"""Exercise a staged processkit distribution without aibox.

The release builder has tag and provenance side effects that do not belong in
ordinary local verification. This test creates a temporary archive from ``src/``
or consumes an existing release archive, extracts it, validates its package
contract, and runs the full MCP workflow from the extracted files.
"""

from __future__ import annotations

import argparse
import importlib.util
import shutil
import sys
import tarfile
import tempfile
from pathlib import Path
from types import ModuleType


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RELEASE_ROOT = REPO_ROOT / "src"
REQUIRED_PATHS = (
    "AGENTS.md",
    "INDEX.md",
    "PROVENANCE.toml",
    "context/.processkit-mcp-manifest.json",
    "context/schemas",
    "context/schemas/src/registry.yaml",
    "context/schemas/_generated/workitem.yaml",
    "context/state-machines",
    "context/skills/_lib/processkit/__init__.py",
    "context/skills/processkit/processkit-gateway/mcp/mcp-config.json",
    "context/skills/processkit/processkit-gateway/mcp/server.py",
)


def _load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _tar_filter(info: tarfile.TarInfo) -> tarfile.TarInfo | None:
    parts = Path(info.name).parts
    if "__pycache__" in parts or info.name.endswith((".pyc", ".DS_Store")):
        return None
    return info


def _archive_source(source: Path, archive: Path) -> None:
    if not source.is_dir():
        raise RuntimeError(f"release root is not a directory: {source}")
    with tarfile.open(archive, "w:gz") as bundle:
        bundle.add(source, arcname="processkit-ci", filter=_tar_filter)


def _extract_archive(archive: Path, destination: Path) -> Path:
    with tarfile.open(archive, "r:*") as bundle:
        members = bundle.getmembers()
        if not members:
            raise RuntimeError(f"archive is empty: {archive}")
        destination_resolved = destination.resolve()
        for member in members:
            if member.issym() or member.islnk():
                raise RuntimeError(
                    f"archive links are not supported: {member.name}"
                )
            target = (destination / member.name).resolve()
            if (
                destination_resolved not in target.parents
                and target != destination_resolved
            ):
                raise RuntimeError(f"unsafe archive member: {member.name}")
        if sys.version_info >= (3, 12):
            bundle.extractall(destination, filter="data")
        else:
            bundle.extractall(destination)

    top_level = {
        Path(member.name).parts[0]
        for member in members
        if member.name
    }
    if len(top_level) != 1:
        raise RuntimeError(
            "package archive must contain one top-level directory"
        )
    return destination / top_level.pop()


def _validate_layout(distribution_root: Path) -> None:
    missing = [
        path
        for path in REQUIRED_PATHS
        if not (distribution_root / path).exists()
    ]
    if missing:
        rendered = "\n".join(f"  - {path}" for path in missing)
        raise RuntimeError(
            f"staged distribution is missing required paths:\n{rendered}"
        )

    validator = _load_module(
        "validate_release_mcp_preauth",
        REPO_ROOT / "scripts" / "validate-release-mcp-preauth.py",
    )
    failures = validator.validate(distribution_root)
    if failures:
        rendered = "\n".join(f"  - {failure}" for failure in failures)
        raise RuntimeError(f"staged MCP metadata is invalid:\n{rendered}")


def run(release_root: Path | None, archive: Path | None) -> None:
    workspace = Path(tempfile.mkdtemp(prefix="processkit-package-smoke-"))
    try:
        if archive is None:
            archive = workspace / "processkit-ci.tar.gz"
            _archive_source(release_root or DEFAULT_RELEASE_ROOT, archive)

        extracted = workspace / "extracted"
        extracted.mkdir()
        distribution_root = _extract_archive(archive.resolve(), extracted)
        _validate_layout(distribution_root)

        generator = _load_module(
            "processkit_schema_generation",
            distribution_root
            / "context/skills/_lib/processkit/schema_generation.py",
        )
        generated = generator.regenerate_schemas(
            distribution_root / "context/schemas",
            check=True,
        )
        if generated["errors"] or generated["rebuilt"]:
            raise RuntimeError(
                f"staged generated schemas are stale: {generated}"
            )

        smoke = _load_module(
            "processkit_server_smoke",
            REPO_ROOT / "scripts" / "smoke-test-servers.py",
        )
        smoke.run(distribution_root)
        print(f"package smoke passed: {distribution_root.name}")
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    inputs = parser.add_mutually_exclusive_group()
    inputs.add_argument(
        "--release-root",
        type=Path,
        help="distribution tree to stage (default: src/)",
    )
    inputs.add_argument(
        "--archive",
        type=Path,
        help="existing processkit release archive to extract and test",
    )
    args = parser.parse_args(argv)
    run(args.release_root, args.archive)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
