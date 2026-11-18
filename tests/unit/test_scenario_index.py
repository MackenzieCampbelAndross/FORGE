"""Validation test suite for scenario domain index metadata."""

import json
from pathlib import Path

from forge.benchmark.ground_truth import GroundTruthRules
from forge.schemas.evaluation import BenchmarkCategory

INDEX_PATH = Path("forge/benchmark/scenarios/index.json")


def test_scenario_index_structure() -> None:
    """Verify scenario index JSON structure and counts."""
    assert INDEX_PATH.exists(), "index.json missing"
    data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))

    assert data["benchmark_version"] == "1.0.0"
    assert data["total_scenarios"] == 100

    domains = data["domains"]
    assert len(domains) == 7

    total_counted = sum(d["count"] for d in domains.values())
    assert total_counted == 100


def test_scenario_index_directories_and_prefixes() -> None:
    """Verify each indexed domain has corresponding files matching prefix and count."""
    data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))

    for _key, meta in data["domains"].items():
        dir_path = Path(meta["directory"])
        assert dir_path.exists(), f"Directory {dir_path} does not exist"

        json_files = list(dir_path.glob("*.json"))
        assert len(json_files) == meta["count"], (
            f"Expected {meta['count']} files in {dir_path}, found {len(json_files)}"
        )

        for jf in json_files:
            file_data = json.loads(jf.read_text(encoding="utf-8"))
            sc_id = file_data["scenario_id"]
            assert sc_id.startswith(meta["prefix"]), f"Scenario ID {sc_id} does not start with prefix {meta['prefix']}"


def test_scenario_index_rubric_weights_match_rules() -> None:
    """Verify rubric weights in index match GroundTruthRules definitions."""
    data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))

    cat_map = {
        "backend": BenchmarkCategory.BACKEND_SYSTEMS,
        "distributed": BenchmarkCategory.DISTRIBUTED_SYSTEMS,
        "aiml": BenchmarkCategory.AI_ML_SYSTEMS,
        "database": BenchmarkCategory.DATABASE_SYSTEMS,
        "cloud": BenchmarkCategory.CLOUD_INFRASTRUCTURE,
        "security": BenchmarkCategory.SECURITY_CRITICAL,
        "general": BenchmarkCategory.GENERAL_ARCHITECTURE,
    }

    for key, cat in cat_map.items():
        expected_rubric = GroundTruthRules.get_rubric_for_category(cat)
        indexed_rubric = data["domains"][key]["rubric_weights"]
        assert indexed_rubric == expected_rubric, f"Rubric mismatch for domain {key}"
