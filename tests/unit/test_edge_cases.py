"""Edge case and failure mode tests for FORGE v1.0."""

import pytest
from pydantic import ValidationError

from forge.core.exceptions import SchemaValidationError
from forge.core.model_provider import MockModelProvider
from forge.intelligence.architecture_validator import ArchitectureValidator
from forge.intelligence.requirements import RequirementAnalyzer
from forge.orchestration.workflows import ForgeWorkflow
from forge.schemas.architecture import ArchitectureBlueprint, DeploymentModel
from forge.schemas.report import FinalStatus, ValidationIssueSeverity
from forge.schemas.requirements import (
    FunctionalRequirement,
    ProjectObjective,
    RequirementsDoc,
    RequirementSource,
)


def test_empty_or_too_short_objective():
    with pytest.raises(ValidationError):
        ProjectObjective(project_id="P1", objective="")

    with pytest.raises(ValidationError):
        ProjectObjective(project_id="P1", objective="abc")


def test_contradictory_requirements_detection():
    doc = RequirementsDoc(
        document_id="D1",
        project_id="P1",
        executive_summary="Summary claiming strictly synchronous only communication and asynchronous event-driven queues.",
        functional_requirements=[
            FunctionalRequirement(
                requirement_id="FR-001",
                description="Strictly synchronous calls",
                source=RequirementSource.EXPLICIT,
            ),
            FunctionalRequirement(
                requirement_id="FR-002",
                description="Asynchronous event message broker",
                source=RequirementSource.EXPLICIT,
            ),
        ],
        non_functional_requirements=[],
        constraints=[],
        missing_information=[],
        ambiguous_requirements=[],
        contradictions=[],
        assumptions=[],
    )

    detected = RequirementAnalyzer.detect_contradictions(doc)
    assert len(detected) > 0
    assert any("synchronous" in c.lower() and "asynchronous" in c.lower() for c in detected)


def test_missing_architecture_components_validator():
    empty_arch = ArchitectureBlueprint(
        architecture_id="A-EMPTY",
        title="Empty Architecture",
        overview="Architecture missing components.",
        components=[],
        data_flows=[],
        deployment_model=DeploymentModel.CONTAINERIZED,
        technology_choices=[],
        tradeoffs=[],
    )
    issues = ArchitectureValidator.validate_blueprint(empty_arch)
    assert len(issues) == 1
    assert issues[0].severity == ValidationIssueSeverity.BLOCKER
    assert "zero components" in issues[0].message


def test_maximum_revision_attempts_exceeded_results_in_partial_or_failed():
    # If security agent is absent, revisions occur up to max_revisions and then terminate with PARTIAL
    obj = ProjectObjective(project_id="P-REV-LIMIT", objective="Test revision limit bounded loop")
    workflow = ForgeWorkflow()

    from forge.schemas.evaluation import AblationConfig

    no_sec_cfg = AblationConfig(
        name="No Sec",
        enable_security_agent=False,
    )

    state = workflow.run(obj, max_revisions=2, ablation_config=no_sec_cfg)
    report = state.get("engineering_report")
    assert report is not None
    # Must report PARTIAL or FAILED instead of falsely declaring success!
    assert report.final_status in [FinalStatus.PARTIAL, FinalStatus.FAILED]
    assert len(report.revision_history) == 2


def test_invalid_structured_parsing_raises_schema_validation_error():
    # Mocking invalid raw text parsing
    with pytest.raises(SchemaValidationError):
        # Force invalid schema parse
        from pydantic import BaseModel

        class StrictModel(BaseModel):
            strictly_required_id: int

        # Calling generate_structured with non-conforming prompt / schema
        class RealFailProvider(MockModelProvider):
            def generate_text(self, prompt, system_instruction=None):
                from forge.core.model_provider import ProviderResponse

                return ProviderResponse(content="NOT_VALID_JSON{", model_name="mock")

        fail_provider = RealFailProvider()
        from forge.core.model_provider import GeminiProvider

        # Verify generate_structured handles bad JSON
        fail_provider.generate_structured = GeminiProvider.generate_structured.__get__(
            fail_provider
        )
        fail_provider.generate_structured("test", StrictModel)
