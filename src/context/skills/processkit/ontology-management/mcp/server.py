#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "mcp[cli]>=1.0,<2.0",
#   "pyyaml>=6.0",
#   "jsonschema>=4.0",
# ]
# ///
"""Generic, schema-driven tools for the completed v1 ontology."""
from __future__ import annotations

import os
import sys
from pathlib import Path


def _find_lib() -> Path:
    env = os.environ.get("PROCESSKIT_LIB_PATH")
    if env:
        return Path(env).resolve()
    here = Path(__file__).resolve().parent
    while True:
        for candidate in (here / "src" / "lib", here / "_lib"):
            if (candidate / "processkit" / "__init__.py").is_file():
                return candidate
        if here.parent == here:
            raise RuntimeError("processkit lib not found")
        here = here.parent


sys.path.insert(0, str(_find_lib()))

from mcp.server.fastmcp import FastMCP  # noqa: E402
from mcp.types import ToolAnnotations  # noqa: E402

from processkit import entity, index, log, paths, schema, state_machine  # noqa: E402

server = FastMCP("processkit-ontology-management")

_MANAGED_KINDS = {
    "Archive",
    "Container",
    "EvaluationRun",
    "Iteration",
    "Location",
    "Measurement",
    "ProgramIncrement",
    "Release",
    "Roadmap",
    "ScopePlan",
    "Service",
    "WorkItemTemplate",
}


def _check_kind(kind: str) -> str | None:
    if kind not in _MANAGED_KINDS:
        return (
            f"unsupported generic ontology kind {kind!r}; use its dedicated "
            "domain server or extend ontology-management explicitly"
        )
    return None


def _load(kind: str, entity_id: str) -> entity.Entity | None:
    db = index.open_db()
    try:
        row, _ = index.resolve_entity(db, entity_id, kind=kind)
    finally:
        db.close()
    if row and row.get("path"):
        return entity.load(row["path"])
    candidate = paths.context_dir(kind) / f"{entity_id}.md"
    return entity.load(candidate) if candidate.is_file() else None


def _persist(ent: entity.Entity, event_type: str, summary: str) -> dict:
    ent.write()
    db = index.open_db()
    try:
        index.upsert_entity(db, ent)
    finally:
        db.close()
    event_id = log.log_side_effect(
        ent.kind,
        ent.id,
        event_type,
        summary,
        root=paths.find_project_root(),
        actor=ent.id,
    )
    return {
        "index_updated": True,
        "event_logged": event_id is not None,
        "event_id": event_id,
    }


@server.tool(annotations=ToolAnnotations(
    readOnlyHint=False, destructiveHint=False,
    idempotentHint=False, openWorldHint=False,
))
def create_ontology_entity(kind: str, id: str, spec: dict) -> dict:
    """Create one explicitly identified entity under a generated schema."""
    error = _check_kind(kind)
    if error:
        return {"error": error}
    if _load(kind, id) is not None:
        return {"error": f"{kind} {id!r} already exists"}
    errors = schema.validate_spec(kind, spec)
    if errors:
        return {"error": "schema validation failed", "details": errors}
    ent = entity.new(kind, id, spec)
    target = paths.entity_path(kind, id, ent.created)
    ent.write(target)
    status = _persist(ent, f"{kind.lower()}.created", f"Created {kind} {id}")
    return {"id": id, "kind": kind, "path": str(ent.path), **status}


@server.tool(annotations=ToolAnnotations(
    readOnlyHint=True, destructiveHint=False,
    idempotentHint=True, openWorldHint=False,
))
def get_ontology_entity(kind: str, id: str) -> dict:
    """Read one generic ontology entity."""
    error = _check_kind(kind)
    if error:
        return {"error": error}
    ent = _load(kind, id)
    if ent is None:
        return {"error": f"{kind} {id!r} not found"}
    return {"id": ent.id, "kind": ent.kind, "spec": ent.spec, "path": str(ent.path)}


@server.tool(annotations=ToolAnnotations(
    readOnlyHint=False, destructiveHint=False,
    idempotentHint=False, openWorldHint=False,
))
def update_ontology_entity(kind: str, id: str, changes: dict) -> dict:
    """Merge validated non-state fields into one generic ontology entity."""
    error = _check_kind(kind)
    if error:
        return {"error": error}
    if "state" in changes:
        return {"error": "use transition_ontology_entity for lifecycle state"}
    ent = _load(kind, id)
    if ent is None:
        return {"error": f"{kind} {id!r} not found"}
    candidate = {**ent.spec, **changes}
    errors = schema.validate_spec(kind, candidate)
    if errors:
        return {"error": "schema validation failed", "details": errors}
    ent.spec = candidate
    status = _persist(ent, f"{kind.lower()}.updated", f"Updated {kind} {id}")
    return {"ok": True, "id": id, "updated": sorted(changes), **status}


@server.tool(annotations=ToolAnnotations(
    readOnlyHint=False, destructiveHint=False,
    idempotentHint=False, openWorldHint=False,
))
def transition_ontology_entity(kind: str, id: str, to_state: str) -> dict:
    """Transition a generic ontology entity through its declared machine."""
    error = _check_kind(kind)
    if error:
        return {"error": error}
    ent = _load(kind, id)
    if ent is None:
        return {"error": f"{kind} {id!r} not found"}
    contract = schema.load_schema(kind)
    machine = contract.get("state_machine")
    if not machine:
        return {"error": f"{kind} has no lifecycle state machine"}
    from_state = str(ent.spec.get("state") or "")
    try:
        state_machine.validate_transition(str(machine), from_state, to_state)
    except state_machine.StateMachineError as exc:
        return {"error": str(exc)}
    ent.spec["state"] = to_state
    errors = schema.validate_spec(kind, ent.spec)
    if errors:
        return {"error": "schema validation failed", "details": errors}
    status = _persist(
        ent,
        f"{kind.lower()}.transitioned",
        f"{kind} {id}: {from_state} → {to_state}",
    )
    return {
        "ok": True, "id": id, "from_state": from_state,
        "to_state": to_state, **status,
    }


@server.tool(annotations=ToolAnnotations(
    readOnlyHint=True, destructiveHint=False,
    idempotentHint=True, openWorldHint=False,
))
def list_ontology_entities(kind: str, limit: int = 100) -> list[dict]:
    """List indexed entities for one supported generic ontology kind."""
    error = _check_kind(kind)
    if error:
        return [{"error": error}]
    db = index.open_db()
    try:
        return index.query_entities(db, kind=kind, limit=max(1, min(limit, 500)))
    finally:
        db.close()


if __name__ == "__main__":
    server.run()
