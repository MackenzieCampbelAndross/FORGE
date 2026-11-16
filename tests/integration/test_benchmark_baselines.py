"""Integration tests for Benchmark, Baseline comparisons, and Ablations."""

from forge.benchmark.loader import BenchmarkLoader
from forge.benchmark.runner import BenchmarkRunner
from forge.evaluation.ablation import AblationRunner
from forge.evaluation.baselines import BaselineRunner
from forge.schemas.evaluation import BaselineType


def test_benchmark_loader_and_runner():
    scenarios = BenchmarkLoader.load_from_file("forge/benchmark/scenarios/feb_v1_dataset.jsonl")
    assert len(scenarios) == 100

    report = BenchmarkLoader.validate_dataset(scenarios)
    assert report["is_valid"] is True
    assert len(report["duplicates"]) == 0

    runner = BenchmarkRunner()
    result = runner.run_suite(scenarios, limit=2)
    assert result["total_scenarios_evaluated"] == 2
    assert result["summary"]["total_runs"] == 2


def test_baseline_runner_comparisons():
    scenarios = BenchmarkLoader.load_from_file("forge/benchmark/scenarios/feb_v1_dataset.jsonl")
    s = scenarios[0]

    runner = BaselineRunner()
    res_a = runner.run_baseline_a_single_llm(s)
    assert res_a.configuration_type == BaselineType.BASELINE_A_SINGLE_LLM.value
    assert res_a.final_status == "PARTIAL"

    res_b = runner.run_baseline_b_sequential(s)
    assert res_b.configuration_type == BaselineType.BASELINE_B_SEQUENTIAL_NO_SUPERVISOR.value
    assert res_b.final_status == "APPROVED"

    res_forge = runner.run_forge_v1(s)
    assert res_forge.configuration_type == BaselineType.FORGE_V1_FULL.value
    assert res_forge.final_status == "APPROVED"


def test_ablation_runner():
    scenarios = BenchmarkLoader.load_from_file("forge/benchmark/scenarios/feb_v1_dataset.jsonl")
    s = scenarios[0]

    ab_runner = AblationRunner()
    # Test without security agent: should trigger supervisor rejection and end with PARTIAL
    res = ab_runner.run_ablation("no_security_agent", s)
    assert res.final_status == "PARTIAL"
    assert res.scorecard.composite_score < 90.0
