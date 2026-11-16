"""Unit tests for intelligence engines (Traceability, Validators, Constraints, Decisions)."""

from forge.intelligence.architecture_validator import ArchitectureValidator
from forge.intelligence.constraint_analyzer import ConstraintAnalyzer
from forge.intelligence.technology_evaluator import TechnologyEvaluator
from forge.intelligence.traceability import TraceabilityEngine
from forge.schemas.architecture import (
    ArchitectureBlueprint,
    ArchitectureComponent,
    DataFlow,
    DeploymentModel,
)
from forge.schemas.report import ValidationIssueSeverity
from forge.schemas.requirements import (
    ConstraintCategory,
    FunctionalRequirement,
    NonFunctionalRequirement,
    RequirementCategory,
    RequirementsDoc,
    RequirementSource,
    SystemConstraint,
)


def create_sample_requirements() -> RequirementsDoc:
    return RequirementsDoc(
        document_id="DOC-001",
        project_id="PRJ-001",
        executive_summary="Sample requirements doc for testing.",
        functional_requirements=[
            FunctionalRequirement(
                requirement_id="FR-001",
                description="Process payment transaction",
                acceptance_criteria=["Validate card"],
                source=RequirementSource.EXPLICIT,
            ),
            FunctionalRequirement(
                requirement_id="FR-002",
                description="Send notification email",
                acceptance_criteria=["Deliver receipt"],
                source=RequirementSource.EXPLICIT,
            ),
        ],
        non_functional_requirements=[
            NonFunctionalRequirement(
                requirement_id="NFR-001",
                category=RequirementCategory.PERFORMANCE,
                description="Fast response",
                measurable_target="< 100ms p95",
            )
        ],
        constraints=[
            SystemConstraint(
                constraint_id="CON-001",
                category=ConstraintCategory.TECHNICAL,
                description="Must deploy on Kubernetes",
                mandatory=True,
            )
        ],
        missing_information=[],
        ambiguous_requirements=[],
        contradictions=[],
        assumptions=[],
    )


def create_sample_blueprint() -> ArchitectureBlueprint:
    return ArchitectureBlueprint(
        architecture_id="ARCH-001",
        title="Test Architecture",
        overview="Sample architecture description.",
        components=[
            ArchitectureComponent(
                component_id="COMP-001",
                name="Payment Service",
                responsibility="Executes financial card charges",
                technology="FastAPI",
                dependencies=["COMP-002"],
                related_requirements=["FR-001", "CON-001"],
            ),
            ArchitectureComponent(
                component_id="COMP-002",
                name="Notification Worker",
                responsibility="Dispatches customer email notifications",
                technology="Celery",
                dependencies=[],
                related_requirements=["FR-002"],
            ),
        ],
        data_flows=[
            DataFlow(
                flow_id="FLOW-001",
                source_component_id="COMP-001",
                target_component_id="COMP-002",
                protocol="AMQP",
                description="Dispatch email notification",
            )
        ],
        deployment_model=DeploymentModel.CONTAINERIZED,
        technology_choices=[],
        tradeoffs=[],
        requirement_mapping={
            "FR-001": ["COMP-001"],
            "FR-002": ["COMP-002"],
            "CON-001": ["COMP-001"],
        },
    )


def test_traceability_calculations():
    reqs = create_sample_requirements()
    blueprint = create_sample_blueprint()

    matrix = TraceabilityEngine.generate_matrix(reqs, blueprint)
    assert matrix.total_requirements == 3  # 2 FR + 1 NFR
    assert matrix.requirement_coverage_pct > 60.0
    assert matrix.constraint_satisfaction_pct == 100.0


def test_architecture_validator_clean():
    reqs = create_sample_requirements()
    blueprint = create_sample_blueprint()

    issues = ArchitectureValidator.validate_blueprint(blueprint, reqs)
    blockers = [i for i in issues if i.severity == ValidationIssueSeverity.BLOCKER]
    assert len(blockers) == 0


def test_architecture_validator_broken_dependency():
    blueprint = create_sample_blueprint()
    # Add dependency to non-existent component
    blueprint.components[0].dependencies.append("COMP-NONEXISTENT")

    issues = ArchitectureValidator.validate_blueprint(blueprint)
    dep_issues = [i for i in issues if i.rule_id == "VAL-ARCH-002"]
    assert len(dep_issues) == 1
    assert "COMP-NONEXISTENT" in dep_issues[0].message


def test_architecture_validator_cycle_detection():
    blueprint = create_sample_blueprint()
    # Create cycle: COMP-001 -> COMP-002 -> COMP-001
    blueprint.components[1].dependencies.append("COMP-001")

    issues = ArchitectureValidator.validate_blueprint(blueprint)
    cycle_issues = [i for i in issues if i.rule_id == "VAL-ARCH-003"]
    assert len(cycle_issues) == 1


def test_constraint_analyzer():
    reqs = create_sample_requirements()
    blueprint = create_sample_blueprint()

    score, satisfied, violated = ConstraintAnalyzer.evaluate_constraints(reqs, blueprint)
    assert score == 100.0
    assert len(satisfied) == 1
    assert len(violated) == 0


def test_technology_evaluator():
    assessment = TechnologyEvaluator.evaluate(
        technology="PostgreSQL",
        category="Relational Database",
    )
    assert assessment.weighted_score > 7.0
    assert assessment.criteria_scores.reliability >= 9.0
    assert assessment.is_heuristic is True
