from __future__ import annotations

import hashlib
import shutil
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src/context/skills/_lib"))

from processkit import corpus_migration, entity, schema  # noqa: E402


def _project(tmp_path: Path) -> Path:
    project = tmp_path / "project"
    shutil.copytree(ROOT / "tests/fixtures/migration-v0-project", project)
    shutil.copytree(
        ROOT / "src/context/schemas",
        project / "context/schemas",
    )
    return project


def test_plan_is_deterministic_and_non_writing(tmp_path: Path) -> None:
    project = _project(tmp_path)
    scope = project / "context/scopes/SCOPE-alpha-sprint.md"
    before = scope.read_bytes()
    first = corpus_migration.plan_v0_to_v1(project)
    second = corpus_migration.plan_v0_to_v1(project)
    assert first == second
    assert first["operation_count"] == 1
    assert first["field_loss_percent"] == 0
    assert scope.read_bytes() == before


def test_execution_preserves_ids_extensions_and_log_bytes(
    tmp_path: Path,
) -> None:
    project = _project(tmp_path)
    log_path = project / "context/logs/LOG-alpha-history.md"
    log_hash = hashlib.sha256(log_path.read_bytes()).hexdigest()
    plan = corpus_migration.plan_v0_to_v1(project)
    report = corpus_migration.execute_v0_to_v1(project, plan)
    assert report["applied"] == 1
    migrated = entity.load(
        project / "context/scopes/SCOPE-alpha-sprint.md"
    )
    assert migrated.id == "SCOPE-alpha-sprint"
    assert migrated.kind == "Container"
    assert migrated.spec["kind"] == "scope"
    assert migrated.spec["scope_type"] == "sprint"
    assert migrated.spec["x_project_extension"] == {"preserved": True}
    assert migrated.spec["starts_at"] == "2026-07-01T00:00:00Z"
    assert schema.validate_spec(
        "Container",
        migrated.spec,
    ) == []
    assert hashlib.sha256(log_path.read_bytes()).hexdigest() == log_hash
    assert corpus_migration.plan_v0_to_v1(project)["operation_count"] == 0


def test_execute_rejects_changed_source(tmp_path: Path) -> None:
    project = _project(tmp_path)
    plan = corpus_migration.plan_v0_to_v1(project)
    scope = project / "context/scopes/SCOPE-alpha-sprint.md"
    scope.write_text(scope.read_text() + "\nchanged\n", encoding="utf-8")
    with pytest.raises(corpus_migration.CorpusMigrationError):
        corpus_migration.execute_v0_to_v1(project, plan)


def test_every_supported_v0_kind_has_an_explicit_disposition() -> None:
    expected = {
        "Actor", "Artifact", "Binding", "Capability", "Category",
        "Constraint", "DecisionRecord", "Discussion", "Gate", "LogEntry",
        "Migration", "Note", "Role", "RoleSlot", "Scope", "TeamMember",
        "WorkItem",
    }
    assert set(corpus_migration.V0_KIND_DISPOSITIONS) == expected
    assert corpus_migration.V0_KIND_DISPOSITIONS["Scope"] == {
        "action": "transform",
        "target_kind": "Container",
        "discriminator": "scope",
    }


def test_unknown_v0_kind_is_rejected_in_the_plan(tmp_path: Path) -> None:
    project = _project(tmp_path)
    unknown = project / "context" / "unknown"
    unknown.mkdir()
    (unknown / "UNKNOWN-alpha.md").write_text(
        "---\n"
        "apiVersion: processkit.projectious.work/v1\n"
        "kind: UnknownLegacy\n"
        "metadata: {id: UNKNOWN-alpha, created: 2026-07-27T00:00:00Z}\n"
        "spec: {value: retained}\n"
        "---\n",
        encoding="utf-8",
    )
    plan = corpus_migration.plan_v0_to_v1(project)
    assert any(
        "no explicit v0-to-v1 disposition" in item["error"]
        for item in plan["errors"]
    )
