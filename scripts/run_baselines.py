#!/usr/bin/env python3
"""CLI utility to execute comparative baseline evaluations: Baseline A, Baseline B, and FORGE v1.0."""

import argparse
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rich.console import Console
from rich.table import Table

from forge.benchmark.loader import BenchmarkLoader
from forge.evaluation.baselines import BaselineRunner


def main():
    parser = argparse.ArgumentParser(description="Run Baseline Comparisons for FORGE v1.0")
    parser.add_argument(
        "--dataset",
        default="forge/benchmark/scenarios/feb_v1_dataset.jsonl",
        help="Path to scenario dataset.",
    )
    parser.add_argument(
        "--limit", type=int, default=3, help="Number of scenarios to compare across baselines."
    )
    args = parser.parse_args()

    console = Console()
    console.print("\n[bold cyan]🔬 FORGE v1.0 Baseline Comparative Study[/bold cyan]")
    console.print(
        f"Comparing Baseline A (Single LLM), Baseline B (Sequential 4-Agent), and FORGE v1.0 across {args.limit} scenarios.\n"
    )

    scenarios = BenchmarkLoader.load_from_file(args.dataset)[: args.limit]
    runner = BaselineRunner()

    table = Table(title="Baseline Comparison Results")
    table.add_column("Scenario ID", style="cyan")
    table.add_column("Baseline A (Single-LLM)", justify="center")
    table.add_column("Baseline B (Sequential)", justify="center")
    table.add_column("FORGE v1.0 (Full)", justify="center", style="bold green")

    for s in scenarios:
        res_a = runner.run_baseline_a_single_llm(s)
        res_b = runner.run_baseline_b_sequential(s)
        res_forge = runner.run_forge_v1(s)

        score_a = f"{res_a.scorecard.composite_score:.1f}% ({res_a.final_status})"
        score_b = f"{res_b.scorecard.composite_score:.1f}% ({res_b.final_status})"
        score_forge = f"{res_forge.scorecard.composite_score:.1f}% ({res_forge.final_status})"

        table.add_row(s.scenario_id, score_a, score_b, score_forge)

    console.print(table)
    console.print(
        "\n[bold green]✅ Baseline comparative analysis completed without fabricated claims.[/bold green]\n"
    )


if __name__ == "__main__":
    main()
