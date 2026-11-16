"""Security Architect Agent: STRIDE threat modeling, attack surface analysis, and risk scoring."""

from forge.agents.base import BaseAgent
from forge.core.logging import logger
from forge.core.model_provider import ModelProvider
from forge.schemas.architecture import ArchitectureBlueprint
from forge.schemas.report import RevisionRecord
from forge.schemas.security import ThreatModel
from forge.security.risk_scoring import RiskScoringEngine


class SecurityAgent(BaseAgent):
    """Chief Information Security Officer agent conducting STRIDE threat modeling."""

    def __init__(self, provider: ModelProvider | None = None):
        super().__init__(
            name="SecurityAgent",
            role="Chief Information Security Officer and Principal Threat Modeler",
            provider=provider,
        )

    def run(
        self,
        blueprint: ArchitectureBlueprint,
        project_id: str,
        revision_request: RevisionRecord | None = None,
    ) -> tuple[ThreatModel, float]:
        """Perform STRIDE threat modeling against proposed architecture blueprint."""
        logger.info(f"[{self.name}] Conducting STRIDE threat analysis for: {project_id}")

        revision_prompt = ""
        if revision_request:
            revision_prompt = (
                f"\n\nIMPORTANT REVISION REQUESTED BY SUPERVISOR:\n"
                f"Issues: {'; '.join(i.message for i in revision_request.issues)}\n"
                f"Requested correction: {revision_request.requested_correction}\n"
                f"Ensure all identified gaps or under-mitigated components are addressed."
            )

        comp_summary = "\n".join(
            [
                f"- [{c.component_id}] {c.name} ({c.technology}): {c.responsibility}"
                for c in blueprint.components
            ]
        )
        flow_summary = "\n".join(
            [
                f"- [{f.flow_id}] {f.source_component_id} -> {f.target_component_id} ({f.protocol}): {f.description}"
                for f in blueprint.data_flows
            ]
        )

        prompt = (
            f"Perform a comprehensive STRIDE Threat Analysis on the following architecture:\n\n"
            f"COMPONENTS:\n{comp_summary}\n\n"
            f"DATA FLOWS:\n{flow_summary}\n\n"
            f"DEPLOYMENT: {blueprint.deployment_model.value}\n"
            f"{revision_prompt}\n\n"
            f"Instructions:\n"
            f"1. Analyze all STRIDE threat categories for key components and boundaries.\n"
            f"2. Provide realistic attack scenarios and assign likelihood, impact, and severity.\n"
            f"3. Provide concrete actionable mitigations with OWASP mappings where applicable.\n"
            f"4. Map attack surfaces and establish residual risk ratings."
        )

        threat_model, elapsed = self.call_structured(prompt, ThreatModel)

        # Enforce deterministic risk calculations on the model's output
        for threat in threat_model.threats:
            score, severity = RiskScoringEngine.calculate_score(threat.likelihood, threat.impact)
            threat.risk_score = score
            threat.severity = severity
            threat.residual_risk = RiskScoringEngine.calculate_residual_risk(
                initial_severity=severity,
                mitigation_provided=bool(threat.mitigation and threat.mitigation.description),
            )

        return threat_model, elapsed
