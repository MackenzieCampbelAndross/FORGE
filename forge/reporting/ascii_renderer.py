"""Terminal ASCII art architecture topology and flow renderer."""

from __future__ import annotations

from forge.schemas.architecture import ArchitectureBlueprint


class ASCIITopologyRenderer:
    """Renders ASCII component boxes and directional data flow streams for terminal display."""

    BOX_WIDTH = 46

    @classmethod
    def _draw_box(cls, title: str, subtitle: str, tech: str) -> list[str]:
        """Render a single ASCII component box."""
        w = cls.BOX_WIDTH
        border = "+" + "-" * (w - 2) + "+"

        def pad_line(text: str) -> str:
            clean = text[: w - 6]
            return f"|  {clean:<{w - 6}}  |"

        return [
            border,
            pad_line(title),
            pad_line(subtitle),
            pad_line(f"Tech: {tech}"),
            border,
        ]

    @classmethod
    def render_topology(cls, blueprint: ArchitectureBlueprint) -> str:
        """Render ASCII diagram representing system components and connections."""
        lines: list[str] = [
            "=" * cls.BOX_WIDTH,
            f" ARCHITECTURE: {blueprint.title[:cls.BOX_WIDTH - 16]}",
            f" DEPLOYMENT:   {blueprint.deployment_model.value}",
            "=" * cls.BOX_WIDTH,
            "",
        ]

        # Map components
        comp_map = {c.component_id: c for c in blueprint.components}

        # Render each component
        for i, comp in enumerate(blueprint.components, 1):
            box = cls._draw_box(
                title=f"[{comp.component_id}] {comp.name}",
                subtitle=comp.responsibility,
                tech=comp.technology,
            )
            lines.extend(box)

            # Find outgoing flows
            out_flows = [df for df in blueprint.data_flows if df.source_component_id == comp.component_id]
            for df in out_flows:
                target_comp = comp_map.get(df.target_component_id)
                target_name = target_comp.name if target_comp else df.target_component_id
                center = cls.BOX_WIDTH // 2
                arrow_lead = " " * (center - 1)
                lines.append(f"{arrow_lead}|")
                lines.append(f"{arrow_lead}| ---> [{df.flow_id}] ({df.protocol}) to {target_name}")
                lines.append(f"{arrow_lead}v")

            if i < len(blueprint.components):
                lines.append("")

        return "\n".join(lines)
