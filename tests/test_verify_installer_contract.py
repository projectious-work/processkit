"""Regression tests for the shipped installer contract validator."""

from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path


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
