"""Graphviz DOT topology exporter for FORGE Architecture Blueprints."""

from __future__ import annotations

from pathlib import Path

from forge.schemas.architecture import ArchitectureBlueprint


class GraphvizExporter:
    """Exports ArchitectureBlueprint components and data flows into Graphviz DOT format."""

    @classmethod
    def generate_dot(cls, blueprint: ArchitectureBlueprint) -> str:
        """Render DOT digraph representation of the architecture topology."""
        lines: list[str] = [
            "digraph ArchitectureTopology {",
            '    graph [rankdir=LR, splines=ortho, nodesep=0.6, ranksep=0.8, bgcolor="#F8FAFC", fontname="Helvetica"];',
            '    node [shape=box, style="filled,rounded", fontname="Helvetica", margin="0.2,0.15", fillcolor="#FFFFFF", color="#CBD5E1", penwidth=1.5];',
            '    edge [fontname="Helvetica", fontsize=10, color="#64748B", penwidth=1.2];',
            "",
        ]

        # Component Nodes
        lines.append("    // Architecture Components")
        for comp in blueprint.components:
            cid = comp.component_id.replace("-", "_")
            label_text = f"<{comp.name}<BR/><FONT POINT-SIZE='10' COLOR='#64748B'>{comp.technology}</FONT>>"
            lines.append(f'    {cid} [label={label_text}, fillcolor="#FFFFFF", color="#3B82F6"];')

        lines.append("")
        lines.append("    // Component Dependencies & Data Flows")

        # Explicit Dependencies
        for comp in blueprint.components:
            src_id = comp.component_id.replace("-", "_")
            for dep_id in comp.dependencies:
                clean_dep = dep_id.replace("-", "_")
                lines.append(f'    {src_id} -> {clean_dep} [style=dashed, label="depends_on", color="#94A3B8"];')

        # Data Flows
        for df in blueprint.data_flows:
            src = df.source_component_id.replace("-", "_")
            dst = df.target_component_id.replace("-", "_")
            proto = df.protocol or "calls"
            lines.append(f'    {src} -> {dst} [label="{df.flow_id}\\n({proto})", color="#2563EB", penwidth=1.5];')

        lines.append("}")
        return "\n".join(lines)

    @classmethod
    def export_dot(cls, blueprint: ArchitectureBlueprint, output_path: str | Path) -> None:
        """Write generated DOT format to file."""
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        dot_str = cls.generate_dot(blueprint)
        target.write_text(dot_str, encoding="utf-8")
