"""Locate the project root, processkit checkout, and per-kind directories.

Project layout (consumer side, post aibox-handover-v2):

    <project-root>/
      aibox.toml
      aibox.lock
      context/
        skills/<name>/...           ← installed processkit skills
        skills/_lib/processkit/...  ← installed processkit lib
        schemas/<f>.yaml            ← installed primitive schemas
        state-machines/<f>.yaml     ← installed state machines
        processes/<f>.md            ← installed process definitions
        templates/processkit/<v>/   ← full upstream reference templates
        workitems/, decisions/, logs/, ...
        .cache/processkit/          ← gitignored runtime cache (index DB)

Processkit checkout layout (this repo, when running servers from
a checkout):

    <processkit-root>/
      aibox.toml
      src/
        primitives/
        skills/
        lib/
      context/

Servers may be invoked in either context. The functions here resolve
paths conservatively: walk upward from `cwd` looking for an `aibox.toml`
file, treat that directory as the project root, and resolve `context/`
relative to it. If no aibox.toml is found, fall back to the current
directory.
"""
from __future__ import annotations

import os
from pathlib import Path

from . import DEFAULT_DIRS

PROJECT_MARKER = "aibox.toml"


def find_project_root(start: Path | str | None = None) -> Path:
    """Walk upward from ``start`` (default: cwd) looking for ``aibox.toml``.

    Returns the directory containing the marker. If none is found, returns
    the starting directory itself (so the caller can still proceed with
    sensible defaults rather than crashing).
    """
    here = Path(start) if start else Path.cwd()
    here = here.resolve()
    if here.is_file():
        here = here.parent
    candidate = here
    while True:
        if (candidate / PROJECT_MARKER).is_file():
            return candidate
        if candidate.parent == candidate:
            return here
        candidate = candidate.parent


def find_processkit_root(server_path: Path | str) -> Path | None:
    """Locate the processkit checkout root containing ``server_path``.

    Looks for ``src/lib/processkit/__init__.py`` upward from the given
    server script. Returns the directory containing ``src/`` or None if
    the script is not running from a processkit checkout (e.g. installed
    by aibox into ``context/skills/``).
    """
    here = Path(server_path).resolve().parent
    while True:
        if (here / "src" / "lib" / "processkit" / "__init__.py").is_file():
            return here
        if here.parent == here:
            return None
        here = here.parent


def context_dir(kind: str, root: Path | str | None = None) -> Path:
    """Return the directory under ``context/`` where entities of ``kind`` live.

    Reads `[context.directories.<kind>]` from aibox.toml if present;
    otherwise uses the default subdirectory from ``DEFAULT_DIRS``.
    """
    root = Path(root) if root else find_project_root()
    overrides = _read_directory_overrides(root)
    sub = overrides.get(kind, DEFAULT_DIRS.get(kind, kind.lower()))
    target = root / "context" / sub
    return target


def primitive_schemas_dir(root: Path | str | None = None) -> Path | None:
    """Where the JSON-Schema YAML files live.

    Tries the consumer's installed location (``context/schemas/``)
    first, then the processkit checkout (``src/primitives/schemas/``).
    Returns None if neither exists.
    """
    root = Path(root) if root else find_project_root()
    consumer = root / "context" / "schemas"
    if consumer.is_dir():
        return consumer
    processkit = root / "src" / "primitives" / "schemas"
    if processkit.is_dir():
        return processkit
    return None


def state_machines_dir(root: Path | str | None = None) -> Path | None:
    """Where state machine YAML files live.

    Tries the consumer's installed location (``context/state-machines/``)
    first, then the processkit checkout
    (``src/primitives/state-machines/``). Returns None if neither
    exists.
    """
    root = Path(root) if root else find_project_root()
    consumer = root / "context" / "state-machines"
    if consumer.is_dir():
        return consumer
    processkit = root / "src" / "primitives" / "state-machines"
    if processkit.is_dir():
        return processkit
    return None


def index_db_path(root: Path | str | None = None) -> Path:
    """Path to the SQLite index database (gitignored runtime cache)."""
    root = Path(root) if root else find_project_root()
    db_dir = root / "context" / ".cache" / "processkit"
    db_dir.mkdir(parents=True, exist_ok=True)
    return db_dir / "index.sqlite"


def _read_directory_overrides(root: Path) -> dict[str, str]:
    toml_path = root / PROJECT_MARKER
    if not toml_path.is_file():
        return {}
    try:
        import tomllib  # py 3.11+
    except ModuleNotFoundError:
        try:
            import tomli as tomllib  # type: ignore
        except ModuleNotFoundError:
            return {}
    try:
        data = tomllib.loads(toml_path.read_text())
    except Exception:
        return {}
    return (
        data.get("context", {})
        .get("directories", {})
        if isinstance(data, dict)
        else {}
    )


def env_override(name: str) -> Path | None:
    """Return an env-var path override if set, else None."""
    value = os.environ.get(name)
    return Path(value) if value else None
