"""
Auth Service - Main Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from apps.auth_service.src.api.routes import auth, oauth2, sessions
from apps.auth_service.src.core.config import settings
from apps.auth_service.src.core.logging import setup_logging
from apps.auth_service.src.infrastructure.database.connection import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация при старте приложения"""
    # Startup
    setup_logging()
    await init_db()
    yield
    # Shutdown
    pass


app = FastAPI(
    title="Auth Service",
    description="Authentication and Authorization Service",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(
    oauth2.router, prefix="/api/v1/auth/oauth2", tags=["oauth2"])
app.include_router(
    sessions.router, prefix="/api/v1/auth/sessions", tags=["sessions"])


@app.get("/health/live")
async def health_live():
    """Liveness probe"""
    return {"status": "alive"}


@app.get("/health/ready")
async def health_ready():
    """Readiness probe"""
    return {"status": "ready"}
