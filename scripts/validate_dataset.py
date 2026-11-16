#!/usr/bin/env python3
"""CLI utility to validate FEB v1.0 benchmark dataset integrity and statistics."""

import argparse
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rich.console import Console
from rich.table import Table

from forge.benchmark.loader import BenchmarkLoader


def main():
    parser = argparse.ArgumentParser(
        description="Validate FORGE Engineering Benchmark (FEB) dataset."
    )
    parser.add_argument(
        "--path",
        default="forge/benchmark/scenarios/feb_v1_dataset.jsonl",
        help="Path to dataset JSONL or directory containing scenario files.",
    )
    args = parser.parse_args()

    console = Console()
    console.print(f"\n[bold blue]FORGE Dataset Validator[/bold blue] - Scanning: `{args.path}`\n")

    try:
        scenarios = BenchmarkLoader.load_from_file(args.path)
        report = BenchmarkLoader.validate_dataset(scenarios)

        table = Table(title="Dataset Category Distribution")
        table.add_column("Category", style="cyan")
        table.add_column("Count", justify="right", style="green")

        for cat, count in report["categories"].items():
            table.add_row(cat, str(count))

        console.print(table)

        status_table = Table(title="Ground Truth Status Breakdown")
        status_table.add_column("Status", style="magenta")
        status_table.add_column("Count", justify="right", style="yellow")
        for stat, count in report["ground_truth_statuses"].items():
            status_table.add_row(stat, str(count))

        console.print(status_table)

        if report["duplicates"]:
            console.print(
                f"[bold red]❌ Validation Failed: Duplicate IDs found: {report['duplicates']}[/bold red]"
            )
            sys.exit(1)

        console.print(
            f"\n[bold green]✅ Dataset Validation PASSED: {report['total_scenarios']} unique scenarios verified.[/bold green]\n"
        )

    except Exception as e:
        console.print(f"[bold red]❌ Validation error: {e}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
