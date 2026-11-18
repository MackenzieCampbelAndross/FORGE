"""Unit tests for database error rollback and repository query filtering."""

import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from forge.storage.database import SessionLocal, init_db
from forge.storage.repositories import ProjectRepository


def test_database_rollback_on_duplicate_id() -> None:
    """Verify primary key conflict triggers IntegrityError and session recovers after rollback."""
    init_db()
    db = SessionLocal()
    prj_id = f"PRJ-ROLLBACK-{uuid.uuid4().hex[:6]}"

    try:
        # 1. Create first record
        ProjectRepository.create(
            db=db,
            project_id=prj_id,
            name="Rollback Test Initial",
            objective="Initial objective",
        )

        # 2. Duplicate insertion must fail with IntegrityError
        with pytest.raises(IntegrityError):
            ProjectRepository.create(
                db=db,
                project_id=prj_id,
                name="Duplicate Collision",
                objective="Duplicate objective",
            )

        db.rollback()

        # 3. Verify session is still valid and initial record is intact
        found = ProjectRepository.get_by_id(db, prj_id)
        assert found is not None
        assert found.name == "Rollback Test Initial"

    finally:
        db.close()


def test_project_repository_pagination() -> None:
    """Verify limit and skip parameters in ProjectRepository.list_all."""
    init_db()
    db = SessionLocal()
    try:
        prefix = uuid.uuid4().hex[:4]
        for i in range(5):
            ProjectRepository.create(
                db=db,
                project_id=f"PRJ-PAGE-{prefix}-{i}",
                name=f"Page Project {i}",
                objective="Pagination check",
            )

        page_1 = ProjectRepository.list_all(db, skip=0, limit=2)
        assert len(page_1) == 2

        page_2 = ProjectRepository.list_all(db, skip=2, limit=2)
        assert len(page_2) == 2
        assert page_1[0].id != page_2[0].id
    finally:
        db.close()
