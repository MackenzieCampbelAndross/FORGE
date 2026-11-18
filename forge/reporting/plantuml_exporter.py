"""PlantUML component diagram exporter for FORGE Architecture Blueprints."""

from __future__ import annotations

import re
from pathlib import Path

from forge.schemas.architecture import ArchitectureBlueprint


class PlantUMLExporter:
    """Exports ArchitectureBlueprint into clean PlantUML component diagram format."""

    @classmethod
    def _clean_token(cls, raw: str) -> str:
        """Create valid PlantUML alias."""
        return re.sub(r"[^a-zA-Z0-9_]", "_", raw.lower())

    @classmethod
    def generate_puml(cls, blueprint: ArchitectureBlueprint) -> str:
        """Render PlantUML component diagram."""
        lines: list[str] = [
            "@startuml",
            "!theme plain",
            "skinparam componentStyle rectangle",
            "skinparam shadowing false",
            "skinparam defaultFontName Helvetica",
            "skinparam ArrowColor #2563EB",
            "skinparam ComponentBorderColor #3B82F6",
            "skinparam ComponentBackgroundColor #EFF6FF",
            "",
            f'title {blueprint.title} - Component Architecture',
            "",
            f'package "{blueprint.deployment_model.value.title()} Environment" {{',
        ]

        # Components
        for comp in blueprint.components:
            alias = cls._clean_token(comp.component_id)
            clean_name = comp.name.replace('"', "'")
            clean_tech = comp.technology.replace('"', "'")
            lines.append(f'    [{clean_name}] as {alias} <<{clean_tech}>>')

        lines.append("}")
        lines.append("")

        # Dependencies
        lines.append("' Dependencies")
        for comp in blueprint.components:
            src_alias = cls._clean_token(comp.component_id)
            for dep in comp.dependencies:
                dep_alias = cls._clean_token(dep)
                lines.append(f"{src_alias} ..> {dep_alias} : depends on")

        # Data Flows
        lines.append("")
        lines.append("' Data Flows")
        for df in blueprint.data_flows:
            src = cls._clean_token(df.source_component_id)
            dst = cls._clean_token(df.target_component_id)
            proto = df.protocol or "calls"
            desc = df.flow_id
            lines.append(f'{src} --> {dst} : {desc}\\n({proto})')

        lines.append("")
        lines.append("@enduml")
        return "\n".join(lines)

    @classmethod
    def export_puml(cls, blueprint: ArchitectureBlueprint, output_path: str | Path) -> None:
        """Write generated PlantUML diagram to file."""
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        content = cls.generate_puml(blueprint)
        target.write_text(content, encoding="utf-8")
