"""Unit tests for Structurizr C4 Model DSL exporter."""

from pathlib import Path

from forge.reporting.c4_exporter import C4Exporter
from forge.schemas.architecture import (
    ArchitectureBlueprint,
    ArchitectureComponent,
    ComponentInterface,
    DataFlow,
    DeploymentModel,
)


def _sample_blueprint() -> ArchitectureBlueprint:
    i1 = ComponentInterface(interface_id="INT-1", name="HTTP API", protocol="REST")
    i2 = ComponentInterface(interface_id="INT-2", name="Order Worker", protocol="Kafka")

    c1 = ArchitectureComponent(
        component_id="COMP-01",
        name="Web Frontend",
        responsibility="Customer UI and session management",
        technology="Next.js / React",
        interfaces=[i1],
        dependencies=["COMP-02"],
        related_requirements=["REQ-1"],
    )
    c2 = ArchitectureComponent(
        component_id="COMP-02",
        name="Order Processor",
        responsibility="Processes orders asynchronously",
        technology="Rust / Tokio",
        interfaces=[i2],
        dependencies=[],
        related_requirements=["REQ-2"],
    )
    flow = DataFlow(
        flow_id="FLOW-01",
        source_component_id="COMP-01",
        target_component_id="COMP-02",
        protocol="Kafka",
        data_payload="OrderPlacedEvent",
        description="Publishes new order event",
    )
    return ArchitectureBlueprint(
        architecture_id="ARCH-C4-01",
        title="E-Commerce Engine",
        overview="Scalable microservices for processing customer orders",
        components=[c1, c2],
        data_flows=[flow],
        deployment_model=DeploymentModel.CONTAINERIZED,
        tradeoffs=[],
        assumptions=[],
    )


def test_c4_dsl_generation() -> None:
    """Verify C4 DSL output tokens and structure."""
    bp = _sample_blueprint()
    dsl = C4Exporter.generate_dsl(bp, system_name="ShopEngine")

    assert "workspace {" in dsl
    assert "model {" in dsl
    assert 'softwareSystem "E-Commerce Engine"' in dsl
    assert 'comp_01 = container "Web Frontend"' in dsl
    assert 'comp_02 = container "Order Processor"' in dsl
    assert 'comp_01 -> comp_02 "Publishes new order event" "Kafka"' in dsl
    assert 'comp_01 -> comp_02 "Depends on" "Internal"' in dsl
    assert "views {" in dsl
    assert "systemContext" in dsl
    assert "container" in dsl


def test_c4_export_file(tmp_path: Path) -> None:
    """Verify writing C4 DSL to filesystem."""
    bp = _sample_blueprint()
    out_file = tmp_path / "c4" / "architecture.dsl"

    C4Exporter.export_c4(bp, out_file)
    assert out_file.exists()

    content = out_file.read_text(encoding="utf-8")
    assert "workspace {" in content
    assert "softwareSystem" in content
