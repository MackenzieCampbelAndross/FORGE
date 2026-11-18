"""LangGraph StateGraph orchestration definition."""

from typing import Any

from langgraph.graph import END, StateGraph

from forge.core.model_provider import ModelProvider
from forge.core.state import ForgeState
from forge.orchestration.nodes import NodeContainer
from forge.orchestration.routing import route_after_supervisor


def build_forge_graph(provider: ModelProvider | None = None) -> Any:
    """Constructs and compiles the executable LangGraph state graph."""
    container = NodeContainer(provider=provider)

    workflow = StateGraph(ForgeState)

    # Register nodes
    workflow.add_node("strategy", container.strategy_node)
    workflow.add_node("architect", container.architect_node)
    workflow.add_node("security", container.security_node)
    workflow.add_node("supervisor", container.supervisor_node)

    # Linear forward pipeline
    workflow.set_entry_point("strategy")
    workflow.add_edge("strategy", "architect")
    workflow.add_edge("architect", "security")
    workflow.add_edge("security", "supervisor")

    # Conditional routing from supervisor
    workflow.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {
            "strategy": "strategy",
            "architect": "architect",
            "security": "security",
            "__end__": END,
        },
    )

    return workflow.compile()
