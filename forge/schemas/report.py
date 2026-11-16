"""Pydantic schemas for the final engineering report and supervisory audit."""

from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from forge.schemas.architecture import ArchitectureBlueprint
from forge.schemas.requirements import RequirementsDoc
from forge.schemas.security import ThreatModel


class FinalStatus(str, Enum):
    APPROVED = "APPROVED"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"


class RevisionTarget(str, Enum):
    STRATEGY = "strategy"
    ARCHITECT = "architect"
    SECURITY = "security"
    NONE = "none"


class ValidationIssueSeverity(str, Enum):
    BLOCKER = "BLOCKER"
    WARNING = "WARNING"
    INFO = "INFO"


class ValidationIssue(BaseModel):
    """Specific finding produced by static or supervisory validation."""

    rule_id: str = Field(..., description="e.g. VAL-ARCH-001")
    category: str = Field(..., description="e.g. Architecture, Traceability, Security")
    severity: ValidationIssueSeverity = Field(default=ValidationIssueSeverity.BLOCKER)
    message: str = Field(...)
    target_id: str | None = Field(
        default=None, description="Affected requirement, component, or threat ID"
    )


class RevisionRecord(BaseModel):
    """Audit log of a supervisory rejection and agent revision."""

    iteration: int = Field(...)
    target_agent: RevisionTarget = Field(...)
    reason: str = Field(...)
    issues: list[ValidationIssue] = Field(default_factory=list)
    requested_correction: str = Field(...)
    resolved: bool = Field(default=False)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ExecutiveSummary(BaseModel):
    """High-level summary of the system blueprint."""

    overview: str = Field(...)
    key_decisions: list[str] = Field(default_factory=list)
    critical_risks: list[str] = Field(default_factory=list)
    readiness_score: float = Field(default=0.0, ge=0.0, le=100.0)


class EngineeringReport(BaseModel):
    """Comprehensive, validated engineering report produced by FORGE."""

    report_id: str = Field(...)
    project_id: str = Field(...)
    objective: str = Field(...)
    executive_summary: ExecutiveSummary = Field(...)
    requirements: RequirementsDoc = Field(...)
    architecture: ArchitectureBlueprint = Field(...)
    threat_model: ThreatModel = Field(...)
    validation_issues: list[ValidationIssue] = Field(default_factory=list)
    revision_history: list[RevisionRecord] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    unresolved_issues: list[str] = Field(default_factory=list)
    evidence_notes: list[str] = Field(default_factory=list)
    metrics_summary: dict[str, Any] = Field(default_factory=dict)
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    final_status: FinalStatus = Field(default=FinalStatus.APPROVED)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
