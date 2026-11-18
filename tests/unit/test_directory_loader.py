"""Unit tests for BenchmarkLoader directory loading and dataset validation."""

from pathlib import Path

import pytest

from forge.benchmark.loader import BenchmarkLoader
from forge.core.exceptions import BenchmarkError
from forge.schemas.evaluation import BenchmarkCategory, BenchmarkScenario, GroundTruthStatus


def test_load_from_directory_backend() -> None:
    """Verify loading a single domain folder loads all 20 scenarios."""
    scenarios = BenchmarkLoader.load_from_directory("forge/benchmark/scenarios/backend")
    assert len(scenarios) == 20
    for s in scenarios:
        assert s.category == BenchmarkCategory.BACKEND_SYSTEMS


def test_load_from_directory_nonexistent() -> None:
    """Verify loading from nonexistent directory raises BenchmarkError."""
    with pytest.raises(BenchmarkError, match="Directory not found"):
        BenchmarkLoader.load_from_directory("nonexistent/directory/path")


def test_load_from_directory_corrupt_json(tmp_path: Path) -> None:
    """Verify corrupted JSON raises BenchmarkError."""
    corrupt_file = tmp_path / "bad.json"
    corrupt_file.write_text("{ broken json content", encoding="utf-8")

    with pytest.raises(BenchmarkError):
        BenchmarkLoader.load_from_directory(str(tmp_path))


def test_validate_dataset_valid() -> None:
    """Verify dataset validation passes on clean scenario collection."""
    scenarios = BenchmarkLoader.load_from_directory("forge/benchmark/scenarios/database")
    report = BenchmarkLoader.validate_dataset(scenarios)

    assert report["is_valid"] is True
    assert report["total_scenarios"] == 15
    assert report["unique_ids_count"] == 15
    assert len(report["duplicates"]) == 0
    assert BenchmarkCategory.DATABASE_SYSTEMS.value in report["categories"]


def test_validate_dataset_detects_duplicates() -> None:
    """Verify validate_dataset catches duplicate scenario IDs."""
    sc1 = BenchmarkScenario(
        scenario_id="FEB-DUP-001",
        category=BenchmarkCategory.BACKEND_SYSTEMS,
        title="Sample Title 1",
        objective="Sample Objective 1",
        ground_truth_status=GroundTruthStatus.DRAFT,
    )
    sc2 = BenchmarkScenario(
        scenario_id="FEB-DUP-001",  # duplicate ID
        category=BenchmarkCategory.BACKEND_SYSTEMS,
        title="Sample Title 2",
        objective="Sample Objective 2",
        ground_truth_status=GroundTruthStatus.DRAFT,
    )

    report = BenchmarkLoader.validate_dataset([sc1, sc2])
    assert report["is_valid"] is False
    assert len(report["duplicates"]) == 1
    assert "FEB-DUP-001" in report["duplicates"]
