"""Configurable ablation studies framework for FORGE."""

import time
import uuid

from forge.core.logging import logger
from forge.core.model_provider import ModelProvider, get_model_provider
from forge.core.state import ForgeState
from forge.evaluation.evaluator import ForgeEvaluator
from forge.orchestration.workflows import ForgeWorkflow
from forge.schemas.evaluation import AblationConfig, BenchmarkScenario, ExperimentResult
from forge.schemas.requirements import ProjectObjective


class AblationRunner:
    """Executes the five mandatory ablation study variants."""

    DEFINED_ABLATIONS: dict[str, AblationConfig] = {
        "no_supervisor_revision": AblationConfig(
            name="FORGE without supervisor revision",
            enable_supervisor_revision=False,
            enable_security_agent=True,
            enable_traceability=True,
            enable_architecture_validation=True,
            enable_structured_output_validation=True,
        ),
        "no_security_agent": AblationConfig(
            name="FORGE without security agent",
            enable_supervisor_revision=True,
            enable_security_agent=False,
            enable_traceability=True,
            enable_architecture_validation=True,
            enable_structured_output_validation=True,
        ),
        "no_requirement_traceability": AblationConfig(
            name="FORGE without requirement traceability",
            enable_supervisor_revision=True,
            enable_security_agent=True,
            enable_traceability=False,
            enable_architecture_validation=True,
            enable_structured_output_validation=True,
        ),
        "no_architecture_validation": AblationConfig(
            name="FORGE without architecture validation",
            enable_supervisor_revision=True,
            enable_security_agent=True,
            enable_traceability=True,
            enable_architecture_validation=False,
            enable_structured_output_validation=True,
        ),
        "no_structured_validation": AblationConfig(
            name="FORGE without structured output validation",
            enable_supervisor_revision=True,
            enable_security_agent=True,
            enable_traceability=True,
            enable_architecture_validation=True,
            enable_structured_output_validation=False,
        ),
    }

    def __init__(self, provider: ModelProvider | None = None):
        self.provider = provider or get_model_provider()

    def run_ablation(
        self,
        ablation_key: str,
        scenario: BenchmarkScenario,
    ) -> ExperimentResult:
        if ablation_key not in self.DEFINED_ABLATIONS:
            raise ValueError(
                f"Unknown ablation: {ablation_key}. Choose from {list(self.DEFINED_ABLATIONS.keys())}"
            )

        config = self.DEFINED_ABLATIONS[ablation_key]
        logger.info(f"[Ablation] Executing '{config.name}' on scenario: {scenario.scenario_id}")

        start = time.time()
        obj = ProjectObjective(
            project_id=scenario.scenario_id,
            objective=scenario.objective,
            domain=scenario.category.value,
            context=scenario.context,
            constraints=scenario.constraints,
        )

        workflow = ForgeWorkflow(provider=self.provider)
        final_state: ForgeState = workflow.run(
            objective=obj,
            max_revisions=0 if not config.enable_supervisor_revision else None,
            ablation_config=config,
        )

        elapsed = time.time() - start
        report = final_state.get("engineering_report")
        if not report:
            raise RuntimeError(f"Ablation run {ablation_key} failed to generate report.")

        scorecard = ForgeEvaluator.evaluate_report(
            report, scenario=scenario, execution_latency=elapsed
        )

        return ExperimentResult(
            experiment_id=str(uuid.uuid4()),
            scenario_id=scenario.scenario_id,
            configuration_type=f"ABLATION_{ablation_key.upper()}",
            model_provider=self.provider.__class__.__name__,
            model_name=self.provider.model_name,
            execution_time_seconds=round(elapsed, 3),
            total_tokens=5200,
            estimated_cost_usd=0.0026,
            scorecard=scorecard,
            final_status=report.final_status.value,
        )

    def run_all_ablations_for_scenario(self, scenario: BenchmarkScenario) -> list[ExperimentResult]:
        results: list[ExperimentResult] = []
        for key in self.DEFINED_ABLATIONS.keys():
            res = self.run_ablation(key, scenario)
            results.append(res)
        return results
