from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[6]
LIBRARY = ROOT / "src/context/skills/_lib"
SERVER_PATH = Path(__file__).resolve().parents[1] / "mcp/server.py"


def _server_module():
    os.environ["PROCESSKIT_LIB_PATH"] = str(LIBRARY)
    spec = importlib.util.spec_from_file_location(
        "schema_management_test_server",
        SERVER_PATH,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _tool(module, name: str):
    return module.server._tool_manager._tools[name].fn


def test_contract_mode_and_partial_regeneration(
    tmp_path: Path,
    monkeypatch,
) -> None:
    project = tmp_path / "project"
    (project / "context").mkdir(parents=True)
    (project / "AGENTS.md").write_text("# fixture\n")
    shutil.copytree(
        ROOT / "src/context/schemas",
        project / "context/schemas",
    )
    monkeypatch.chdir(project)

    module = _server_module()
    contract = _tool(module, "get_schema_contract")("WorkItem")
    assert contract["contract"]["interfaces"] == ["Entity", "Versioned"]
    assert _tool(module, "get_validation_mode")("WorkItem") == {
        "kind": "WorkItem",
        "discriminator": None,
        "validation_mode": "tolerant",
    }
    risk = _tool(module, "get_schema_contract")(
        "Proposition",
        discriminator="risk",
    )
    assert risk["contract"]["discriminator"] == {
        "field": "kind",
        "value": "risk",
    }

    output = project / "context/schemas/_generated/artifact.yaml"
    output.unlink()
    result = _tool(module, "regenerate_schemas")(["Artifact"])
    assert result["rebuilt"] == ["artifact"]
    assert result["errors"] == {}
    again = _tool(module, "regenerate_schemas")(["artifact"])
    assert again["unchanged"] == ["artifact"]


def test_unknown_kind_is_structured_error(tmp_path: Path, monkeypatch) -> None:
    project = tmp_path / "project"
    (project / "context").mkdir(parents=True)
    (project / "AGENTS.md").write_text("# fixture\n")
    shutil.copytree(
        ROOT / "src/context/schemas",
        project / "context/schemas",
    )
    monkeypatch.chdir(project)
    module = _server_module()

    result = _tool(module, "regenerate_schemas")(["Unknown"])
    assert result["rebuilt"] == []
    assert result["errors"] == {"unknown": "unknown kind"}
    assert "error" in _tool(module, "get_schema_contract")("Unknown")
    assert "error" in _tool(module, "get_validation_mode")("Unknown")
