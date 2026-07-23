#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "mcp[cli]>=1.0",
#   "pyyaml>=6.0",
#   "jsonschema>=4.0",
# ]
# ///
"""Capability lifecycle tools for the processkit v1 contract."""
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

from processkit import config, entity, ids, index, log, paths, schema  # noqa: E402
from processkit import state_machine  # noqa: E402

server = FastMCP("processkit-capability-management")

_UPDATABLE = {
    "name",
    "description",
    "owner",
    "providers",
    "consumers",
    "inputs",
    "outputs",
    "constraints",
    "evidence",
    "supersedes",
}


def _load(root: Path, capability_id: str) -> entity.Entity | None:
    candidate = paths.context_dir("Capability", root) / f"{capability_id}.md"
    if candidate.is_file():
        return entity.load(candidate)
    db = index.open_db()
    try:
        row, _ = index.resolve_entity(db, capability_id, kind="Capability")
    finally:
        db.close()
    if row and row.get("path"):
        return entity.load(row["path"])
    return None


def _persist(
    ent: entity.Entity,
    *,
    root: Path,
    event_type: str,
    summary: str,
) -> dict:
    ent.write()
    db = index.open_db()
    try:
        index.upsert_entity(db, ent)
    finally:
        db.close()
    event_id = log.log_side_effect(
        "Capability",
        ent.id,
        event_type,
        summary,
        root=root,
        actor=ent.id,
    )
    return {
        "index_updated": True,
        "event_logged": event_id is not None,
        "event_id": event_id,
    }


@server.tool(annotations=ToolAnnotations(
    readOnlyHint=False,
    destructiveHint=False,
    idempotentHint=False,
    openWorldHint=False,
))
def create_capability(
    name: str,
    description: str,
    owner: str | None = None,
    providers: list[str] | None = None,
    consumers: list[str] | None = None,
    inputs: list[str] | None = None,
    outputs: list[str] | None = None,
    constraints: list[str] | None = None,
    evidence: list[str] | None = None,
) -> dict:
    """Create a draft Capability under the generated v1 schema."""
    root = paths.find_project_root()
    cfg = config.load_config(root)
    db = index.open_db()
    try:
        existing = index.existing_ids(db, "Capability")
    finally:
        db.close()
    capability_id = ids.generate_id(
        "Capability",
        format=cfg.id_format,
        word_style=cfg.id_word_style,
        datetime_prefix=cfg.id_datetime_prefix,
        slug_text=name if cfg.id_slug else None,
        existing=existing,
    )
    spec = {
        "name": name,
        "description": description,
        "kind": "ability",
        "state": "draft",
    }
    for field, value in {
        "owner": owner,
        "providers": providers,
        "consumers": consumers,
        "inputs": inputs,
        "outputs": outputs,
        "constraints": constraints,
        "evidence": evidence,
    }.items():
        if value is not None:
            spec[field] = value
    errors = schema.validate_spec("Capability", spec)
    if errors:
        return {"error": "schema validation failed", "details": errors}
    ent = entity.new("Capability", capability_id, spec)
    target = paths.context_dir("Capability", root) / f"{capability_id}.md"
    ent.write(target)
    status = _persist(
        ent,
        root=root,
        event_type="capability.created",
        summary=f"Created Capability {capability_id!r}: {name!r}",
    )
    return {
        "id": capability_id,
        "path": str(ent.path),
        "state": "draft",
        **status,
    }


@server.tool(annotations=ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
))
def get_capability(id: str) -> dict:
    """Return one Capability by ID."""
    ent = _load(paths.find_project_root(), id)
    if ent is None:
        return {"error": f"Capability {id!r} not found"}
    return {"id": ent.id, "spec": ent.spec, "path": str(ent.path)}


@server.tool(annotations=ToolAnnotations(
    readOnlyHint=False,
    destructiveHint=False,
    idempotentHint=False,
    openWorldHint=False,
))
def update_capability(
    id: str,
    name: str | None = None,
    description: str | None = None,
    owner: str | None = None,
    providers: list[str] | None = None,
    consumers: list[str] | None = None,
    inputs: list[str] | None = None,
    outputs: list[str] | None = None,
    constraints: list[str] | None = None,
    evidence: list[str] | None = None,
    supersedes: str | None = None,
) -> dict:
    """Update non-lifecycle Capability fields."""
    root = paths.find_project_root()
    ent = _load(root, id)
    if ent is None:
        return {"error": f"Capability {id!r} not found"}
    supplied = locals()
    updated = []
    for field in sorted(_UPDATABLE):
        value = supplied.get(field)
        if value is not None:
            ent.spec[field] = value
            updated.append(field)
    if not updated:
        return {"ok": True, "id": id, "updated": []}
    errors = schema.validate_spec("Capability", ent.spec)
    if errors:
        return {"error": "schema validation failed", "details": errors}
    status = _persist(
        ent,
        root=root,
        event_type="capability.updated",
        summary=f"Updated Capability {id!r}: {', '.join(updated)}",
    )
    return {"ok": True, "id": id, "updated": updated, **status}


@server.tool(annotations=ToolAnnotations(
    readOnlyHint=False,
    destructiveHint=False,
    idempotentHint=False,
    openWorldHint=False,
))
def transition_capability(id: str, to_state: str) -> dict:
    """Transition a Capability through its generated state machine."""
    root = paths.find_project_root()
    ent = _load(root, id)
    if ent is None:
        return {"error": f"Capability {id!r} not found"}
    from_state = str(ent.spec.get("state") or "")
    try:
        state_machine.validate_transition(
            "capability",
            from_state,
            to_state,
        )
    except state_machine.StateMachineError as exc:
        return {"error": str(exc)}
    ent.spec["state"] = to_state
    errors = schema.validate_spec("Capability", ent.spec)
    if errors:
        return {"error": "schema validation failed", "details": errors}
    status = _persist(
        ent,
        root=root,
        event_type="capability.transitioned",
        summary=f"Capability {id!r}: {from_state} → {to_state}",
    )
    return {
        "ok": True,
        "id": id,
        "from_state": from_state,
        "to_state": to_state,
        **status,
    }


@server.tool(annotations=ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
))
def list_capabilities(
    state: str | None = None,
    limit: int = 50,
) -> list[dict]:
    """List indexed Capabilities, optionally filtered by lifecycle state."""
    db = index.open_db()
    try:
        return index.query_entities(
            db,
            kind="Capability",
            state=state,
            limit=limit,
        )
    finally:
        db.close()


if __name__ == "__main__":
    server.run(transport="stdio")
