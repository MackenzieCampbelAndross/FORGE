"""Integration tests for SQLAlchemy storage models and repositories."""

import uuid

from forge.storage.database import SessionLocal, init_db
from forge.storage.repositories import (
    AnalysisRepository,
    ExperimentRepository,
    ProjectRepository,
    ReportRepository,
)


def test_database_repositories_flow():
    init_db()
    db = SessionLocal()
    try:
        prj_id = f"PRJ-TEST-{uuid.uuid4().hex[:6]}"
        prj = ProjectRepository.create(
            db=db,
            project_id=prj_id,
            name="Test Persistence Project",
            objective="Verify relational persistence",
        )
        assert prj.id == prj_id

        anl_id = f"ANL-TEST-{uuid.uuid4().hex[:6]}"
        anl = AnalysisRepository.create(db=db, analysis_id=anl_id, project_id=prj_id)
        assert anl.id == anl_id

        AnalysisRepository.update_status(
            db=db, analysis_id=anl_id, status="APPROVED", latency=0.5, revisions=1
        )
        updated_anl = AnalysisRepository.get_by_id(db, anl_id)
        assert updated_anl.status == "APPROVED"
        assert updated_anl.revision_count == 1

        rep_id = f"REP-TEST-{uuid.uuid4().hex[:6]}"
        rep = ReportRepository.save_report(
            db=db,
            report_id=rep_id,
            analysis_id=anl_id,
            project_id=prj_id,
            final_status="APPROVED",
            confidence_score=0.95,
            report_json='{"status": "APPROVED"}',
            markdown_content="# Report",
        )
        assert rep.id == rep_id

        fetched_rep = ReportRepository.get_by_analysis_id(db, anl_id)
        assert fetched_rep is not None
        assert fetched_rep.final_status == "APPROVED"

        exp_id = f"EXP-TEST-{uuid.uuid4().hex[:6]}"
        exp = ExperimentRepository.record_experiment(
            db=db,
            experiment_id=exp_id,
            scenario_id="FEB-001",
            config_type="FORGE_V1",
            composite_score=95.0,
            execution_time=1.2,
            status="SUCCESS",
            payload_json="{}",
        )
        assert exp.id == exp_id
    finally:
        db.close()
