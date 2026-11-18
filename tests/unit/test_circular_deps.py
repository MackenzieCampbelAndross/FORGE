"""Unit tests for cycle detection and topological integrity in ArchitectureValidator."""

from forge.intelligence.architecture_validator import ArchitectureValidator
from forge.schemas.architecture import (
    ArchitectureBlueprint,
    ArchitectureComponent,
    DeploymentModel,
)


def _make_comp(cid: str, deps: list[str]) -> ArchitectureComponent:
    return ArchitectureComponent(
        component_id=cid,
        name=f"Service {cid}",
        responsibility="Testing responsibilities",
        technology="Python",
        dependencies=deps,
    )


def test_two_node_cycle() -> None:
    """Verify A -> B -> A cycle is detected."""
    c1 = _make_comp("COMP-A", ["COMP-B"])
    c2 = _make_comp("COMP-B", ["COMP-A"])
    bp = ArchitectureBlueprint(
        architecture_id="A-01",
        title="2-Node Cycle",
        overview="Comprehensive architecture overview text exceeding twenty chars.",
        components=[c1, c2],
        deployment_model=DeploymentModel.CONTAINERIZED,
    )
    issues = ArchitectureValidator.validate_blueprint(bp)
    cycle_issues = [i for i in issues if i.rule_id == "VAL-ARCH-003"]
    assert len(cycle_issues) == 1
    assert "Cyclic dependency detected" in cycle_issues[0].message


def test_three_node_cycle() -> None:
    """Verify A -> B -> C -> A cycle is detected."""
    c1 = _make_comp("COMP-A", ["COMP-B"])
    c2 = _make_comp("COMP-B", ["COMP-C"])
    c3 = _make_comp("COMP-C", ["COMP-A"])
    bp = ArchitectureBlueprint(
        architecture_id="A-02",
        title="3-Node Cycle",
        overview="Comprehensive architecture overview text exceeding twenty chars.",
        components=[c1, c2, c3],
        deployment_model=DeploymentModel.CONTAINERIZED,
    )
    issues = ArchitectureValidator.validate_blueprint(bp)
    cycle_issues = [i for i in issues if i.rule_id == "VAL-ARCH-003"]
    assert len(cycle_issues) == 1


def test_diamond_dag_no_false_positive_cycle() -> None:
    """Verify diamond DAG (A -> B, A -> C, B -> D, C -> D) reports NO cycles."""
    c1 = _make_comp("COMP-A", ["COMP-B", "COMP-C"])
    c2 = _make_comp("COMP-B", ["COMP-D"])
    c3 = _make_comp("COMP-C", ["COMP-D"])
    c4 = _make_comp("COMP-D", [])
    bp = ArchitectureBlueprint(
        architecture_id="A-03",
        title="Diamond DAG",
        overview="Comprehensive architecture overview text exceeding twenty chars.",
        components=[c1, c2, c3, c4],
        deployment_model=DeploymentModel.CONTAINERIZED,
    )
    issues = ArchitectureValidator.validate_blueprint(bp)
    cycle_issues = [i for i in issues if i.rule_id == "VAL-ARCH-003"]
    assert len(cycle_issues) == 0


def test_self_referential_cycle() -> None:
    """Verify self-referential cycle A -> A is detected."""
    c1 = _make_comp("COMP-SELF", ["COMP-SELF"])
    bp = ArchitectureBlueprint(
        architecture_id="A-04",
        title="Self Cycle",
        overview="Comprehensive architecture overview text exceeding twenty chars.",
        components=[c1],
        deployment_model=DeploymentModel.CONTAINERIZED,
    )
    issues = ArchitectureValidator.validate_blueprint(bp)
    cycle_issues = [i for i in issues if i.rule_id == "VAL-ARCH-003"]
    assert len(cycle_issues) == 1
