"""Data repository layer for database CRUD operations."""

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from forge.storage.models import (
    AnalysisExecutionModel,
    EngineeringReportModel,
    ExperimentRecordModel,
    ProjectModel,
)


class ProjectRepository:
    """CRUD operations for ProjectModel."""

    @classmethod
    def create(
        cls,
        db: Session,
        project_id: str,
        name: str,
        objective: str,
        domain: str = "",
        context: str = "",
    ) -> ProjectModel:
        prj = ProjectModel(
            id=project_id,
            name=name,
            domain=domain,
            objective=objective,
            context=context,
        )
        db.add(prj)
        db.commit()
        db.refresh(prj)
        return prj

    @classmethod
    def get_by_id(cls, db: Session, project_id: str) -> ProjectModel | None:
        return db.query(ProjectModel).filter(ProjectModel.id == project_id).first()

    @classmethod
    def list_all(cls, db: Session, skip: int = 0, limit: int = 100) -> list[ProjectModel]:
        return db.query(ProjectModel).offset(skip).limit(limit).all()


class AnalysisRepository:
    """CRUD operations for AnalysisExecutionModel."""

    @classmethod
    def create(cls, db: Session, analysis_id: str, project_id: str) -> AnalysisExecutionModel:
        exec_model = AnalysisExecutionModel(
            id=analysis_id,
            project_id=project_id,
            status="IN_PROGRESS",
        )
        db.add(exec_model)
        db.commit()
        db.refresh(exec_model)
        return exec_model

    @classmethod
    def update_status(
        cls,
        db: Session,
        analysis_id: str,
        status: str,
        latency: float = 0.0,
        revisions: int = 0,
        error: str | None = None,
    ) -> AnalysisExecutionModel | None:
        exec_model = (
            db.query(AnalysisExecutionModel)
            .filter(AnalysisExecutionModel.id == analysis_id)
            .first()
        )
        if exec_model:
            exec_model.status = status
            exec_model.completed_at = datetime.now(UTC)
            exec_model.latency_seconds = latency
            exec_model.revision_count = revisions
            exec_model.error = error
            db.commit()
            db.refresh(exec_model)
        return exec_model

    @classmethod
    def get_by_id(cls, db: Session, analysis_id: str) -> AnalysisExecutionModel | None:
        return (
            db.query(AnalysisExecutionModel)
            .filter(AnalysisExecutionModel.id == analysis_id)
            .first()
        )


class ReportRepository:
    """CRUD operations for EngineeringReportModel."""

    @classmethod
    def save_report(
        cls,
        db: Session,
        report_id: str,
        analysis_id: str,
        project_id: str,
        final_status: str,
        confidence_score: float,
        report_json: str,
        markdown_content: str,
    ) -> EngineeringReportModel:
        rep = EngineeringReportModel(
            id=report_id,
            analysis_id=analysis_id,
            project_id=project_id,
            final_status=final_status,
            confidence_score=confidence_score,
            report_json=report_json,
            markdown_content=markdown_content,
        )
        db.add(rep)
        db.commit()
        db.refresh(rep)
        return rep

    @classmethod
    def get_by_analysis_id(cls, db: Session, analysis_id: str) -> EngineeringReportModel | None:
        return (
            db.query(EngineeringReportModel)
            .filter(EngineeringReportModel.analysis_id == analysis_id)
            .first()
        )


class ExperimentRepository:
    """CRUD operations for ExperimentRecordModel."""

    @classmethod
    def record_experiment(
        cls,
        db: Session,
        experiment_id: str,
        scenario_id: str,
        config_type: str,
        composite_score: float,
        execution_time: float,
        status: str,
        payload_json: str,
    ) -> ExperimentRecordModel:
        rec = ExperimentRecordModel(
            id=experiment_id,
            scenario_id=scenario_id,
            config_type=config_type,
            composite_score=composite_score,
            execution_time=execution_time,
            status=status,
            payload_json=payload_json,
        )
        db.add(rec)
        db.commit()
        db.refresh(rec)
        return rec

    @classmethod
    def get_by_id(cls, db: Session, experiment_id: str) -> ExperimentRecordModel | None:
        return (
            db.query(ExperimentRecordModel)
            .filter(ExperimentRecordModel.id == experiment_id)
            .first()
        )
