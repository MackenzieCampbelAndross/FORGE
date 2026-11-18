"""Ground-truth rubric validator and weighted scoring engine."""

from __future__ import annotations

import math

from forge.benchmark.ground_truth import GroundTruthRules
from forge.schemas.evaluation import BenchmarkCategory, BenchmarkScenario


class RubricValidationError(Exception):
    """Raised when a benchmark evaluation rubric fails structural or numerical constraints."""


class RubricValidator:
    """Validates rubric weight distributions and computes weighted benchmark scores."""

    REQUIRED_DIMENSIONS = {
        "requirement_coverage",
        "constraint_satisfaction",
        "dependency_validity",
        "decision_traceability",
        "mitigation_coverage",
    }

    @classmethod
    def validate_rubric(cls, rubric: dict[str, float]) -> list[str]:
        """Validate that a rubric map satisfies sum-to-one, positivity, and dimension requirements.

        Returns a list of error strings; empty list indicates valid rubric.
        """
        errors: list[str] = []

        if not rubric:
            return ["Rubric dictionary is empty."]

        # Check weight positivity
        total_weight = 0.0
        for dim, weight in rubric.items():
            if weight <= 0.0:
                errors.append(f"Dimension '{dim}' has non-positive weight: {weight}")
            if weight > 1.0:
                errors.append(f"Dimension '{dim}' exceeds maximum weight 1.0: {weight}")
            total_weight += weight

        # Check sum to 1.0
        if not math.isclose(total_weight, 1.0, rel_tol=1e-4, abs_tol=1e-4):
            errors.append(f"Rubric weights do not sum to 1.0 (got {total_weight:.4f})")

        # Check required dimensions
        missing = cls.REQUIRED_DIMENSIONS - set(rubric.keys())
        if missing:
            errors.append(f"Missing required metric dimensions: {sorted(missing)}")

        return errors

    @classmethod
    def validate_scenario(cls, scenario: BenchmarkScenario) -> list[str]:
        """Validate the rubric of a single scenario against category rules."""
        errors: list[str] = []
        if scenario.evaluation_rubric:
            errors.extend(cls.validate_rubric(scenario.evaluation_rubric))
        else:
            # Fallback to category rules
            default_rubric = GroundTruthRules.get_rubric_for_category(scenario.category)
            errors.extend(cls.validate_rubric(default_rubric))
        return errors

    @classmethod
    def compute_weighted_score(
        cls,
        metric_values: dict[str, float],
        rubric: dict[str, float] | None = None,
        category: BenchmarkCategory | None = None,
    ) -> tuple[float, dict[str, float]]:
        """Calculate aggregate weighted score and detailed dimensional contribution.

        Returns (total_score, per_dimension_contributions).
        """
        active_rubric = rubric
        if not active_rubric:
            cat = category or BenchmarkCategory.GENERAL_ARCHITECTURE
            active_rubric = GroundTruthRules.get_rubric_for_category(cat)

        validation_errors = cls.validate_rubric(active_rubric)
        if validation_errors:
            raise RubricValidationError("; ".join(validation_errors))

        contributions: dict[str, float] = {}
        total_score = 0.0

        for dim, weight in active_rubric.items():
            raw_val = metric_values.get(dim, 0.0)
            clamped = max(0.0, min(1.0, float(raw_val)))
            contribution = clamped * weight
            contributions[dim] = round(contribution, 4)
            total_score += contribution

        return round(total_score, 4), contributions
