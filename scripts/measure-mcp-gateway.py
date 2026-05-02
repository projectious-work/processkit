#!/usr/bin/env python3
"""Report processkit MCP config shape for gateway validation.

This is intentionally report-only: it reads MCP config fragments and
does not spawn MCP servers. Use ``--include-metadata`` when you also
want to import the aggregate/gateway modules and collect their exposed
metadata; imports may load source server modules but still do not run
stdio servers.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path
from types import ModuleType
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSKIT_ROOT = PROJECT_ROOT / "context" / "skills" / "processkit"
SRC_PROCESSKIT_ROOT = PROJECT_ROOT / "src" / "context" / "skills" / "processkit"
LIB_ROOT = PROJECT_ROOT / "src" / "context" / "skills" / "_lib"


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def mcp_servers(config: dict[str, Any] | None) -> dict[str, Any]:
    if not config:
        return {}
    servers = config.get("mcpServers", {})
    if isinstance(servers, dict):
        return servers
    return {}


def command_signature(server: dict[str, Any]) -> str:
    command = str(server.get("command", "")).strip()
    args = server.get("args", [])
    if not isinstance(args, list):
        args = []
    return " ".join([command, *[str(arg) for arg in args]]).strip()


def processkit_mode(server: dict[str, Any]) -> str | None:
    env = server.get("env", {})
    if not isinstance(env, dict):
        return None
    mode = env.get("PROCESSKIT_MCP_MODE")
    return str(mode) if mode is not None else None


def gateway_runtime_shape(server: dict[str, Any]) -> str:
    """Classify a processkit-gateway config by command args."""
    args = server.get("args", [])
    if not isinstance(args, list):
        args = []
    args_text = [str(arg) for arg in args]
    if "stdio-proxy" in args_text:
        return "stdio-proxy"
    if "serve" in args_text and "streamable-http" in args_text:
        return "daemon"
    return "direct-stdio"


def discover_granular_configs() -> list[Path]:
    root = PROCESSKIT_ROOT if PROCESSKIT_ROOT.is_dir() else SRC_PROCESSKIT_ROOT
    if not root.is_dir():
        return []
    return sorted(
        path
        for path in root.glob("*/mcp/mcp-config.json")
        if "templates" not in path.parts
        and path.parents[1].name != "processkit-gateway"
    )


def summarize_config(path: Path) -> dict[str, Any]:
    config = read_json(path)
    servers = mcp_servers(config)
    server_items = []
    for name, server in sorted(servers.items()):
        if not isinstance(server, dict):
            server = {}
        server_items.append({
            "name": name,
            "command": command_signature(server),
            "mode": processkit_mode(server),
            "runtime_shape": gateway_runtime_shape(server)
            if name == "processkit-gateway" else None,
        })
    return {
        "path": path.relative_to(PROJECT_ROOT).as_posix(),
        "exists": path.is_file(),
        "server_count": len(server_items),
        "servers": server_items,
    }


def summarize_granular() -> dict[str, Any]:
    configs = discover_granular_configs()
    summaries = [summarize_config(path) for path in configs]
    server_count = sum(item["server_count"] for item in summaries)
    modes = sorted({
        server["mode"]
        for item in summaries
        for server in item["servers"]
        if server["mode"] is not None
    })
    return {
        "label": "granular",
        "config_count": len(configs),
        "intended_client_processes": server_count,
        "modes": modes,
        "configs": summaries,
    }


def summarize_single_mode(
    label: str,
    path: Path,
    expected_mode: str,
) -> dict[str, Any]:
    summary = summarize_config(path)
    modes = sorted({
        server["mode"]
        for server in summary["servers"]
        if server["mode"] is not None
    })
    return {
        "label": label,
        "expected_mode": expected_mode,
        "intended_client_processes": summary["server_count"],
        "modes": modes,
        "config": summary,
        "mode_matches": modes == [expected_mode],
    }


def summarize_daemon_proxy(gateway: dict[str, Any]) -> dict[str, Any]:
    """Report the expected daemon plus stdio-proxy deployment shape.

    Harness config registers one lightweight stdio proxy per harness. The
    daemon is an external long-lived process supervised by aibox, systemd, or
    a developer shell.
    """
    configured = bool(gateway["config"]["exists"])
    return {
        "label": "daemon_proxy",
        "expected_mode": "gateway",
        "intended_client_processes": 1 if configured else 0,
        "runtime_processes": 2 if configured else 0,
        "modes": gateway["modes"],
        "config": gateway["config"],
        "mode_matches": gateway["mode_matches"],
        "daemon_external": True,
        "proxy_per_harness": True,
    }


def import_module(path: Path, module_name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def collect_optional_metadata() -> dict[str, Any]:
    sys.path.insert(0, str(LIB_ROOT))
    os.environ.setdefault("PROCESSKIT_LIB_PATH", str(LIB_ROOT))
    metadata: dict[str, Any] = {}

    targets = {
        "aggregate": (
            SRC_PROCESSKIT_ROOT / "aggregate-mcp" / "mcp" / "server.py",
            "processkit_measure_aggregate",
            "list_aggregate_tools",
        ),
        "gateway": (
            SRC_PROCESSKIT_ROOT / "processkit-gateway" / "mcp" / "server.py",
            "processkit_measure_gateway",
            "list_gateway_tools",
        ),
    }
    for label, (path, module_name, function_name) in targets.items():
        if not path.is_file():
            metadata[label] = {
                "ok": False,
                "error": f"missing {path.relative_to(PROJECT_ROOT)}",
            }
            continue
        try:
            module = import_module(path, module_name)
            payload = getattr(module, function_name)()
            metadata[label] = {
                "ok": True,
                "tool_count": payload.get("count"),
                "source_server_count": payload.get("source_server_count"),
                "runtime": payload.get("runtime"),
            }
        except Exception as exc:  # pragma: no cover - diagnostic path
            metadata[label] = {
                "ok": False,
                "error": f"{type(exc).__name__}: {exc}",
            }
    return metadata


def build_report(include_metadata: bool) -> dict[str, Any]:
    granular = summarize_granular()
    aggregate_config = (
        PROCESSKIT_ROOT / "aggregate-mcp" / "mcp"
        / "mcp-config.aggregate.json"
    )
    if not aggregate_config.is_file():
        aggregate_config = (
            SRC_PROCESSKIT_ROOT / "aggregate-mcp" / "mcp"
            / "mcp-config.aggregate.json"
        )
    gateway_config = (
        PROCESSKIT_ROOT / "processkit-gateway" / "mcp" / "mcp-config.json"
    )
    if not gateway_config.is_file():
        gateway_config = (
            SRC_PROCESSKIT_ROOT / "processkit-gateway" / "mcp"
            / "mcp-config.json"
        )
    aggregate = summarize_single_mode(
        "aggregate",
        aggregate_config,
        "aggregate",
    )
    gateway = summarize_single_mode(
        "gateway",
        gateway_config,
        "gateway",
    )
    daemon_proxy = summarize_daemon_proxy(gateway)
    modes = [granular, aggregate, gateway, daemon_proxy]
    process_counts = {
        item["label"]: item["intended_client_processes"]
        for item in modes
    }
    report: dict[str, Any] = {
        "project_root": PROJECT_ROOT.as_posix(),
        "summary": {
            "granular_config_count": granular["config_count"],
            "intended_client_processes": process_counts,
            "process_count_delta": {
                "granular_minus_aggregate": (
                    process_counts["granular"] - process_counts["aggregate"]
                ),
                "granular_minus_gateway": (
                    process_counts["granular"] - process_counts["gateway"]
                ),
                "granular_minus_daemon_proxy_client": (
                    process_counts["granular"]
                    - process_counts["daemon_proxy"]
                ),
            },
            "checks": {
                "aggregate_mode_configured": aggregate["mode_matches"],
                "gateway_mode_configured": gateway["mode_matches"],
                "gateway_is_single_client_process": (
                    process_counts["gateway"] == 1
                ),
                "aggregate_is_single_client_process": (
                    process_counts["aggregate"] == 1
                ),
                "daemon_proxy_has_single_harness_process": (
                    process_counts["daemon_proxy"] == 1
                ),
            },
        },
        "modes": modes,
    }
    if include_metadata:
        report["metadata"] = collect_optional_metadata()
    return report


def print_text(report: dict[str, Any]) -> None:
    summary = report["summary"]
    counts = summary["intended_client_processes"]
    print("processkit MCP gateway measurement")
    print(f"project_root: {report['project_root']}")
    print(
        "intended_client_processes: "
        f"granular={counts['granular']} "
        f"aggregate={counts['aggregate']} "
        f"gateway={counts['gateway']} "
        f"daemon_proxy={counts['daemon_proxy']}"
    )
    print(
        "process_count_delta: "
        f"granular_minus_aggregate="
        f"{summary['process_count_delta']['granular_minus_aggregate']} "
        f"granular_minus_gateway="
        f"{summary['process_count_delta']['granular_minus_gateway']} "
        f"granular_minus_daemon_proxy_client="
        f"{summary['process_count_delta']['granular_minus_daemon_proxy_client']}"
    )
    for check, ok in summary["checks"].items():
        print(f"check.{check}: {'ok' if ok else 'attention'}")
    if "metadata" in report:
        for label, payload in sorted(report["metadata"].items()):
            if payload.get("ok"):
                print(
                    f"metadata.{label}: ok "
                    f"tools={payload.get('tool_count')} "
                    f"sources={payload.get('source_server_count')}"
                )
            else:
                print(f"metadata.{label}: {payload.get('error')}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Report processkit MCP process-count config modes.",
    )
    parser.add_argument(
        "--format",
        choices=["json", "text"],
        default="json",
        help="Report format. Default: json.",
    )
    parser.add_argument(
        "--include-metadata",
        action="store_true",
        help="Import aggregate/gateway modules and include tool metadata.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    report = build_report(include_metadata=args.include_metadata)
    if args.format == "text":
        print_text(report)
    else:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
