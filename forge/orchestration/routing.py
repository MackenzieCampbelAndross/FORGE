"""Conditional routing logic for LangGraph orchestration."""

from typing import Literal

from forge.core.logging import logger
from forge.core.state import ForgeState
from forge.schemas.report import RevisionTarget


def route_after_supervisor(
    state: ForgeState,
) -> Literal["strategy", "architect", "security", "__end__"]:
    """
    Evaluates supervisor outcome:
    - If revision needed: route to targeted agent.
    - If approved or revisions completed: route to end.
    """
    next_agent = state.get("next_agent", "none")
    rev_count = state.get("revision_count", 0)
    max_revs = state.get("max_revisions", 3)

    if next_agent == RevisionTarget.NONE.value or not next_agent:
        logger.info(
            f"[Router] Workflow completed (next_agent=none, revisions={rev_count}/{max_revs})."
        )
        return "__end__"

    if next_agent == RevisionTarget.STRATEGY.value:
        logger.info(f"[Router] Routing to Strategy Agent for revision #{rev_count}...")
        return "strategy"
    elif next_agent == RevisionTarget.ARCHITECT.value:
        logger.info(f"[Router] Routing to Architect Agent for revision #{rev_count}...")
        return "architect"
    elif next_agent == RevisionTarget.SECURITY.value:
        logger.info(f"[Router] Routing to Security Agent for revision #{rev_count}...")
        return "security"

    return "__end__"
