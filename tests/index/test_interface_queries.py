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
        assert stats.entities == 8

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
            "Proposition",
        }
        assert index.query_by_interface(
            db, "Versioned", kind="Gate"
        )[0]["kind"] == "Gate"
        assert index.query_by_interface(db, "Unknown") == []

        propositions = index.query_by_interface(db, "Proposition")
        assert {row["id"] for row in propositions} == {
            "PROP-20260722_0001-ClearPath-alpha-claim",
            "PROP-20260722_0002-ClearPath-alpha-risk",
        }
        by_id = {row["id"]: row for row in propositions}
        assert by_id[
            "PROP-20260722_0001-ClearPath-alpha-claim"
        ]["discriminator"] is None
        assert by_id[
            "PROP-20260722_0002-ClearPath-alpha-risk"
        ]["discriminator"] == "risk"
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


def test_existing_index_adds_discriminator_column(tmp_path: Path) -> None:
    import sqlite3

    path = tmp_path / "legacy.sqlite3"
    db = sqlite3.connect(path)
    db.execute(
        "CREATE TABLE entities ("
        "id TEXT PRIMARY KEY, kind TEXT NOT NULL, api_version TEXT NOT NULL,"
        "path TEXT NOT NULL, storage_location TEXT, created TEXT NOT NULL,"
        "updated TEXT, title TEXT, state TEXT, labels_json TEXT,"
        "spec_json TEXT NOT NULL, body TEXT)"
    )
    db.commit()
    db.close()

    migrated = index.open_db(path)
    try:
        columns = {
            row["name"]
            for row in migrated.execute("PRAGMA table_info(entities)")
        }
        assert "discriminator" in columns
    finally:
        migrated.close()
