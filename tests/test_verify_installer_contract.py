"""Regression tests for the shipped installer contract validator."""

from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

import jsonschema
import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "verify-installer-contract.py"
RUNTIME_SCRIPT = REPO_ROOT / "scripts/generate-python-runtime-manifest.py"


def _module():
    spec = importlib.util.spec_from_file_location("installer_contract", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _runtime_module():
    spec = importlib.util.spec_from_file_location(
        "python_runtime_manifest",
        RUNTIME_SCRIPT,
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_shipped_contract_is_valid() -> None:
    assert _module().validate(REPO_ROOT / "src") == []


def test_python_runtime_manifest_is_current_and_valid() -> None:
    generated = _runtime_module().build_manifest(REPO_ROOT / "src")
    tracked = json.loads(
        (
            REPO_ROOT
            / "src/.processkit/installer/runtime/python-uv.json"
        ).read_text(encoding="utf-8")
    )
    assert generated == tracked
    shipped_servers = list(
        (
            REPO_ROOT / "src/context/skills"
        ).glob("*/*/mcp/server.py")
    )
    assert len(tracked["servers"]) == len(shipped_servers)
    assert all(
        server["path"].startswith("context/skills/")
        for server in tracked["servers"]
    )
    schema = json.loads(
        (
            REPO_ROOT
            / "src/.processkit/installer/schemas/"
            "python-runtime-policy.schema.json"
        ).read_text(encoding="utf-8")
    )
    jsonschema.Draft202012Validator(schema).validate(tracked)


def test_python_runtime_manifest_ignores_dogfood_tree(
    tmp_path: Path,
) -> None:
    server = (
        tmp_path
        / "context/skills/processkit/example/mcp/server.py"
    )
    server.parent.mkdir(parents=True)
    server.write_text(
        "# /// script\n"
        '# requires-python = ">=3.10"\n'
        '# dependencies = ["mcp>=1"]\n'
        "# ///\n",
        encoding="utf-8",
    )
    dogfood = (
        tmp_path
        / "dogfood/context/skills/processkit/ignored/mcp/server.py"
    )
    dogfood.parent.mkdir(parents=True)
    dogfood.write_text(server.read_text(encoding="utf-8"), encoding="utf-8")
    lock = (
        tmp_path
        / ".processkit/installer/runtime/python-requirements.lock"
    )
    lock.parent.mkdir(parents=True)
    lock.write_text(
        "mcp==1.0.0 \\\n"
        "    --hash=sha256:" + "0" * 64 + "\n",
        encoding="utf-8",
    )
    manifest = _runtime_module().build_manifest(tmp_path)
    assert [item["path"] for item in manifest["servers"]] == [
        "context/skills/processkit/example/mcp/server.py"
    ]


def test_runtime_policy_header_drift_is_rejected(tmp_path: Path) -> None:
    target = tmp_path / "release"
    shutil.copytree(REPO_ROOT / "src", target)
    gateway = (
        target
        / "context/skills/processkit/processkit-gateway/mcp/server.py"
    )
    gateway.write_text(
        gateway.read_text(encoding="utf-8").replace(
            '"httpx>=0.27",',
            '"httpx>=0.28",',
        ),
        encoding="utf-8",
    )
    failures = _module().validate(target)
    assert any(
        "runtime policy header digest differs" in failure
        for failure in failures
    )


def test_runtime_policy_profile_tampering_is_rejected(
    tmp_path: Path,
) -> None:
    target = tmp_path / "release"
    shutil.copytree(REPO_ROOT / "src", target)
    policy_path = (
        target / ".processkit/installer/runtime/python-uv.json"
    )
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    policy["dependencyProfiles"][0]["serverPaths"].append(
        "context/skills/processkit/not-shipped/mcp/server.py"
    )
    policy_path.write_text(
        json.dumps(policy, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    failures = _module().validate(target)
    assert "runtime policy dependency profiles are inconsistent" in failures
    assert "runtime policy aggregate digest differs" in failures


def test_installer_result_schema_accepts_plan_contract() -> None:
    schema = json.loads(
        (
            REPO_ROOT
            / "src/.processkit/installer/schemas/installer-result.schema.json"
        ).read_text(encoding="utf-8")
    )
    result = {
        "apiVersion": "processkit.projectious.work/installer/v1alpha1",
        "status": "planned",
        "distribution": {
            "name": "processkit",
            "version": "v1.0.0-alpha.3",
            "manifestSha256": "a" * 64,
        },
        "selectedProfiles": ["managed"],
        "harnesses": ["codex"],
        "changes": [],
        "conflicts": [],
        "warnings": [],
        "errors": [],
    }
    jsonschema.Draft202012Validator(schema).validate(result)


def test_execute_failure_golden_envelopes_match_result_schema() -> None:
    schema = json.loads(
        (
            REPO_ROOT
            / "src/.processkit/installer/schemas/installer-result.schema.json"
        ).read_text(encoding="utf-8")
    )
    fixtures = (
        REPO_ROOT
        / "installer/crates/processkit/tests/fixtures/execute-failures"
    )
    for expected_path in sorted(fixtures.glob("*/expected.json")):
        expected = json.loads(expected_path.read_text(encoding="utf-8"))
        if "messagePrefix" in expected:
            continue
        jsonschema.Draft202012Validator(schema).validate(expected)


def test_planner_golden_envelopes_match_result_schema() -> None:
    schema = json.loads(
        (
            REPO_ROOT
            / "src/.processkit/installer/schemas/installer-result.schema.json"
        ).read_text(encoding="utf-8")
    )
    fixtures = REPO_ROOT / "installer/crates/processkit/tests/fixtures/plans"
    for expected_path in sorted(fixtures.glob("*/expected.json")):
        expected = json.loads(expected_path.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(schema).validate(expected)


def test_recovery_result_schema_accepts_clean_contract() -> None:
    schema = json.loads(
        (
            REPO_ROOT
            / "src/.processkit/installer/schemas/recovery-result.schema.json"
        ).read_text(encoding="utf-8")
    )
    result = {
        "apiVersion": "processkit.projectious.work/installer/v1alpha1",
        "status": "clean",
        "recovered": 0,
        "errors": [],
    }
    jsonschema.Draft202012Validator(schema).validate(result)


def test_installer_request_requires_complete_signed_release_input() -> None:
    schema = json.loads(
        (
            REPO_ROOT
            / "src/.processkit/installer/schemas/installer-request.schema.json"
        ).read_text(encoding="utf-8")
    )
    request = {
        "apiVersion": "processkit.projectious.work/installer/v1alpha1",
        "operation": "plan",
        "root": ".",
        "distributionPath": "/release",
        "envelopePath": "/release.json",
    }
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(request)


@pytest.mark.parametrize(
    "operation",
    ["install", "update", "uninstall", "recover"],
)
def test_installer_request_requires_mutation_acknowledgement(
    operation: str,
) -> None:
    schema = json.loads(
        (
            REPO_ROOT
            / "src/.processkit/installer/schemas/installer-request.schema.json"
        ).read_text(encoding="utf-8")
    )
    request = {
        "apiVersion": "processkit.projectious.work/installer/v1alpha1",
        "operation": operation,
        "root": ".",
        "yes": False,
    }
    if operation in {"install", "update"}:
        request["distributionPath"] = "/release"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(request)


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
