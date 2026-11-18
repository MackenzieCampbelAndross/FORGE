"""Unit tests for Graphviz DOT component topology exporter."""

from pathlib import Path

from forge.reporting.graphviz_exporter import GraphvizExporter
from forge.schemas.architecture import (
    ArchitectureBlueprint,
    ArchitectureComponent,
    ComponentInterface,
    DataFlow,
    DeploymentModel,
)


def _create_sample_blueprint() -> ArchitectureBlueprint:
    i1 = ComponentInterface(
        interface_id="INT-001",
        name="REST API",
        protocol="HTTPS/REST",
    )
    i2 = ComponentInterface(
        interface_id="INT-002",
        name="Auth gRPC",
        protocol="gRPC",
    )
    c1 = ArchitectureComponent(
        component_id="COMP-001",
        name="API Gateway",
        responsibility="Request routing, rate limiting and TLS termination",
        technology="Kong / Envoy",
        interfaces=[i1],
        dependencies=["COMP-002"],
        related_requirements=["REQ-001"],
    )
    c2 = ArchitectureComponent(
        component_id="COMP-002",
        name="Auth Service",
        responsibility="OAuth2 tokens and user identity verification",
        technology="Go / PostgreSQL",
        interfaces=[i2],
        dependencies=[],
        related_requirements=["REQ-002"],
    )
    flow = DataFlow(
        flow_id="FLOW-001",
        source_component_id="COMP-001",
        target_component_id="COMP-002",
        protocol="gRPC",
        data_payload="JWT token validation request",
        description="Verify token",
    )
    return ArchitectureBlueprint(
        architecture_id="ARCH-TEST-001",
        title="Sample Test Architecture",
        overview="High-performance edge routing system",
        components=[c1, c2],
        data_flows=[flow],
        deployment_model=DeploymentModel.CONTAINERIZED,
        tradeoffs=[],
        assumptions=["Low internal network jitter"],
    )


def test_generate_dot_string() -> None:
    """Verify generated DOT string syntax and content."""
    bp = _create_sample_blueprint()
    dot_str = GraphvizExporter.generate_dot(bp)

    assert "digraph ArchitectureTopology {" in dot_str
    assert "COMP_001" in dot_str
    assert "COMP_002" in dot_str
    assert "API Gateway" in dot_str
    assert "Kong / Envoy" in dot_str
    assert "COMP_001 -> COMP_002 [style=dashed" in dot_str
    assert 'COMP_001 -> COMP_002 [label="FLOW-001' in dot_str
    assert dot_str.strip().endswith("}")


def test_export_dot_file(tmp_path: Path) -> None:
    """Verify writing DOT file to disk."""
    bp = _create_sample_blueprint()
    out_file = tmp_path / "diagrams" / "topology.dot"

    GraphvizExporter.export_dot(bp, out_file)
    assert out_file.exists()

    content = out_file.read_text(encoding="utf-8")
    assert "digraph ArchitectureTopology" in content
