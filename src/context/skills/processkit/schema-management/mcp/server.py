#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "mcp[cli]>=1.0",
#   "pyyaml>=6.0",
#   "jinja2>=3.1",
# ]
# ///
"""processkit schema-management MCP server."""
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

from processkit import paths, schema, schema_generation  # noqa: E402

server = FastMCP("processkit-schema-management")


@server.tool(annotations=ToolAnnotations(
    readOnlyHint=False,
    destructiveHint=True,
    idempotentHint=True,
    openWorldHint=False,
))
def regenerate_schemas(kinds: list[str] | None = None) -> dict:
    """Rebuild all or selected committed generated schema contracts."""
    schemas_root = paths.primitive_schemas_dir()
    if schemas_root is None or not (schemas_root / "src").is_dir():
        return {
            "rebuilt": [],
            "unchanged": [],
            "errors": {"schemas": "canonical schema sources not found"},
        }
    normalized = [kind.lower() for kind in kinds] if kinds else None
    result = schema_generation.regenerate_schemas(
        schemas_root,
        kinds=normalized,
    )
    if result["rebuilt"] and not result["errors"]:
        schema.reload_caches()
    return result


@server.tool(annotations=ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
))
def get_schema_contract(
    kind: str,
    discriminator: str | None = None,
) -> dict:
    """Return a base or discriminator-specific runtime Schema spec."""
    try:
        contract = schema.load_schema(kind, discriminator=discriminator)
    except schema.SchemaError as exc:
        return {
            "error": str(exc),
            "kind": kind,
            "discriminator": discriminator,
        }
    return {
        "kind": kind,
        "discriminator": discriminator,
        "contract": contract,
    }


@server.tool(annotations=ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
))
def get_validation_mode(
    kind: str,
    discriminator: str | None = None,
) -> dict:
    """Return a base or discriminator-specific schema validation mode."""
    mode = schema.validation_mode(kind, discriminator=discriminator)
    if mode is None:
        return {
            "error": f"no schema for kind={kind!r}",
            "kind": kind,
            "discriminator": discriminator,
        }
    return {
        "kind": kind,
        "discriminator": discriminator,
        "validation_mode": mode,
    }


if __name__ == "__main__":
    server.run(transport="stdio")
