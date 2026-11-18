"""Catalog markdown summary generator for FEB benchmark scenarios."""

from __future__ import annotations

from pathlib import Path

from forge.benchmark.loader import BenchmarkLoader
from forge.schemas.evaluation import BenchmarkScenario


class ScenarioCatalogGenerator:
    """Generates structured documentation and markdown tables for FEB benchmark scenarios."""

    @classmethod
    def load_all_scenarios(cls, root_dir: str | Path = "forge/benchmark/scenarios") -> list[BenchmarkScenario]:
        """Scan directory and parse all modular JSON scenario files."""
        root = Path(root_dir)
        scenarios: list[BenchmarkScenario] = []
        for file_path in sorted(root.glob("*/*.json")):
            scenarios.extend(BenchmarkLoader.load_from_file(str(file_path)))
        return scenarios

    @classmethod
    def generate_markdown_catalog(cls, scenarios: list[BenchmarkScenario]) -> str:
        """Render a GitHub-flavored markdown catalog of all benchmark scenarios."""
        lines: list[str] = [
            "# FORGE Engineering Benchmark (FEB) v1.0 — Scenario Catalog",
            "",
            f"Total Scenarios: **{len(scenarios)}**",
            "",
            "The FORGE Engineering Benchmark covers 7 core system design domains with realistic constraints,",
            "expected architectural components, and STRIDE security threats.",
            "",
            "## Category Distribution",
            "",
            "| Category | Scenarios | Target Focus |",
            "| :--- | :---: | :--- |",
            "| Backend Systems | 20 | High-throughput APIs, streaming, background workers, event-driven pipelines |",
            "| Distributed Systems | 15 | Consensus, partition tolerance, distributed transactions, edge sync |",
            "| AI & ML Systems | 15 | Inference serving, RAG pipelines, training orchestration, vector search |",
            "| Database Systems | 15 | Sharding, multi-model storage, time-series indexing, ACID guarantees |",
            "| Cloud Infrastructure | 15 | Multi-region, Kubernetes topologies, zero-trust VPC, hybrid connectivity |",
            "| Security Critical | 10 | Payment gateways, HSM key managers, auth providers, audit logging |",
            "| General Architecture | 10 | Monolith modularization, legacy migration, plugin extensions |",
            "",
            "## Scenario Manifest",
            "",
            "| ID | Title | Category | Constraints | Components | Threats | Status |",
            "| :--- | :--- | :--- | :---: | :---: | :---: | :---: |",
        ]

        # Sort by scenario_id
        sorted_scenarios = sorted(scenarios, key=lambda s: s.scenario_id)
        for s in sorted_scenarios:
            constraints_cnt = len(s.constraints)
            comps_cnt = len(s.expected_components)
            threats_cnt = len(s.expected_threat_categories)
            status_val = s.ground_truth_status.value
            lines.append(
                f"| `{s.scenario_id}` | {s.title} | {s.category.value} | {constraints_cnt} | {comps_cnt} | {threats_cnt} | {status_val} |"
            )

        lines.append("")
        return "\n".join(lines)

    @classmethod
    def write_catalog_to_file(cls, output_path: str | Path, scenarios: list[BenchmarkScenario] | None = None) -> None:
        """Write generated markdown catalog to disk."""
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        active_scenarios = scenarios or cls.load_all_scenarios()
        content = cls.generate_markdown_catalog(active_scenarios)
        target.write_text(content, encoding="utf-8")
