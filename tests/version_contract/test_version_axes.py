from __future__ import annotations

from pathlib import Path
import sys

import yaml


ROOT = Path(__file__).resolve().parents[2]
LIBRARY = ROOT / "src/context/skills/_lib"
sys.path.insert(0, str(LIBRARY))

import processkit  # noqa: E402


def test_product_and_entity_api_versions_are_independent() -> None:
    assert processkit.__version__ == "1.0.0-alpha.1"
    assert processkit.API_VERSION == "processkit.projectious.work/v2"

    registry = yaml.safe_load(
        (ROOT / "src/context/schemas/src/registry.yaml").read_text()
    )
    assert registry["version"] == 1
    assert registry["release_track"] == "v1.0"
    assert registry["entity_api_version"] == processkit.API_VERSION


def test_schema_versions_remain_per_kind() -> None:
    generated = ROOT / "src/context/schemas/_generated"
    workitem = yaml.safe_load((generated / "workitem.yaml").read_text())
    gate = yaml.safe_load((generated / "gate.yaml").read_text())
    assert workitem["metadata"]["version"] == "2.0.0-alpha.1"
    assert gate["metadata"]["version"] == "1.0.0"
