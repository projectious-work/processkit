"""context_consumption check — estimate processkit context footprint.

This check is intentionally INFO-only. It measures likely startup and
processkit-adapter surfaces without adding a new MCP tool whose schema would
itself increase harness context.
"""
from __future__ import annotations

import math
from pathlib import Path

from .common import CheckResult


_STARTUP_PATHS = [
    Path("AGENTS.md"),
    Path(".claude/settings.json"),
    Path(".codex/config.toml"),
    Path("context/.processkit-mcp-manifest.json"),
]


def _measure_file(path: Path) -> dict | None:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    data = text.encode("utf-8")
    words = len(text.split())
    return {
        "path": path.as_posix(),
        "bytes": len(data),
        "lines": text.count("\n") + (0 if text.endswith("\n") or not text else 1),
        "words": words,
        "estimated_tokens": math.ceil(len(data) / 4),
    }


def _sum(items: list[dict]) -> dict:
    out = {"bytes": 0, "lines": 0, "words": 0, "estimated_tokens": 0}
    for item in items:
        for key in out:
            out[key] += int(item.get(key, 0))
    return out


def _collect_files(repo_root: Path) -> dict[str, list[dict]]:
    startup: list[dict] = []
    for rel in _STARTUP_PATHS:
        item = _measure_file(repo_root / rel)
        if item:
            item["path"] = rel.as_posix()
            startup.append(item)

    commands: list[dict] = []
    for root in (repo_root / ".agents" / "skills", repo_root / ".claude" / "commands"):
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.md")):
            item = _measure_file(path)
            if item:
                item["path"] = path.relative_to(repo_root).as_posix()
                commands.append(item)

    skill_docs: list[dict] = []
    for path in sorted((repo_root / "context" / "skills" / "processkit").glob("*/*.md")):
        if path.name != "SKILL.md":
            continue
        item = _measure_file(path)
        if item:
            item["path"] = path.relative_to(repo_root).as_posix()
            skill_docs.append(item)

    mcp_configs: list[dict] = []
    for path in sorted((repo_root / "context" / "skills").glob("*/*/mcp/mcp-config.json")):
        item = _measure_file(path)
        if item:
            item["path"] = path.relative_to(repo_root).as_posix()
            mcp_configs.append(item)

    return {
        "startup": startup,
        "commands": commands,
        "skill_docs": skill_docs,
        "mcp_configs": mcp_configs,
    }


def run(ctx) -> list[CheckResult]:
    repo_root: Path = ctx["repo_root"]
    groups = _collect_files(repo_root)
    totals = {name: _sum(items) for name, items in groups.items()}
    overall = _sum(list(totals.values()))

    return [CheckResult(
        severity="INFO",
        category="context_consumption",
        id="context_consumption.estimated",
        message=(
            "estimated processkit context footprint: "
            f"{overall['estimated_tokens']} tokens across "
            f"{sum(len(items) for items in groups.values())} files "
            "(heuristic: ceil(utf8 bytes / 4))"
        ),
        extra={
            "heuristic": "ceil(utf8_bytes / 4)",
            "groups": totals,
        },
    )]
