"""Pydantic schemas for system architecture design."""

from enum import Enum

from pydantic import BaseModel, Field


class DeploymentModel(str, Enum):
    CLOUD_NATIVE = "CLOUD_NATIVE"
    HYBRID = "HYBRID"
    ON_PREMISE = "ON_PREMISE"
    SERVERLESS = "SERVERLESS"
    EDGE = "EDGE"
    CONTAINERIZED = "CONTAINERIZED"


class ComponentInterface(BaseModel):
    """External or internal communication interface exposed by a component."""

    interface_id: str = Field(..., description="Unique ID, e.g. INT-001")
    name: str = Field(..., description="Interface name, e.g. REST API, gRPC endpoint")
    protocol: str = Field(default="HTTPS/REST", description="Protocol, e.g. gRPC, REST, Kafka")
    description: str = Field(default="")


class ArchitectureComponent(BaseModel):
    """A major structural subsystem or service."""

    component_id: str = Field(..., description="Unique ID, e.g. COMP-001")
    name: str = Field(..., min_length=2, description="Component name")
    responsibility: str = Field(..., min_length=10, description="Defined single responsibility")
    technology: str = Field(..., description="Selected technology / runtime")
    interfaces: list[ComponentInterface] = Field(default_factory=list)
    dependencies: list[str] = Field(
        default_factory=list, description="IDs of components this component depends on"
    )
    related_requirements: list[str] = Field(
        default_factory=list, description="Requirement IDs mapped to this component"
    )


class DataFlow(BaseModel):
    """Data movement between components."""

    flow_id: str = Field(..., description="Unique ID, e.g. FLOW-001")
    source_component_id: str = Field(...)
    target_component_id: str = Field(...)
    protocol: str = Field(default="HTTPS")
    data_payload: str = Field(default="", description="Description of data exchanged")
    description: str = Field(default="")


class TechnologyChoice(BaseModel):
    """Defensible decision rationale for selecting a specific technology."""

    technology: str = Field(...)
    category: str = Field(..., description="e.g. Backend, Database, Message Broker, Cache")
    rationale: str = Field(..., min_length=10)
    alternatives_considered: list[str] = Field(default_factory=list)
    tradeoffs: list[str] = Field(default_factory=list)


class TradeoffAnalysis(BaseModel):
    """Architectural trade-off assessment."""

    dimension: str = Field(..., description="e.g. Latency vs Consistency, Cost vs Redundancy")
    decision: str = Field(...)
    pros: list[str] = Field(default_factory=list)
    cons: list[str] = Field(default_factory=list)


class ArchitectureBlueprint(BaseModel):
    """Structured architectural specification produced by the System Architect."""

    architecture_id: str = Field(...)
    title: str = Field(..., min_length=5)
    overview: str = Field(..., min_length=20)
    components: list[ArchitectureComponent] = Field(default_factory=list)
    data_flows: list[DataFlow] = Field(default_factory=list)
    deployment_model: DeploymentModel = Field(default=DeploymentModel.CONTAINERIZED)
    technology_choices: list[TechnologyChoice] = Field(default_factory=list)
    tradeoffs: list[TradeoffAnalysis] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    requirement_mapping: dict[str, list[str]] = Field(
        default_factory=dict, description="Requirement ID -> List of Component IDs addressing it"
    )
