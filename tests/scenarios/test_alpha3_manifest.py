from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_alpha3_scenario_corpus_is_complete_and_below_threshold() -> None:
    manifest = yaml.safe_load(
        (ROOT / "scenarios/alpha3/manifest.yaml").read_text()
    )
    scenarios = manifest["scenarios"]
    assert len(scenarios) >= 20
    assert len({item["id"] for item in scenarios}) == len(scenarios)
    required = {
        "archive", "art", "decisions", "evaluation", "evidence", "gates",
        "interoperability", "migration", "ontology", "propositions",
        "quality", "relations", "release", "team", "work",
    }
    assert required <= {item["area"] for item in scenarios}
    results = manifest["results"]
    assert results["executed"] == len(scenarios)
    assert results["malformed_percent"] == (
        results["malformed"] * 100 / results["executed"]
    )
    assert results["malformed_percent"] < (
        manifest["malformed_output_threshold_percent"]
    )
