"""Dataset loader and validator for FORGE Engineering Benchmark (FEB) v1.0."""

import json
import os
from typing import Any

from forge.core.exceptions import BenchmarkError
from forge.core.logging import logger
from forge.schemas.evaluation import BenchmarkScenario


class BenchmarkLoader:
    """Loads and validates benchmark scenarios."""

    @classmethod
    def load_from_file(cls, file_path: str) -> list[BenchmarkScenario]:
        if not os.path.exists(file_path):
            raise BenchmarkError(f"Scenario file not found: {file_path}")

        scenarios: list[BenchmarkScenario] = []
        if file_path.endswith(".jsonl"):
            with open(file_path, encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        raw = json.loads(line)
                        scenarios.append(BenchmarkScenario.model_validate(raw))
                    except Exception as e:
                        raise BenchmarkError(
                            f"Failed parsing scenario line {line_num} in {file_path}: {e}"
                        ) from e
        else:
            with open(file_path, encoding="utf-8") as f:
                raw_data = json.load(f)
                if isinstance(raw_data, list):
                    for idx, item in enumerate(raw_data):
                        try:
                            scenarios.append(BenchmarkScenario.model_validate(item))
                        except Exception as e:
                            raise BenchmarkError(
                                f"Failed parsing scenario item {idx} in {file_path}: {e}"
                            ) from e
                elif isinstance(raw_data, dict):
                    scenarios.append(BenchmarkScenario.model_validate(raw_data))

        logger.info(f"[BenchmarkLoader] Loaded {len(scenarios)} scenarios from {file_path}")
        return scenarios

    @classmethod
    def load_from_directory(cls, dir_path: str) -> list[BenchmarkScenario]:
        if not os.path.exists(dir_path):
            raise BenchmarkError(f"Directory not found: {dir_path}")

        all_scenarios: list[BenchmarkScenario] = []
        for root, _, files in os.walk(dir_path):
            for file in sorted(files):
                if file.endswith(".json") or file.endswith(".jsonl"):
                    full_path = os.path.join(root, file)
                    all_scenarios.extend(cls.load_from_file(full_path))

        logger.info(
            f"[BenchmarkLoader] Loaded total {len(all_scenarios)} scenarios from {dir_path}"
        )
        return all_scenarios

    @classmethod
    def validate_dataset(cls, scenarios: list[BenchmarkScenario]) -> dict[str, Any]:
        """Validate scenario dataset completeness and generate report."""
        category_counts: dict[str, int] = {}
        status_counts: dict[str, int] = {}
        unique_ids = set()
        duplicates = []

        for s in scenarios:
            category_counts[s.category.value] = category_counts.get(s.category.value, 0) + 1
            status_counts[s.ground_truth_status.value] = (
                status_counts.get(s.ground_truth_status.value, 0) + 1
            )

            if s.scenario_id in unique_ids:
                duplicates.append(s.scenario_id)
            unique_ids.add(s.scenario_id)

        is_valid = len(duplicates) == 0 and len(scenarios) > 0

        return {
            "is_valid": is_valid,
            "total_scenarios": len(scenarios),
            "unique_ids_count": len(unique_ids),
            "duplicates": duplicates,
            "categories": category_counts,
            "ground_truth_statuses": status_counts,
        }
