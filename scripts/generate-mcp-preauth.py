#!/usr/bin/env python3
"""Generate processkit MCP preauthorization specs from shipped configs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RELATIVE_SPEC = Path(
    "context/skills/processkit/skill-gate/assets/preauth.json"
)
GATEWAY_SERVER = "processkit-gateway"
DESCRIPTION = (
    "processkit MCP preauth spec — read by aibox sync and merged into "
    "derived projects' harness config so users do not re-prompt for "
    "processkit MCP tools after every container rebuild. Claude Code "
    "consumes permissions.allow/enabledMcpjsonServers; Codex consumes "
    "codex.mcp.allowed_tools. See projectious-work/aibox#55 (consumer) "
    "and BACK-20260425_1316-WildGrove (producer)."
)


def _config_paths(root: Path) -> list[Path]:
    skills = root / "context" / "skills"
    paths = {
        *skills.glob("*/*/mcp/mcp-config.json"),
        *skills.glob("*/mcp/mcp-config.json"),
    }
    return sorted(path for path in paths if path.is_file())


def _server_names(root: Path) -> list[str]:
    names: set[str] = set()
    for path in _config_paths(root):
        data = json.loads(path.read_text(encoding="utf-8"))
        servers = data.get("mcpServers")
        if not isinstance(servers, dict) or not servers:
            raise ValueError(f"{path} must define non-empty mcpServers")
        names.update(
            name
            for name in servers
            if isinstance(name, str) and name != GATEWAY_SERVER
        )
    if not names:
        raise ValueError(f"no granular MCP servers found below {root}")
    return sorted(names)


def _payload(servers: list[str]) -> dict:
    patterns = [f"mcp__{server}__*" for server in servers]
    return {
        "version": 1,
        "description": DESCRIPTION,
        "permissions": {"allow": patterns},
        "enabledMcpjsonServers": servers,
        "codex": {"mcp": {"allowed_tools": patterns}},
    }


def _all_server_names(roots: tuple[Path, ...]) -> list[str]:
    names: set[str] = set()
    for root in roots:
        names.update(_server_names(root))
    return sorted(names)


def _render(servers: list[str]) -> str:
    return json.dumps(_payload(servers), indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify generated specs without writing",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="repository root to generate (default: script repository)",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    target_roots = (repo_root, repo_root / "src")
    expected = _render(_all_server_names(target_roots))
    stale: list[Path] = []
    for root in target_roots:
        target = root / RELATIVE_SPEC
        current = (
            target.read_text(encoding="utf-8") if target.is_file() else None
        )
        if current == expected:
            continue
        stale.append(target)
        if not args.check:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(expected, encoding="utf-8")

    if args.check and stale:
        print("MCP preauth specs are out of date:")
        for path in stale:
            print(f"  {path.relative_to(repo_root)}")
        print("Regenerate with: uv run scripts/generate-mcp-preauth.py")
        return 1

    action = "verified" if args.check else "wrote"
    print(f"{action} MCP preauth specs for {len(target_roots)} trees")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
