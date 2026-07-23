"""Deterministic v0.x to v1 ontology migration planning and execution."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from . import API_VERSION, entity, schema


class CorpusMigrationError(ValueError):
    """Raised when a migration plan is stale or cannot be applied safely."""


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _entity_paths(root: Path) -> list[Path]:
    context = root / "context"
    if not context.is_dir():
        return []
    paths: list[Path] = []
    for path in context.rglob("*.md"):
        relative = path.relative_to(context)
        if relative.parts and relative.parts[0] in {"templates", "skills"}:
            continue
        paths.append(path)
    return sorted(paths)


def _normalize_datetime(value: Any) -> Any:
    text = str(value)
    if len(text) == 10 and text[4] == "-" and text[7] == "-":
        return f"{text}T00:00:00Z"
    return value


def _transform(ent: entity.Entity) -> tuple[entity.Entity, list[str]]:
    changes: list[str] = []
    if ent.apiVersion != API_VERSION:
        ent.apiVersion = API_VERSION
        changes.append("apiVersion")
    if ent.kind == "Scope":
        legacy_type = ent.spec.get("kind")
        ent.kind = "Container"
        ent.spec["kind"] = "scope"
        if legacy_type and legacy_type != "scope":
            ent.spec["scope_type"] = legacy_type
        for field in ("starts_at", "ends_at"):
            if field in ent.spec:
                ent.spec[field] = _normalize_datetime(ent.spec[field])
        changes.append("Scope→Container(scope)")
    return ent, changes


def _field_count(value: Any) -> int:
    if isinstance(value, dict):
        return len(value) + sum(_field_count(item) for item in value.values())
    if isinstance(value, list):
        return sum(_field_count(item) for item in value)
    return 0


def plan_v0_to_v1(
    root: Path | str,
    *,
    source_version: str = "v0.28.3",
    target_version: str = "v1.0.0-alpha.1",
) -> dict[str, Any]:
    """Return a deterministic, non-writing corpus migration plan."""
    root = Path(root).resolve()
    operations: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    source_hashes: list[str] = []
    for path in _entity_paths(root):
        before = path.read_bytes()
        relative = path.relative_to(root).as_posix()
        source_hashes.append(f"{relative}:{_sha256(before)}")
        try:
            ent = entity.from_text(before.decode("utf-8"), path)
        except entity.NotAnEntityError:
            continue
        except (UnicodeDecodeError, entity.EntityError) as exc:
            errors.append({"path": relative, "error": str(exc)})
            continue
        before_fields = _field_count(ent.to_dict())
        transformed, changes = _transform(ent)
        if not changes:
            continue
        validation_errors = schema.validate_spec(
            transformed.kind,
            transformed.spec,
        )
        if validation_errors:
            errors.append({
                "path": relative,
                "error": "; ".join(validation_errors),
            })
            continue
        after = transformed.to_text().encode("utf-8")
        after_fields = _field_count(transformed.to_dict())
        operations.append({
            "path": relative,
            "source_sha256": _sha256(before),
            "target_sha256": _sha256(after),
            "changes": changes,
            "source_field_count": before_fields,
            "target_field_count": after_fields,
            "field_loss_count": max(0, before_fields - after_fields),
        })
    tree_hash = _sha256("\n".join(source_hashes).encode("utf-8"))
    plan_material = {
        "source_processkit_version": source_version,
        "target_processkit_version": target_version,
        "target_api_version": API_VERSION,
        "source_tree_sha256": tree_hash,
        "operations": operations,
        "errors": errors,
    }
    plan_id = f"v0-v1-{_sha256(json.dumps(plan_material, sort_keys=True).encode())[:16]}"
    total_source = sum(item["source_field_count"] for item in operations)
    total_loss = sum(item["field_loss_count"] for item in operations)
    return {
        "plan_id": plan_id,
        **plan_material,
        "operation_count": len(operations),
        "field_loss_count": total_loss,
        "field_loss_percent": (
            round(total_loss * 100 / total_source, 4)
            if total_source
            else 0.0
        ),
    }


def execute_v0_to_v1(
    root: Path | str,
    plan: dict[str, Any],
) -> dict[str, Any]:
    """Validate every precondition, then apply the supplied plan."""
    root = Path(root).resolve()
    if plan.get("errors"):
        raise CorpusMigrationError("cannot execute a plan containing errors")
    staged: list[tuple[Path, bytes]] = []
    for operation in plan.get("operations") or []:
        path = (root / operation["path"]).resolve()
        try:
            path.relative_to(root)
        except ValueError as exc:
            raise CorpusMigrationError("plan path escapes project root") from exc
        before = path.read_bytes()
        actual = _sha256(before)
        if actual != operation["source_sha256"]:
            raise CorpusMigrationError(
                f"source hash changed for {operation['path']}: "
                f"expected {operation['source_sha256']}, got {actual}"
            )
        ent = entity.from_text(before.decode("utf-8"), path)
        transformed, changes = _transform(ent)
        if changes != operation["changes"]:
            raise CorpusMigrationError(
                f"planned transformation changed for {operation['path']}"
            )
        errors = schema.validate_spec(transformed.kind, transformed.spec)
        if errors:
            raise CorpusMigrationError(
                f"target validation failed for {operation['path']}: "
                f"{'; '.join(errors)}"
            )
        after = transformed.to_text().encode("utf-8")
        if _sha256(after) != operation["target_sha256"]:
            raise CorpusMigrationError(
                f"target hash changed for {operation['path']}"
            )
        staged.append((path, after))

    for path, payload in staged:
        temporary = path.with_name(f".{path.name}.{plan['plan_id']}.tmp")
        temporary.write_bytes(payload)
        os.replace(temporary, path)

    journal = root / ".processkit" / "migrations" / f"{plan['plan_id']}.json"
    journal.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "plan_id": plan["plan_id"],
        "applied": len(staged),
        "field_loss_count": plan.get("field_loss_count", 0),
        "field_loss_percent": plan.get("field_loss_percent", 0.0),
        "paths": [path.relative_to(root).as_posix() for path, _ in staged],
    }
    journal.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {**report, "journal": str(journal)}
