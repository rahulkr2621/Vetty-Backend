"""
Health check service for monitoring application and third-party services.

Provides health status of the application and external API dependencies.
"""

from typing import Dict, Any
from datetime import datetime
from app.config import get_settings
from app.utils.http_client import HTTPClient
from app.utils.logger import logger


class HealthCheckService:
    """
    Service for monitoring application and third-party service health.

    Checks CoinGecko API availability and returns overall system health.
    """

    def __init__(self):
        """Initialize health check service."""
        self.settings = get_settings()

    async def check_coingecko_health(self) -> Dict[str, Any]:
        """
        Check CoinGecko API health.

        Returns:
            Dict[str, Any]: Health status with timestamp.
        """
        try:
            url = f"{self.settings.coingecko_api_url}/ping"
            params = {}

            if self.settings.coingecko_api_key:
                params["x_cg_pro_api_key"] = self.settings.coingecko_api_key

            await HTTPClient.get(url, params=params, timeout=self.settings.health_check_timeout)

            return {
                "status": "healthy",
                "service": "CoinGecko API",
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.warning(f"CoinGecko health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "service": "CoinGecko API",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def get_full_health(self) -> Dict[str, Any]:
        """
        Get comprehensive health status of application and services.

        Returns:
            Dict[str, Any]: Full health report with all service statuses.
        """
        coingecko_status = await self.check_coingecko_health()

        overall_status = "healthy" if coingecko_status["status"] == "healthy" else "degraded"

        return {
            "status": overall_status,
            "app": {
                "name": self.settings.app_name,
                "version": self.settings.app_version,
                "timestamp": datetime.utcnow().isoformat(),
            },
            "services": {"coingecko": coingecko_status},
        }
