"""Comprehensive validation test suite for modular FEB scenario JSON definitions."""

import re
from pathlib import Path

from forge.benchmark.loader import BenchmarkLoader
from forge.benchmark.search import ScenarioSearchEngine
from forge.schemas.evaluation import BenchmarkCategory, BenchmarkScenario

SCENARIOS_DIR = Path("forge/benchmark/scenarios")

DOMAIN_DIR_MAP = {
    "backend": BenchmarkCategory.BACKEND_SYSTEMS,
    "distributed": BenchmarkCategory.DISTRIBUTED_SYSTEMS,
    "aiml": BenchmarkCategory.AI_ML_SYSTEMS,
    "database": BenchmarkCategory.DATABASE_SYSTEMS,
    "cloud": BenchmarkCategory.CLOUD_INFRASTRUCTURE,
    "security": BenchmarkCategory.SECURITY_CRITICAL,
    "general": BenchmarkCategory.GENERAL_ARCHITECTURE,
}


def test_modular_scenarios_discovery() -> None:
    """Verify all 100 modular scenario JSON files exist across the 7 category folders."""
    json_files = list(SCENARIOS_DIR.glob("*/*.json"))
    assert len(json_files) == 100, f"Expected 100 JSON scenario files, found {len(json_files)}"


def test_modular_scenarios_parsing_and_schema() -> None:
    """Verify each scenario file parses cleanly into BenchmarkScenario with valid fields."""
    scenarios: list[BenchmarkScenario] = []

    for domain_dir, expected_category in DOMAIN_DIR_MAP.items():
        domain_path = SCENARIOS_DIR / domain_dir
        assert domain_path.exists(), f"Domain directory {domain_path} missing"

        files = list(domain_path.glob("*.json"))
        assert len(files) > 0, f"No JSON files found in {domain_path}"

        for f in files:
            loaded = BenchmarkLoader.load_from_file(str(f))
            assert len(loaded) == 1, f"Expected 1 scenario in {f}, got {len(loaded)}"
            sc = loaded[0]

            assert re.match(r"^FEB-[A-Z0-9]+-\d{3}$", sc.scenario_id), f"Invalid ID format: {sc.scenario_id}"
            assert sc.category == expected_category, f"Mismatch in category for {f.name}"
            assert len(sc.title.strip()) > 5
            assert len(sc.objective.strip()) > 10
            assert len(sc.constraints) > 0
            assert len(sc.expected_functional_requirements) > 0
            assert len(sc.expected_components) > 0
            assert len(sc.expected_threat_categories) > 0

            scenarios.append(sc)

    assert len(scenarios) == 100


def test_scenario_search_and_filter() -> None:
    """Verify ScenarioSearchEngine works across the full suite."""
    all_scenarios: list[BenchmarkScenario] = []
    for f in SCENARIOS_DIR.glob("*/*.json"):
        all_scenarios.extend(BenchmarkLoader.load_from_file(str(f)))

    engine = ScenarioSearchEngine(all_scenarios)
    assert engine.count() == 100

    backend_scenarios = engine.filter(category=BenchmarkCategory.BACKEND_SYSTEMS)
    assert len(backend_scenarios) == 20

    dist_scenarios = engine.filter(category=BenchmarkCategory.DISTRIBUTED_SYSTEMS)
    assert len(dist_scenarios) == 15

    # Keyword filter test
    cached_scenarios = engine.filter(keyword="cache")
    assert len(cached_scenarios) > 0

    # Constraint count filter
    constrained = engine.filter(min_constraints=2)
    assert len(constrained) > 50
