"""High-level workflow runner for FORGE analysis."""

import time
from typing import Any

from forge.core.config import settings
from forge.core.logging import logger
from forge.core.model_provider import ModelProvider, get_model_provider
from forge.core.state import ForgeState
from forge.orchestration.graph import build_forge_graph
from forge.schemas.evaluation import AblationConfig
from forge.schemas.requirements import ProjectObjective


class ForgeWorkflow:
    """Executes end-to-end multi-agent system design workflow."""

    def __init__(self, provider: ModelProvider | None = None):
        self.provider = provider or get_model_provider()
        self.compiled_graph: Any = build_forge_graph(self.provider)

    def run(
        self,
        objective: ProjectObjective,
        max_revisions: int | None = None,
        ablation_config: AblationConfig | None = None,
    ) -> ForgeState:
        """Execute full engineering analysis workflow."""
        start_time = time.time()
        logger.info(f"[Workflow] Starting FORGE v1.0 run for project: {objective.project_id}")

        initial_state: ForgeState = {
            "objective": objective,
            "revision_count": 0,
            "max_revisions": max_revisions or settings.max_revisions,
            "revision_history": [],
            "validation_issues": [],
            "next_agent": "strategy",
            "current_step": "initialized",
            "status": "IN_PROGRESS",
            "execution_metadata": {
                "start_time": start_time,
                "model_provider": self.provider.__class__.__name__,
                "model_name": self.provider.model_name,
            },
            "ablation_config": ablation_config,
        }

        # Execute compiled LangGraph
        final_state: ForgeState = self.compiled_graph.invoke(initial_state)

        total_elapsed = time.time() - start_time
        meta = final_state.get("execution_metadata", {})
        meta["total_workflow_latency_seconds"] = total_elapsed
        final_state["execution_metadata"] = meta

        logger.info(
            f"[Workflow] Run completed in {total_elapsed:.2f}s with status: {final_state.get('status')} "
            f"(Revisions: {final_state.get('revision_count', 0)})"
        )
        return final_state
