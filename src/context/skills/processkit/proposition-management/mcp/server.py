#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "mcp[cli]>=1.0",
#   "pyyaml>=6.0",
#   "jsonschema>=4.0",
# ]
# ///
"""Claim and risk tools for the processkit v1 Proposition contract."""
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

server = FastMCP("processkit-proposition-management")

_KINDS = {"claim", "risk"}
_FIELDS = {
    "statement",
    "status",
    "confidence",
    "owner",
    "evidence",
    "scope",
    "source",
    "valid_from",
    "valid_until",
    "supersedes",
    "likelihood",
    "probability",
    "impact",
    "risk_status",
    "response",
    "mitigation",
    "contingency",
    "affected_entities",
    "review_at",
    "realized_at",
}


def _load(root: Path, proposition_id: str) -> entity.Entity | None:
    candidate = paths.context_dir("Proposition", root) / f"{proposition_id}.md"
    if candidate.is_file():
        return entity.load(candidate)
    db = index.open_db()
    try:
        row, _ = index.resolve_entity(db, proposition_id, kind="Proposition")
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
        "Proposition",
        ent.id,
        event_type,
        summary,
        root=root,
        actor=ent.spec.get("owner") or ent.id,
        details={"discriminator": ent.spec.get("kind")},
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
def create_proposition(
    statement: str,
    kind: str = "claim",
    status: str | None = None,
    confidence: float | None = None,
    owner: str | None = None,
    evidence: list[str] | None = None,
    scope: str | None = None,
    source: str | None = None,
    likelihood: str | None = None,
    probability: float | None = None,
    impact: str | None = None,
    risk_status: str | None = None,
    response: str | None = None,
    mitigation: str | None = None,
    contingency: str | None = None,
    affected_entities: list[str] | None = None,
    review_at: str | None = None,
) -> dict:
    """Create a claim or Risk discriminator under one Proposition kind."""
    if kind not in _KINDS:
        return {"error": f"kind must be one of {sorted(_KINDS)}"}
    root = paths.find_project_root()
    cfg = config.load_config(root)
    db = index.open_db()
    try:
        existing = index.existing_ids(db, "Proposition")
    finally:
        db.close()
    proposition_id = ids.generate_id(
        "Proposition",
        format=cfg.id_format,
        word_style=cfg.id_word_style,
        datetime_prefix=cfg.id_datetime_prefix,
        slug_text=statement if cfg.id_slug else None,
        existing=existing,
    )
    spec = {"kind": kind, "statement": statement}
    values = {
        "status": status,
        "confidence": confidence,
        "owner": owner,
        "evidence": evidence,
        "scope": scope,
        "source": source,
        "likelihood": likelihood,
        "probability": probability,
        "impact": impact,
        "risk_status": risk_status,
        "response": response,
        "mitigation": mitigation,
        "contingency": contingency,
        "affected_entities": affected_entities,
        "review_at": review_at,
    }
    for field, value in values.items():
        if value is not None:
            spec[field] = value
    errors = schema.validate_spec("Proposition", spec)
    if errors:
        return {"error": "schema validation failed", "details": errors}
    ent = entity.new("Proposition", proposition_id, spec)
    target = paths.context_dir("Proposition", root) / f"{proposition_id}.md"
    ent.write(target)
    persistence = _persist(
        ent,
        root=root,
        event_type="proposition.created",
        summary=f"Created {kind} Proposition {proposition_id!r}",
    )
    return {
        "id": proposition_id,
        "kind": kind,
        "path": str(ent.path),
        **persistence,
    }


@server.tool(annotations=ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
))
def get_proposition(id: str) -> dict:
    """Return one Proposition by ID."""
    ent = _load(paths.find_project_root(), id)
    if ent is None:
        return {"error": f"Proposition {id!r} not found"}
    return {"id": ent.id, "spec": ent.spec, "path": str(ent.path)}


@server.tool(annotations=ToolAnnotations(
    readOnlyHint=False,
    destructiveHint=False,
    idempotentHint=False,
    openWorldHint=False,
))
def update_proposition(
    id: str,
    statement: str | None = None,
    status: str | None = None,
    confidence: float | None = None,
    owner: str | None = None,
    evidence: list[str] | None = None,
    scope: str | None = None,
    source: str | None = None,
    valid_from: str | None = None,
    valid_until: str | None = None,
    supersedes: str | None = None,
    likelihood: str | None = None,
    probability: float | None = None,
    impact: str | None = None,
    risk_status: str | None = None,
    response: str | None = None,
    mitigation: str | None = None,
    contingency: str | None = None,
    affected_entities: list[str] | None = None,
    review_at: str | None = None,
    realized_at: str | None = None,
) -> dict:
    """Update a Proposition while preserving its discriminator."""
    root = paths.find_project_root()
    ent = _load(root, id)
    if ent is None:
        return {"error": f"Proposition {id!r} not found"}
    supplied = locals()
    updated = []
    for field in sorted(_FIELDS):
        value = supplied.get(field)
        if value is not None:
            ent.spec[field] = value
            updated.append(field)
    if not updated:
        return {"ok": True, "id": id, "updated": []}
    errors = schema.validate_spec("Proposition", ent.spec)
    if errors:
        return {"error": "schema validation failed", "details": errors}
    persistence = _persist(
        ent,
        root=root,
        event_type="proposition.updated",
        summary=f"Updated Proposition {id!r}: {', '.join(updated)}",
    )
    return {"ok": True, "id": id, "updated": updated, **persistence}


@server.tool(annotations=ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
))
def query_propositions(
    kind: str | None = None,
    status: str | None = None,
    limit: int = 50,
) -> list[dict]:
    """Query Propositions by discriminator and epistemic status."""
    if kind is not None and kind not in _KINDS:
        return [{"error": f"kind must be one of {sorted(_KINDS)}"}]
    db = index.open_db()
    try:
        rows = index.query_by_interface(
            db,
            "Proposition",
            kind="Proposition",
            limit=limit,
        )
        out = []
        for row in rows:
            if kind is not None and row.get("discriminator") != kind:
                continue
            loaded = index.get_entity(db, row["id"])
            spec = (loaded or {}).get("spec") or {}
            if status is not None and spec.get("status") != status:
                continue
            out.append({**row, "spec": spec})
        return out
    finally:
        db.close()


if __name__ == "__main__":
    server.run(transport="stdio")
