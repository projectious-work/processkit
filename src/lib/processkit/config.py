"""Read processkit-relevant settings from aibox.toml.

aibox.toml is the consumer project's configuration. The sections relevant
to MCP servers are:

    [context]
    id_format = "word"        # word | uuid
    id_slug = false

    [context.directories]
    WorkItem = "workitems"
    LogEntry = "logs"
    DecisionRecord = "decisions"

    [context.sharding.LogEntry]
    scheme = "date"
    pattern = "context/logs/{year}/{month}/"

If the file is missing or unparseable, defaults apply.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from . import paths


@dataclass
class Config:
    id_format: str = "word"
    id_slug: bool = False
    directory_overrides: dict[str, str] | None = None
    sharding: dict[str, dict[str, Any]] | None = None

    def directory_for(self, kind: str) -> str | None:
        return (self.directory_overrides or {}).get(kind)


@lru_cache(maxsize=4)
def load_config(root: Path | None = None) -> Config:
    """Load processkit settings from the project's aibox.toml.

    Cached per-root. Returns defaults if the file is missing.
    """
    root = root or paths.find_project_root()
    toml_path = root / "aibox.toml"
    if not toml_path.is_file():
        return Config()
    try:
        import tomllib  # py 3.11+
    except ModuleNotFoundError:
        try:
            import tomli as tomllib  # type: ignore
        except ModuleNotFoundError:
            return Config()
    try:
        data = tomllib.loads(toml_path.read_text())
    except Exception:
        return Config()
    ctx = data.get("context", {}) if isinstance(data, dict) else {}
    return Config(
        id_format=ctx.get("id_format", "word"),
        id_slug=bool(ctx.get("id_slug", False)),
        directory_overrides=ctx.get("directories"),
        sharding=ctx.get("sharding"),
    )
