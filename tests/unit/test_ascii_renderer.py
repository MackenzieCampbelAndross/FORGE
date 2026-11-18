"""Unit tests for terminal ASCII topology renderer."""

from forge.reporting.ascii_renderer import ASCIITopologyRenderer
from forge.schemas.architecture import (
    ArchitectureBlueprint,
    ArchitectureComponent,
    DataFlow,
    DeploymentModel,
)


def test_ascii_topology_rendering() -> None:
    """Verify ASCII box structure and directional flow lines."""
    c1 = ArchitectureComponent(
        component_id="COMP-001",
        name="Ingress Gateway",
        responsibility="Rate limits incoming traffic",
        technology="Envoy",
        interfaces=[],
        dependencies=["COMP-002"],
        related_requirements=[],
    )
    c2 = ArchitectureComponent(
        component_id="COMP-002",
        name="Worker Pool",
        responsibility="Executes heavy background tasks",
        technology="Celery / Redis",
        interfaces=[],
        dependencies=[],
        related_requirements=[],
    )
    df = DataFlow(
        flow_id="FLOW-001",
        source_component_id="COMP-001",
        target_component_id="COMP-002",
        protocol="HTTP",
        data_payload="JobPayload",
        description="Forward job",
    )
    bp = ArchitectureBlueprint(
        architecture_id="ARCH-ASCII-001",
        title="Async Job Pipeline",
        overview="Scalable task execution",
        components=[c1, c2],
        data_flows=[df],
        deployment_model=DeploymentModel.CONTAINERIZED,
        tradeoffs=[],
        assumptions=[],
    )

    rendered = ASCIITopologyRenderer.render_topology(bp)

    assert "ARCHITECTURE: Async Job Pipeline" in rendered
    assert "DEPLOYMENT:   CONTAINERIZED" in rendered
    assert "+--------------------------------------------+" in rendered
    assert "[COMP-001] Ingress Gateway" in rendered
    assert "Tech: Envoy" in rendered
    assert "[COMP-002] Worker Pool" in rendered
    assert "Tech: Celery / Redis" in rendered
    assert "---> [FLOW-001] (HTTP) to Worker Pool" in rendered
