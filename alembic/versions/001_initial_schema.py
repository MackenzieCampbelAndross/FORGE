"""Initial schema migration for FORGE v1.0.

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-11-17 01:20:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "001_initial_schema"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "projects",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("domain", sa.String(length=128), nullable=True),
        sa.Column("objective", sa.Text(), nullable=False),
        sa.Column("context", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_index(op.f("ix_projects_id"), "projects", ["id"], unique=False)

    op.create_table(
        "analysis_executions",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("project_id", sa.String(length=64), sa.ForeignKey("projects.id"), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("latency_seconds", sa.Float(), nullable=True),
        sa.Column("revision_count", sa.Integer(), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
    )
    op.create_index(op.f("ix_analysis_executions_id"), "analysis_executions", ["id"], unique=False)
    op.create_index(
        op.f("ix_analysis_executions_project_id"),
        "analysis_executions",
        ["project_id"],
        unique=False,
    )

    op.create_table(
        "engineering_reports",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column(
            "analysis_id",
            sa.String(length=64),
            sa.ForeignKey("analysis_executions.id"),
            nullable=False,
            unique=True,
        ),
        sa.Column("project_id", sa.String(length=64), nullable=False),
        sa.Column("final_status", sa.String(length=32), nullable=True),
        sa.Column("confidence_score", sa.Float(), nullable=True),
        sa.Column("report_json", sa.Text(), nullable=False),
        sa.Column("markdown_content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_index(op.f("ix_engineering_reports_id"), "engineering_reports", ["id"], unique=False)
    op.create_index(
        op.f("ix_engineering_reports_analysis_id"),
        "engineering_reports",
        ["analysis_id"],
        unique=True,
    )
    op.create_index(
        op.f("ix_engineering_reports_project_id"),
        "engineering_reports",
        ["project_id"],
        unique=False,
    )

    op.create_table(
        "experiment_records",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("scenario_id", sa.String(length=64), nullable=False),
        sa.Column("config_type", sa.String(length=64), nullable=False),
        sa.Column("composite_score", sa.Float(), nullable=True),
        sa.Column("execution_time", sa.Float(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=True),
        sa.Column("payload_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_index(op.f("ix_experiment_records_id"), "experiment_records", ["id"], unique=False)
    op.create_index(
        op.f("ix_experiment_records_scenario_id"),
        "experiment_records",
        ["scenario_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_table("experiment_records")
    op.drop_table("engineering_reports")
    op.drop_table("analysis_executions")
    op.drop_table("projects")
