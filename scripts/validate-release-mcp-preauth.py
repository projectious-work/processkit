#!/usr/bin/env python3
"""Validate release MCP manifest and preauth metadata.

The release source of truth is the shipped MCP config files, not the
generated manifest. This guard catches stale metadata that agrees with
itself while omitting a shipped MCP server.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


GATEWAY_SERVER = "processkit-gateway"
MANIFEST_REL = Path("context/.processkit-mcp-manifest.json")
PREAUTH_REL = Path("context/skills/processkit/skill-gate/assets/preauth.json")


def _canonical_json(data: object) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha256_of_json(path: Path) -> str:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()


def _load_json(path: Path, failures: list[str]) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        failures.append(f"could not read {path}: {exc}")
        return {}
    except json.JSONDecodeError as exc:
        failures.append(f"could not parse {path}: {exc}")
        return {}
    if not isinstance(data, dict):
        failures.append(f"{path} must contain a JSON object")
        return {}
    return data


def _mcp_configs(release_root: Path) -> list[Path]:
    skills_root = release_root / "context" / "skills"
    configs = {
        *skills_root.glob("*/*/mcp/mcp-config.json"),
        *skills_root.glob("*/mcp/mcp-config.json"),
    }
    return sorted(path for path in configs if path.is_file())


def _servers_for_config(path: Path, failures: list[str]) -> set[str]:
    data = _load_json(path, failures)
    servers = data.get("mcpServers") or {}
    if not isinstance(servers, dict) or not servers:
        failures.append(f"{path} must define non-empty mcpServers")
        return set()
    return {name for name in servers if isinstance(name, str)}


def _entry_map(entries: object, key: str, failures: list[str]) -> dict[str, str]:
    if not isinstance(entries, list):
        failures.append(f"manifest {key} must be a list")
        return {}
    out: dict[str, str] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            failures.append(f"manifest {key} contains a non-object entry")
            continue
        path = entry.get("path")
        sha = entry.get("sha256")
        if not isinstance(path, str) or not isinstance(sha, str):
            failures.append(f"manifest {key} entry missing path/sha256")
            continue
        out[path] = sha
    return out


def validate(release_root: Path) -> list[str]:
    failures: list[str] = []
    release_root = release_root.resolve()
    context_root = release_root / "context"
    manifest_path = release_root / MANIFEST_REL
    preauth_path = release_root / PREAUTH_REL

    if not context_root.is_dir():
        return [f"release root does not contain context/: {release_root}"]
    if not manifest_path.is_file():
        failures.append(f"missing MCP manifest: {MANIFEST_REL.as_posix()}")
    if not preauth_path.is_file():
        failures.append(f"missing preauth spec: {PREAUTH_REL.as_posix()}")

    configs = _mcp_configs(release_root)
    if not configs:
        failures.append("no shipped MCP config files found under context/skills")

    granular_paths: dict[str, Path] = {}
    gateway_paths: dict[str, Path] = {}
    expected_servers: set[str] = set()
    gateway_servers: set[str] = set()

    for cfg in configs:
        rel = cfg.relative_to(release_root).as_posix()
        servers = _servers_for_config(cfg, failures)
        if GATEWAY_SERVER in servers:
            gateway_paths[rel] = cfg
            gateway_servers.update(servers)
            extra = sorted(servers - {GATEWAY_SERVER})
            if extra:
                failures.append(
                    f"{rel} mixes gateway and granular servers: {', '.join(extra)}"
                )
            continue
        granular_paths[rel] = cfg
        expected_servers.update(servers)

    if manifest_path.is_file():
        manifest = _load_json(manifest_path, failures)
        per_skill = _entry_map(manifest.get("per_skill"), "per_skill", failures)
        per_gateway = _entry_map(
            manifest.get("per_gateway") or [],
            "per_gateway",
            failures,
        )
        missing_manifest = sorted(set(granular_paths) - set(per_skill))
        extra_manifest = sorted(set(per_skill) - set(granular_paths))
        for rel in missing_manifest:
            failures.append(f"manifest per_skill missing shipped MCP config: {rel}")
        for rel in extra_manifest:
            failures.append(f"manifest per_skill has stale MCP config path: {rel}")
        for rel, cfg in granular_paths.items():
            if per_skill.get(rel) and per_skill[rel] != _sha256_of_json(cfg):
                failures.append(f"manifest per_skill sha256 stale for {rel}")

        missing_gateway = sorted(set(gateway_paths) - set(per_gateway))
        for rel in missing_gateway:
            failures.append(f"manifest per_gateway missing gateway config: {rel}")
        for rel, cfg in gateway_paths.items():
            if per_gateway.get(rel) and per_gateway[rel] != _sha256_of_json(cfg):
                failures.append(f"manifest per_gateway sha256 stale for {rel}")

    if preauth_path.is_file():
        preauth = _load_json(preauth_path, failures)
        permissions = set((preauth.get("permissions") or {}).get("allow") or [])
        enabled = set(preauth.get("enabledMcpjsonServers") or [])
        codex_tools = set(
            (((preauth.get("codex") or {}).get("mcp") or {}).get("allowed_tools"))
            or []
        )
        for server in sorted(expected_servers):
            pattern = f"mcp__{server}__*"
            if server not in enabled:
                failures.append(
                    f"preauth enabledMcpjsonServers missing shipped server: {server}"
                )
            if pattern not in permissions:
                failures.append(f"preauth permissions.allow missing: {pattern}")
            if pattern not in codex_tools:
                failures.append(f"preauth codex.mcp.allowed_tools missing: {pattern}")
        for server in sorted(enabled - expected_servers - gateway_servers):
            failures.append(
                f"preauth enabledMcpjsonServers has no shipped MCP config: {server}"
            )
        for server in sorted(gateway_servers & enabled):
            failures.append(
                f"preauth enabledMcpjsonServers should not list gateway server: {server}"
            )

    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "release_root",
        help="directory containing the shipped context/ tree",
    )
    args = parser.parse_args(argv)

    failures = validate(Path(args.release_root))
    if failures:
        print("MCP PREAUTH RELEASE CONTRACT VIOLATIONS:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    print("OK: MCP manifest and preauth release contract passed.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
