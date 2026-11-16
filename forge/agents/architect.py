"""System Architect Agent: System architecture design, component topology, and technology evaluation."""

from forge.agents.base import BaseAgent
from forge.core.logging import logger
from forge.core.model_provider import ModelProvider
from forge.schemas.architecture import ArchitectureBlueprint
from forge.schemas.report import RevisionRecord
from forge.schemas.requirements import RequirementsDoc


class ArchitectAgent(BaseAgent):
    """System Architect agent producing structured architecture blueprints."""

    def __init__(self, provider: ModelProvider | None = None):
        super().__init__(
            name="ArchitectAgent",
            role="Principal System Architect and Distributed Systems Engineer",
            provider=provider,
        )

    def run(
        self,
        requirements: RequirementsDoc,
        revision_request: RevisionRecord | None = None,
    ) -> tuple[ArchitectureBlueprint, float]:
        """Generate structured architecture blueprint based on validated requirements."""
        logger.info(f"[{self.name}] Designing system architecture for: {requirements.project_id}")

        revision_prompt = ""
        if revision_request:
            revision_prompt = (
                f"\n\nIMPORTANT REVISION REQUESTED BY SUPERVISOR:\n"
                f"Issues: {'; '.join(i.message for i in revision_request.issues)}\n"
                f"Requested correction: {revision_request.requested_correction}\n"
                f"Refine component dependencies, interfaces, and technology choices accordingly."
            )

        req_summary = "\n".join(
            [
                f"- [{fr.requirement_id}] {fr.description} (Priority: {fr.priority.value})"
                for fr in requirements.functional_requirements
            ]
        )
        nfr_summary = "\n".join(
            [
                f"- [{nfr.requirement_id}] ({nfr.category.value}) {nfr.description} -> Target: {nfr.measurable_target}"
                for nfr in requirements.non_functional_requirements
            ]
        )
        con_summary = "\n".join(
            [
                f"- [{c.constraint_id}] {c.description} (Mandatory: {c.mandatory})"
                for c in requirements.constraints
            ]
        )

        prompt = (
            f"Produce a complete, technically sound, and structured Architecture Blueprint based on these validated requirements:\n\n"
            f"EXECUTIVE SUMMARY:\n{requirements.executive_summary}\n\n"
            f"FUNCTIONAL REQUIREMENTS:\n{req_summary}\n\n"
            f"NON-FUNCTIONAL REQUIREMENTS:\n{nfr_summary}\n\n"
            f"CONSTRAINTS:\n{con_summary}\n"
            f"{revision_prompt}\n\n"
            f"Instructions:\n"
            f"1. Define components with unique IDs (e.g. COMP-001), distinct responsibilities, and technologies.\n"
            f"2. Explicitly establish component interfaces and valid dependency IDs.\n"
            f"3. Model end-to-end data flows with source and target component IDs.\n"
            f"4. Provide defensible technology choices with alternatives and trade-offs.\n"
            f"5. Map every requirement to one or more components in requirement_mapping."
        )

        blueprint, elapsed = self.call_structured(prompt, ArchitectureBlueprint)
        return blueprint, elapsed
