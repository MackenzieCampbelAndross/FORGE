"""Benchmark scenario models and ground truth definitions."""

from forge.schemas.evaluation import BenchmarkCategory


class GroundTruthRules:
    """Standard evaluation rubrics for benchmark categories."""

    RUBRICS: dict[BenchmarkCategory, dict[str, float]] = {
        BenchmarkCategory.BACKEND_SYSTEMS: {
            "requirement_coverage": 0.25,
            "constraint_satisfaction": 0.25,
            "dependency_validity": 0.20,
            "mitigation_coverage": 0.15,
            "decision_traceability": 0.15,
        },
        BenchmarkCategory.DISTRIBUTED_SYSTEMS: {
            "requirement_coverage": 0.20,
            "constraint_satisfaction": 0.20,
            "dependency_validity": 0.25,
            "decision_traceability": 0.20,
            "mitigation_coverage": 0.15,
        },
        BenchmarkCategory.AI_ML_SYSTEMS: {
            "requirement_coverage": 0.25,
            "constraint_satisfaction": 0.20,
            "decision_traceability": 0.25,
            "dependency_validity": 0.15,
            "mitigation_coverage": 0.15,
        },
        BenchmarkCategory.DATABASE_SYSTEMS: {
            "constraint_satisfaction": 0.30,
            "requirement_coverage": 0.20,
            "decision_traceability": 0.25,
            "dependency_validity": 0.15,
            "mitigation_coverage": 0.10,
        },
        BenchmarkCategory.CLOUD_INFRASTRUCTURE: {
            "constraint_satisfaction": 0.25,
            "dependency_validity": 0.25,
            "requirement_coverage": 0.20,
            "mitigation_coverage": 0.15,
            "decision_traceability": 0.15,
        },
        BenchmarkCategory.SECURITY_CRITICAL: {
            "mitigation_coverage": 0.35,
            "constraint_satisfaction": 0.25,
            "requirement_coverage": 0.15,
            "dependency_validity": 0.15,
            "decision_traceability": 0.10,
        },
        BenchmarkCategory.GENERAL_ARCHITECTURE: {
            "requirement_coverage": 0.25,
            "constraint_satisfaction": 0.25,
            "dependency_validity": 0.20,
            "decision_traceability": 0.15,
            "mitigation_coverage": 0.15,
        },
    }

    @classmethod
    def get_rubric_for_category(cls, category: BenchmarkCategory) -> dict[str, float]:
        return cls.RUBRICS.get(category, cls.RUBRICS[BenchmarkCategory.GENERAL_ARCHITECTURE])
