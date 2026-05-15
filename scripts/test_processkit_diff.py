"""Regression tests for scripts/processkit-diff.sh."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "processkit-diff.sh"


def _run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)


def _write_provenance(repo: Path, files: dict[str, str]) -> None:
    src = repo / "src"
    src.mkdir(exist_ok=True)
    lines = [
        "[source]",
        'url = "https://example.invalid/processkit.git"',
        'ref = "test"',
        "",
        "[files]",
    ]
    lines.extend(f'"{path}" = "{version}"' for path, version in sorted(files.items()))
    (src / "PROVENANCE.toml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_processkit_diff_emits_affected_files_for_generators(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _run(["git", "init"], repo)
    _run(["git", "config", "user.email", "test@example.invalid"], repo)
    _run(["git", "config", "user.name", "Test User"], repo)

    _write_provenance(repo, {
        "context/skills/processkit/old/SKILL.md": "old-v1",
        "context/skills/processkit/stable/SKILL.md": "same",
        "context/skills/processkit/changed/SKILL.md": "changed-v1",
    })
    _run(["git", "add", "src/PROVENANCE.toml"], repo)
    _run(["git", "commit", "-m", "old"], repo)
    _run(["git", "tag", "v-old"], repo)

    _write_provenance(repo, {
        "context/skills/processkit/new/SKILL.md": "new-v1",
        "context/skills/processkit/stable/SKILL.md": "same",
        "context/skills/processkit/changed/SKILL.md": "changed-v2",
    })
    _run(["git", "add", "src/PROVENANCE.toml"], repo)
    _run(["git", "commit", "-m", "new"], repo)
    _run(["git", "tag", "v-new"], repo)

    result = _run([
        "bash",
        str(SCRIPT),
        "--repo",
        str(repo),
        "--from",
        "v-old",
        "--to",
        "v-new",
        "--format",
        "json",
    ], REPO_ROOT)
    affected = json.loads(result.stdout)["diff"]["affected_files"]
    by_path = {item["path"]: item for item in affected}

    assert by_path["context/skills/processkit/new/SKILL.md"] == {
        "path": "context/skills/processkit/new/SKILL.md",
        "classification": "new-upstream",
        "to_version": "new-v1",
    }
    assert by_path["context/skills/processkit/changed/SKILL.md"] == {
        "path": "context/skills/processkit/changed/SKILL.md",
        "classification": "changed-upstream-only",
        "from_version": "changed-v1",
        "to_version": "changed-v2",
    }
    assert by_path["context/skills/processkit/old/SKILL.md"] == {
        "path": "context/skills/processkit/old/SKILL.md",
        "classification": "removed-upstream",
        "from_version": "old-v1",
    }
