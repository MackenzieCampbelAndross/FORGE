"""Exporters for saving reports and diagrams to disk in multiple formats."""

from __future__ import annotations

from pathlib import Path

from forge.core.logging import logger
from forge.reporting.ascii_renderer import ASCIITopologyRenderer
from forge.reporting.c4_exporter import C4Exporter
from forge.reporting.generator import ReportGenerator
from forge.reporting.graphviz_exporter import GraphvizExporter
from forge.reporting.html_exporter import HTMLExporter
from forge.reporting.plantuml_exporter import PlantUMLExporter
from forge.schemas.architecture import ArchitectureBlueprint
from forge.schemas.report import EngineeringReport

BlueprintOrReport = ArchitectureBlueprint | EngineeringReport


class ReportExporter:
    """Facade for exporting EngineeringReport and ArchitectureBlueprint to Markdown, JSON, HTML, and diagram DSLs."""

    @classmethod
    def _extract_blueprint(cls, target: BlueprintOrReport) -> ArchitectureBlueprint:
        if isinstance(target, ArchitectureBlueprint):
            return target
        return target.architecture

    @classmethod
    def export_markdown(cls, report: EngineeringReport, output_path: str | Path) -> None:
        """Export full 20-section report to Markdown."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        md = ReportGenerator.generate_markdown(report)
        path.write_text(md, encoding="utf-8")
        logger.info(f"[ReportExporter] Markdown report saved to {path}")

    @classmethod
    def export_json(cls, report: EngineeringReport, output_path: str | Path) -> None:
        """Export report data to JSON."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(report.model_dump_json(indent=2), encoding="utf-8")
        logger.info(f"[ReportExporter] JSON report saved to {path}")

    @classmethod
    def export_html(cls, report: EngineeringReport, output_path: str | Path) -> None:
        """Export standalone HTML report with embedded styles and Mermaid diagram."""
        HTMLExporter.export_html(report, output_path)
        logger.info(f"[ReportExporter] HTML report saved to {output_path}")

    @classmethod
    def export_dot(cls, target: BlueprintOrReport, output_path: str | Path) -> None:
        """Export architecture topology to Graphviz DOT format."""
        bp = cls._extract_blueprint(target)
        GraphvizExporter.export_dot(bp, output_path)
        logger.info(f"[ReportExporter] DOT graph saved to {output_path}")

    @classmethod
    def export_c4(cls, target: BlueprintOrReport, output_path: str | Path) -> None:
        """Export architecture to Structurizr C4 Model DSL."""
        bp = cls._extract_blueprint(target)
        C4Exporter.export_c4(bp, output_path)
        logger.info(f"[ReportExporter] C4 DSL saved to {output_path}")

    @classmethod
    def export_puml(cls, target: BlueprintOrReport, output_path: str | Path) -> None:
        """Export architecture to PlantUML component diagram."""
        bp = cls._extract_blueprint(target)
        PlantUMLExporter.export_puml(bp, output_path)
        logger.info(f"[ReportExporter] PlantUML saved to {output_path}")

    @classmethod
    def render_ascii(cls, target: BlueprintOrReport) -> str:
        """Render architecture topology in ASCII art string."""
        bp = cls._extract_blueprint(target)
        return ASCIITopologyRenderer.render_topology(bp)

    @classmethod
    def export_all(cls, report: EngineeringReport, output_dir: str | Path, base_name: str = "blueprint") -> dict[str, str]:
        """Export report into all supported formats inside output_dir."""
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        paths = {
            "markdown": str(out / f"{base_name}.md"),
            "json": str(out / f"{base_name}.json"),
            "html": str(out / f"{base_name}.html"),
            "dot": str(out / f"{base_name}.dot"),
            "c4": str(out / f"{base_name}.dsl"),
            "puml": str(out / f"{base_name}.puml"),
        }

        cls.export_markdown(report, paths["markdown"])
        cls.export_json(report, paths["json"])
        cls.export_html(report, paths["html"])
        cls.export_dot(report, paths["dot"])
        cls.export_c4(report, paths["c4"])
        cls.export_puml(report, paths["puml"])

        logger.info(f"[ReportExporter] All formats exported to directory: {output_dir}")
        return paths
