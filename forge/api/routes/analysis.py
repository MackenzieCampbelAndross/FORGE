"""Analysis execution and report retrieval routes."""

import json
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from forge.core.logging import logger
from forge.orchestration.workflows import ForgeWorkflow
from forge.reporting.generator import ReportGenerator
from forge.schemas.report import EngineeringReport
from forge.schemas.requirements import ProjectObjective
from forge.storage.database import get_db
from forge.storage.repositories import AnalysisRepository, ProjectRepository, ReportRepository

router = APIRouter(prefix="/api/v1", tags=["Analysis"])


class AnalyzeRequest(BaseModel):
    project_id: str | None = Field(default=None)
    objective: str = Field(..., min_length=10, max_length=5000)
    domain: str | None = Field(default="General Software")
    context: str | None = Field(default="")
    constraints: list[str] = Field(default_factory=list)
    max_revisions: int = Field(default=3, ge=0, le=5)


class AnalyzeResponse(BaseModel):
    analysis_id: str
    project_id: str
    status: str
    message: str


class AnalysisStatusResponse(BaseModel):
    analysis_id: str
    project_id: str
    status: str
    latency_seconds: float
    revision_count: int
    error: str | None = None


@router.post("/analyze", response_model=AnalyzeResponse, status_code=status.HTTP_202_ACCEPTED)
def start_analysis(
    req: AnalyzeRequest,
    db: Session = Depends(get_db),
):
    """Trigger synchronous or background engineering analysis."""
    prj_id = req.project_id or f"PRJ-{uuid.uuid4().hex[:8].upper()}"
    analysis_id = f"ANL-{uuid.uuid4().hex[:8].upper()}"

    # Ensure project exists
    prj = ProjectRepository.get_by_id(db, prj_id)
    if not prj:
        ProjectRepository.create(
            db=db,
            project_id=prj_id,
            name=f"Project {prj_id}",
            objective=req.objective,
            domain=req.domain or "General Software",
            context=req.context or "",
        )

    AnalysisRepository.create(db=db, analysis_id=analysis_id, project_id=prj_id)

    # Execute workflow
    try:
        obj = ProjectObjective(
            project_id=prj_id,
            objective=req.objective,
            domain=req.domain,
            context=req.context,
            constraints=req.constraints,
        )
        workflow = ForgeWorkflow()
        state = workflow.run(obj, max_revisions=req.max_revisions)

        report: EngineeringReport | None = state.get("engineering_report")
        if not report:
            raise RuntimeError("Workflow finished without generating report.")

        meta = state.get("execution_metadata", {})
        latency = meta.get("total_workflow_latency_seconds", 0.0)
        rev_count = state.get("revision_count", 0)

        AnalysisRepository.update_status(
            db=db,
            analysis_id=analysis_id,
            status=report.final_status.value,
            latency=latency,
            revisions=rev_count,
        )

        md_content = ReportGenerator.generate_markdown(report)
        ReportRepository.save_report(
            db=db,
            report_id=report.report_id,
            analysis_id=analysis_id,
            project_id=prj_id,
            final_status=report.final_status.value,
            confidence_score=report.confidence_score,
            report_json=report.model_dump_json(),
            markdown_content=md_content,
        )

        return AnalyzeResponse(
            analysis_id=analysis_id,
            project_id=prj_id,
            status=report.final_status.value,
            message=f"Analysis completed successfully under status {report.final_status.value}.",
        )

    except Exception as e:
        logger.error(f"Analysis {analysis_id} failed: {e}", exc_info=True)
        AnalysisRepository.update_status(
            db=db,
            analysis_id=analysis_id,
            status="FAILED",
            error=str(e),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Engineering analysis failed. Check server logs.",
        ) from e


@router.get("/analysis/{analysis_id}", response_model=AnalysisStatusResponse)
def get_analysis_status(analysis_id: str, db: Session = Depends(get_db)):
    """Retrieve execution status of an analysis run."""
    model = AnalysisRepository.get_by_id(db, analysis_id)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis execution '{analysis_id}' not found.",
        )
    return AnalysisStatusResponse(
        analysis_id=model.id,
        project_id=model.project_id,
        status=model.status,
        latency_seconds=model.latency_seconds,
        revision_count=model.revision_count,
        error=model.error,
    )


@router.get("/analysis/{analysis_id}/report")
def get_analysis_report(
    analysis_id: str,
    format: str = Query(default="json", regex="^(json|markdown)$"),
    db: Session = Depends(get_db),
):
    """Retrieve generated engineering report in JSON or Markdown."""
    rep_model = ReportRepository.get_by_analysis_id(db, analysis_id)
    if not rep_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report for analysis '{analysis_id}' not found.",
        )

    if format == "markdown":
        return Response(content=rep_model.markdown_content, media_type="text/markdown")

    return json.loads(str(rep_model.report_json))
