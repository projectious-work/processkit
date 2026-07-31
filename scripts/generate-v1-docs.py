#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Generate v1 CLI and release-fact documentation from source."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FACTS_SOURCE = ROOT / "release" / "v1-release-facts.json"
CLI_OUTPUT = ROOT / "docs-site/content/en/docs/installer/cli-generated.md"
FACTS_OUTPUT = (
    ROOT / "docs-site/content/en/docs/reference/v1-alpha-release-facts.md"
)


def cli_help() -> str:
    result = subprocess.run(
        [
            "cargo",
            "run",
            "--quiet",
            "--offline",
            "--locked",
            "--manifest-path",
            str(ROOT / "installer/Cargo.toml"),
            "--",
            "--help",
        ],
        check=True,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    return result.stdout.rstrip()


def render_cli(help_text: str, version: str) -> str:
    return f'''---
title: "Generated CLI Reference"
description: "Generated from the processkit {version} executable."
weight: 11
---

Do not edit this page by hand. Regenerate it with
`uv run scripts/generate-v1-docs.py`.

```text
{help_text}
```
'''


def render_facts(facts: dict[str, object]) -> str:
    version = str(facts["release"])
    targets = facts["targets"]
    if not isinstance(targets, list):
        raise ValueError("targets must be a list")
    assets = "\n".join(
        f"- `processkit-{version}-{target}`" for target in targets
    )
    return f'''---
title: "v1 Alpha Release Facts"
description: "Generated facts for processkit {version}."
weight: 15
---

Do not edit this page by hand. Its authoritative source is
`release/v1-release-facts.json`.

| Fact | Value |
| --- | --- |
| Release | `{version}` |
| Status | {facts["status"]} |
| Signature | `{facts["signatureAlgorithm"]}` |
| Installer protocol | `{facts["installerProtocol"]}` |
| Entity API version | `{facts["entityApiVersion"]}` |

## Native Assets

{assets}

Every published asset has a checksum sidecar and is bound into the signed
release envelope. The public release is the authority for final checksums and
host provenance.
'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    facts = json.loads(FACTS_SOURCE.read_text(encoding="utf-8"))
    cargo = tomllib.loads(
        (ROOT / "installer/crates/processkit/Cargo.toml").read_text(
            encoding="utf-8"
        )
    )
    version = f'v{cargo["package"]["version"]}'
    if facts.get("release") != version:
        raise ValueError("release facts and Cargo package version differ")
    outputs = {
        CLI_OUTPUT: render_cli(cli_help(), version),
        FACTS_OUTPUT: render_facts(facts),
    }
    stale = []
    for path, payload in outputs.items():
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != payload:
                stale.append(path)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(payload, encoding="utf-8")
    if stale:
        print("stale generated v1 documentation:", file=sys.stderr)
        for path in stale:
            print(f"- {path.relative_to(ROOT)}", file=sys.stderr)
        return 1
    print("generated v1 CLI reference and release facts are current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
