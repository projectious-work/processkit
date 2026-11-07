from __future__ import annotations

import importlib.util
import os
import shutil
import tempfile
from pathlib import Path


SERVER = Path(__file__).resolve().parents[1] / "mcp" / "server.py"


def _load():
    spec = importlib.util.spec_from_file_location("skill_management", SERVER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_skill_lifecycle_uses_package_manifest() -> None:
    module = _load()
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "AGENTS.md").write_text("# fixture\n", encoding="utf-8")
        machines = root / "context" / "state-machines"
        machines.mkdir(parents=True)
        shutil.copy2(
            Path(__file__).resolve().parents[4] / "state-machines" / "skill.yaml",
            machines / "skill.yaml",
        )
        old = Path.cwd()
        try:
            os.chdir(root)
            created = module.create_skill(
                "alpha-review",
                "Review alpha contracts.",
            )
            assert created["state"] == "draft"
            updated = module.update_skill(
                "alpha-review", {"capabilities": ["CAP-alpha"]}
            )
            assert updated["updated"] == ["capabilities"]
            transitioned = module.transition_skill("alpha-review", "active")
            assert transitioned["to_state"] == "active"
            loaded = module.get_skill("alpha-review")
        finally:
            os.chdir(old)
        assert loaded["validation_errors"] == []
        assert loaded["spec"]["capabilities"] == ["CAP-alpha"]
        assert Path(loaded["path"]).name == "SKILL.md"


if __name__ == "__main__":
    test_skill_lifecycle_uses_package_manifest()
    print("All tests passed.")
