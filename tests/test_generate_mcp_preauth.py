from __future__ import annotations

import importlib.util
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "generate-mcp-preauth.py"
)


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "generate_mcp_preauth",
        SCRIPT,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_payload_is_sorted_and_consistent() -> None:
    module = _load_module()
    payload = module._payload(["processkit-a", "processkit-b"])

    assert payload["enabledMcpjsonServers"] == [
        "processkit-a",
        "processkit-b",
    ]
    expected = [
        "mcp__processkit-a__*",
        "mcp__processkit-b__*",
    ]
    assert payload["permissions"]["allow"] == expected
    assert payload["codex"]["mcp"]["allowed_tools"] == expected


def test_server_names_exclude_gateway(tmp_path: Path) -> None:
    module = _load_module()
    config = (
        tmp_path
        / "context"
        / "skills"
        / "processkit"
        / "example"
        / "mcp"
        / "mcp-config.json"
    )
    config.parent.mkdir(parents=True)
    config.write_text(
        '{"mcpServers":{"processkit-example":{},'
        '"processkit-gateway":{}}}',
        encoding="utf-8",
    )

    assert module._server_names(tmp_path) == ["processkit-example"]


def test_all_server_names_are_the_union(tmp_path: Path) -> None:
    module = _load_module()
    roots = (tmp_path / "dogfood", tmp_path / "release")
    for root, server in zip(roots, ("processkit-a", "processkit-b")):
        config = (
            root
            / "context"
            / "skills"
            / "processkit"
            / server
            / "mcp"
            / "mcp-config.json"
        )
        config.parent.mkdir(parents=True)
        config.write_text(
            f'{{"mcpServers":{{"{server}":{{}}}}}}',
            encoding="utf-8",
        )

    assert module._all_server_names(roots) == [
        "processkit-a",
        "processkit-b",
    ]
