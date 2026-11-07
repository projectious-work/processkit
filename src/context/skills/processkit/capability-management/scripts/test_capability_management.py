from __future__ import annotations

import importlib.util
import os
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[6]
SERVER = (
    ROOT
    / "src/context/skills/processkit/capability-management/mcp/server.py"
)


def _load_server():
    spec = importlib.util.spec_from_file_location(
        "capability_management_server",
        SERVER,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_capability_lifecycle_uses_generated_contract(
    tmp_path: Path,
    monkeypatch,
) -> None:
    server = _load_server()
    project = tmp_path / "project"
    project.mkdir()
    (project / "context").mkdir()
    shutil.copytree(
        ROOT / "src/context/schemas",
        project / "context/schemas",
    )
    shutil.copytree(
        ROOT / "src/context/state-machines",
        project / "context/state-machines",
    )
    monkeypatch.chdir(project)
    monkeypatch.setenv(
        "PROCESSKIT_LIB_PATH",
        str(ROOT / "src/context/skills/_lib"),
    )
    server.schema.load_schema.cache_clear()
    server.state_machine.load.cache_clear()

    created = server.create_capability(
        name="alpha-validation",
        description="Validate the v1 alpha contract.",
        providers=["SKILL-schema-management"],
    )
    assert "error" not in created
    assert created["event_logged"] is True
    capability_id = created["id"]
    loaded = server.get_capability(capability_id)
    assert loaded["spec"]["kind"] == "ability"
    assert loaded["spec"]["state"] == "draft"

    active = server.transition_capability(capability_id, "active")
    assert active["to_state"] == "active"
    invalid = server.transition_capability(capability_id, "draft")
    assert "error" in invalid
    assert server.list_capabilities(state="active")[0]["id"] == capability_id
