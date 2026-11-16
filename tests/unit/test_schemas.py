"""Unit tests for Pydantic core data models."""

import pytest
from pydantic import ValidationError

from forge.schemas.architecture import (
    ArchitectureBlueprint,
    ArchitectureComponent,
    ComponentInterface,
    DeploymentModel,
    TechnologyChoice,
)
from forge.schemas.requirements import (
    FunctionalRequirement,
    NonFunctionalRequirement,
    ProjectObjective,
    RequirementCategory,
    RequirementPriority,
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


def test_project_objective_validation():
    obj = ProjectObjective(
        project_id="PRJ-TEST-001",
        objective="Valid engineering objective for test",
        domain="Fintech",
        constraints=["Latency < 100ms"],
    )
    assert obj.project_id == "PRJ-TEST-001"
    assert len(obj.constraints) == 1

    with pytest.raises(ValidationError):
        # Objective too short
        ProjectObjective(project_id="P1", objective="bad")


def test_functional_and_nonfunctional_requirements():
    fr = FunctionalRequirement(
        requirement_id="FR-001",
        description="Ingest stream events",
        priority=RequirementPriority.CRITICAL,
        acceptance_criteria=["Pass validation"],
        source=RequirementSource.EXPLICIT,
    )
    assert fr.requirement_id == "FR-001"

    nfr = NonFunctionalRequirement(
        requirement_id="NFR-001",
        category=RequirementCategory.PERFORMANCE,
        description="Low latency",
        measurable_target="< 50ms p95",
        priority=RequirementPriority.HIGH,
    )
    assert nfr.category == RequirementCategory.PERFORMANCE


def test_architecture_blueprint_validation():
    comp = ArchitectureComponent(
        component_id="COMP-001",
        name="Ingress Gateway",
        responsibility="Reverse proxy and route authentication",
        technology="FastAPI / Envoy",
        interfaces=[
            ComponentInterface(interface_id="INT-001", name="HTTP Ingress", protocol="HTTPS")
        ],
        dependencies=[],
        related_requirements=["FR-001"],
    )

    blueprint = ArchitectureBlueprint(
        architecture_id="ARCH-001",
        title="Distributed Event Platform",
        overview="High performance decoupled event streaming architecture.",
        components=[comp],
        data_flows=[],
        deployment_model=DeploymentModel.CONTAINERIZED,
        technology_choices=[
            TechnologyChoice(
                technology="Kafka",
                category="Message Bus",
                rationale="Partitioned high-throughput message streaming log.",
            )
        ],
        tradeoffs=[],
        requirement_mapping={"FR-001": ["COMP-001"]},
    )
    assert len(blueprint.components) == 1
    assert blueprint.components[0].component_id == "COMP-001"


def test_threat_model_validation():
    threat = ThreatItem(
        threat_id="THR-001",
        category=STRIDECategory.DENIAL_OF_SERVICE,
        affected_component_id="COMP-001",
        attack_scenario="Volumetric HTTP flood targeting the public authentication gateway.",
        likelihood=LikelihoodLevel.HIGH,
        impact=ImpactLevel.HIGH,
        severity=SeverityLevel.HIGH,
        risk_score=7.5,
        mitigation=SecurityMitigation(
            mitigation_id="MIT-001",
            description="Distributed rate limiting and Cloudflare WAF.",
            owasp_mapping="OWASP API4:2023",
        ),
        residual_risk=SeverityLevel.LOW,
    )

    tm = ThreatModel(
        threat_model_id="TM-001",
        project_id="PRJ-001",
        threats=[threat],
        overall_risk_posture=SeverityLevel.HIGH,
    )
    assert len(tm.threats) == 1
    assert tm.threats[0].risk_score == 7.5
