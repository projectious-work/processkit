from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
LIBRARY = ROOT / "src/context/skills/_lib"
FIXTURE = ROOT / "tests/fixtures/alpha-project"
sys.path.insert(0, str(LIBRARY))

from processkit import entity, index  # noqa: E402


def test_reindex_groups_entities_by_declared_interface(tmp_path: Path) -> None:
    db = index.open_db(tmp_path / "index.sqlite3")
    try:
        stats = index.reindex(FIXTURE, db)
        assert stats.entities == 6

        records = index.query_by_interface(db, "Record")
        assert {row["kind"] for row in records} == {
            "DecisionRecord",
            "LogEntry",
        }

        versioned = index.query_by_interface(db, "Versioned")
        assert {row["kind"] for row in versioned} == {
            "Artifact",
            "Binding",
            "DecisionRecord",
            "Gate",
            "WorkItem",
        }
        assert index.query_by_interface(
            db, "Versioned", kind="Gate"
        )[0]["kind"] == "Gate"
        assert index.query_by_interface(db, "Unknown") == []
    finally:
        db.close()


def test_upsert_replaces_stale_interface_rows(tmp_path: Path) -> None:
    db = index.open_db(tmp_path / "index.sqlite3")
    try:
        work = entity.load(next((FIXTURE / "context/workitems").glob("*.md")))
        index.upsert_entity(db, work)
        assert index.query_by_interface(db, "Versioned")[0]["kind"] == (
            "WorkItem"
        )

        work.kind = "LogEntry"
        index.upsert_entity(db, work)
        assert index.query_by_interface(db, "Versioned") == []
        assert index.query_by_interface(db, "Record")[0]["kind"] == (
            "LogEntry"
        )
    finally:
        db.close()
