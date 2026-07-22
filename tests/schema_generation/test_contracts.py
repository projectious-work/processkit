from __future__ import annotations

from pathlib import Path
import sys

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "src/context/schemas/_generated"
FIXTURE = ROOT / "tests/fixtures/alpha-project"


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    return yaml.safe_load(text.split("---\n", 2)[1])


def _schema(kind: str) -> dict:
    filename = "proposition-risk" if kind == "risk" else kind.lower()
    document = yaml.safe_load((SCHEMAS / f"{filename}.yaml").read_text())
    schema = document["spec"]["spec_schema"]
    jsonschema.Draft202012Validator.check_schema(schema)
    return document


def _without_descriptions(value):
    if isinstance(value, dict):
        return {
            key: _without_descriptions(item)
            for key, item in value.items()
            if key != "description"
        }
    if isinstance(value, list):
        return [_without_descriptions(item) for item in value]
    return value


def test_generated_schema_contracts_and_interfaces() -> None:
    expected = {
        "workitem": ["Entity", "Versioned"],
        "decisionrecord": ["Entity", "Record", "Versioned"],
        "binding": ["Entity", "Versioned", "Relationship"],
        "logentry": ["Entity", "Record"],
        "artifact": ["Entity", "Versioned"],
        "gate": ["Entity", "Versioned"],
        "proposition": ["Entity", "Versioned", "Proposition"],
        "risk": ["Entity", "Versioned", "Proposition"],
    }
    for kind, interfaces in expected.items():
        document = _schema(kind)
        assert document["apiVersion"] == "processkit.projectious.work/v2"
        assert document["spec"]["interfaces"] == interfaces
        assert document["spec"]["validation_mode"] == "tolerant"


def test_generated_schemas_preserve_flat_compatibility() -> None:
    for kind in (
        "workitem",
        "decisionrecord",
        "binding",
        "logentry",
        "artifact",
        "gate",
    ):
        generated = _schema(kind)
        flat = yaml.safe_load(
            (ROOT / f"src/context/schemas/{kind}.yaml").read_text()
        )
        generated_spec = dict(generated["spec"])
        generated_spec.pop("interfaces")
        generated_spec.pop("validation_mode")
        generated_spec.pop("generation")
        assert generated["apiVersion"] == flat["apiVersion"]
        assert generated["kind"] == flat["kind"]
        assert generated["metadata"] == flat["metadata"]
        if kind in {"artifact", "gate"}:
            assert _without_descriptions(generated_spec) == (
                _without_descriptions(flat["spec"])
            )
        else:
            assert generated_spec == flat["spec"]


def test_alpha_fixture_validates_and_matches_manifest() -> None:
    manifest = yaml.safe_load((FIXTURE / "fixture.yaml").read_text())
    seen: dict[str, int] = {}
    by_interface: dict[str, list[str]] = {}
    for path in sorted((FIXTURE / "context").rglob("*.md")):
        entity = _frontmatter(path)
        kind = entity["kind"]
        selector = (
            "risk"
            if kind == "Proposition" and entity["spec"].get("kind") == "risk"
            else kind.lower()
        )
        document = _schema(selector)
        validator = jsonschema.Draft202012Validator(
            document["spec"]["spec_schema"]
        )
        assert list(validator.iter_errors(entity["spec"])) == []
        seen[kind] = seen.get(kind, 0) + 1
        for interface in document["spec"]["interfaces"]:
            by_interface.setdefault(interface, []).append(
                entity["metadata"]["id"]
            )
    assert seen == manifest["expected"]["entity_counts"]
    for interface, expected in manifest["expected"]["interfaces"].items():
        assert by_interface[interface] == expected


def test_required_fields_and_closed_vocabularies_reject_invalid_data() -> None:
    work = _schema("workitem")["spec"]["spec_schema"]
    decision = _schema("decisionrecord")["spec"]["spec_schema"]
    log = _schema("logentry")["spec"]["spec_schema"]
    proposition = _schema("proposition")["spec"]["spec_schema"]
    risk = _schema("risk")["spec"]["spec_schema"]
    assert list(jsonschema.Draft202012Validator(work).iter_errors({}))
    assert list(jsonschema.Draft202012Validator(decision).iter_errors({}))
    assert list(jsonschema.Draft202012Validator(log).iter_errors({}))
    assert list(jsonschema.Draft202012Validator(proposition).iter_errors({}))
    assert list(
        jsonschema.Draft202012Validator(risk).iter_errors(
            {"kind": "risk", "statement": "Incomplete risk"}
        )
    )

    library = ROOT / "src/context/skills/_lib"
    sys.path.insert(0, str(library))
    try:
        from processkit import schema

        schema.load_schema.cache_clear()
        errors = schema.validate_spec(
            "WorkItem",
            {"title": "Invalid vocabulary", "state": "backlog", "type": "x"},
        )
        assert "not declared in Schema.known_types" in errors[0]
        assert schema.interfaces_for_kind("DecisionRecord") == [
            "Entity",
            "Record",
            "Versioned",
        ]
        assert schema.validation_mode("Artifact") == "tolerant"
        assert schema.validate_spec(
            "Proposition",
            {
                "kind": "risk",
                "statement": "Valid risk",
                "likelihood": "possible",
                "impact": "major",
            },
        ) == []
        assert schema.validate_spec(
            "Proposition",
            {"kind": "risk", "statement": "Incomplete risk"},
        )
        assert schema.validate_spec(
            "Proposition",
            {"kind": "unknown", "statement": "Unknown variant"},
        )
    finally:
        sys.path.remove(str(library))


def test_empty_fixture_has_no_canonical_context() -> None:
    fixture = ROOT / "tests/fixtures/empty-project"
    manifest = yaml.safe_load((fixture / "fixture.yaml").read_text())
    assert not (fixture / "context").exists()
    assert manifest["expected"]["entity_counts"] == {}
