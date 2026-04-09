#!/usr/bin/env python3
"""Migrate all existing processkit entity IDs to CamelCase + datetime format.

Old format: PREFIX-adj-noun[-slug...]
New format: PREFIX-YYYYMMDD_HHMM-AdjNoun[-slug...]

Steps:
1. Scan context/ for entity files with old-format IDs
2. Build old→new ID mapping using metadata.created for the datetime part
3. Rename entity files to match new IDs
4. Rewrite metadata.id in each file
5. Find and replace all old ID references across all files
6. Move LogEntry files into sharded year/month subdirectories
7. Reindex

Skips: Migration entities (MIG-*), already-migrated IDs (those containing
an underscore in the word-pair component).

Run from the project root:
    python3 scripts/migrate-ids-to-camel-datetime.py
"""
from __future__ import annotations

import re
import sys
from datetime import datetime, timezone
from pathlib import Path


# ── helpers ──────────────────────────────────────────────────────────────────

def parse_created(created_str: str) -> str:
    """Convert an ISO 8601 created timestamp to YYYYMMDD_HHMM."""
    s = str(created_str).strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        dt = datetime.now(timezone.utc)
    return dt.strftime("%Y%m%d_%H%M")


def parse_old_id(entity_id: str) -> tuple[str, str, str, str] | None:
    """Decompose an old-format ID into (prefix, adj, noun, slug).

    Returns None for IDs that are already in the new format or should
    not be migrated (e.g. MIG-* with timestamp IDs, UUIDs).
    """
    parts = entity_id.split("-")
    if len(parts) < 3:
        return None
    prefix = parts[0]
    # Skip Migration entities — they use timestamp IDs, not word pairs
    if prefix == "MIG":
        return None
    adj = parts[1]
    noun = parts[2]
    # Skip if already CamelCase (contains uppercase) or datetime-prefixed
    if any(c.isupper() for c in adj + noun):
        return None
    # Skip if adj looks like a datetime (all digits + underscore)
    if re.match(r"^\d{8}$", adj):
        return None
    # Slug is everything after adj-noun
    slug = "-".join(parts[3:]) if len(parts) > 3 else ""
    return prefix, adj, noun, slug


def new_id_for(old_id: str, created_str: str) -> str | None:
    """Generate the new ID for an old-format entity ID."""
    parsed = parse_old_id(old_id)
    if parsed is None:
        return None
    prefix, adj, noun, slug = parsed
    dt_part = parse_created(created_str)
    camel = f"{adj.capitalize()}{noun.capitalize()}"
    body = f"{dt_part}-{camel}"
    if slug:
        body = f"{body}-{slug}"
    return f"{prefix}-{body}"


def load_frontmatter_id_and_created(path: Path) -> tuple[str, str] | None:
    """Extract (metadata.id, metadata.created) from a file's YAML frontmatter.

    Returns None if the file is not a valid entity file.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    end = text.find("---", 3)
    if end == -1:
        return None
    fm = text[3:end]
    # Simple regex extraction — avoids a full YAML parse dependency
    id_m = re.search(r"^\s*id:\s*['\"]?([^\s'\"]+)['\"]?", fm, re.MULTILINE)
    created_m = re.search(r"^\s*created:\s*['\"]?([^\s'\"]+)['\"]?", fm, re.MULTILINE)
    if not id_m:
        return None
    entity_id = id_m.group(1)
    created = created_m.group(1) if created_m else "2026-01-01T00:00:00Z"
    return entity_id, created


# ── main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    root = Path(__file__).resolve().parent.parent
    context = root / "context"

    if not context.is_dir():
        print(f"ERROR: context/ directory not found at {context}", file=sys.stderr)
        sys.exit(1)

    # ── Phase 1: Build the migration map ─────────────────────────────────────
    print("Phase 1: scanning entity files …")
    migration: dict[str, str] = {}  # old_id → new_id
    file_map: dict[str, Path] = {}  # old_id → current file path

    for path in sorted(context.rglob("*.md")):
        # Skip templates, cache, INDEX files, non-entity directories
        parts = path.relative_to(context).parts
        if parts[0] in ("templates", ".cache"):
            continue
        if path.name in ("INDEX.md", "HANDOVER.md", "CHANGELOG.md"):
            continue
        result = load_frontmatter_id_and_created(path)
        if result is None:
            continue
        old_id, created = result
        new_id = new_id_for(old_id, created)
        if new_id is None:
            print(f"  skip  {old_id}  (already migrated or excluded)")
            continue
        migration[old_id] = new_id
        file_map[old_id] = path
        print(f"  plan  {old_id}")
        print(f"     →  {new_id}")

    if not migration:
        print("Nothing to migrate.")
        return

    print(f"\n{len(migration)} entities to migrate.\n")

    # ── Phase 2: Update metadata.id inside each file ──────────────────────────
    print("Phase 2: rewriting metadata.id in entity files …")
    for old_id, new_id in migration.items():
        path = file_map[old_id]
        text = path.read_text(encoding="utf-8")
        # Replace the id: field value
        new_text = re.sub(
            r"(^\s*id:\s*['\"]?)" + re.escape(old_id) + r"(['\"]?\s*$)",
            rf"\g<1>{new_id}\2",
            text,
            flags=re.MULTILINE,
        )
        # Also update spec.location for Artifact entities
        new_text = new_text.replace(
            f"context/artifacts/{path.name}",
            f"context/artifacts/{new_id}.md",
        )
        path.write_text(new_text, encoding="utf-8")
        print(f"  updated id in {path.name}")

    # ── Phase 3: Cross-reference rewriting (all .md files in context/) ────────
    print("\nPhase 3: updating cross-references across all files …")
    all_md = [p for p in context.rglob("*.md")
              if p.relative_to(context).parts[0] not in ("templates", ".cache")]
    for path in sorted(all_md):
        text = path.read_text(encoding="utf-8")
        changed = False
        for old_id, new_id in migration.items():
            if old_id in text:
                text = text.replace(old_id, new_id)
                changed = True
        if changed:
            path.write_text(text, encoding="utf-8")
            print(f"  refs updated in {path.relative_to(context)}")

    # ── Phase 4: Rename files ─────────────────────────────────────────────────
    # Only rename files whose current filename matches "{old_id}.md".
    # Fixed-name files (SKILL.md, bug-fix.md, goals-and-context.md, …) keep
    # their names — only the metadata.id inside them is updated.
    print("\nPhase 4: renaming entity files …")
    for old_id, new_id in migration.items():
        old_path = file_map[old_id]
        if old_path.name != f"{old_id}.md":
            print(f"  skip rename (fixed name): {old_path.name}")
            continue
        # New path: same directory, new filename
        new_path = old_path.parent / f"{new_id}.md"
        if old_path != new_path:
            old_path.rename(new_path)
            print(f"  {old_path.name} → {new_path.name}")

    # ── Phase 5: Shard LogEntry files ────────────────────────────────────────
    print("\nPhase 5: sharding LogEntry files into year/month dirs …")
    logs_dir = context / "logs"
    if logs_dir.is_dir():
        for log_file in sorted(logs_dir.glob("*.md")):
            # Read created from frontmatter
            result = load_frontmatter_id_and_created(log_file)
            if result is None:
                continue
            entity_id, created_str = result
            s = created_str.replace("Z", "+00:00")
            try:
                dt = datetime.fromisoformat(s)
            except ValueError:
                dt = datetime.now(timezone.utc)
            shard_dir = logs_dir / f"{dt.year:04d}" / f"{dt.month:02d}"
            shard_dir.mkdir(parents=True, exist_ok=True)
            new_path = shard_dir / log_file.name
            if log_file != new_path:
                log_file.rename(new_path)
                print(f"  {log_file.name} → logs/{dt.year:04d}/{dt.month:02d}/")

    # ── Phase 6: Reindex ─────────────────────────────────────────────────────
    print("\nPhase 6: reindexing …")
    sys.path.insert(0, str(root / "src" / "lib"))
    try:
        from processkit import index as idx, paths as pkpaths
        import os
        os.chdir(root)
        db = idx.open_db()
        stats = idx.reindex(root, db)
        db.close()
        print(f"  index rebuilt: {stats.entities} entities, "
              f"{stats.events} events, {stats.errors} errors")
        if stats.errors:
            print("  WARNING: some files had errors — run reindex MCP tool to inspect")
    except Exception as exc:
        print(f"  reindex failed: {exc} — run reindex MCP tool manually")

    print("\nMigration complete.")


if __name__ == "__main__":
    main()
