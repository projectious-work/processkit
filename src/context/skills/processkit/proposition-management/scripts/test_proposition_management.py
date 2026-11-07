from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[6]
SERVER = (
    ROOT
    / "src/context/skills/processkit/proposition-management/mcp/server.py"
)


def _load_server():
    spec = importlib.util.spec_from_file_location(
        "proposition_management_server",
        SERVER,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_claim_and_risk_share_proposition_interface(
    tmp_path: Path,
    monkeypatch,
) -> None:
    server = _load_server()
    project = tmp_path / "project"
    (project / "context").mkdir(parents=True)
    shutil.copytree(
        ROOT / "src/context/schemas",
        project / "context/schemas",
    )
    monkeypatch.chdir(project)
    server.schema.load_schema.cache_clear()

    claim = server.create_proposition(statement="Alpha schemas are generated.")
    assert "error" not in claim
    risk = server.create_proposition(
        statement="A migrated reference may be lost.",
        kind="risk",
        likelihood="possible",
        impact="major",
    )
    assert "error" not in risk
    invalid = server.create_proposition(
        statement="Incomplete risk.",
        kind="risk",
    )
    assert invalid["error"] == "schema validation failed"

    rows = server.query_propositions()
    assert {row["id"] for row in rows} == {claim["id"], risk["id"]}
    risks = server.query_propositions(kind="risk")
    assert [row["id"] for row in risks] == [risk["id"]]
    assert risk["event_logged"] is True


def test_beta_discriminators_validate_update_and_query(
    tmp_path: Path,
    monkeypatch,
) -> None:
    server = _load_server()
    project = tmp_path / "project"
    (project / "context").mkdir(parents=True)
    shutil.copytree(
        ROOT / "src/context/schemas",
        project / "context/schemas",
    )
    monkeypatch.chdir(project)
    server.schema.load_schema.cache_clear()

    created = {
        "belief": server.create_proposition(
            statement="The beta model is understandable.",
            kind="belief",
            rationale="The alpha workflow completed without ambiguity.",
        ),
        "world-fact": server.create_proposition(
            statement="The alpha release archive validates locally.",
            kind="world-fact",
            source="scripts/test-release-trust-local.sh",
            observed_at="2026-07-27T05:00:00Z",
        ),
        "wsjf-estimate": server.create_proposition(
            statement="Activate beta Proposition discriminators first.",
            kind="wsjf-estimate",
            cost_of_delay=13,
            job_size=3,
            score=4.33,
        ),
        "assumption": server.create_proposition(
            statement="Downstream consumers accept additive MCP arguments.",
            kind="assumption",
            validation_due="2026-08-03T00:00:00Z",
            validation_method="Run the staged-package smoke suite.",
        ),
    }
    assert all("error" not in result for result in created.values())

    invalid_world_fact = server.create_proposition(
        statement="This fact has no source.",
        kind="world-fact",
    )
    assert invalid_world_fact["error"] == "schema validation failed"
    invalid_wsjf = server.create_proposition(
        statement="This estimate has no job size.",
        kind="wsjf-estimate",
        cost_of_delay=8,
    )
    assert invalid_wsjf["error"] == "schema validation failed"

    updated = server.update_proposition(
        created["assumption"]["id"],
        validation_method="Verify in two independent fixture projects.",
    )
    assert updated["updated"] == ["validation_method"]
    assumption = server.get_proposition(created["assumption"]["id"])
    assert (
        assumption["spec"]["validation_method"]
        == "Verify in two independent fixture projects."
    )

    for kind, result in created.items():
        rows = server.query_propositions(kind=kind)
        assert [row["id"] for row in rows] == [result["id"]]
