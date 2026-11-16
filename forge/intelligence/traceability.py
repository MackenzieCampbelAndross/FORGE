"""Requirement traceability matrix generator and mathematical coverage calculator."""

from pydantic import BaseModel, Field

from forge.schemas.architecture import ArchitectureBlueprint
from forge.schemas.requirements import RequirementsDoc
from forge.schemas.security import ThreatModel


class TraceabilityEntry(BaseModel):
    """Detailed bidirectional traceability mapping for a requirement."""

    requirement_id: str
    description: str
    requirement_type: str  # Functional, NonFunctional, Constraint
    mapped_components: list[str] = Field(default_factory=list)
    mapped_interfaces: list[str] = Field(default_factory=list)
    addressed_by_threat_mitigation: list[str] = Field(default_factory=list)
    is_addressed: bool = False
    is_traceable: bool = False


class TraceabilityMatrix(BaseModel):
    """Full bidirectional traceability matrix."""

    entries: list[TraceabilityEntry] = Field(default_factory=list)
    total_requirements: int = 0
    addressed_requirements: int = 0
    traceable_requirements: int = 0
    requirement_coverage_pct: float = 0.0
    requirement_traceability_pct: float = 0.0
    constraint_satisfaction_pct: float = 0.0


class TraceabilityEngine:
    """Computes rigorous bidirectional traceability mappings and metrics."""

    @classmethod
    def generate_matrix(
        cls,
        req_doc: RequirementsDoc,
        blueprint: ArchitectureBlueprint,
        threat_model: ThreatModel | None = None,
    ) -> TraceabilityMatrix:
        entries: list[TraceabilityEntry] = []
        valid_comp_ids = {c.component_id for c in blueprint.components}

        # Build component to interfaces lookup
        comp_interfaces: dict[str, list[str]] = {
            c.component_id: [i.name for i in c.interfaces] for c in blueprint.components
        }

        # Map threats to components
        threat_comp_map: dict[str, list[str]] = {}
        if threat_model:
            for t in threat_model.threats:
                threat_comp_map.setdefault(t.affected_component_id, []).append(t.threat_id)

        # 1. Process Functional Requirements
        for fr in req_doc.functional_requirements:
            mapped_comps = []
            # Check component's internal list
            for c in blueprint.components:
                if fr.requirement_id in c.related_requirements:
                    mapped_comps.append(c.component_id)

            # Check blueprint requirement_mapping dict
            if fr.requirement_id in blueprint.requirement_mapping:
                for cid in blueprint.requirement_mapping[fr.requirement_id]:
                    if cid not in mapped_comps:
                        mapped_comps.append(cid)

            # Filter valid components
            valid_mapped = [cid for cid in mapped_comps if cid in valid_comp_ids]

            # Gather interfaces
            interfaces: list[str] = []
            for cid in valid_mapped:
                interfaces.extend(comp_interfaces.get(cid, []))

            # Gather threat mitigations
            threats: list[str] = []
            for cid in valid_mapped:
                threats.extend(threat_comp_map.get(cid, []))

            is_addressed = len(valid_mapped) > 0
            is_traceable = len(valid_mapped) > 0 and (
                len(interfaces) > 0 or len(threats) > 0 or len(valid_mapped) >= 1
            )

            entries.append(
                TraceabilityEntry(
                    requirement_id=fr.requirement_id,
                    description=fr.description,
                    requirement_type="Functional",
                    mapped_components=valid_mapped,
                    mapped_interfaces=list(set(interfaces)),
                    addressed_by_threat_mitigation=list(set(threats)),
                    is_addressed=is_addressed,
                    is_traceable=is_traceable,
                )
            )

        # 2. Process Non-Functional Requirements
        for nfr in req_doc.non_functional_requirements:
            mapped_comps = []
            if nfr.requirement_id in blueprint.requirement_mapping:
                mapped_comps = [
                    cid
                    for cid in blueprint.requirement_mapping[nfr.requirement_id]
                    if cid in valid_comp_ids
                ]
            else:
                # Heuristic: check if any component relates to this NFR
                for c in blueprint.components:
                    if (
                        nfr.requirement_id in c.related_requirements
                        and c.component_id in valid_comp_ids
                    ):
                        mapped_comps.append(c.component_id)

            is_addressed = len(mapped_comps) > 0
            entries.append(
                TraceabilityEntry(
                    requirement_id=nfr.requirement_id,
                    description=nfr.description,
                    requirement_type="NonFunctional",
                    mapped_components=mapped_comps,
                    mapped_interfaces=[],
                    addressed_by_threat_mitigation=[],
                    is_addressed=is_addressed,
                    is_traceable=is_addressed,
                )
            )

        total_reqs = len(entries)
        addressed_count = sum(1 for e in entries if e.is_addressed)
        traceable_count = sum(1 for e in entries if e.is_traceable)

        # Explicit zero denominator handling
        coverage_pct = (addressed_count / total_reqs * 100.0) if total_reqs > 0 else 100.0
        traceability_pct = (traceable_count / total_reqs * 100.0) if total_reqs > 0 else 100.0

        # Constraints
        mandatory_constraints = [c for c in req_doc.constraints if c.mandatory]
        total_mandatory = len(mandatory_constraints)
        if total_mandatory > 0:
            satisfied_c = sum(
                1 for c in mandatory_constraints if c.constraint_id in blueprint.requirement_mapping
            )
            constraint_pct = (satisfied_c / total_mandatory) * 100.0
        else:
            constraint_pct = 100.0

        return TraceabilityMatrix(
            entries=entries,
            total_requirements=total_reqs,
            addressed_requirements=addressed_count,
            traceable_requirements=traceable_count,
            requirement_coverage_pct=round(coverage_pct, 2),
            requirement_traceability_pct=round(traceability_pct, 2),
            constraint_satisfaction_pct=round(constraint_pct, 2),
        )
