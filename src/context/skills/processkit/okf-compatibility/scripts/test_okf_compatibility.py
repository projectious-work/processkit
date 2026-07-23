from __future__ import annotations

import importlib.util
import os
import shutil
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[6]
SERVER = Path(__file__).resolve().parents[1] / "mcp" / "server.py"
FIXTURE = ROOT / "tests" / "fixtures" / "alpha-project"


def _load():
    spec = importlib.util.spec_from_file_location("okf_compatibility", SERVER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_alpha_fixture_exports_conformant_bundle() -> None:
    module = _load()
    with tempfile.TemporaryDirectory() as td:
        project = Path(td) / "project"
        shutil.copytree(FIXTURE, project)
        old = Path.cwd()
        try:
            os.chdir(project)
            result = module.export_okf_bundle("exports/alpha-okf")
            checked = module.validate_okf_bundle("exports/alpha-okf")
        finally:
            os.chdir(old)
        assert result["ok"] is True
        expected = sum(
            yaml.safe_load((project / "fixture.yaml").read_text())["expected"][
                "entity_counts"
            ].values()
        )
        assert result["entity_count"] == expected
        assert checked["valid"] is True
        assert checked["document_count"] == expected
        assert (project / "exports/alpha-okf/index.md").is_file()


if __name__ == "__main__":
    test_alpha_fixture_exports_conformant_bundle()
    print("All tests passed.")
