"""Unit tests for requirement ambiguity and contradiction detection."""

from forge.intelligence.requirements import RequirementAnalyzer
from forge.schemas.requirements import (
    FunctionalRequirement,
    NonFunctionalRequirement,
    RequirementCategory,
    RequirementPriority,
    RequirementsDoc,
    RequirementSource,
)


def _build_doc(nfr_targets: list[str], extra_text: str = "") -> RequirementsDoc:
    nfrs = [
        NonFunctionalRequirement(
            requirement_id=f"NFR-{i:03d}",
            category=RequirementCategory.PERFORMANCE,
            description=f"Performance requirement {i}",
            measurable_target=target,
            priority=RequirementPriority.HIGH,
        )
        for i, target in enumerate(nfr_targets, 1)
    ]
    frs = [
        FunctionalRequirement(
            requirement_id="REQ-001",
            description=f"Payment processing service {extra_text}",
            priority=RequirementPriority.CRITICAL,
            acceptance_criteria=["Processes charge"],
            source=RequirementSource.EXPLICIT,
        )
    ]
    return RequirementsDoc(
        document_id="DOC-AMBIG-001",
        project_id="PRJ-AMBIG-001",
        executive_summary="Testing ambiguity analysis",
        functional_requirements=frs,
        non_functional_requirements=nfrs,
    )


def test_vague_target_triggers_ambiguity_finding() -> None:
    """Verify non-numeric words like 'fast' or 'scalable' trigger ambiguity warnings."""
    doc = _build_doc(nfr_targets=["Must be fast and scalable", "Very user-friendly system"])
    ambiguities = RequirementAnalyzer.identify_ambiguities(doc)

    assert len(ambiguities) >= 1
    assert any("lacks measurable numeric threshold" in a for a in ambiguities)


def test_quantified_target_passes_without_ambiguity() -> None:
    """Verify numeric thresholds like 'P99 < 50ms' pass cleanly."""
    doc = _build_doc(nfr_targets=["P99 latency < 50ms", "Throughput >= 10000 req/sec"])
    ambiguities = RequirementAnalyzer.identify_ambiguities(doc)

    assert len(ambiguities) == 0


def test_synchronous_vs_event_driven_contradiction() -> None:
    """Verify contradiction detected when strictly synchronous clashes with event-driven."""
    doc = _build_doc(
        nfr_targets=["P99 < 100ms"],
        extra_text="System is strictly synchronous but utilizes asynchronous event-driven queues.",
    )
    contradictions = RequirementAnalyzer.detect_contradictions(doc)
    assert any("synchronous-only communication but also mandates asynchronous event-driven" in c for c in contradictions)


def test_physics_constraint_contradiction() -> None:
    """Verify contradiction detected for sub-millisecond multi-region two-phase commit."""
    doc = _build_doc(
        nfr_targets=["sub-millisecond zero latency"],
        extra_text="Requires multi-region strong consistency with distributed two-phase commit.",
    )
    contradictions = RequirementAnalyzer.detect_contradictions(doc)
    assert any("Physics constraint violation" in c for c in contradictions)


def test_duplicate_requirement_id_validation() -> None:
    """Verify validate_requirements_document catches duplicate IDs."""
    doc = RequirementsDoc(
        document_id="DOC-DUP-01",
        project_id="PRJ-DUP-REQ",
        executive_summary="Duplicate ID test",
        functional_requirements=[
            FunctionalRequirement(
                requirement_id="REQ-DUP-01",
                description="First req",
                priority=RequirementPriority.HIGH,
                acceptance_criteria=[],
                source=RequirementSource.EXPLICIT,
            ),
            FunctionalRequirement(
                requirement_id="REQ-DUP-01",  # duplicate ID
                description="Second req",
                priority=RequirementPriority.HIGH,
                acceptance_criteria=[],
                source=RequirementSource.EXPLICIT,
            ),
        ],
        non_functional_requirements=[
            NonFunctionalRequirement(
                requirement_id="NFR-001",
                category=RequirementCategory.RELIABILITY,
                description="99.99% availability",
                measurable_target="99.99%",
                priority=RequirementPriority.HIGH,
            )
        ],
    )
    valid, issues = RequirementAnalyzer.validate_requirements_document(doc)
    assert valid is False
    assert any("Duplicate requirement ID: REQ-DUP-01" in err for err in issues)
