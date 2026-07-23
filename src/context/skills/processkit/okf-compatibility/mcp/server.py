#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "mcp[cli]>=1.0",
#   "pyyaml>=6.0",
# ]
# ///
"""Open Knowledge Format v0.1 export and validation tools."""
from __future__ import annotations

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

from processkit import entity, log, paths, schema  # noqa: E402
from processkit.frontmatter import FrontmatterError, parse, render  # noqa: E402

server = FastMCP("processkit-okf-compatibility")

_ID_TOKEN = re.compile(r"\b[A-Z][A-Z0-9]*-[A-Za-z0-9_-]+\b")
_MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def _safe_output(root: Path, output_dir: str) -> Path:
    raw = Path(output_dir)
    target = raw if raw.is_absolute() else root / raw
    resolved = target.resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError("output_dir must remain beneath the project root")
    return resolved


def _entities(root: Path, kinds: list[str] | None) -> list[entity.Entity]:
    selected = set(kinds or [])
    results: list[entity.Entity] = []
    for path in sorted((root / "context").rglob("*.md")):
        if any(part in {"skills", "templates", "archives"} for part in path.parts):
            continue
        try:
            ent = entity.load(path)
        except entity.EntityError:
            continue
        if selected and ent.kind not in selected:
            continue
        results.append(ent)
    return results


def _slug_kind(kind: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "-", kind).lower()


def _description(ent: entity.Entity) -> str | None:
    value = ent.spec.get("description") or ent.spec.get("summary")
    return str(value) if value else None


def _relations(ent: entity.Entity, known_ids: set[str]) -> list[dict]:
    found: list[dict] = []
    for field, value in sorted(ent.spec.items()):
        values = value if isinstance(value, list) else [value]
        for item in values:
            if isinstance(item, str) and item in known_ids:
                found.append({"type": field, "target": item})
    return found


def _document_path(bundle: Path, ent: entity.Entity) -> Path:
    return bundle / "concepts" / _slug_kind(ent.kind) / f"{ent.id}.md"


@server.tool(annotations=ToolAnnotations(
    readOnlyHint=False,
    destructiveHint=False,
    idempotentHint=False,
    openWorldHint=False,
))
def export_okf_bundle(
    output_dir: str = ".processkit/exports/okf-alpha",
    kinds: list[str] | None = None,
    include_log_summary: bool = True,
) -> dict:
    """Export selected processkit entities into a new OKF v0.1 bundle."""
    root = paths.find_project_root()
    try:
        bundle = _safe_output(root, output_dir)
    except ValueError as exc:
        return {"error": str(exc)}
    if bundle.exists():
        return {"error": f"output directory already exists: {bundle}"}

    entities = _entities(root, kinds)
    known_ids = {ent.id for ent in entities}
    locations = {ent.id: _document_path(bundle, ent) for ent in entities}
    bundle.mkdir(parents=True)
    exported: list[str] = []
    relation_count = 0

    for ent in entities:
        destination = locations[ent.id]
        destination.parent.mkdir(parents=True, exist_ok=True)
        relations = _relations(ent, known_ids)
        relation_count += len(relations)
        title = (
            ent.spec.get("title")
            or ent.spec.get("name")
            or ent.spec.get("summary")
            or ent.id
        )
        frontmatter: dict[str, Any] = {
            "type": f"processkit.{_slug_kind(ent.kind)}",
            "title": str(title),
            "timestamp": str(ent.updated or ent.created),
            "processkit_id": ent.id,
            "processkit_kind": ent.kind,
            "processkit_interfaces": schema.interfaces_for_kind(
                ent.kind,
                discriminator=schema.discriminator_for_kind(ent.kind, ent.spec),
            ),
        }
        description = _description(ent)
        if description:
            frontmatter["description"] = description
        if ent.labels:
            frontmatter["tags"] = sorted(ent.labels)
        if relations:
            frontmatter["processkit_relations"] = relations
        body = ent.body.strip()
        if relations:
            links = []
            for relation in relations:
                target = locations[relation["target"]]
                relative = os.path.relpath(target, destination.parent)
                links.append(
                    f"- {relation['type']}: "
                    f"[{relation['target']}]({relative})"
                )
            body = f"{body}\n\n## Related\n\n" + "\n".join(links)
        destination.write_text(
            render(frontmatter, body.strip() + "\n"),
            encoding="utf-8",
        )
        exported.append(str(destination.relative_to(bundle)))

    index_lines = ["# processkit OKF export", ""]
    index_lines.extend(
        f"- [{ent.id}]({locations[ent.id].relative_to(bundle)})"
        for ent in entities
    )
    (bundle / "index.md").write_text(
        "\n".join(index_lines) + "\n", encoding="utf-8"
    )
    if include_log_summary:
        log_entities = [ent for ent in entities if ent.kind == "LogEntry"]
        lines = ["# Event summary", ""]
        lines.extend(
            f"- {ent.spec.get('timestamp', ent.created)} "
            f"{ent.spec.get('event_type', 'event')}: "
            f"{ent.spec.get('summary', ent.id)}"
            for ent in log_entities
        )
        (bundle / "log.md").write_text(
            "\n".join(lines) + "\n", encoding="utf-8"
        )

    validation = _validate(bundle)
    event_id = log.log_side_effect(
        "Artifact",
        "okf-alpha",
        "okf.bundle-exported",
        f"Exported {len(exported)} entities as OKF v0.1",
        root=root,
        actor="processkit-okf-compatibility",
        details={
            "output_dir": str(bundle.relative_to(root)),
            "entity_count": len(exported),
            "relation_count": relation_count,
        },
    )
    return {
        "ok": validation["valid"],
        "bundle": str(bundle),
        "profile": "okf-v0.1",
        "entity_count": len(exported),
        "relation_count": relation_count,
        "files": exported,
        "validation": validation,
        "event_logged": event_id is not None,
        "event_id": event_id,
    }


def _validate(bundle: Path) -> dict:
    errors: list[dict] = []
    documents = sorted((bundle / "concepts").rglob("*.md"))
    for path in documents:
        try:
            frontmatter, _body = parse(path.read_text(encoding="utf-8"))
        except (OSError, FrontmatterError) as exc:
            errors.append({"path": str(path), "error": str(exc)})
            continue
        if not isinstance(frontmatter.get("type"), str):
            errors.append({
                "path": str(path),
                "error": "OKF v0.1 requires string frontmatter.type",
            })
        text = path.read_text(encoding="utf-8")
        for href in _MARKDOWN_LINK.findall(text):
            if "://" in href or href.startswith("#"):
                continue
            target = (path.parent / href.split("#", 1)[0]).resolve()
            if not target.exists():
                errors.append({
                    "path": str(path),
                    "error": f"broken internal link: {href}",
                })
    return {
        "valid": not errors,
        "profile": "okf-v0.1",
        "document_count": len(documents),
        "errors": errors,
    }


@server.tool(annotations=ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
))
def validate_okf_bundle(bundle_dir: str) -> dict:
    """Validate an OKF v0.1 bundle and its internal Markdown links."""
    root = paths.find_project_root()
    try:
        bundle = _safe_output(root, bundle_dir)
    except ValueError as exc:
        return {"valid": False, "errors": [{"error": str(exc)}]}
    if not bundle.is_dir():
        return {
            "valid": False,
            "errors": [{"error": f"bundle directory not found: {bundle}"}],
        }
    return _validate(bundle)


if __name__ == "__main__":
    server.run(transport="stdio")
