"""Unit tests for standalone interactive HTML report exporter."""

from pathlib import Path

from forge.core.model_provider import MockModelProvider
from forge.orchestration.workflows import ForgeWorkflow
from forge.reporting.html_exporter import HTMLExporter
from forge.schemas.requirements import ProjectObjective


def _generate_report():
    provider = MockModelProvider()
    workflow = ForgeWorkflow(provider=provider)
    obj = ProjectObjective(
        project_id="PRJ-HTML-001",
        objective="Design an interactive distributed caching pipeline with edge nodes",
        domain="Distributed Systems",
        constraints=["Max P99 latency under 5ms"],
    )
    final_state = workflow.run(obj, max_revisions=1)
    return final_state["engineering_report"]


def test_generate_html_content() -> None:
    """Verify HTML document structure, tags, styling, and embedded Mermaid."""
    report = _generate_report()
    html_output = HTMLExporter.generate_html(report)

    assert "<!DOCTYPE html>" in html_output
    assert "<html lang=\"en\">" in html_output
    assert "<title>FORGE Blueprint:" in html_output
    assert "mermaid.initialize" in html_output
    assert "class=\"mermaid\"" in html_output
    assert "1. Executive Summary" in html_output
    assert "2. Architectural Topology" in html_output
    assert "3. STRIDE Threat Analysis" in html_output
    assert report.report_id in html_output
    assert report.final_status.value in html_output
    assert "</html>" in html_output


def test_export_html_file(tmp_path: Path) -> None:
    """Verify writing HTML report to filesystem."""
    report = _generate_report()
    out_file = tmp_path / "reports" / "blueprint.html"

    HTMLExporter.export_html(report, out_file)
    assert out_file.exists()

    content = out_file.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in content
    assert report.project_id in content
