"""Pydantic schemas for requirements engineering and project objectives."""

from datetime import UTC, datetime
from enum import Enum

from pydantic import BaseModel, Field


class RequirementPriority(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class RequirementSource(str, Enum):
    EXPLICIT = "EXPLICIT"
    INFERRED = "INFERRED"
    ASSUMPTION = "ASSUMPTION"
    UNKNOWN = "UNKNOWN"


class RequirementCategory(str, Enum):
    PERFORMANCE = "PERFORMANCE"
    SECURITY = "SECURITY"
    SCALABILITY = "SCALABILITY"
    RELIABILITY = "RELIABILITY"
    COMPLIANCE = "COMPLIANCE"
    OPERATIONAL = "OPERATIONAL"
    USABILITY = "USABILITY"


class ConstraintCategory(str, Enum):
    REGULATORY = "REGULATORY"
    TECHNICAL = "TECHNICAL"
    BUDGET = "BUDGET"
    TIMELINE = "TIMELINE"
    INFRASTRUCTURE = "INFRASTRUCTURE"


class ProjectObjective(BaseModel):
    """User-supplied high-level project objective and context."""

    project_id: str = Field(..., description="Unique project identifier")
    objective: str = Field(
        ..., min_length=5, description="High level software engineering objective"
    )
    domain: str | None = Field(default="General Software", description="Domain/industry context")
    context: str | None = Field(
        default="", description="Additional organizational or technical context"
    )
    constraints: list[str] = Field(default_factory=list, description="Raw initial constraints")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class FunctionalRequirement(BaseModel):
    """Specific functional requirement."""

    requirement_id: str = Field(..., description="Unique ID, e.g. FR-001")
    description: str = Field(
        ..., min_length=5, description="Clear description of functional capability"
    )
    priority: RequirementPriority = Field(default=RequirementPriority.HIGH)
    acceptance_criteria: list[str] = Field(
        default_factory=list, description="Verifiable test criteria"
    )
    source: RequirementSource = Field(default=RequirementSource.EXPLICIT)


class NonFunctionalRequirement(BaseModel):
    """Measurable non-functional quality attribute."""

    requirement_id: str = Field(..., description="Unique ID, e.g. NFR-001")
    category: RequirementCategory = Field(...)
    description: str = Field(..., min_length=5)
    measurable_target: str = Field(..., description="Specific target e.g. '< 200ms p99 latency'")
    priority: RequirementPriority = Field(default=RequirementPriority.HIGH)
    source: RequirementSource = Field(default=RequirementSource.EXPLICIT)


class SystemConstraint(BaseModel):
    """System boundary or invariant constraint."""

    constraint_id: str = Field(..., description="Unique ID, e.g. CON-001")
    category: ConstraintCategory = Field(default=ConstraintCategory.TECHNICAL)
    description: str = Field(..., min_length=5)
    mandatory: bool = Field(default=True)
    source: RequirementSource = Field(default=RequirementSource.EXPLICIT)


class RequirementsDoc(BaseModel):
    """Structured requirements document produced by the Strategy Agent."""

    document_id: str = Field(..., description="Unique requirements document ID")
    project_id: str = Field(...)
    executive_summary: str = Field(..., min_length=10)
    functional_requirements: list[FunctionalRequirement] = Field(default_factory=list)
    non_functional_requirements: list[NonFunctionalRequirement] = Field(default_factory=list)
    constraints: list[SystemConstraint] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    ambiguous_requirements: list[str] = Field(default_factory=list)
    contradictions: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
