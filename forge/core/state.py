"""LangGraph state representation for FORGE agent workflows."""

from typing import Any

from typing_extensions import TypedDict

from forge.schemas.architecture import ArchitectureBlueprint
from forge.schemas.evaluation import AblationConfig
from forge.schemas.report import EngineeringReport, RevisionRecord, ValidationIssue
from forge.schemas.requirements import ProjectObjective, RequirementsDoc
from forge.schemas.security import ThreatModel


class ForgeState(TypedDict, total=False):
    """Shared immutable state passed between LangGraph nodes."""

    # Project input
    objective: ProjectObjective

    # Agent outputs
    requirements: RequirementsDoc | None
    architecture: ArchitectureBlueprint | None
    threat_model: ThreatModel | None
    engineering_report: EngineeringReport | None

    # Supervision & Revision control
    revision_count: int
    max_revisions: int
    revision_history: list[RevisionRecord]
    validation_issues: list[ValidationIssue]
    next_agent: str

    # Workflow tracing & metadata
    current_step: str
    status: str
    error: str | None
    execution_metadata: dict[str, Any]
    ablation_config: AblationConfig | None
