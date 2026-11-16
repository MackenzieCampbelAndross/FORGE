"""Strategy Agent: Requirements extraction, constraint identification, and ambiguity analysis."""

from forge.agents.base import BaseAgent
from forge.core.logging import logger
from forge.core.model_provider import ModelProvider
from forge.intelligence.requirements import RequirementAnalyzer
from forge.schemas.report import RevisionRecord
from forge.schemas.requirements import ProjectObjective, RequirementsDoc


class StrategyAgent(BaseAgent):
    """Chief Strategy Officer agent producing structured requirements documents."""

    def __init__(self, provider: ModelProvider | None = None):
        super().__init__(
            name="StrategyAgent",
            role="Chief Strategy Officer and Principal Requirements Engineer",
            provider=provider,
        )

    def run(
        self,
        objective: ProjectObjective,
        revision_request: RevisionRecord | None = None,
    ) -> tuple[RequirementsDoc, float]:
        """Execute requirement synthesis and extraction."""
        logger.info(f"[{self.name}] Analyzing objective for project: {objective.project_id}")

        revision_prompt = ""
        if revision_request:
            revision_prompt = (
                f"\n\nIMPORTANT REVISION REQUESTED BY SUPERVISOR:\n"
                f"Issues: {'; '.join(i.message for i in revision_request.issues)}\n"
                f"Requested correction: {revision_request.requested_correction}\n"
                f"Please update and refine the requirements document to resolve these findings."
            )

        prompt = (
            f"Analyze the following engineering objective and extract a complete, structured Requirements Document:\n\n"
            f"PROJECT ID: {objective.project_id}\n"
            f"OBJECTIVE: {objective.objective}\n"
            f"DOMAIN: {objective.domain}\n"
            f"CONTEXT: {objective.context}\n"
            f"GIVEN CONSTRAINTS: {', '.join(objective.constraints) if objective.constraints else 'None specified'}\n"
            f"{revision_prompt}\n\n"
            f"Requirements:\n"
            f"1. Extract all functional requirements with unique IDs (e.g. FR-001) and acceptance criteria.\n"
            f"2. Extract measurable non-functional requirements (e.g. NFR-001) with explicit numeric targets.\n"
            f"3. Identify mandatory and optional constraints with unique IDs (e.g. CON-001).\n"
            f"4. Identify missing information, ambiguous claims, contradictions, and assumptions.\n"
            f"5. Categorize sources clearly as EXPLICIT, INFERRED, ASSUMPTION, or UNKNOWN."
        )

        doc, elapsed = self.call_structured(prompt, RequirementsDoc)

        # Apply deterministic intelligence checks on the result
        detected_contradictions = RequirementAnalyzer.detect_contradictions(doc)
        if detected_contradictions:
            doc.contradictions = list(set(doc.contradictions + detected_contradictions))

        detected_ambiguities = RequirementAnalyzer.identify_ambiguities(doc)
        if detected_ambiguities:
            doc.ambiguous_requirements = list(
                set(doc.ambiguous_requirements + detected_ambiguities)
            )

        return doc, elapsed
