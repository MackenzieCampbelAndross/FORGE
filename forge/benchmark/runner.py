"""Runner for the FORGE Engineering Benchmark (FEB) v1.0."""

from typing import Any

from forge.core.logging import logger
from forge.core.model_provider import ModelProvider, get_model_provider
from forge.evaluation.baselines import BaselineRunner
from forge.evaluation.experiments import ExperimentTracker
from forge.evaluation.scoring import ScorecardAggregator
from forge.schemas.evaluation import BenchmarkScenario, EvaluationScorecard, ExperimentResult


class BenchmarkRunner:
    """Executes benchmark suites across scenarios and collects aggregate scorecards."""

    def __init__(self, provider: ModelProvider | None = None, experiment_name: str | None = None):
        self.provider = provider or get_model_provider()
        self.tracker = ExperimentTracker(experiment_name=experiment_name)
        self.baseline_runner = BaselineRunner(provider=self.provider)

    def run_scenario(self, scenario: BenchmarkScenario) -> ExperimentResult:
        """Run FORGE v1.0 on a single benchmark scenario."""
        res = self.baseline_runner.run_forge_v1(scenario)
        self.tracker.log_experiment(res)
        return res

    def run_suite(
        self,
        scenarios: list[BenchmarkScenario],
        limit: int | None = None,
        export_json_path: str | None = None,
        export_csv_path: str | None = None,
    ) -> dict[str, Any]:
        """Run benchmark suite across multiple scenarios and return aggregate summary."""
        target_scenarios = scenarios[:limit] if limit else scenarios
        results: list[ExperimentResult] = []
        scorecards: list[EvaluationScorecard] = []

        logger.info(
            f"[BenchmarkRunner] Starting FEB v1.0 run on {len(target_scenarios)} scenarios..."
        )

        for s in target_scenarios:
            res = self.run_scenario(s)
            results.append(res)
            scorecards.append(res.scorecard)

        # Aggregate metrics
        aggregation = ScorecardAggregator.aggregate(scorecards)

        if export_json_path:
            self.tracker.export_to_json(results, export_json_path)
        if export_csv_path:
            self.tracker.export_to_csv(results, export_csv_path)

        return {
            "total_scenarios_evaluated": len(results),
            "summary": aggregation,
            "results": [r.model_dump(mode="json") for r in results],
        }
