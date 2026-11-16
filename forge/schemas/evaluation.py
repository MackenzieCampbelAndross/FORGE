"""Pydantic schemas for metrics, benchmarks, baselines, and ablation studies."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class BenchmarkCategory(str, Enum):
    BACKEND_SYSTEMS = "Backend systems"
    DISTRIBUTED_SYSTEMS = "Distributed systems"
    AI_ML_SYSTEMS = "AI and ML systems"
    DATABASE_SYSTEMS = "Database systems"
    CLOUD_INFRASTRUCTURE = "Cloud infrastructure"
    SECURITY_CRITICAL = "Security critical systems"
    GENERAL_ARCHITECTURE = "General software architecture"


class GroundTruthStatus(str, Enum):
    DRAFT = "Draft"
    PROGRAMMATICALLY_VALIDATED = "Programmatically validated"
    EXPERT_REVIEWED = "Expert reviewed"


class BenchmarkScenario(BaseModel):
    """A standardized engineering scenario in FEB v1.0."""

    scenario_id: str = Field(..., description="Unique ID, e.g. FEB-BACKEND-001")
    category: BenchmarkCategory = Field(...)
    title: str = Field(...)
    objective: str = Field(...)
    context: str | None = Field(default="")
    constraints: list[str] = Field(default_factory=list)
    expected_functional_requirements: list[str] = Field(default_factory=list)
    expected_nfr_categories: list[str] = Field(default_factory=list)
    expected_components: list[str] = Field(default_factory=list)
    expected_threat_categories: list[str] = Field(default_factory=list)
    evaluation_rubric: dict[str, float] = Field(default_factory=dict)
    ground_truth_status: GroundTruthStatus = Field(default=GroundTruthStatus.DRAFT)
    dataset_version: str = Field(default="1.0.0")


class MetricResult(BaseModel):
    """Result of a single engineering metric evaluation."""

    name: str = Field(...)
    category: str = Field(
        ..., description="e.g. Requirement, Architecture, Security, Reliability, Efficiency"
    )
    value: float | None = Field(
        default=None, description="Computed numerical value or None if not measurable"
    )
    unit: str = Field(default="percent", description="percent, seconds, count, ratio, usd")
    status: str = Field(default="VALID", description="VALID, ZERO_DENOMINATOR, NOT_MEASURED")
    details: dict[str, Any] = Field(default_factory=dict)


class EvaluationScorecard(BaseModel):
    """Comprehensive evaluation scorecard for a system run."""

    run_id: str = Field(...)
    scenario_id: str | None = Field(default=None)
    metrics: dict[str, MetricResult] = Field(default_factory=dict)
    composite_score: float = Field(default=0.0)
    passed: bool = Field(default=True)
    summary_notes: list[str] = Field(default_factory=list)


class AblationConfig(BaseModel):
    """Configuration for an ablation experiment."""

    name: str = Field(...)
    enable_supervisor_revision: bool = Field(default=True)
    enable_security_agent: bool = Field(default=True)
    enable_traceability: bool = Field(default=True)
    enable_architecture_validation: bool = Field(default=True)
    enable_structured_output_validation: bool = Field(default=True)


class BaselineType(str, Enum):
    BASELINE_A_SINGLE_LLM = "BASELINE_A"
    BASELINE_B_SEQUENTIAL_NO_SUPERVISOR = "BASELINE_B"
    FORGE_V1_FULL = "FORGE_V1"


class ExperimentResult(BaseModel):
    """Record of a single benchmark/baseline/ablation execution."""

    experiment_id: str = Field(...)
    scenario_id: str = Field(...)
    configuration_type: str = Field(...)
    model_provider: str = Field(...)
    model_name: str = Field(...)
    execution_time_seconds: float = Field(...)
    total_tokens: int | None = Field(default=None)
    estimated_cost_usd: float | None = Field(default=None)
    scorecard: EvaluationScorecard = Field(...)
    final_status: str = Field(...)
    error_message: str | None = Field(default=None)
