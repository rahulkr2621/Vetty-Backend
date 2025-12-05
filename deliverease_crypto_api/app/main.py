"""
Deliverease Crypto API - Main Application File

A production-ready REST API for cryptocurrency data using FastAPI.
Built with clean architecture, JWT authentication, and comprehensive testing.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.utils import setup_logging
from app.routers import coins, categories, health, auth

# Setup logging
logger = setup_logging()

# Get settings
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifespan events.

    Handles startup and shutdown logic for the FastAPI application.
    """
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    yield
    # Shutdown
    logger.info(f"Shutting down {settings.app_name}")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Production-ready Cryptocurrency REST API with JWT authentication",
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(health.router)  # Health endpoints (no auth required)
app.include_router(auth.router)  # Auth endpoints
app.include_router(coins.router)  # Coins endpoints (JWT protected)
app.include_router(categories.router)  # Categories endpoints (JWT protected)


@app.get("/", tags=["root"])
async def root() -> dict:
    """
    Root endpoint providing API information.

    Returns:
        dict: API metadata and available endpoints.
    """
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "documentation": "/docs",
        "available_endpoints": {
            "auth": "/v1/auth/login",
            "health": "/health",
            "version": "/version",
            "coins": "/v1/coins",
            "categories": "/v1/categories",
            "filter": "/v1/coins/filter",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app=app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower(),
        reload=settings.debug,
    )
