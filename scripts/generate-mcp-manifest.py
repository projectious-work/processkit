#!/usr/bin/env -S uv run --quiet
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Generate the MCP-config manifest for a processkit release.

Walks every `context/skills/**/mcp-config.json`, computes a stable sha256
over each file's canonical JSON (sorted keys, compact separators), and
writes the manifest to both `context/.processkit-mcp-manifest.json` and
`src/context/.processkit-mcp-manifest.json`.

Also records `per_server_header`: sha256 of the PEP 723 inline metadata
block (`# /// script` ... `# ///`) of every `mcp/server.py`. The
pk-doctor `server_header_drift` check (RapidSwan) compares these against
the live files to detect dep edits that need a harness restart.
`aggregate_sha256` continues to cover per_skill mcp-config.json files
only — it is the public contract aibox#54 watches and intentionally
unaffected by header drift.

Downstream installers (notably `aibox sync`) are expected to compare the
`aggregate_sha256` against their last-merged state and re-merge the
consumer's `.mcp.json` when they differ — independently of whether the
processkit version changed. Without this signal, per-skill MCP-config
edits made within a release cycle never reach derived projects.

See DEC-20260423_2049-VastLake (truequail split) and the tracking GitHub
issue at projectious-work/aibox#54.

Usage:
    uv run scripts/generate-mcp-manifest.py

Exits 0 on success, 1 on any error.
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


MANIFEST_VERSION = 1
REPO_ROOT = Path(__file__).resolve().parent.parent
DOGFOOD_MANIFEST = REPO_ROOT / "context" / ".processkit-mcp-manifest.json"
SRC_MANIFEST = REPO_ROOT / "src" / "context" / ".processkit-mcp-manifest.json"


def _canonical_json(data: object) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha256_of_file(path: Path) -> str:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()


def _processkit_version(repo_root: Path) -> str:
    # aibox.lock is the de-facto version pin for both dogfood and consumer
    # trees; parse the [processkit] version = "vX.Y.Z" line without
    # pulling in tomllib (keeps the script dependency-free).
    lock = repo_root / "aibox.lock"
    if lock.is_file():
        try:
            text = lock.read_text(encoding="utf-8")
        except OSError:
            text = ""
        in_pk = False
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("["):
                in_pk = stripped == "[processkit]"
                continue
            if in_pk and stripped.startswith("version"):
                _, _, rhs = stripped.partition("=")
                return rhs.strip().strip('"').strip("'") or "unknown"
    version_file = repo_root / "VERSION"
    if version_file.is_file():
        try:
            value = version_file.read_text(encoding="utf-8").strip()
            if value:
                return value
        except OSError:
            pass
    return "unknown"


def _collect_entries(repo_root: Path) -> list[dict]:
    skills_root = repo_root / "context" / "skills"
    entries: list[dict] = []
    seen: set[str] = set()
    # Current layout: context/skills/<category>/<slug>/mcp/mcp-config.json
    for cfg in sorted(skills_root.glob("*/*/mcp/mcp-config.json")):
        rel = cfg.relative_to(repo_root).as_posix()
        if rel in seen:
            continue
        seen.add(rel)
        entries.append({"path": rel, "sha256": _sha256_of_file(cfg)})
    # Fallback flat layout: context/skills/<slug>/mcp/mcp-config.json
    for cfg in sorted(skills_root.glob("*/mcp/mcp-config.json")):
        rel = cfg.relative_to(repo_root).as_posix()
        if rel in seen:
            continue
        seen.add(rel)
        entries.append({"path": rel, "sha256": _sha256_of_file(cfg)})
    entries.sort(key=lambda e: e["path"])
    return entries


def _extract_pep723_header(path: Path) -> str | None:
    """Return the raw PEP 723 block (inclusive of fences), or None."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    in_block = False
    block: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not in_block:
            if stripped == "# /// script":
                in_block = True
                block.append(line)
            continue
        block.append(line)
        if stripped == "# ///":
            return "\n".join(block) + "\n"
    return None


def _collect_server_headers(repo_root: Path) -> list[dict]:
    """Hash PEP 723 dep headers for every MCP server.py.

    Used by the pk-doctor `server_header_drift` check (RapidSwan) to
    detect when a server's dep header changed since the last manifest
    regeneration — signal that the harness needs a restart and the
    manifest needs regenerating.
    """
    skills_root = repo_root / "context" / "skills"
    entries: list[dict] = []
    seen: set[str] = set()
    for server in sorted(skills_root.glob("*/*/mcp/server.py")):
        rel = server.relative_to(repo_root).as_posix()
        if rel in seen:
            continue
        seen.add(rel)
        header = _extract_pep723_header(server)
        if header is None:
            continue
        entries.append({
            "path": rel,
            "sha256": hashlib.sha256(header.encode("utf-8")).hexdigest(),
        })
    entries.sort(key=lambda e: e["path"])
    return entries


def _aggregate(entries: list[dict]) -> str:
    joined = "\n".join(e["sha256"] for e in entries)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


def _load_existing(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _write_manifest(path: Path, manifest: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    path.write_text(payload, encoding="utf-8")


def main() -> int:
    try:
        entries = _collect_entries(REPO_ROOT)
    except Exception as e:
        print(f"error: failed to collect mcp-config.json files: {e}", file=sys.stderr)
        return 1
    if not entries:
        print(
            "error: no context/skills/*/mcp/mcp-config.json files found",
            file=sys.stderr,
        )
        return 1

    aggregate = _aggregate(entries)
    version = _processkit_version(REPO_ROOT)
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    try:
        server_headers = _collect_server_headers(REPO_ROOT)
    except Exception as e:
        print(f"error: failed to collect server headers: {e}", file=sys.stderr)
        return 1

    existing = _load_existing(DOGFOOD_MANIFEST)
    generated_at = now_iso
    if (
        existing
        and existing.get("aggregate_sha256") == aggregate
        and existing.get("per_skill") == entries
        and existing.get("per_server_header") == server_headers
        and existing.get("processkit_version") == version
        and isinstance(existing.get("generated_at"), str)
    ):
        # Preserve generated_at on no-op regenerations to keep git diffs clean.
        generated_at = existing["generated_at"]

    manifest = {
        "version": MANIFEST_VERSION,
        "generated_at": generated_at,
        "processkit_version": version,
        "per_skill": entries,
        "per_server_header": server_headers,
        "aggregate_sha256": aggregate,
    }

    try:
        _write_manifest(DOGFOOD_MANIFEST, manifest)
        _write_manifest(SRC_MANIFEST, manifest)
    except OSError as e:
        print(f"error: failed to write manifest: {e}", file=sys.stderr)
        return 1

    print(
        f"wrote {DOGFOOD_MANIFEST.relative_to(REPO_ROOT)} "
        f"and {SRC_MANIFEST.relative_to(REPO_ROOT)} "
        f"({len(entries)} skills, {len(server_headers)} server header(s), "
        f"aggregate {aggregate[:12]}...)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
