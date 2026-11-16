#!/usr/bin/env python3
"""CLI utility to execute FORGE engineering analysis on a system objective or input file."""

import argparse
import json
import os
import sys
import uuid

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rich.console import Console
from rich.panel import Panel

from forge.orchestration.workflows import ForgeWorkflow
from forge.reporting.exporters import ReportExporter
from forge.schemas.requirements import ProjectObjective


def main():
    parser = argparse.ArgumentParser(description="FORGE v1.0 Engineering Analysis CLI")
    parser.add_argument("--objective", type=str, help="High-level software objective to analyze.")
    parser.add_argument("--input", type=str, help="Path to JSON file containing project objective.")
    parser.add_argument(
        "--domain", type=str, default="General Software", help="Application domain."
    )
    parser.add_argument("--constraints", nargs="*", default=[], help="List of system constraints.")
    parser.add_argument("--max-revisions", type=int, default=3, help="Max supervisory revisions.")
    parser.add_argument(
        "--output-dir", type=str, default="outputs", help="Directory to save generated reports."
    )
    args = parser.parse_args()

    console = Console()
    console.print(
        "\n[bold cyan]🔥 FORGE v1.0 — Multi-Agent Engineering Intelligence Engine[/bold cyan]\n"
    )

    if args.input:
        if not os.path.exists(args.input):
            console.print(f"[bold red]❌ Input file '{args.input}' not found.[/bold red]")
            sys.exit(1)
        with open(args.input, encoding="utf-8") as f:
            data = json.load(f)
            objective_str = data.get("objective", "")
            domain_str = data.get("domain", args.domain)
            constraints_list = data.get("constraints", args.constraints)
            project_id = data.get("project_id", f"PRJ-{uuid.uuid4().hex[:8].upper()}")
    elif args.objective:
        objective_str = args.objective
        domain_str = args.domain
        constraints_list = args.constraints
        project_id = f"PRJ-{uuid.uuid4().hex[:8].upper()}"
    else:
        console.print(
            "[bold red]❌ Must provide either --objective or --input JSON file.[/bold red]"
        )
        sys.exit(1)

    obj = ProjectObjective(
        project_id=project_id,
        objective=objective_str,
        domain=domain_str,
        constraints=constraints_list,
    )

    console.print(
        Panel(
            f"[bold]Project ID:[/bold] {obj.project_id}\n"
            f"[bold]Objective:[/bold] {obj.objective}\n"
            f"[bold]Domain:[/bold] {obj.domain}\n"
            f"[bold]Constraints:[/bold] {', '.join(obj.constraints) if obj.constraints else 'None'}",
            title="Input Specification",
            border_style="blue",
        )
    )

    workflow = ForgeWorkflow()
    final_state = workflow.run(obj, max_revisions=args.max_revisions)
    report = final_state.get("engineering_report")

    if not report:
        console.print("[bold red]❌ Workflow execution failed to compile report.[/bold red]")
        sys.exit(1)

    # Save outputs
    os.makedirs(args.output_dir, exist_ok=True)
    md_path = os.path.join(args.output_dir, f"{report.project_id}_report.md")
    json_path = os.path.join(args.output_dir, f"{report.project_id}_report.json")

    ReportExporter.export_markdown(report, md_path)
    ReportExporter.export_json(report, json_path)

    status_color = (
        "green"
        if report.final_status.value == "APPROVED"
        else ("yellow" if report.final_status.value == "PARTIAL" else "red")
    )
    console.print(
        Panel(
            f"[bold]Final Status:[/bold] [{status_color}]{report.final_status.value}[/{status_color}]\n"
            f"[bold]Confidence Score:[/bold] {report.confidence_score * 100:.1f}%\n"
            f"[bold]Revisions Required:[/bold] {len(report.revision_history)}\n"
            f"[bold]Markdown Report:[/bold] [link=file://{os.path.abspath(md_path)}]{md_path}[/link]\n"
            f"[bold]JSON Artifact:[/bold] [link=file://{os.path.abspath(json_path)}]{json_path}[/link]",
            title="Execution Summary",
            border_style=status_color,
        )
    )


if __name__ == "__main__":
    main()
