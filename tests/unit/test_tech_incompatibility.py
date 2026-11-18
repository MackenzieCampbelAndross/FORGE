"""Unit tests for technology incompatibility rules in ArchitectureValidator."""

import pytest

from forge.intelligence.architecture_validator import ArchitectureValidator
from forge.schemas.architecture import (
    ArchitectureBlueprint,
    ArchitectureComponent,
    DeploymentModel,
)


@pytest.mark.parametrize(
    ("tech1", "tech2", "expected_phrase"),
    [
        ("SQLite", "multi-region distributed cluster", "cannot function as a distributed multi-region database"),
        ("Redis", "durable cold archive storage", "primarily an in-memory datastore"),
        ("Kafka", "embedded sensor device", "unsuitable for resource-constrained embedded microcontrollers"),
        ("Elasticsearch", "acid transactional ledger", "lacks distributed ACID transaction guarantees"),
    ],
)
def test_technology_incompatibility_detected(tech1: str, tech2: str, expected_phrase: str) -> None:
    """Verify incompatible technology pairs trigger VAL-ARCH-006 warning."""
    c1 = ArchitectureComponent(
        component_id="COMP-001",
        name="Component 1",
        responsibility="Testing responsibilities",
        technology=f"{tech1} with {tech2}",
        dependencies=[],
    )
    bp = ArchitectureBlueprint(
        architecture_id="ARCH-INCOMPAT-001",
        title="Incompatible Tech Stack",
        overview="Testing architecture validator incompatibility rules thoroughly.",
        components=[c1],
        deployment_model=DeploymentModel.CONTAINERIZED,
    )

    issues = ArchitectureValidator.validate_blueprint(bp)
    incompat_issues = [i for i in issues if i.rule_id == "VAL-ARCH-006"]

    assert len(incompat_issues) >= 1
    assert any(expected_phrase in i.message for i in incompat_issues)
