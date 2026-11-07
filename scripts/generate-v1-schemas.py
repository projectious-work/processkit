#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "jinja2>=3.1",
#   "pyyaml>=6.0",
# ]
# ///
"""Generate the committed processkit v1 schema slice without aibox."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE = (
    REPO_ROOT
    / "src/context/skills/_lib/processkit/schema_generation.py"
)


def _load_generator():
    spec = importlib.util.spec_from_file_location("schema_generation", MODULE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load schema generator: {MODULE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("kinds", nargs="*")
    parser.add_argument(
        "--schemas-root",
        type=Path,
        default=REPO_ROOT / "src/context/schemas",
    )
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    result = _load_generator().regenerate_schemas(
        args.schemas_root,
        kinds=args.kinds or None,
        output_dir=args.output_dir,
        check=args.check,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if result["errors"] or (args.check and result["rebuilt"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
