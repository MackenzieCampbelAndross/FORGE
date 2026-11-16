"""Experiment tracking engine with MLflow integration and JSON/CSV exporters."""

import csv
import json
import os
from typing import Any

from forge.core.config import settings
from forge.core.logging import logger
from forge.schemas.evaluation import ExperimentResult


class ExperimentTracker:
    """Manages experiment metadata, MLflow logging, and disk export."""

    def __init__(self, experiment_name: str | None = None):
        self.experiment_name = experiment_name or settings.mlflow_experiment_name
        self._mlflow_available = False
        self._init_mlflow()

    def _init_mlflow(self):
        try:
            os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"
            import mlflow

            mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
            mlflow.set_experiment(self.experiment_name)
            self._mlflow_available = True
            logger.info(
                f"[ExperimentTracker] MLflow tracking initialized at {settings.mlflow_tracking_uri}"
            )
        except Exception as e:
            logger.warning(
                f"[ExperimentTracker] MLflow tracking unavailable ({e}). Continuing with local logging."
            )
            self._mlflow_available = False

    def log_experiment(self, result: ExperimentResult):
        """Log experiment parameters and metrics to MLflow and local registry."""
        if self._mlflow_available:
            try:
                import mlflow

                with mlflow.start_run(run_name=f"{result.configuration_type}_{result.scenario_id}"):
                    mlflow.log_param("scenario_id", result.scenario_id)
                    mlflow.log_param("configuration_type", result.configuration_type)
                    mlflow.log_param("model_provider", result.model_provider)
                    mlflow.log_param("model_name", result.model_name)
                    mlflow.log_param("final_status", result.final_status)

                    mlflow.log_metric("execution_time_seconds", result.execution_time_seconds)
                    mlflow.log_metric("composite_score", result.scorecard.composite_score)

                    for m_name, m_val in result.scorecard.metrics.items():
                        if m_val.value is not None:
                            mlflow.log_metric(m_name, float(m_val.value))

                    if result.total_tokens:
                        mlflow.log_metric("total_tokens", float(result.total_tokens))
                    if result.estimated_cost_usd:
                        mlflow.log_metric("estimated_cost_usd", float(result.estimated_cost_usd))
            except Exception as e:
                logger.warning(f"[ExperimentTracker] Failed logging to MLflow: {e}")

    @classmethod
    def export_to_json(cls, results: list[ExperimentResult], file_path: str):
        """Export experiment results to JSON."""
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        data = [r.model_dump(mode="json") for r in results]
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logger.info(f"[ExperimentTracker] Exported {len(results)} experiments to {file_path}")

    @classmethod
    def export_to_csv(cls, results: list[ExperimentResult], file_path: str):
        """Export experiment summary metrics to CSV."""
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        if not results:
            return

        rows = []
        for r in results:
            row: dict[str, Any] = {
                "experiment_id": r.experiment_id,
                "scenario_id": r.scenario_id,
                "configuration_type": r.configuration_type,
                "model_provider": r.model_provider,
                "model_name": r.model_name,
                "execution_time_seconds": r.execution_time_seconds,
                "composite_score": r.scorecard.composite_score,
                "final_status": r.final_status,
                "passed": r.scorecard.passed,
            }
            for m_name, m_val in r.scorecard.metrics.items():
                if m_val.value is not None:
                    row[f"metric_{m_name}"] = m_val.value
            rows.append(row)

        fieldnames = list(rows[0].keys())
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        logger.info(f"[ExperimentTracker] Exported CSV summary to {file_path}")
