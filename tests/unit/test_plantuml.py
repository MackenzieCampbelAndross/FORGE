"""Unit tests for PlantUML component diagram exporter."""

from pathlib import Path

from forge.reporting.plantuml_exporter import PlantUMLExporter
from forge.schemas.architecture import (
    ArchitectureBlueprint,
    ArchitectureComponent,
    ComponentInterface,
    DataFlow,
    DeploymentModel,
)


def _sample_blueprint() -> ArchitectureBlueprint:
    i1 = ComponentInterface(interface_id="INT-1", name="GraphQL API", protocol="GraphQL")
    c1 = ArchitectureComponent(
        component_id="COMP-GRAPHQL",
        name="Federation Gateway",
        responsibility="GraphQL query routing and caching",
        technology="Apollo Router",
        interfaces=[i1],
        dependencies=["COMP-USERS"],
        related_requirements=["REQ-1"],
    )
    c2 = ArchitectureComponent(
        component_id="COMP-USERS",
        name="User Microservice",
        responsibility="User profile CRUD and authentication",
        technology="FastAPI / PostgreSQL",
        interfaces=[],
        dependencies=[],
        related_requirements=["REQ-2"],
    )
    df = DataFlow(
        flow_id="FLOW-GQL-USER",
        source_component_id="COMP-GRAPHQL",
        target_component_id="COMP-USERS",
        protocol="gRPC",
        data_payload="UserEntityRequest",
        description="Query subgraph",
    )
    return ArchitectureBlueprint(
        architecture_id="ARCH-PUML-01",
        title="Federated GraphQL System",
        overview="High throughput subgraph federation",
        components=[c1, c2],
        data_flows=[df],
        deployment_model=DeploymentModel.CLOUD_NATIVE,
        tradeoffs=[],
        assumptions=[],
    )


def test_plantuml_generation() -> None:
    """Verify PlantUML syntax, stereotypes, and edge connectors."""
    bp = _sample_blueprint()
    puml = PlantUMLExporter.generate_puml(bp)

    assert puml.startswith("@startuml")
    assert puml.strip().endswith("@enduml")
    assert 'package "Cloud_Native Environment"' in puml
    assert "[Federation Gateway] as comp_graphql <<Apollo Router>>" in puml
    assert "[User Microservice] as comp_users <<FastAPI / PostgreSQL>>" in puml
    assert "comp_graphql ..> comp_users : depends on" in puml
    assert "comp_graphql --> comp_users : FLOW-GQL-USER\\n(gRPC)" in puml


def test_plantuml_export_file(tmp_path: Path) -> None:
    """Verify writing PlantUML file to disk."""
    bp = _sample_blueprint()
    out_file = tmp_path / "diagrams" / "architecture.puml"

    PlantUMLExporter.export_puml(bp, out_file)
    assert out_file.exists()

    content = out_file.read_text(encoding="utf-8")
    assert "@startuml" in content
    assert "Federation Gateway" in content
