from __future__ import annotations

import importlib.util
import shutil
import sys
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = (
    ROOT / "src/context/skills/_lib/processkit/schema_generation.py"
)
SCHEMAS_ROOT = ROOT / "src/context/schemas"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


generation = _load_module("schema_generation_test", MODULE_PATH)


def test_committed_generation_is_current() -> None:
    result = generation.regenerate_schemas(SCHEMAS_ROOT, check=True)
    assert result == {
        "rebuilt": [],
        "unchanged": [
            "workitem",
            "decisionrecord",
            "binding",
            "logentry",
        ],
        "errors": {},
    }


def test_source_level_jinja_include_is_rendered() -> None:
    source = (
        SCHEMAS_ROOT / "src/fragments/entity.yaml"
    ).read_text(encoding="utf-8")
    assert "{% include" in source
    document = yaml.safe_load(
        (SCHEMAS_ROOT / "_generated/workitem.yaml").read_text()
    )
    assert document["spec"]["generation"]["format"] == (
        "processkit-schema-source-v1"
    )


def test_full_generation_is_deterministic(tmp_path: Path) -> None:
    first = generation.regenerate_schemas(SCHEMAS_ROOT, output_dir=tmp_path)
    first_bytes = {
        path.name: path.read_bytes() for path in sorted(tmp_path.glob("*.yaml"))
    }
    second = generation.regenerate_schemas(SCHEMAS_ROOT, output_dir=tmp_path)
    second_bytes = {
        path.name: path.read_bytes() for path in sorted(tmp_path.glob("*.yaml"))
    }
    assert first["rebuilt"] == [
        "workitem",
        "decisionrecord",
        "binding",
        "logentry",
    ]
    assert second["rebuilt"] == []
    assert first_bytes == second_bytes


def test_partial_generation_does_not_touch_other_kinds(tmp_path: Path) -> None:
    result = generation.regenerate_schemas(
        SCHEMAS_ROOT,
        kinds=["decisionrecord"],
        output_dir=tmp_path,
    )
    assert result["rebuilt"] == ["decisionrecord"]
    assert [path.name for path in tmp_path.iterdir()] == [
        "decisionrecord.yaml"
    ]


def test_merge_strategies() -> None:
    parent = {"items": ["a"], "properties": {"a": {"type": "string"}}}
    merged = generation.merge_documents(
        parent,
        {
            "items": {"__merge": "concat", "value": ["b"]},
            "properties": {
                "__merge": "name-merge",
                "value": {
                    "a": {"minLength": 1},
                    "b": {"type": "integer"},
                },
            },
        },
    )
    assert merged == {
        "items": ["a", "b"],
        "properties": {
            "a": {"type": "string", "minLength": 1},
            "b": {"type": "integer"},
        },
    }
    assert generation.merge_documents(
        {"value": [1]},
        {"value": {"__merge": "replace", "value": [2]}},
    ) == {"value": [2]}


def test_invalid_merge_and_unknown_kind_are_reported() -> None:
    with pytest.raises(
        generation.SchemaGenerationError, match="requires lists"
    ):
        generation.merge_documents(
            {"value": {}},
            {"value": {"__merge": "concat", "value": []}},
        )
    result = generation.regenerate_schemas(SCHEMAS_ROOT, ["unknown"])
    assert result["errors"] == {"unknown": "unknown kind"}


def test_output_path_escape_is_rejected(tmp_path: Path) -> None:
    schemas = tmp_path / "schemas"
    shutil.copytree(SCHEMAS_ROOT, schemas)
    registry_path = schemas / "src/registry.yaml"
    registry = yaml.safe_load(registry_path.read_text())
    registry["kinds"]["workitem"]["output"] = "../escaped.yaml"
    registry_path.write_text(yaml.safe_dump(registry, sort_keys=False))

    output = tmp_path / "output"
    result = generation.regenerate_schemas(schemas, output_dir=output)
    assert "workitem" in result["errors"]
    assert not (tmp_path / "escaped.yaml").exists()


def test_render_failure_does_not_partially_update_outputs(
    tmp_path: Path,
) -> None:
    schemas = tmp_path / "schemas"
    shutil.copytree(SCHEMAS_ROOT, schemas)
    output = tmp_path / "output"
    output.mkdir()
    existing = output / "workitem.yaml"
    existing.write_text("previous output\n")
    broken = schemas / "src/compositions/logentry.yaml"
    broken.write_text("[\n")

    result = generation.regenerate_schemas(schemas, output_dir=output)
    assert "logentry" in result["errors"]
    assert result["rebuilt"] == []
    assert existing.read_text() == "previous output\n"


def test_registry_target_and_output_collisions_are_rejected(
    tmp_path: Path,
) -> None:
    schemas = tmp_path / "schemas"
    shutil.copytree(SCHEMAS_ROOT, schemas)
    registry_path = schemas / "src/registry.yaml"
    registry = yaml.safe_load(registry_path.read_text())
    registry["kinds"]["decisionrecord"]["output"] = "workitem.yaml"
    registry_path.write_text(yaml.safe_dump(registry, sort_keys=False))
    result = generation.regenerate_schemas(
        schemas, output_dir=tmp_path / "output"
    )
    assert "decisionrecord" in result["errors"]

    registry["kinds"]["decisionrecord"]["output"] = "decisionrecord.yaml"
    registry_path.write_text(yaml.safe_dump(registry, sort_keys=False))
    decision = schemas / "src/compositions/decisionrecord.yaml"
    decision.write_text(
        decision.read_text().replace(
            "target_kind: DecisionRecord", "target_kind: WorkItem"
        )
    )
    result = generation.regenerate_schemas(
        schemas, output_dir=tmp_path / "output"
    )
    assert "decisionrecord" in result["errors"]


def test_generated_schema_precedes_flat_fallback(tmp_path: Path) -> None:
    library = ROOT / "src/context/skills/_lib"
    sys.path.insert(0, str(library))
    try:
        from processkit import schema

        (tmp_path / "_generated").mkdir()
        flat = {"kind": "Schema", "spec": {"description": "flat"}}
        generated = {
            "kind": "Schema",
            "spec": {"description": "generated"},
        }
        (tmp_path / "workitem.yaml").write_text(yaml.safe_dump(flat))
        (tmp_path / "_generated/workitem.yaml").write_text(
            yaml.safe_dump(generated)
        )
        schema.load_schema.cache_clear()
        assert schema.load_schema("WorkItem", tmp_path)["description"] == (
            "generated"
        )
        (tmp_path / "_generated/workitem.yaml").unlink()
        schema.load_schema.cache_clear()
        assert schema.load_schema("WorkItem", tmp_path)["description"] == "flat"
    finally:
        sys.path.remove(str(library))


def test_checkout_prefers_shipped_generated_schema_root(
    tmp_path: Path,
) -> None:
    library = ROOT / "src/context/skills/_lib"
    sys.path.insert(0, str(library))
    try:
        from processkit import paths

        consumer = tmp_path / "context/schemas"
        shipped = tmp_path / "src/context/schemas"
        consumer.mkdir(parents=True)
        (shipped / "_generated").mkdir(parents=True)
        assert paths.primitive_schemas_dir(tmp_path) == shipped
    finally:
        sys.path.remove(str(library))
