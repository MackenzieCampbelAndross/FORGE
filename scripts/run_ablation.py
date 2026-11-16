#!/usr/bin/env python3
"""CLI utility to execute systematic ablation experiments on FORGE v1.0."""

import argparse
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rich.console import Console
from rich.table import Table

from forge.benchmark.loader import BenchmarkLoader
from forge.evaluation.ablation import AblationRunner


def main():
    parser = argparse.ArgumentParser(description="Run Systematic Ablation Studies for FORGE v1.0")
    parser.add_argument(
        "--dataset",
        default="forge/benchmark/scenarios/feb_v1_dataset.jsonl",
        help="Path to scenario dataset.",
    )
    parser.add_argument(
        "--scenario-id",
        type=str,
        default="FEB-BACKEND-001",
        help="Specific scenario ID to run ablations on.",
    )
    args = parser.parse_args()

    console = Console()
    console.print("\n[bold cyan]🧪 FORGE v1.0 Systematic Ablation Study[/bold cyan]")
    console.print(f"Target Scenario: `{args.scenario_id}`\n")

    scenarios = BenchmarkLoader.load_from_file(args.dataset)
    target_s = next((s for s in scenarios if s.scenario_id == args.scenario_id), scenarios[0])

    runner = AblationRunner()

    table = Table(title=f"Ablation Results for {target_s.scenario_id}: {target_s.title}")
    table.add_column("Ablation Configuration", style="cyan")
    table.add_column("Composite Score", justify="right")
    table.add_column("Final Status", justify="center")
    table.add_column("Latency (s)", justify="right")

    for key, cfg in runner.DEFINED_ABLATIONS.items():
        res = runner.run_ablation(key, target_s)
        status_style = (
            "green"
            if res.final_status == "APPROVED"
            else ("yellow" if res.final_status == "PARTIAL" else "red")
        )
        table.add_row(
            cfg.name,
            f"{res.scorecard.composite_score:.2f}%",
            f"[{status_style}]{res.final_status}[/{status_style}]",
            f"{res.execution_time_seconds:.3f}",
        )

    console.print(table)
    console.print(
        "\n[bold green]✅ Ablation experiments executed cleanly and recorded independently.[/bold green]\n"
    )


if __name__ == "__main__":
    main()
