#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Generate exact-release ownership baselines for mixed v0 roots."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import subprocess
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "src/.processkit/installer/compatibility"
RELEASES = ("v0.27.1", "v0.28.4")
ROOTS = (
    "src/context/artifacts",
    "src/context/bindings",
    "src/context/roles",
    "src/context/team-members",
)


def baseline(tag: str) -> str:
    archive = subprocess.run(
        ["git", "archive", tag, *ROOTS],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    files: dict[str, str] = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as bundle:
        for member in bundle.getmembers():
            if not member.isfile() or not member.name.endswith(".md"):
                continue
            source = bundle.extractfile(member)
            if source is None:
                raise ValueError(f"cannot read {member.name}")
            relative = member.name.removeprefix("src/")
            files[relative] = hashlib.sha256(source.read()).hexdigest()
    payload = {"releaseVersion": tag, "files": dict(sorted(files.items()))}
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []
    for tag in RELEASES:
        path = OUTPUT / f"{tag}-ownership.json"
        payload = baseline(tag)
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != payload:
                stale.append(path)
        else:
            path.write_text(payload, encoding="utf-8")
    if stale:
        raise SystemExit("stale ownership baseline: " + ", ".join(map(str, stale)))
    print("v0 ownership baselines are current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
