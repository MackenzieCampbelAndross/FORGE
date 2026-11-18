"""Scenario search, filtering, and indexing engine for FEB Benchmark."""

from __future__ import annotations

import re
from collections.abc import Sequence

from forge.schemas.evaluation import BenchmarkCategory, BenchmarkScenario, GroundTruthStatus


class ScenarioSearchEngine:
    """In-memory search, filtering, and indexer for benchmark scenarios."""

    def __init__(self, scenarios: Sequence[BenchmarkScenario] | None = None) -> None:
        self._scenarios: list[BenchmarkScenario] = list(scenarios) if scenarios else []
        self._index_by_id: dict[str, BenchmarkScenario] = {s.scenario_id: s for s in self._scenarios}

    def add_scenario(self, scenario: BenchmarkScenario) -> None:
        """Add or update a scenario in the search engine index."""
        self._scenarios.append(scenario)
        self._index_by_id[scenario.scenario_id] = scenario

    def get_by_id(self, scenario_id: str) -> BenchmarkScenario | None:
        """Retrieve a scenario by its exact unique identifier."""
        return self._index_by_id.get(scenario_id)

    def filter(
        self,
        category: BenchmarkCategory | str | None = None,
        status: GroundTruthStatus | str | None = None,
        keyword: str | None = None,
        min_constraints: int = 0,
        max_constraints: int | None = None,
    ) -> list[BenchmarkScenario]:
        """Filter scenarios matching all supplied criteria."""
        results: list[BenchmarkScenario] = []

        cat_val = category.value if isinstance(category, BenchmarkCategory) else category
        stat_val = status.value if isinstance(status, GroundTruthStatus) else status

        for s in self._scenarios:
            if cat_val and s.category.value != cat_val:
                continue

            if stat_val and s.ground_truth_status.value != stat_val:
                continue

            constraints_count = len(s.constraints)
            if constraints_count < min_constraints:
                continue
            if max_constraints is not None and constraints_count > max_constraints:
                continue

            if keyword:
                kw_lower = keyword.lower()
                text_corpus = f"{s.title} {s.objective} {' '.join(s.constraints)} {s.scenario_id}".lower()
                if not re.search(r"\b" + re.escape(kw_lower) + r"\b", text_corpus) and kw_lower not in text_corpus:
                    continue

            results.append(s)

        return results

    def list_categories(self) -> dict[str, int]:
        """Return counts of scenarios per category."""
        counts: dict[str, int] = {}
        for s in self._scenarios:
            cat = s.category.value
            counts[cat] = counts.get(cat, 0) + 1
        return counts

    def list_statuses(self) -> dict[str, int]:
        """Return counts of scenarios per ground truth status."""
        counts: dict[str, int] = {}
        for s in self._scenarios:
            st = s.ground_truth_status.value
            counts[st] = counts.get(st, 0) + 1
        return counts

    def count(self) -> int:
        """Total number of indexed scenarios."""
        return len(self._scenarios)
