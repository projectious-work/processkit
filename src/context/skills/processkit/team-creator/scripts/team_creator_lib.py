"""team-creator v2 helper library.

Catalog-driven archetype resolution for pk-team-create, pk-team-rebalance,
and pk-team-review. The skill itself is documentation-driven (commands/*.md
narrate the workflow), but the mapping loader is shared by the migration
apply script and the test suite.

Public surface:
  - load_archetype_catalog_mapping(project_root)
  - resolve_archetype(name, mapping)            -> {role, seniority, ...}
  - mapping_source(...)                         -> "kit-default" | "project" | "cli"

The loader implements the layered precedence promised by SKILL.md:

    cli (--archetype-catalog-mapping <path>) > project > kit-default

Project override: context/team/archetype-catalog-mapping.yaml (delta semantics
by default; replace semantics only when the override file declares
``override_semantics: replace`` at the top level).

The kit default ships at
``context/skills/processkit/team-creator/assets/archetype-catalog-mapping.yaml``
and contains the 8 archetypes listed in the SmartPanda design artifact §"Gap 1".
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


# The 8 processkit archetypes (kept as a stable tuple for validation).
ARCHETYPES: tuple[str, ...] = (
    "project-manager",
    "senior-architect",
    "senior-researcher",
    "junior-architect",
    "developer",
    "junior-researcher",
    "junior-developer",
    "assistant",
)


_VALID_OVERRIDE_SEMANTICS = {"delta", "replace"}


# ---------------------------------------------------------------------------
# Kit-default discovery
# ---------------------------------------------------------------------------

def kit_default_mapping_path() -> Path:
    """Return the absolute path to the kit-default mapping shipped here."""
    return Path(__file__).resolve().parent.parent / "assets" / "archetype-catalog-mapping.yaml"


def project_override_mapping_path(project_root: Path) -> Path:
    """Return the project override path.

    Always returned regardless of existence — the caller decides whether
    to apply the override based on ``Path.is_file()``.
    """
    return project_root / "context" / "team" / "archetype-catalog-mapping.yaml"


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------

@dataclass
class ArchetypeMapping:
    """Resolved archetype-to-catalog mapping.

    Attributes
    ----------
    archetypes: dict mapping archetype-name -> {"role": ROLE-id,
        "seniority": <enum>, optional "primary_contact": bool, ...}
    source: "kit-default" | "project" | "cli"
    overrides: list of per-archetype delta entries when source == "project"
        and the project file is in delta mode. Each entry:
        {"archetype": <name>, "field": <name>, "kit_default": ...,
         "project_value": ...}
    semantics: "delta" | "replace" — only meaningful when source == "project"
    """

    archetypes: dict[str, dict[str, Any]]
    source: str = "kit-default"
    overrides: list[dict[str, Any]] = field(default_factory=list)
    semantics: str | None = None
    files: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def _load_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    data = yaml.safe_load(text) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top-level YAML must be a mapping")
    return data


def _extract_archetypes(doc: dict[str, Any], path: Path) -> dict[str, dict[str, Any]]:
    """Pull the ``spec.archetypes`` block (or top-level ``archetypes``)."""
    spec = doc.get("spec") or doc
    archetypes = spec.get("archetypes")
    if not isinstance(archetypes, dict):
        raise ValueError(f"{path}: missing or invalid 'archetypes' map")
    out: dict[str, dict[str, Any]] = {}
    for name, body in archetypes.items():
        if not isinstance(body, dict):
            raise ValueError(f"{path}: archetype {name!r} must be a mapping")
        role = body.get("role")
        seniority = body.get("seniority")
        if not role or not str(role).startswith("ROLE-"):
            raise ValueError(
                f"{path}: archetype {name!r} requires a 'role' starting with 'ROLE-'"
            )
        if not seniority:
            raise ValueError(f"{path}: archetype {name!r} requires a 'seniority'")
        entry: dict[str, Any] = {"role": role, "seniority": seniority}
        for opt in ("primary_contact", "default_model_profile",
                    "effort_floor", "effort_ceiling", "rationale"):
            if opt in body:
                entry[opt] = body[opt]
        out[name] = entry
    return out


def _load_kit_default() -> dict[str, dict[str, Any]]:
    path = kit_default_mapping_path()
    if not path.is_file():
        raise FileNotFoundError(
            f"kit-default mapping missing at {path} — team-creator install corrupted?"
        )
    doc = _load_yaml(path)
    return _extract_archetypes(doc, path)


def _validate_replace_completeness(archetypes: dict[str, dict[str, Any]],
                                    path: Path) -> None:
    missing = [a for a in ARCHETYPES if a not in archetypes]
    if missing:
        raise ValueError(
            f"{path}: replace-mode override missing archetypes: {missing!r}"
        )


def load_archetype_catalog_mapping(
    project_root: Path,
    cli_path: Path | None = None,
) -> ArchetypeMapping:
    """Load the archetype→catalog mapping with three-level precedence.

    Order:
      1. ``cli_path`` (if supplied; mode determined by file's
         ``override_semantics``)
      2. ``<project_root>/context/team/archetype-catalog-mapping.yaml``
      3. kit default shipped under team-creator/assets/

    Returns an :class:`ArchetypeMapping` describing the resolved set,
    its source, and any per-archetype delta entries.
    """
    project_root = Path(project_root)
    kit_archetypes = _load_kit_default()
    files: list[str] = [str(kit_default_mapping_path())]

    # --- Layer 1: CLI ------------------------------------------------------
    if cli_path is not None:
        cli_path = Path(cli_path)
        if not cli_path.is_file():
            raise FileNotFoundError(
                f"--archetype-catalog-mapping {cli_path} not found"
            )
        doc = _load_yaml(cli_path)
        semantics = doc.get("override_semantics", "replace")
        if semantics not in _VALID_OVERRIDE_SEMANTICS:
            raise ValueError(
                f"{cli_path}: override_semantics must be 'delta' or 'replace'; "
                f"got {semantics!r}"
            )
        cli_archetypes = _extract_archetypes(doc, cli_path)
        if semantics == "replace":
            _validate_replace_completeness(cli_archetypes, cli_path)
            merged = cli_archetypes
        else:
            merged = {**kit_archetypes, **cli_archetypes}
        overrides = _delta_overrides(kit_archetypes, cli_archetypes)
        files.append(str(cli_path))
        return ArchetypeMapping(
            archetypes=merged,
            source="cli",
            overrides=overrides,
            semantics=semantics,
            files=files,
        )

    # --- Layer 2: Project override ----------------------------------------
    proj_path = project_override_mapping_path(project_root)
    if proj_path.is_file():
        doc = _load_yaml(proj_path)
        semantics = doc.get("override_semantics", "delta")
        if semantics not in _VALID_OVERRIDE_SEMANTICS:
            raise ValueError(
                f"{proj_path}: override_semantics must be 'delta' or 'replace'; "
                f"got {semantics!r}"
            )
        proj_archetypes = _extract_archetypes(doc, proj_path)
        if semantics == "replace":
            _validate_replace_completeness(proj_archetypes, proj_path)
            merged = proj_archetypes
        else:
            merged = {**kit_archetypes, **proj_archetypes}
        overrides = _delta_overrides(kit_archetypes, proj_archetypes)
        files.append(str(proj_path))
        return ArchetypeMapping(
            archetypes=merged,
            source="project",
            overrides=overrides,
            semantics=semantics,
            files=files,
        )

    # --- Layer 3: kit default ---------------------------------------------
    return ArchetypeMapping(
        archetypes=kit_archetypes,
        source="kit-default",
        overrides=[],
        semantics=None,
        files=files,
    )


def _delta_overrides(
    kit: dict[str, dict[str, Any]],
    layer: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Return per-archetype-per-field delta entries.

    Used for the chartering DEC's ``inputs_snapshot.archetype_catalog_overrides``
    audit field.
    """
    out: list[dict[str, Any]] = []
    for name, entry in layer.items():
        kit_entry = kit.get(name) or {}
        for fld, val in entry.items():
            kit_val = kit_entry.get(fld)
            if kit_val != val:
                out.append({
                    "archetype": name,
                    "field": fld,
                    "kit_default": kit_val,
                    "project_value": val,
                })
        # New archetype not in kit: treat as a single "add" entry
        if name not in kit:
            out.append({
                "archetype": name,
                "field": "*",
                "kit_default": None,
                "project_value": "<new archetype>",
            })
    return out


def resolve_archetype(name: str, mapping: ArchetypeMapping) -> dict[str, Any]:
    """Look up an archetype in the resolved mapping. KeyError on miss."""
    if name not in mapping.archetypes:
        raise KeyError(
            f"archetype {name!r} not found in mapping (source={mapping.source}); "
            f"known archetypes: {sorted(mapping.archetypes)}"
        )
    return mapping.archetypes[name]


def archetype_for_role_slot(
    role: str, seniority: str, mapping: ArchetypeMapping,
) -> str | None:
    """Reverse lookup: given (role, seniority), return the archetype name.

    Used by pk-team-review for human-readable diff labels. Returns None
    when no archetype maps to the (role, seniority) pair.
    """
    for name, entry in mapping.archetypes.items():
        if entry["role"] == role and entry["seniority"] == seniority:
            return name
    return None
