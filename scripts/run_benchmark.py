#!/usr/bin/env python3
"""CLI utility to execute FORGE Engineering Benchmark (FEB) v1.0."""

import argparse
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rich.console import Console
from rich.table import Table

from forge.benchmark.loader import BenchmarkLoader
from forge.benchmark.runner import BenchmarkRunner


def main():
    parser = argparse.ArgumentParser(description="Run FORGE Engineering Benchmark (FEB) v1.0")
    parser.add_argument(
        "--dataset",
        default="forge/benchmark/scenarios/feb_v1_dataset.jsonl",
        help="Path to scenario JSONL or directory.",
    )
    parser.add_argument("--category", type=str, default=None, help="Filter by specific category.")
    parser.add_argument(
        "--limit", type=int, default=10, help="Number of scenarios to evaluate (default 10)."
    )
    parser.add_argument(
        "--export-json",
        type=str,
        default="outputs/benchmark_results.json",
        help="Path to export JSON results.",
    )
    parser.add_argument(
        "--export-csv",
        type=str,
        default="outputs/benchmark_results.csv",
        help="Path to export CSV results.",
    )
    args = parser.parse_args()

    console = Console()
    console.print("\n[bold cyan]🚀 FORGE Engineering Benchmark (FEB) v1.0 Runner[/bold cyan]")
    console.print(
        f"Dataset: `{args.dataset}` | Limit: `{args.limit}` | Category: `{args.category or 'ALL'}`\n"
    )

    scenarios = BenchmarkLoader.load_from_file(args.dataset)
    if args.category:
        scenarios = [s for s in scenarios if s.category.value.lower() == args.category.lower()]

    runner = BenchmarkRunner()
    summary = runner.run_suite(
        scenarios=scenarios,
        limit=args.limit,
        export_json_path=args.export_json,
        export_csv_path=args.export_csv,
    )

    agg = summary["summary"]
    table = Table(title="FEB v1.0 Aggregate Benchmark Performance")
    table.add_column("Metric", style="cyan")
    table.add_column("Mean Score", justify="right", style="green")
    table.add_column("Min", justify="right", style="yellow")
    table.add_column("Max", justify="right", style="magenta")

    for m_name, mean_val in agg.get("metrics_mean", {}).items():
        min_val = agg.get("metrics_min", {}).get(m_name, 0.0)
        max_val = agg.get("metrics_max", {}).get(m_name, 0.0)
        table.add_row(m_name, f"{mean_val:.2f}", f"{min_val:.2f}", f"{max_val:.2f}")

    console.print(table)
    console.print(
        f"\n[bold]Total Evaluated:[/bold] {agg['total_runs']} | "
        f"[bold]Pass Rate:[/bold] [green]{agg['pass_rate_pct']}%[/green] | "
        f"Exported: `{args.export_json}` & `{args.export_csv}`\n"
    )


if __name__ == "__main__":
    main()
