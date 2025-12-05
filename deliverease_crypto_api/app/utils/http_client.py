"""
HTTP client utilities for making external API calls.

Provides helper functions for HTTP requests with error handling.
"""

from typing import Optional, Dict, Any
import httpx
from app.utils.logger import logger


class HTTPClient:
    """
    HTTP client wrapper for making API calls.

    Handles request/response processing and error handling.
    """

    @staticmethod
    async def get(
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: int = 10,
    ) -> Dict[str, Any]:
        """
        Make async GET request.

        Args:
            url: Request URL.
            headers: Optional HTTP headers.
            params: Optional query parameters.
            timeout: Request timeout in seconds.

        Returns:
            Dict[str, Any]: Response JSON data.

        Raises:
            httpx.RequestError: If request fails.
        """
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(url, headers=headers, params=params)
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            logger.error(f"HTTP request failed to {url}: {str(e)}")
            raise

    @staticmethod
    async def post(
        url: str,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 10,
    ) -> Dict[str, Any]:
        """
        Make async POST request.

        Args:
            url: Request URL.
            json: Optional JSON body.
            headers: Optional HTTP headers.
            timeout: Request timeout in seconds.

        Returns:
            Dict[str, Any]: Response JSON data.

        Raises:
            httpx.RequestError: If request fails.
        """
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(url, json=json, headers=headers)
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            logger.error(f"HTTP request failed to {url}: {str(e)}")
            raise
