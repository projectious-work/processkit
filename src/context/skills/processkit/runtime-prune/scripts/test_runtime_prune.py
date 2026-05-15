"""Tests for provider-neutral runtime prune planning."""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SERVER_PATH = SKILL_ROOT / "mcp" / "server.py"


def _load_server():
    spec = importlib.util.spec_from_file_location(
        "runtime_prune_server",
        SERVER_PATH,
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_analyze_disk_usage_counts_only_selected_cache_paths(tmp_path):
    root = tmp_path / "repo"
    runtime = root / ".aibox-home" / "cache"
    runtime_keep = root / ".aibox-home" / "state"
    build = root / "target" / "debug" / "incremental"
    other = root / "target" / "debug" / "deps"
    runtime.mkdir(parents=True)
    runtime_keep.mkdir(parents=True)
    build.mkdir(parents=True)
    other.mkdir(parents=True)
    (runtime / "runtime.bin").write_bytes(b"x" * 10)
    (runtime_keep / "state.db").write_bytes(b"s" * 300)
    (build / "build.bin").write_bytes(b"y" * 20)
    (other / "not-counted.bin").write_bytes(b"z" * 200)

    server = _load_server()
    out = server.analyze_disk_usage(
        project_root=str(root),
        scopes=["runtime-home", "build-cache"],
    )

    assert "error" not in out
    assert out["total_expected_reclaim_bytes"] < 230
    by_scope = {item["scope"]: item for item in out["scope_data"]}
    assert by_scope["runtime-home"]["expected_reclaim_bytes"] >= 10
    assert by_scope["build-cache"]["expected_reclaim_bytes"] >= 20
    paths = {
        target["path"]
        for item in out["scope_data"]
        for target in item["targets"]
    }
    assert "target/debug/deps" not in paths
    assert ".aibox-home" not in paths
    assert ".aibox-home/state" not in paths


def test_plan_prune_requires_exact_confirmation_and_reports_no_aibox(
    tmp_path,
    monkeypatch,
):
    root = tmp_path / "repo"
    root.mkdir()
    monkeypatch.setenv("PATH", "")

    server = _load_server()
    plan = server.plan_prune(
        project_root=str(root),
        scopes=["runtime-home", "containers"],
    )

    assert plan["required_confirmation"] == (
        "apply-prune:runtime-home,containers"
    )
    assert plan["aibox_prune_available"] is False
    by_scope = {action["scope"]: action for action in plan["actions"]}
    assert by_scope["runtime-home"]["apply_supported"] is True
    assert by_scope["runtime-home"]["apply_owner"] == "processkit"
    assert by_scope["containers"]["apply_supported"] is False
    assert by_scope["containers"]["apply_owner"] == "aibox prune"

    denied = server.apply_prune(
        project_root=str(root),
        scopes=["runtime-home", "containers"],
        confirmation="yes",
    )
    assert denied["error"] == "confirmation mismatch"

    unavailable = server.apply_prune(
        project_root=str(root),
        scopes=["runtime-home", "containers"],
        confirmation=plan["required_confirmation"],
    )
    assert unavailable["applied"] is False
    assert unavailable["partial"] is False
    by_result = {item["scope"]: item for item in unavailable["results"]}
    assert by_result["runtime-home"]["unsupported"] is False
    assert by_result["containers"]["unsupported"] is True
    assert by_result["containers"]["reason"] == (
        "aibox prune is not available on PATH"
    )


def test_apply_prune_removes_low_risk_allowlist_without_aibox(
    tmp_path,
    monkeypatch,
):
    root = tmp_path / "repo"
    cache = root / ".aibox-home" / "cache"
    keep = root / ".aibox-home" / "state"
    build = root / "target" / "debug" / "build"
    deps = root / "target" / "debug" / "deps"
    cache.mkdir(parents=True)
    keep.mkdir(parents=True)
    build.mkdir(parents=True)
    deps.mkdir(parents=True)
    (cache / "cache.bin").write_bytes(b"x")
    (keep / "state.db").write_bytes(b"s")
    (build / "build.bin").write_bytes(b"b")
    (deps / "dep.rlib").write_bytes(b"d")
    monkeypatch.setenv("PATH", "")

    server = _load_server()
    out = server.apply_prune(
        project_root=str(root),
        scopes=["runtime-home", "build-cache"],
        confirmation="apply-prune:runtime-home,build-cache",
    )

    assert out["applied"] is True
    assert out["partial"] is True
    assert not cache.exists()
    assert not build.exists()
    assert keep.exists()
    assert deps.exists()


def test_apply_prune_delegates_high_risk_scopes_to_aibox(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    root.mkdir()
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    log = tmp_path / "aibox-argv.txt"
    fake = bin_dir / "aibox"
    fake.write_text(
        "#!/usr/bin/env sh\n"
        "printf '%s\\n' \"$@\" > \"$AIBOX_PRUNE_LOG\"\n"
        "printf '{\"ok\":true}\\n'\n",
        encoding="utf-8",
    )
    fake.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setenv("AIBOX_PRUNE_LOG", str(log))

    server = _load_server()
    out = server.apply_prune(
        project_root=str(root),
        scopes=["containers"],
        confirmation="apply-prune:containers",
    )

    assert out["applied"] is True
    result = out["results"][0]
    assert result["exit_code"] == 0
    assert result["command"] == ["aibox", "prune", "containers", "--yes"]
    assert log.read_text(encoding="utf-8").splitlines() == [
        "prune",
        "containers",
        "--yes",
    ]
