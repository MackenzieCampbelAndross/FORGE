"""FastAPI application factory and server entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from forge.api.routes import analysis, evaluation, health, projects
from forge.core.config import settings
from forge.core.exceptions import ForgeError
from forge.core.logging import logger
from forge.storage.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown routines."""
    logger.info(f"Starting {settings.app_name} v{settings.version}...")
    init_db()
    yield
    logger.info(f"Shutting down {settings.app_name}...")


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Automated System Design, Threat Modeling, and Architecture Engineering Intelligence Platform.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ForgeError)
async def forge_exception_handler(request: Request, exc: ForgeError):
    """Handle domain-specific exceptions safely without leaking stack traces."""
    logger.error(
        f"Domain error processing {request.url.path}: {exc.message}",
        extra={"extra_fields": exc.details},
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "details": exc.details,
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Fallback handler for unhandled exceptions."""
    logger.critical(f"Unhandled server error processing {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "message": "An internal error occurred. Please contact systems engineering.",
        },
    )


# Include sub-routers
app.include_router(health.router)
app.include_router(projects.router)
app.include_router(analysis.router)
app.include_router(evaluation.router)
