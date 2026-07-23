#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "mcp[cli]>=1.0",
#   "pyyaml>=6.0",
#   "jsonschema>=4.0",
# ]
# ///
"""Lifecycle tools for package-backed v1 Skill entities."""
from __future__ import annotations

import datetime as _dt
import os
import re
import sys
from pathlib import Path
from typing import Any


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

from processkit import API_VERSION, entity, index, log, paths, schema  # noqa: E402
from processkit import state_machine  # noqa: E402
from processkit.frontmatter import parse, render  # noqa: E402

server = FastMCP("processkit-skill-management")

_SAFE_NAME = re.compile(r"^[a-z0-9][a-z0-9-]*$")
_UPDATABLE = {
    "description",
    "version",
    "layer",
    "uses",
    "provides",
    "commands",
    "triggers",
    "owners",
    "capabilities",
}


def _now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")


def _find_manifest(root: Path, name: str) -> Path | None:
    matches = sorted((root / "context" / "skills").glob(f"*/{name}/SKILL.md"))
    return matches[0] if matches else None


def _load_manifest(path: Path) -> tuple[dict[str, Any], str]:
    return parse(path.read_text(encoding="utf-8"))


def _projection(path: Path, manifest: dict, body: str) -> entity.Entity:
    processkit = (manifest.get("metadata") or {}).get("processkit") or {}
    spec = schema.skill_spec_from_manifest(manifest)
    return entity.Entity(
        apiVersion=processkit.get("apiVersion") or API_VERSION,
        kind="Skill",
        metadata={
            "id": processkit.get("id") or f"SKILL-{spec.get('name')}",
            "created": processkit.get("created") or _now_iso(),
        },
        spec=spec,
        body=body,
        path=path,
    )


def _validate(manifest: dict) -> list[str]:
    return schema.validate_spec(
        "Skill", schema.skill_spec_from_manifest(manifest)
    )


def _persist(
    path: Path,
    manifest: dict,
    body: str,
    *,
    event_type: str,
    summary: str,
) -> dict:
    errors = _validate(manifest)
    if errors:
        return {"error": "schema validation failed", "details": errors}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render(manifest, body), encoding="utf-8")
    ent = _projection(path, manifest, body)
    db = index.open_db()
    try:
        index.upsert_entity(db, ent)
    finally:
        db.close()
    event_id = log.log_side_effect(
        "Skill",
        ent.id,
        event_type,
        summary,
        root=paths.find_project_root(),
        actor="processkit-skill-management",
    )
    return {
        "ok": True,
        "id": ent.id,
        "path": str(path),
        "state": ent.spec.get("state"),
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
def create_skill(
    name: str,
    description: str,
    category: str = "processkit",
    version: str = "1.0.0-alpha.1",
    layer: int | None = None,
    body: str = "",
) -> dict:
    """Create a minimal draft Skill package."""
    if not _SAFE_NAME.fullmatch(name) or not _SAFE_NAME.fullmatch(category):
        return {"error": "name and category must be safe kebab-case values"}
    root = paths.find_project_root()
    path = root / "context" / "skills" / category / name / "SKILL.md"
    if path.exists():
        return {"error": f"Skill {name!r} already exists at {path}"}
    processkit: dict[str, Any] = {
        "apiVersion": API_VERSION,
        "id": f"SKILL-{name}",
        "version": version,
        "state": "draft",
        "created": _now_iso(),
        "category": category,
        "provides": {"primitives": [], "mcp_tools": []},
    }
    if layer is not None:
        processkit["layer"] = layer
    manifest = {
        "name": name,
        "description": description,
        "metadata": {"processkit": processkit},
    }
    default_body = (
        f"# {name.replace('-', ' ').title()}\n\n"
        "## Intro\n\nDescribe the skill's purpose.\n"
    )
    return _persist(
        path,
        manifest,
        body.strip() or default_body,
        event_type="skill.implemented",
        summary=f"Created draft Skill {name!r}",
    )


@server.tool(annotations=ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
))
def get_skill(name: str) -> dict:
    """Return a projected Skill package by name."""
    path = _find_manifest(paths.find_project_root(), name)
    if path is None:
        return {"error": f"Skill {name!r} not found"}
    manifest, body = _load_manifest(path)
    ent = _projection(path, manifest, body)
    return {
        "id": ent.id,
        "spec": ent.spec,
        "path": str(path),
        "validation_errors": _validate(manifest),
    }


@server.tool(annotations=ToolAnnotations(
    readOnlyHint=False,
    destructiveHint=False,
    idempotentHint=False,
    openWorldHint=False,
))
def update_skill(name: str, updates: dict[str, Any]) -> dict:
    """Update non-lifecycle fields in a Skill manifest."""
    path = _find_manifest(paths.find_project_root(), name)
    if path is None:
        return {"error": f"Skill {name!r} not found"}
    unknown = sorted(set(updates) - _UPDATABLE)
    if unknown:
        return {"error": f"unsupported update fields: {unknown}"}
    manifest, body = _load_manifest(path)
    processkit = manifest.setdefault("metadata", {}).setdefault(
        "processkit", {}
    )
    changed: list[str] = []
    for field, value in updates.items():
        if field == "description":
            manifest[field] = value
        else:
            processkit[field] = value
        changed.append(field)
    result = _persist(
        path,
        manifest,
        body,
        event_type="skill.updated",
        summary=f"Updated Skill {name!r}: {', '.join(sorted(changed))}",
    )
    if "error" not in result:
        result["updated"] = sorted(changed)
    return result


@server.tool(annotations=ToolAnnotations(
    readOnlyHint=False,
    destructiveHint=False,
    idempotentHint=False,
    openWorldHint=False,
))
def transition_skill(name: str, to_state: str) -> dict:
    """Transition a package-backed Skill through its v1 state machine."""
    path = _find_manifest(paths.find_project_root(), name)
    if path is None:
        return {"error": f"Skill {name!r} not found"}
    manifest, body = _load_manifest(path)
    processkit = manifest.setdefault("metadata", {}).setdefault(
        "processkit", {}
    )
    from_state = str(processkit.get("state") or "active")
    if from_state == to_state:
        result = get_skill(name)
        result.update({"ok": True, "from_state": from_state, "to_state": to_state})
        return result
    try:
        state_machine.validate_transition("skill", from_state, to_state)
    except state_machine.StateMachineError as exc:
        return {"error": str(exc)}
    processkit["state"] = to_state
    result = _persist(
        path,
        manifest,
        body,
        event_type="skill.transitioned",
        summary=f"Skill {name!r}: {from_state} → {to_state}",
    )
    if "error" not in result:
        result.update({"from_state": from_state, "to_state": to_state})
    return result


@server.tool(annotations=ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
))
def list_skills(
    category: str | None = None,
    state: str | None = None,
    limit: int = 200,
) -> list[dict]:
    """List package-backed Skill projections."""
    root = paths.find_project_root() / "context" / "skills"
    pattern = f"{category}/*/SKILL.md" if category else "*/*/SKILL.md"
    results: list[dict] = []
    for path in sorted(root.glob(pattern)):
        manifest, body = _load_manifest(path)
        ent = _projection(path, manifest, body)
        if state is not None and ent.spec.get("state") != state:
            continue
        results.append({
            "id": ent.id,
            "name": ent.spec.get("name"),
            "category": ent.spec.get("category"),
            "version": ent.spec.get("version"),
            "state": ent.spec.get("state"),
            "path": str(path),
        })
        if len(results) >= max(1, min(limit, 500)):
            break
    return results


if __name__ == "__main__":
    server.run(transport="stdio")
