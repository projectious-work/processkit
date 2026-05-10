#!/usr/bin/env python3
"""Cold-start benchmark for aggregate-mcp eager vs lazy_catalog modes.

Spawns a fresh subprocess per run so module-level work and Python
import overhead are paid every iteration — that is the actual
client-visible startup cost when a harness boots the MCP server.

Each iteration imports the aggregate-mcp server, calls
``list_aggregate_tools()``, prints the runtime metadata, and exits.
The harness records wall-clock seconds and reports min/median/max for
each mode plus the lazy speedup factor.

Usage::

    uv run --with mcp --with pyyaml --with jsonschema --with httpx \
        --with sqlite-vec scripts/bench-aggregate-mcp-coldstart.py [N]

``N`` defaults to 5 iterations per mode.
"""
from __future__ import annotations

import json
import os
import statistics
import subprocess
import sys
import time
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SERVER_PATH = (
    REPO_ROOT
    / "context"
    / "skills"
    / "processkit"
    / "aggregate-mcp"
    / "mcp"
    / "server.py"
)


CHILD_SCRIPT = """
import importlib.util
import json
import sys
import time
from pathlib import Path

server_path = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("aggregate_mcp_bench", server_path)
module = importlib.util.module_from_spec(spec)
start = time.perf_counter()
spec.loader.exec_module(module)
result = module.list_aggregate_tools()
elapsed = time.perf_counter() - start

print(json.dumps({
    "elapsed_seconds": elapsed,
    "tool_count": result["count"],
    "import_mode": result["runtime"]["import_mode"],
    "lazy_daemon": result["runtime"]["lazy_daemon"],
}))
"""


def _run_iteration(mode: str) -> dict:
    env = os.environ.copy()
    env.pop("PROCESSKIT_MCP_LAZY", None)
    env.pop("PROCESSKIT_MCP_MODE", None)
    if mode == "lazy_catalog":
        env["PROCESSKIT_MCP_LAZY"] = "1"

    t0 = time.perf_counter()
    proc = subprocess.run(
        [sys.executable, "-c", CHILD_SCRIPT, str(SERVER_PATH)],
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    wall = time.perf_counter() - t0
    payload = json.loads(proc.stdout.strip().splitlines()[-1])
    payload["wall_seconds"] = wall
    return payload


def _summarize(label: str, samples: list[dict]) -> dict:
    walls = [s["wall_seconds"] for s in samples]
    inner = [s["elapsed_seconds"] for s in samples]
    summary = {
        "mode": label,
        "samples": len(samples),
        "tool_count": samples[0]["tool_count"],
        "import_mode": samples[0]["import_mode"],
        "wall": {
            "min": min(walls),
            "median": statistics.median(walls),
            "max": max(walls),
        },
        "module_init": {
            "min": min(inner),
            "median": statistics.median(inner),
            "max": max(inner),
        },
    }
    print(
        f"[{label}] n={len(samples)} "
        f"wall median={summary['wall']['median']*1000:.0f} ms "
        f"(min {summary['wall']['min']*1000:.0f}, "
        f"max {summary['wall']['max']*1000:.0f}); "
        f"module_init median={summary['module_init']['median']*1000:.0f} ms; "
        f"import_mode={summary['import_mode']}; "
        f"tool_count={summary['tool_count']}"
    )
    return summary


def main(argv: list[str]) -> int:
    iterations = int(argv[1]) if len(argv) > 1 else 5

    print(f"benchmarking aggregate-mcp cold-start ({iterations} runs/mode)")
    print(f"server: {SERVER_PATH.relative_to(REPO_ROOT)}")
    print()

    eager_samples = [_run_iteration("eager") for _ in range(iterations)]
    lazy_samples = [_run_iteration("lazy_catalog") for _ in range(iterations)]

    print()
    eager_summary = _summarize("eager", eager_samples)
    lazy_summary = _summarize("lazy_catalog", lazy_samples)

    speedup = (
        eager_summary["wall"]["median"] / lazy_summary["wall"]["median"]
        if lazy_summary["wall"]["median"] > 0 else float("inf")
    )
    delta_ms = (
        eager_summary["wall"]["median"] - lazy_summary["wall"]["median"]
    ) * 1000
    print()
    print(
        f"lazy_catalog cold-start median is {delta_ms:.0f} ms faster "
        f"({speedup:.2f}x speedup)"
    )

    print()
    print(json.dumps({
        "iterations": iterations,
        "eager": eager_summary,
        "lazy_catalog": lazy_summary,
        "speedup_x": speedup,
        "delta_ms": delta_ms,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
