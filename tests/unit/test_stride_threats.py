"""Unit tests for STRIDE threat modeling analysis across all 6 threat categories."""


from forge.schemas.architecture import (
    ArchitectureBlueprint,
    ArchitectureComponent,
    ComponentInterface,
    DeploymentModel,
)
from forge.schemas.security import STRIDECategory
from forge.security.stride import STRIDEAnalyzer


def _build_test_blueprint(with_interfaces: bool = True) -> ArchitectureBlueprint:
    interfaces = []
    if with_interfaces:
        interfaces = [
            ComponentInterface(interface_id="INT-1", name="Public API", protocol="HTTPS"),
            ComponentInterface(interface_id="INT-2", name="Internal Bus", protocol="Kafka"),
        ]

    c1 = ArchitectureComponent(
        component_id="COMP-001",
        name="Ingress Gateway",
        responsibility="Public API routing and auth",
        technology="Kong",
        interfaces=interfaces,
        dependencies=[],
        related_requirements=[],
    )
    c2 = ArchitectureComponent(
        component_id="COMP-002",
        name="Database Tier",
        responsibility="Data persistence",
        technology="PostgreSQL",
        interfaces=[],
        dependencies=[],
        related_requirements=[],
    )
    return ArchitectureBlueprint(
        architecture_id="ARCH-STRIDE-001",
        title="Secured Enterprise App",
        overview="Multi-tier secure architecture",
        components=[c1, c2],
        data_flows=[],
        deployment_model=DeploymentModel.CONTAINERIZED,
        tradeoffs=[],
        assumptions=[],
    )


def test_stride_all_six_categories_generated() -> None:
    """Verify STRIDEAnalyzer generates threats for all 6 STRIDE categories."""
    bp = _build_test_blueprint()
    threat_model = STRIDEAnalyzer.analyze_blueprint(bp, project_id="PRJ-STRIDE-TEST")

    categories_present = {t.category for t in threat_model.threats}
    for cat in STRIDECategory:
        assert cat in categories_present, f"Missing STRIDE category {cat}"


def test_stride_attack_surfaces_mapped_to_interfaces() -> None:
    """Verify attack surfaces correlate with exposed component interfaces."""
    bp = _build_test_blueprint(with_interfaces=True)
    threat_model = STRIDEAnalyzer.analyze_blueprint(bp)

    assert len(threat_model.attack_surfaces) == 2
    https_surf = next(s for s in threat_model.attack_surfaces if "HTTPS" in s.description)
    assert https_surf.exposure_type == "Public / Network Service"


def test_stride_risk_score_boundaries() -> None:
    """Verify all generated threats have valid risk scores and mitigations."""
    bp = _build_test_blueprint()
    threat_model = STRIDEAnalyzer.analyze_blueprint(bp)

    for t in threat_model.threats:
        assert 0.0 <= t.risk_score <= 10.0
        assert t.mitigation is not None
        assert len(t.mitigation.description) > 0
        assert t.mitigation.owasp_mapping is not None
