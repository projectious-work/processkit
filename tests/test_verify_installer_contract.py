"""Regression tests for the shipped installer contract validator."""

from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "verify-installer-contract.py"


def _module():
    spec = importlib.util.spec_from_file_location("installer_contract", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_shipped_contract_is_valid() -> None:
    assert _module().validate(REPO_ROOT / "src") == []


def test_mcp_catalog_projects_the_gateway() -> None:
    catalog = yaml.safe_load(
        (
            REPO_ROOT / "src/.processkit/installer/catalogs/mcp.yaml"
        ).read_text(encoding="utf-8")
    )
    servers = {server["id"]: server for server in catalog["servers"]}
    gateway = servers["processkit-gateway"]
    assert gateway["command"] == "uv"
    assert gateway["args"][-1].endswith("processkit-gateway/mcp/server.py")
    assert gateway["env"]["PROCESSKIT_MCP_MODE"] == "gateway"


def test_traversal_destination_is_rejected(tmp_path: Path) -> None:
    target = tmp_path / "release"
    shutil.copytree(REPO_ROOT / "src", target)
    manifest = target / ".processkit/installer/distribution.yaml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace(
            "destination: AGENTS.md", "destination: ../AGENTS.md"
        ),
        encoding="utf-8",
    )
    failures = _module().validate(target)
    assert any("unsafe destination" in failure for failure in failures)


def test_ambiguous_and_missing_sources_are_rejected(tmp_path: Path) -> None:
    target = tmp_path / "release"
    shutil.copytree(REPO_ROOT / "src", target)
    manifest = target / ".processkit/installer/distribution.yaml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace(
            "file: AGENTS.md", "file: missing.md\n        include: [context/**]"
        ),
        encoding="utf-8",
    )
    failures = _module().validate(target)
    assert any("exactly one source form" in failure for failure in failures)


def test_descriptor_digest_and_adapter_destination_are_checked(tmp_path: Path) -> None:
    target = tmp_path / "release"
    shutil.copytree(REPO_ROOT / "src", target)
    adapter = target / ".processkit/installer/adapters/codex.yaml"
    adapter.write_text(
        adapter.read_text(encoding="utf-8").replace(
            "destination: .mcp.json", "destination: ../.mcp.json"
        ),
        encoding="utf-8",
    )
    manifest = target / ".processkit/installer/distribution.yaml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace(
            "ownership: shared", "ownership: user-owned"
        ),
        encoding="utf-8",
    )
    failures = _module().validate(target)
    assert any("manifest digest does not match" in failure for failure in failures)
    assert any("unsafe adapter destination" in failure for failure in failures)
