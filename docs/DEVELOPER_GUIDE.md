# FORGE Developer Guide — Extending Agents and Workflows

This guide explains how to extend the FORGE multi-agent AI architecture by implementing custom specialized agents, wiring them into the LangGraph state machine, and ensuring complete schema validation.

---

## 1. Agent Architecture Principles

All agents in FORGE inherit from `forge.agents.base.BaseAgent` and adhere to six core tenets:
1. **Pydantic Validation**: All inputs and outputs are strictly typed schemas; unstructured strings are rejected.
2. **Deterministic Fallbacks**: Agents never fabricate facts or hallucinate non-existent dependencies.
3. **Traceability**: Decisions, constraints, and requirements maintain unique ID lineage (`REQ-xxx -> COMP-xxx -> THR-xxx`).
4. **Execution Audit**: Every agent run records wall-clock latency, token consumption, and revision attempts.

---

## 2. Implementing a Custom Agent

To implement a new specialized agent (e.g., `FinOpsCostAgent`):

### Step 1: Define the Structured Output Schema

In `forge/schemas/cost.py`:

```python
from pydantic import BaseModel, Field

class CloudResourceEstimate(BaseModel):
    component_id: str
    estimated_monthly_usd: float = Field(..., ge=0.0)
    instance_family: str
    scaling_tier: str

class FinOpsAnalysis(BaseModel):
    analysis_id: str
    total_monthly_usd: float
    optimizations: list[str] = Field(default_factory=list)
    breakdown: list[CloudResourceEstimate] = Field(default_factory=list)
```

### Step 2: Subclass `BaseAgent`

In `forge/agents/finops.py`:

```python
from forge.agents.base import BaseAgent
from forge.core.model_provider import ModelProvider
from forge.schemas.architecture import ArchitectureBlueprint
from forge.schemas.cost import FinOpsAnalysis

class FinOpsCostAgent(BaseAgent[FinOpsAnalysis]):
    """Analyzes cloud infrastructure costs and scaling optimizations."""

    def __init__(self, provider: ModelProvider):
        super().__init__(name="FinOpsCostAgent", provider=provider, schema=FinOpsAnalysis)

    def run(self, blueprint: ArchitectureBlueprint) -> FinOpsAnalysis:
        prompt = (
            f"Analyze the financial cost of this architecture:\n"
            f"Title: {blueprint.title}\n"
            f"Deployment: {blueprint.deployment_model.value}\n"
            f"Components: {len(blueprint.components)}\n"
        )
        return self._invoke_structured(
            prompt=prompt,
            system_instruction="You are a Principal FinOps Cloud Architect. Output valid JSON only."
        )
```

---

## 3. Registering the Agent in LangGraph

Update `forge/orchestration/graph.py` and `forge/orchestration/nodes.py`:

```python
# In nodes.py:
def finops_node(state: ForgeState) -> dict:
    agent = FinOpsCostAgent(provider=state["provider"])
    result = agent.run(state["architecture"])
    return {"finops_analysis": result}

# In graph.py:
builder.add_node("finops", finops_node)
builder.add_edge("architect", "finops")
builder.add_edge("finops", "security")
```

---

## 4. Writing Deterministic Agent Tests

Test all agent methods with `MockModelProvider` to verify contract compliance without external API dependencies:

```python
from forge.core.model_provider import MockModelProvider
from forge.agents.finops import FinOpsCostAgent

def test_finops_agent_contract():
    provider = MockModelProvider()
    agent = FinOpsCostAgent(provider=provider)
    result = agent.run(sample_blueprint)
    assert result.total_monthly_usd >= 0.0
```
