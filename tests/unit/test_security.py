"""Unit tests for STRIDE threat modeling, risk scoring, and mitigations."""

from forge.schemas.architecture import ArchitectureBlueprint, ArchitectureComponent, DeploymentModel
from forge.schemas.security import ImpactLevel, LikelihoodLevel, SeverityLevel
from forge.security.mitigation import MitigationCatalog
from forge.security.risk_scoring import RiskScoringEngine
from forge.security.stride import STRIDEAnalyzer


def test_deterministic_risk_scoring():
    # High likelihood (3.0) x High impact (3.33) -> 9.99 ~ 10.0 -> CRITICAL
    score, severity = RiskScoringEngine.calculate_score(LikelihoodLevel.HIGH, ImpactLevel.HIGH)
    assert score >= 9.0
    assert severity == SeverityLevel.CRITICAL

    # Low likelihood (1.0) x Low impact (1.0) -> 1.0 -> LOW
    score_low, severity_low = RiskScoringEngine.calculate_score(
        LikelihoodLevel.LOW, ImpactLevel.LOW
    )
    assert score_low == 1.0
    assert severity_low == SeverityLevel.LOW


def test_residual_risk_reduction():
    # Critical reduced by 2 levels when verified mitigation exists
    res = RiskScoringEngine.calculate_residual_risk(
        SeverityLevel.CRITICAL, mitigation_provided=True, has_verification=True
    )
    assert res == SeverityLevel.MEDIUM

    # If unmitigated, residual risk equals initial severity
    res_unmitigated = RiskScoringEngine.calculate_residual_risk(
        SeverityLevel.HIGH, mitigation_provided=False
    )
    assert res_unmitigated == SeverityLevel.HIGH


def test_stride_analyzer_on_blueprint():
    blueprint = ArchitectureBlueprint(
        architecture_id="ARCH-001",
        title="Payment Core",
        overview="Payment processing architecture.",
        components=[
            ArchitectureComponent(
                component_id="COMP-001",
                name="Payment API",
                responsibility="Ingests user card authorizations",
                technology="FastAPI",
            )
        ],
        data_flows=[],
        deployment_model=DeploymentModel.CONTAINERIZED,
        technology_choices=[],
        tradeoffs=[],
    )

    tm = STRIDEAnalyzer.analyze_blueprint(blueprint, project_id="PRJ-TEST-001")
    assert len(tm.threats) >= 3  # Spoofing, Tampering, DoS
    assert all(t.risk_score > 0 for t in tm.threats)
    assert all(t.mitigation.description for t in tm.threats)


def test_owasp_mitigation_catalog():
    mapping = MitigationCatalog.get_owasp_mapping("SPOOFING")
    assert mapping is not None
    assert "A07:2021" in mapping

    controls = MitigationCatalog.get_controls_for_category("DENIAL_OF_SERVICE")
    assert len(controls) > 0
    assert any("rate limiting" in c.lower() for c in controls)
