#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "mcp[cli]>=1.0,<2.0",
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
import json
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path
from pathlib import PurePosixPath
from types import ModuleType


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RELEASE_ROOT = REPO_ROOT / "src"
REQUIRED_PATHS = (
    "AGENTS.md",
    "INDEX.md",
    "PROVENANCE.toml",
    ".processkit/installer/distribution.yaml",
    ".processkit/installer/release-descriptor.json",
    ".processkit/installer/runtime/python-uv.json",
    ".processkit/installer/schemas/python-runtime-policy.schema.json",
    ".processkit/installer/schemas/distribution.schema.json",
    "context/.processkit-mcp-manifest.json",
    "context/schemas",
    "context/schemas/src/registry.yaml",
    "context/schemas/_generated/workitem.yaml",
    "context/schemas/_generated/proposition.yaml",
    "context/schemas/_generated/capability.yaml",
    "context/schemas/_generated/migration.yaml",
    "context/state-machines",
    "context/skills/_lib/processkit/__init__.py",
    "context/skills/processkit/processkit-gateway/mcp/mcp-config.json",
    "context/skills/processkit/processkit-gateway/mcp/server.py",
    "context/skills/processkit/schema-management/mcp/mcp-config.json",
    "context/skills/processkit/schema-management/mcp/server.py",
    "context/skills/processkit/capability-management/mcp/server.py",
    "context/skills/processkit/proposition-management/mcp/server.py",
    "context/skills/processkit/skill-management/mcp/server.py",
    "context/skills/processkit/okf-compatibility/mcp/server.py",
)
MAX_ARCHIVE_MEMBERS = 10_000
MAX_ARCHIVE_MEMBER_BYTES = 64 * 1024 * 1024
MAX_ARCHIVE_TOTAL_BYTES = 256 * 1024 * 1024
MAX_ARCHIVE_PATH_LENGTH = 1_024
MAX_ARCHIVE_PATH_DEPTH = 32


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
        if len(members) > MAX_ARCHIVE_MEMBERS:
            raise RuntimeError("archive has too many members")
        destination_resolved = destination.resolve()
        seen: set[str] = set()
        total_size = 0
        for member in members:
            path = PurePosixPath(member.name)
            if (
                not member.name
                or "\\" in member.name
                or len(member.name) > MAX_ARCHIVE_PATH_LENGTH
                or len(path.parts) > MAX_ARCHIVE_PATH_DEPTH
                or path.is_absolute()
                or ".." in path.parts
            ):
                raise RuntimeError(f"unsafe archive member: {member.name}")
            normalized = str(path)
            if normalized in seen:
                raise RuntimeError(f"duplicate archive member: {member.name}")
            seen.add(normalized)
            if member.issym() or member.islnk() or not (
                member.isfile() or member.isdir()
            ):
                raise RuntimeError(
                    f"archive member type is not supported: {member.name}"
                )
            if member.isfile():
                if member.size > MAX_ARCHIVE_MEMBER_BYTES:
                    raise RuntimeError(
                        f"archive member exceeds size limit: {member.name}"
                    )
                total_size += member.size
                if total_size > MAX_ARCHIVE_TOTAL_BYTES:
                    raise RuntimeError("archive exceeds total size limit")
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

    top_level = {PurePosixPath(member.name).parts[0] for member in members}
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

    installer_validator = _load_module(
        "verify_installer_contract",
        REPO_ROOT / "scripts" / "verify-installer-contract.py",
    )
    installer_failures = installer_validator.validate(distribution_root)
    if installer_failures:
        rendered = "\n".join(f"  - {failure}" for failure in installer_failures)
        raise RuntimeError(f"staged installer contract is invalid:\n{rendered}")


def _run_installer_planner(
    planner_source: Path,
    distribution_root: Path,
    workspace: Path,
) -> None:
    """Exercise the Rust planner against the exact extracted artifact."""
    manifest = planner_source / "Cargo.toml"
    if not manifest.is_file():
        raise RuntimeError(
            f"installer planner workspace is missing Cargo.toml: {planner_source}"
        )
    project_root = workspace / "installer-project"
    project_root.mkdir()
    command = [
        "cargo",
        "run",
        "--quiet",
        "--locked",
        "--manifest-path",
        str(manifest),
        "--",
        "plan",
        "--root",
        str(project_root),
        "--distribution",
        str(distribution_root),
        "--profile",
        "managed",
        "--dry-run",
        "--json",
    ]
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        raise RuntimeError(
            "installer planner failed against extracted artifact:\n"
            f"{completed.stderr}"
        )
    try:
        plan = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"installer planner did not emit JSON: {error}"
        ) from error
    if plan.get("status") != "planned":
        raise RuntimeError(f"installer planner rejected extracted artifact: {plan}")
    if any(project_root.iterdir()):
        raise RuntimeError("installer planner mutated its disposable project")


def run(
    release_root: Path | None,
    archive: Path | None,
    planner_source: Path | None = None,
) -> None:
    workspace = Path(tempfile.mkdtemp(prefix="processkit-package-smoke-"))
    try:
        if archive is None:
            archive = workspace / "processkit-ci.tar.gz"
            _archive_source(release_root or DEFAULT_RELEASE_ROOT, archive)

        extracted = workspace / "extracted"
        extracted.mkdir()
        distribution_root = _extract_archive(archive.resolve(), extracted)
        _validate_layout(distribution_root)
        if planner_source is not None:
            _run_installer_planner(
                planner_source.resolve(), distribution_root, workspace
            )

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
    parser.add_argument(
        "--planner-source",
        type=Path,
        help=(
            "Rust installer workspace used to plan against the extracted "
            "artifact (release gate only)"
        ),
    )
    args = parser.parse_args(argv)
    run(args.release_root, args.archive, args.planner_source)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
