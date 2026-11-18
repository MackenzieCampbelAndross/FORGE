"""Structurizr C4 Model DSL architecture exporter for FORGE Architecture Blueprints."""

from __future__ import annotations

import re
from pathlib import Path

from forge.schemas.architecture import ArchitectureBlueprint


class C4Exporter:
    """Exports ArchitectureBlueprint into standard Structurizr C4 DSL format."""

    @classmethod
    def _sanitize_identifier(cls, name: str) -> str:
        """Convert component identifier into valid Structurizr DSL variable token."""
        token = re.sub(r"[^a-zA-Z0-9_]", "_", name.lower())
        if token[0].isdigit():
            token = f"comp_{token}"
        return token

    @classmethod
    def generate_dsl(cls, blueprint: ArchitectureBlueprint, system_name: str = "SystemArchitecture") -> str:
        """Generate C4 Structurizr DSL string from blueprint."""
        clean_sys_id = cls._sanitize_identifier(system_name)
        lines: list[str] = [
            "workspace {",
            "    model {",
            f'        user = person "Client / User" "Interacts with {blueprint.title}"',
            f'        {clean_sys_id} = softwareSystem "{blueprint.title}" "{blueprint.overview}" {{',
        ]

        # Containers / Components
        for comp in blueprint.components:
            var_id = cls._sanitize_identifier(comp.component_id)
            desc = comp.responsibility.replace('"', "'")
            tech = comp.technology.replace('"', "'")
            lines.append(f'            {var_id} = container "{comp.name}" "{desc}" "{tech}"')

        lines.append("")
        lines.append("            // Data flows and relationships")

        # Data Flows
        for df in blueprint.data_flows:
            src_var = cls._sanitize_identifier(df.source_component_id)
            dst_var = cls._sanitize_identifier(df.target_component_id)
            desc = (df.description or df.data_payload or "Calls").replace('"', "'")
            proto = df.protocol.replace('"', "'") if df.protocol else "HTTPS"
            lines.append(f'            {src_var} -> {dst_var} "{desc}" "{proto}"')

        # Static Dependencies
        for comp in blueprint.components:
            src_var = cls._sanitize_identifier(comp.component_id)
            for dep in comp.dependencies:
                dep_var = cls._sanitize_identifier(dep)
                lines.append(f'            {src_var} -> {dep_var} "Depends on" "Internal"')

        lines.append("        }")
        lines.append(f'        user -> {clean_sys_id} "Uses"')
        lines.append("    }")
        lines.append("    views {")
        lines.append(f'        systemContext {clean_sys_id} "SystemContext" {{')
        lines.append("            include *")
        lines.append("            autoLayout lr")
        lines.append("        }")
        lines.append(f'        container {clean_sys_id} "Containers" {{')
        lines.append("            include *")
        lines.append("            autoLayout lr")
        lines.append("        }")
        lines.append("        theme default")
        lines.append("    }")
        lines.append("}")

        return "\n".join(lines)

    @classmethod
    def export_c4(
        cls, blueprint: ArchitectureBlueprint, output_path: str | Path, system_name: str = "SystemArchitecture"
    ) -> None:
        """Write generated C4 DSL to disk."""
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        content = cls.generate_dsl(blueprint, system_name=system_name)
        target.write_text(content, encoding="utf-8")
