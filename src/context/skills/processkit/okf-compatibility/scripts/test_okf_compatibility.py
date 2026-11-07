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


def test_producer_profile_round_trips_into_empty_project() -> None:
    module = _load()
    with tempfile.TemporaryDirectory() as td:
        temp = Path(td)
        source = temp / "source"
        target = temp / "target"
        shutil.copytree(FIXTURE, source)
        (target / "context").mkdir(parents=True)
        (target / "AGENTS.md").write_text("# import fixture\n")
        shutil.copytree(
            ROOT / "src/context/schemas",
            target / "context/schemas",
        )
        old = Path.cwd()
        try:
            os.chdir(source)
            exported = module.export_okf_bundle("exports/round-trip")
            shutil.copytree(
                source / "exports/round-trip",
                target / "imports/round-trip",
            )
            os.chdir(target)
            planned = module.import_okf_bundle(
                "imports/round-trip",
                dry_run=True,
            )
            imported = module.import_okf_bundle("imports/round-trip")
            refused = module.import_okf_bundle("imports/round-trip")
        finally:
            os.chdir(old)

        assert exported["ok"] is True
        assert planned["ok"] is True
        assert len(planned["planned"]) == exported["entity_count"]
        assert planned["imported"] == []
        assert imported["ok"] is True
        assert len(imported["imported"]) == exported["entity_count"]
        assert refused["ok"] is False
        assert all(
            "target entity already exists" in error["error"]
            for error in refused["errors"]
        )
        for source_path in sorted((source / "context").rglob("*.md")):
            try:
                source_entity = module.entity.load(source_path)
            except module.entity.EntityError:
                continue
            if source_entity.id not in imported["imported"]:
                continue
            matches = list(
                (target / "context").rglob(f"{source_entity.id}.md")
            )
            assert len(matches) == 1, source_entity.id
            imported_entity = module.entity.load(matches[0])
            assert imported_entity.kind == source_entity.kind
            assert imported_entity.spec == source_entity.spec
            assert imported_entity.body == source_entity.body


def test_import_rejects_adversarial_producer_profile() -> None:
    module = _load()
    with tempfile.TemporaryDirectory() as td:
        project = Path(td) / "project"
        shutil.copytree(FIXTURE, project)
        old = Path.cwd()
        try:
            os.chdir(project)
            exported = module.export_okf_bundle("exports/adversarial")
            assert exported["ok"] is True
            documents = sorted(
                (project / "exports/adversarial/concepts").rglob("*.md")
            )
            frontmatter, body = module.parse(documents[0].read_text())
            frontmatter["type"] = "processkit.wrong-kind"
            documents[0].write_text(module.render(frontmatter, body))
            frontmatter, body = module.parse(documents[1].read_text())
            frontmatter["processkit_id"] = "not-a-processkit-id"
            documents[1].write_text(module.render(frontmatter, body))
            for document in documents[2:]:
                frontmatter, body = module.parse(document.read_text())
                if frontmatter.get("processkit_kind") == "WorkItem":
                    frontmatter["processkit_spec"] = {}
                    document.write_text(module.render(frontmatter, body))
                    break
            result = module.import_okf_bundle(
                "exports/adversarial",
                dry_run=True,
            )
        finally:
            os.chdir(old)

        assert result["ok"] is False
        messages = [error["error"] for error in result["errors"]]
        assert any("does not match processkit_kind" in item for item in messages)
        assert any("valid processkit_id" in item for item in messages)
        assert any("schema validation" in item for item in messages)


if __name__ == "__main__":
    test_alpha_fixture_exports_conformant_bundle()
    print("All tests passed.")
