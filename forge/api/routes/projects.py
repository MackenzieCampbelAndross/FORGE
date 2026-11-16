"""Project management API routes."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from forge.storage.database import get_db
from forge.storage.repositories import ProjectRepository

router = APIRouter(prefix="/api/v1/projects", tags=["Projects"])


class CreateProjectRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    objective: str = Field(..., min_length=10, max_length=5000)
    domain: str | None = Field(default="General Software", max_length=100)
    context: str | None = Field(default="", max_length=5000)


class ProjectResponse(BaseModel):
    id: str
    name: str
    domain: str
    objective: str
    context: str
    created_at: str


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(req: CreateProjectRequest, db: Session = Depends(get_db)):
    """Create a new engineering analysis project."""
    prj_id = f"PRJ-{uuid.uuid4().hex[:8].upper()}"
    model = ProjectRepository.create(
        db=db,
        project_id=prj_id,
        name=req.name,
        objective=req.objective,
        domain=req.domain or "General Software",
        context=req.context or "",
    )
    return ProjectResponse(
        id=model.id,
        name=model.name,
        domain=model.domain,
        objective=model.objective,
        context=model.context,
        created_at=model.created_at.isoformat(),
    )


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str, db: Session = Depends(get_db)):
    """Retrieve an existing project by identifier."""
    model = ProjectRepository.get_by_id(db, project_id)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Project '{project_id}' not found."
        )
    return ProjectResponse(
        id=model.id,
        name=model.name,
        domain=model.domain,
        objective=model.objective,
        context=model.context,
        created_at=model.created_at.isoformat(),
    )
