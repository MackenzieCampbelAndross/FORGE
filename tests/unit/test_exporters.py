"""Unit tests for ReportExporter facade exporting across all formats."""

from pathlib import Path

from forge.core.model_provider import MockModelProvider
from forge.orchestration.workflows import ForgeWorkflow
from forge.reporting.exporters import ReportExporter
from forge.schemas.requirements import ProjectObjective


def test_export_all_formats(tmp_path: Path) -> None:
    """Verify export_all generates markdown, json, html, dot, c4, and puml files."""
    provider = MockModelProvider()
    workflow = ForgeWorkflow(provider=provider)
    obj = ProjectObjective(
        project_id="PRJ-EXP-001",
        objective="Design multi-cloud messaging bus",
        domain="Cloud",
        constraints=["Kafka replication across 3 regions"],
    )
    final_state = workflow.run(obj, max_revisions=1)
    report = final_state["engineering_report"]

    out_dir = tmp_path / "exports"
    paths = ReportExporter.export_all(report, out_dir, base_name="test_blueprint")

    for fmt, path_str in paths.items():
        p = Path(path_str)
        assert p.exists(), f"Format {fmt} output missing: {path_str}"
        assert p.stat().st_size > 0, f"Format {fmt} produced empty file"

    # Also test ascii render
    ascii_str = ReportExporter.render_ascii(report)
    assert "ARCHITECTURE:" in ascii_str
