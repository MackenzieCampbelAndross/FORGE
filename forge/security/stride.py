"""STRIDE threat modeling analyzer."""

from forge.schemas.architecture import ArchitectureBlueprint
from forge.schemas.security import (
    AttackSurface,
    ImpactLevel,
    LikelihoodLevel,
    SecurityMitigation,
    SeverityLevel,
    STRIDECategory,
    ThreatItem,
    ThreatModel,
)
from forge.security.mitigation import MitigationCatalog
from forge.security.risk_scoring import RiskScoringEngine


class STRIDEAnalyzer:
    """Performs STRIDE threat modeling on architecture blueprints."""

    @classmethod
    def analyze_blueprint(
        cls, blueprint: ArchitectureBlueprint, project_id: str = "PRJ-001"
    ) -> ThreatModel:
        threats: list[ThreatItem] = []
        attack_surfaces: list[AttackSurface] = []

        # Identify attack surfaces based on components exposing interfaces or public ingress
        for comp in blueprint.components:
            for iface in comp.interfaces:
                surface = AttackSurface(
                    surface_id=f"SURF-{comp.component_id}-{iface.interface_id}",
                    name=f"Interface: {iface.name} on {comp.name}",
                    exposure_type="Public / Network Service"
                    if "http" in iface.protocol.lower()
                    else "Internal RPC",
                    description=f"Endpoint exposing {iface.protocol} for {comp.name}",
                    protected_by=["Authentication Gateway", "TLS Encryption"],
                )
                attack_surfaces.append(surface)

        # Generate STRIDE threats for each component
        t_counter = 1
        for comp in blueprint.components:
            # Spoofing
            score, sev = RiskScoringEngine.calculate_score(LikelihoodLevel.MEDIUM, ImpactLevel.HIGH)
            res = RiskScoringEngine.calculate_residual_risk(sev, mitigation_provided=True)
            threats.append(
                ThreatItem(
                    threat_id=f"THR-{t_counter:03d}",
                    category=STRIDECategory.SPOOFING,
                    affected_component_id=comp.component_id,
                    attack_scenario=f"Adversary impersonates a legitimate client or service calling {comp.name}.",
                    likelihood=LikelihoodLevel.MEDIUM,
                    impact=ImpactLevel.HIGH,
                    severity=sev,
                    risk_score=score,
                    mitigation=SecurityMitigation(
                        mitigation_id=f"MIT-{t_counter:03d}",
                        description="Enforce mTLS and cryptographically signed JWT tokens with short TTLs.",
                        owasp_mapping=MitigationCatalog.get_owasp_mapping("SPOOFING"),
                        verification_method="Automated auth integration tests",
                    ),
                    residual_risk=res,
                    owasp_reference="A07:2021",
                )
            )
            t_counter += 1

            # Tampering
            score, sev = RiskScoringEngine.calculate_score(LikelihoodLevel.LOW, ImpactLevel.HIGH)
            res = RiskScoringEngine.calculate_residual_risk(sev, mitigation_provided=True)
            threats.append(
                ThreatItem(
                    threat_id=f"THR-{t_counter:03d}",
                    category=STRIDECategory.TAMPERING,
                    affected_component_id=comp.component_id,
                    attack_scenario=f"Unauthorized modification of data in transit or storage for {comp.name}.",
                    likelihood=LikelihoodLevel.LOW,
                    impact=ImpactLevel.HIGH,
                    severity=sev,
                    risk_score=score,
                    mitigation=SecurityMitigation(
                        mitigation_id=f"MIT-{t_counter:03d}",
                        description="Strict input schema validation and cryptographic checksum verification.",
                        owasp_mapping=MitigationCatalog.get_owasp_mapping("TAMPERING"),
                        verification_method="Schema contract tests and fuzz testing",
                    ),
                    residual_risk=res,
                    owasp_reference="A08:2021",
                )
            )
            t_counter += 1

            # Denial of Service
            score, sev = RiskScoringEngine.calculate_score(LikelihoodLevel.HIGH, ImpactLevel.HIGH)
            res = RiskScoringEngine.calculate_residual_risk(sev, mitigation_provided=True)
            threats.append(
                ThreatItem(
                    threat_id=f"THR-{t_counter:03d}",
                    category=STRIDECategory.DENIAL_OF_SERVICE,
                    affected_component_id=comp.component_id,
                    attack_scenario=f"Resource exhaustion attack flooding {comp.name} with requests.",
                    likelihood=LikelihoodLevel.HIGH,
                    impact=ImpactLevel.HIGH,
                    severity=sev,
                    risk_score=score,
                    mitigation=SecurityMitigation(
                        mitigation_id=f"MIT-{t_counter:03d}",
                        description="Distributed token-bucket rate limiting, circuit breakers, and autoscaling.",
                        owasp_mapping=MitigationCatalog.get_owasp_mapping("DENIAL_OF_SERVICE"),
                        verification_method="Stress and load testing",
                    ),
                    residual_risk=res,
                    owasp_reference="API4:2023",
                )
            )
            t_counter += 1

            # Repudiation
            score, sev = RiskScoringEngine.calculate_score(LikelihoodLevel.LOW, ImpactLevel.MEDIUM)
            res = RiskScoringEngine.calculate_residual_risk(sev, mitigation_provided=True)
            threats.append(
                ThreatItem(
                    threat_id=f"THR-{t_counter:03d}",
                    category=STRIDECategory.REPUDIATION,
                    affected_component_id=comp.component_id,
                    attack_scenario=f"Adversary performs unauthorized action on {comp.name} and denies action due to absent audit logging.",
                    likelihood=LikelihoodLevel.LOW,
                    impact=ImpactLevel.MEDIUM,
                    severity=sev,
                    risk_score=score,
                    mitigation=SecurityMitigation(
                        mitigation_id=f"MIT-{t_counter:03d}",
                        description="Centralized append-only audit trail with cryptographic signatures and NTP sync.",
                        owasp_mapping=MitigationCatalog.get_owasp_mapping("REPUDIATION"),
                        verification_method="Log immutability audit and monitoring alert test",
                    ),
                    residual_risk=res,
                    owasp_reference="A09:2021",
                )
            )
            t_counter += 1

            # Information Disclosure
            score, sev = RiskScoringEngine.calculate_score(LikelihoodLevel.MEDIUM, ImpactLevel.HIGH)
            res = RiskScoringEngine.calculate_residual_risk(sev, mitigation_provided=True)
            threats.append(
                ThreatItem(
                    threat_id=f"THR-{t_counter:03d}",
                    category=STRIDECategory.INFORMATION_DISCLOSURE,
                    affected_component_id=comp.component_id,
                    attack_scenario=f"Sensitive application data or tokens leaked in transit or memory by {comp.name}.",
                    likelihood=LikelihoodLevel.MEDIUM,
                    impact=ImpactLevel.HIGH,
                    severity=sev,
                    risk_score=score,
                    mitigation=SecurityMitigation(
                        mitigation_id=f"MIT-{t_counter:03d}",
                        description="Enforce TLS 1.3 in transit, AES-256 at rest, and automated secret scanning.",
                        owasp_mapping=MitigationCatalog.get_owasp_mapping("INFORMATION_DISCLOSURE"),
                        verification_method="Static code analysis and SAST pipeline",
                    ),
                    residual_risk=res,
                    owasp_reference="A02:2021",
                )
            )
            t_counter += 1

            # Elevation of Privilege
            score, sev = RiskScoringEngine.calculate_score(LikelihoodLevel.LOW, ImpactLevel.HIGH)
            res = RiskScoringEngine.calculate_residual_risk(sev, mitigation_provided=True)
            threats.append(
                ThreatItem(
                    threat_id=f"THR-{t_counter:03d}",
                    category=STRIDECategory.ELEVATION_OF_PRIVILEGE,
                    affected_component_id=comp.component_id,
                    attack_scenario=f"Privilege escalation exploiting permissive RBAC or missing authorization checks on {comp.name}.",
                    likelihood=LikelihoodLevel.LOW,
                    impact=ImpactLevel.HIGH,
                    severity=sev,
                    risk_score=score,
                    mitigation=SecurityMitigation(
                        mitigation_id=f"MIT-{t_counter:03d}",
                        description="Enforce fine-grained RBAC/ABAC and context-aware policy enforcement points.",
                        owasp_mapping=MitigationCatalog.get_owasp_mapping("ELEVATION_OF_PRIVILEGE"),
                        verification_method="Role boundary penetration testing",
                    ),
                    residual_risk=res,
                    owasp_reference="A01:2021",
                )
            )
            t_counter += 1

        overall_posture = (
            max((t.severity for t in threats), key=lambda s: s.value)
            if threats
            else SeverityLevel.LOW
        )

        return ThreatModel(
            threat_model_id=f"TM-{project_id}",
            project_id=project_id,
            threats=threats,
            attack_surfaces=attack_surfaces,
            overall_risk_posture=overall_posture,
            recommendations=[
                "Implement defense-in-depth zero-trust network policies between all services.",
                "Conduct quarterly automated threat modeling and dependency vulnerability reviews.",
            ],
        )
