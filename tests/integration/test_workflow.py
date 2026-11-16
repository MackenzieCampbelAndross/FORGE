"""Integration tests for end-to-end LangGraph multi-agent workflow."""

from forge.core.model_provider import MockModelProvider
from forge.orchestration.workflows import ForgeWorkflow
from forge.reporting.generator import ReportGenerator
from forge.schemas.report import FinalStatus
from forge.schemas.requirements import ProjectObjective


def test_full_workflow_execution():
    provider = MockModelProvider()
    workflow = ForgeWorkflow(provider=provider)

    obj = ProjectObjective(
        project_id="PRJ-INTEG-001",
        objective="Design an enterprise multi-tenant payment and audit platform",
        domain="Fintech",
        constraints=["PCI-DSS Level 1 compliance", "Multi-region cloud redundancy"],
    )

    final_state = workflow.run(obj, max_revisions=2)

    assert final_state["status"] == FinalStatus.APPROVED.value
    assert final_state["requirements"] is not None
    assert final_state["architecture"] is not None
    assert final_state["threat_model"] is not None

    report = final_state.get("engineering_report")
    assert report is not None
    assert report.final_status == FinalStatus.APPROVED
    assert report.confidence_score >= 0.85

    # Check Markdown generation
    md = ReportGenerator.generate_markdown(report)
    assert "# FORGE ENGINEERING BLUEPRINT REPORT" in md
    assert "## 1. Executive Summary" in md
    assert "## 12. Security Threat Model (STRIDE)" in md
    assert "## 20. Final Status" in md
