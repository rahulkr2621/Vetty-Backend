"""
Health check API router for system monitoring.

Provides endpoints for checking application and service health status.
"""

from fastapi import APIRouter, HTTPException, status
from app.services import HealthCheckService
from app.utils.logger import logger

router = APIRouter(tags=["health"])


@router.get("/health", response_model=dict)
async def health_check() -> dict:
    """
    Check application and third-party service health.

    This endpoint is NOT protected by JWT authentication.
    It returns the health status of the application and external services.

    Returns:
        dict: Health status with service information.
    """
    try:
        service = HealthCheckService()
        health = await service.get_full_health()
        logger.info("Health check completed")
        return health
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Health check failed"
        )


@router.get("/version", response_model=dict)
async def version_info() -> dict:
    """
    Get application version and info.

    This endpoint is NOT protected by JWT authentication.
    Returns version information and metadata about the API.

    Returns:
        dict: Version information and metadata.
    """
    from app.config import get_settings

    settings = get_settings()

    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug,
        "api_version": "v1",
        "documentation": "/docs",
    }
