"""Exporters for saving reports to disk in multiple formats."""

import os

from forge.core.logging import logger
from forge.reporting.generator import ReportGenerator
from forge.schemas.report import EngineeringReport


class ReportExporter:
    """Exports EngineeringReport instances to Markdown and JSON files."""

    @classmethod
    def export_markdown(cls, report: EngineeringReport, output_path: str):
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        md = ReportGenerator.generate_markdown(report)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md)
        logger.info(f"[ReportExporter] Markdown report saved to {output_path}")

    @classmethod
    def export_json(cls, report: EngineeringReport, output_path: str):
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report.model_dump_json(indent=2))
        logger.info(f"[ReportExporter] JSON report saved to {output_path}")
