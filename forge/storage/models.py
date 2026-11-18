"""SQLAlchemy 2.x ORM models for persistent storage with modern Mapped types."""

from datetime import UTC, datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from forge.storage.database import Base


class ProjectModel(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    domain: Mapped[str] = mapped_column(String(128), default="General Software")
    objective: Mapped[str] = mapped_column(Text, nullable=False)
    context: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    executions: Mapped[list["AnalysisExecutionModel"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )


class AnalysisExecutionModel(Base):
    __tablename__ = "analysis_executions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(32), default="IN_PROGRESS")
    started_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    completed_at: Mapped[datetime | None] = mapped_column(default=None)
    latency_seconds: Mapped[float] = mapped_column(default=0.0)
    revision_count: Mapped[int] = mapped_column(default=0)
    error: Mapped[str | None] = mapped_column(Text, default=None)

    project: Mapped["ProjectModel"] = relationship(back_populates="executions")
    report: Mapped[Optional["EngineeringReportModel"]] = relationship(
        uselist=False, back_populates="execution", cascade="all, delete-orphan"
    )


class EngineeringReportModel(Base):
    __tablename__ = "engineering_reports"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    analysis_id: Mapped[str] = mapped_column(
        ForeignKey("analysis_executions.id"), nullable=False, unique=True, index=True
    )
    project_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    final_status: Mapped[str] = mapped_column(String(32), default="APPROVED")
    confidence_score: Mapped[float] = mapped_column(default=0.0)
    report_json: Mapped[str] = mapped_column(Text, nullable=False)
    markdown_content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    execution: Mapped["AnalysisExecutionModel"] = relationship(back_populates="report")


class ExperimentRecordModel(Base):
    __tablename__ = "experiment_records"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    scenario_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    config_type: Mapped[str] = mapped_column(String(64), nullable=False)
    composite_score: Mapped[float] = mapped_column(default=0.0)
    execution_time: Mapped[float] = mapped_column(default=0.0)
    status: Mapped[str] = mapped_column(String(32), default="SUCCESS")
    payload_json: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
