"""Health check and system readiness endpoints."""

from fastapi import APIRouter

from forge.core.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    """System health and readiness probe."""
    return {
        "status": "HEALTHY",
        "service": settings.app_name,
        "version": settings.version,
        "environment": settings.environment,
        "provider": settings.model_provider,
    }
