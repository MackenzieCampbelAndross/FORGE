"""Unit tests for ground truth rubrics and RubricValidator scoring engine."""

import pytest

from forge.benchmark.ground_truth import GroundTruthRules
from forge.benchmark.rubric_validator import RubricValidationError, RubricValidator
from forge.schemas.evaluation import BenchmarkCategory


def test_all_category_rubrics_are_valid() -> None:
    """Verify default rubrics for all 7 benchmark categories are structurally sound."""
    for category in BenchmarkCategory:
        rubric = GroundTruthRules.get_rubric_for_category(category)
        errors = RubricValidator.validate_rubric(rubric)
        assert len(errors) == 0, f"Rubric for {category} has validation errors: {errors}"


def test_rubric_validation_catches_invalid_sums() -> None:
    """Verify weights not summing to 1.0 are caught."""
    bad_rubric = {
        "requirement_coverage": 0.50,
        "constraint_satisfaction": 0.20,
        "dependency_validity": 0.10,
        "decision_traceability": 0.10,
        "mitigation_coverage": 0.05,  # Sum is 0.95
    }
    errors = RubricValidator.validate_rubric(bad_rubric)
    assert any("do not sum to 1.0" in err for err in errors)


def test_rubric_validation_catches_negative_weights() -> None:
    """Verify negative weights are rejected."""
    bad_rubric = {
        "requirement_coverage": 0.50,
        "constraint_satisfaction": 0.60,
        "dependency_validity": -0.10,
        "decision_traceability": 0.0,
        "mitigation_coverage": 0.0,
    }
    errors = RubricValidator.validate_rubric(bad_rubric)
    assert any("non-positive weight" in err for err in errors)


def test_rubric_validation_catches_missing_dimensions() -> None:
    """Verify missing required metric dimensions are reported."""
    incomplete = {
        "requirement_coverage": 0.50,
        "constraint_satisfaction": 0.50,
    }
    errors = RubricValidator.validate_rubric(incomplete)
    assert any("Missing required metric dimensions" in err for err in errors)


def test_compute_weighted_score_exact() -> None:
    """Verify accurate weighted score computation."""
    rubric = {
        "requirement_coverage": 0.40,
        "constraint_satisfaction": 0.30,
        "dependency_validity": 0.10,
        "decision_traceability": 0.10,
        "mitigation_coverage": 0.10,
    }
    metrics = {
        "requirement_coverage": 1.0,
        "constraint_satisfaction": 0.8,
        "dependency_validity": 0.5,
        "decision_traceability": 0.7,
        "mitigation_coverage": 0.9,
    }
    # Expected: 0.4*1.0 + 0.3*0.8 + 0.1*0.5 + 0.1*0.7 + 0.1*0.9
    # = 0.40 + 0.24 + 0.05 + 0.07 + 0.09 = 0.85
    score, contributions = RubricValidator.compute_weighted_score(metrics, rubric=rubric)
    assert score == 0.85
    assert contributions["requirement_coverage"] == 0.4
    assert contributions["constraint_satisfaction"] == 0.24


def test_compute_weighted_score_clamping() -> None:
    """Verify metric values > 1.0 or < 0.0 are clamped to [0.0, 1.0]."""
    rubric = GroundTruthRules.get_rubric_for_category(BenchmarkCategory.BACKEND_SYSTEMS)
    metrics = {
        "requirement_coverage": 1.5,  # clamped to 1.0
        "constraint_satisfaction": -0.2,  # clamped to 0.0
        "dependency_validity": 1.0,
        "decision_traceability": 1.0,
        "mitigation_coverage": 1.0,
    }
    score, _ = RubricValidator.compute_weighted_score(metrics, rubric=rubric)
    assert 0.0 <= score <= 1.0


def test_compute_weighted_score_raises_on_invalid_rubric() -> None:
    """Verify invalid rubric raises RubricValidationError."""
    invalid = {"requirement_coverage": 0.1}
    with pytest.raises(RubricValidationError):
        RubricValidator.compute_weighted_score({}, rubric=invalid)
