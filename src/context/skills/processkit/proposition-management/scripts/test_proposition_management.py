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
