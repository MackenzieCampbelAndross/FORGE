"""Evaluation and benchmark API routes."""

import json
import os

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from forge.benchmark.loader import BenchmarkLoader
from forge.benchmark.runner import BenchmarkRunner
from forge.storage.database import get_db
from forge.storage.repositories import ExperimentRepository

router = APIRouter(prefix="/api/v1", tags=["Evaluation & Benchmark"])

DATASET_FILE = "forge/benchmark/scenarios/feb_v1_dataset.jsonl"


class RunEvaluationRequest(BaseModel):
    scenario_id: str | None = Field(default=None)
    category: str | None = Field(default=None)
    limit: int | None = Field(default=5, ge=1, le=100)


@router.post("/evaluation/run", status_code=status.HTTP_200_OK)
def run_evaluation(req: RunEvaluationRequest, db: Session = Depends(get_db)):
    """Run benchmark evaluation suite across selected scenarios."""
    if not os.path.exists(DATASET_FILE):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="FEB dataset file not found."
        )

    all_scenarios = BenchmarkLoader.load_from_file(DATASET_FILE)

    if req.scenario_id:
        target_scenarios = [s for s in all_scenarios if s.scenario_id == req.scenario_id]
        if not target_scenarios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Scenario '{req.scenario_id}' not found in FEB dataset.",
            )
    elif req.category:
        target_scenarios = [
            s for s in all_scenarios if s.category.value.lower() == req.category.lower()
        ]
    else:
        target_scenarios = all_scenarios

    runner = BenchmarkRunner()
    summary = runner.run_suite(target_scenarios, limit=req.limit)

    # Persist experiment records
    for r in summary["results"]:
        ExperimentRepository.record_experiment(
            db=db,
            experiment_id=r["experiment_id"],
            scenario_id=r["scenario_id"],
            config_type=r["configuration_type"],
            composite_score=r["scorecard"]["composite_score"],
            execution_time=r["execution_time_seconds"],
            status=r["final_status"],
            payload_json=json.dumps(r),
        )

    return summary


@router.get("/evaluation/{experiment_id}")
def get_evaluation_experiment(experiment_id: str, db: Session = Depends(get_db)):
    """Retrieve details of an evaluation experiment."""
    rec = ExperimentRepository.get_by_id(db, experiment_id)
    if not rec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Experiment '{experiment_id}' not found."
        )
    return json.loads(str(rec.payload_json))


@router.get("/benchmark/summary")
def get_benchmark_summary():
    """Retrieve validation summary of the FEB v1.0 benchmark dataset."""
    if not os.path.exists(DATASET_FILE):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="FEB dataset file not found."
        )

    scenarios = BenchmarkLoader.load_from_file(DATASET_FILE)
    validation = BenchmarkLoader.validate_dataset(scenarios)
    return {
        "dataset_name": "FORGE Engineering Benchmark (FEB)",
        "version": "1.0.0",
        "validation": validation,
    }
