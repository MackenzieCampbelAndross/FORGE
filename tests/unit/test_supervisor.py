"""Unit tests for Supervisor Agent quality evaluation and revision routing."""

from forge.agents.supervisor import SupervisorAgent
from forge.schemas.architecture import ArchitectureBlueprint, ArchitectureComponent, DeploymentModel
from forge.schemas.report import FinalStatus, RevisionTarget
from forge.schemas.requirements import (
    FunctionalRequirement,
    NonFunctionalRequirement,
    ProjectObjective,
    RequirementCategory,
    RequirementsDoc,
    RequirementSource,
)
from forge.schemas.security import (
    ImpactLevel,
    LikelihoodLevel,
    SecurityMitigation,
    SeverityLevel,
    STRIDECategory,
    ThreatItem,
    ThreatModel,
)


def test_supervisor_detects_broken_architecture_and_routes():
    supervisor = SupervisorAgent()
    obj = ProjectObjective(project_id="P1", objective="Test system design")

    # Incomplete architecture: broken dependency reference
    reqs = RequirementsDoc(
        document_id="D1",
        project_id="P1",
        executive_summary="Summary text here.",
        functional_requirements=[
            FunctionalRequirement(
                requirement_id="FR-001",
                description="User login flow",
                source=RequirementSource.EXPLICIT,
            )
        ],
        non_functional_requirements=[
            NonFunctionalRequirement(
                requirement_id="NFR-001",
                category=RequirementCategory.SECURITY,
                description="Token expiration",
                measurable_target="< 15 minutes",
            )
        ],
        constraints=[],
        missing_information=[],
        ambiguous_requirements=[],
        contradictions=[],
        assumptions=[],
    )

    bad_arch = ArchitectureBlueprint(
        architecture_id="A1",
        title="Bad Arch",
        overview="Broken architecture overview.",
        components=[
            ArchitectureComponent(
                component_id="COMP-001",
                name="Auth Service",
                responsibility="Authenticate users",
                technology="Node.js",
                dependencies=["COMP-GHOST"],  # Broken dependency!
                related_requirements=["FR-001"],
            )
        ],
        data_flows=[],
        deployment_model=DeploymentModel.CONTAINERIZED,
        technology_choices=[],
        tradeoffs=[],
        requirement_mapping={"FR-001": ["COMP-001"]},
    )

    tm = ThreatModel(
        threat_model_id="T1",
        project_id="P1",
        threats=[
            ThreatItem(
                threat_id="THR-001",
                category=STRIDECategory.SPOOFING,
                affected_component_id="COMP-001",
                attack_scenario="Credential stuffing attack against login endpoint.",
                likelihood=LikelihoodLevel.MEDIUM,
                impact=ImpactLevel.HIGH,
                severity=SeverityLevel.HIGH,
                risk_score=7.0,
                mitigation=SecurityMitigation(
                    mitigation_id="MIT-001",
                    description="Implement MFA and rate limiting on auth endpoint.",
                ),
            )
        ],
    )

    rev_request, issues = supervisor.evaluate_and_route(
        objective=obj,
        requirements=reqs,
        architecture=bad_arch,
        threat_model=tm,
        revision_count=0,
        max_revisions=3,
    )

    assert rev_request is not None
    assert rev_request.target_agent == RevisionTarget.ARCHITECT
    assert any("COMP-GHOST" in i.message for i in issues)


def test_supervisor_compiles_final_report():
    supervisor = SupervisorAgent()
    obj = ProjectObjective(project_id="P1", objective="Clean system design objective")

    reqs = RequirementsDoc(
        document_id="D1",
        project_id="P1",
        executive_summary="Executive summary of requirements.",
        functional_requirements=[
            FunctionalRequirement(
                requirement_id="FR-001",
                description="Process event ingestion",
                source=RequirementSource.EXPLICIT,
            )
        ],
        non_functional_requirements=[],
        constraints=[],
        missing_information=[],
        ambiguous_requirements=[],
        contradictions=[],
        assumptions=[],
    )

    good_arch = ArchitectureBlueprint(
        architecture_id="A1",
        title="Good Arch",
        overview="Clean architecture overview text.",
        components=[
            ArchitectureComponent(
                component_id="COMP-001",
                name="Ingestion API",
                responsibility="Ingests events into topic",
                technology="FastAPI",
                dependencies=[],
                related_requirements=["FR-001"],
            )
        ],
        data_flows=[],
        deployment_model=DeploymentModel.CONTAINERIZED,
        technology_choices=[],
        tradeoffs=[],
        requirement_mapping={"FR-001": ["COMP-001"]},
    )

    tm = ThreatModel(
        threat_model_id="T1",
        project_id="P1",
        threats=[
            ThreatItem(
                threat_id="THR-001",
                category=STRIDECategory.DENIAL_OF_SERVICE,
                affected_component_id="COMP-001",
                attack_scenario="Volumetric HTTP flood targeting the public endpoint.",
                likelihood=LikelihoodLevel.HIGH,
                impact=ImpactLevel.HIGH,
                severity=SeverityLevel.HIGH,
                risk_score=8.0,
                mitigation=SecurityMitigation(
                    mitigation_id="MIT-001",
                    description="Token bucket rate limiter at edge proxy.",
                ),
            )
        ],
    )

    report, elapsed = supervisor.compile_report(
        objective=obj,
        requirements=reqs,
        architecture=good_arch,
        threat_model=tm,
        validation_issues=[],
        revision_history=[],
    )

    assert report.final_status == FinalStatus.APPROVED
    assert report.confidence_score >= 0.85
    assert report.executive_summary.readiness_score > 70.0
