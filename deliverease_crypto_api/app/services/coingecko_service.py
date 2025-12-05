"""
CoinGecko API service for cryptocurrency data.

Handles all interactions with the CoinGecko API for coin and market data.
"""

from typing import List, Dict, Any, Optional
from app.config import get_settings
from app.utils.http_client import HTTPClient
from app.utils.logger import logger


class CoinGeckoService:
    """
    Service for interacting with CoinGecko cryptocurrency API.

    Provides methods to fetch coin data, categories, and market information
    in multiple currencies (INR, CAD, USD).
    """

    def __init__(self):
        """Initialize CoinGecko service with configuration."""
        self.settings = get_settings()
        self.base_url = self.settings.coingecko_api_url
        self.api_key = self.settings.coingecko_api_key

    async def get_all_coins(
        self, page: int = 1, per_page: int = 10, order: str = "market_cap_desc"
    ) -> Dict[str, Any]:
        """
        Fetch paginated list of all coins.

        Args:
            page: Page number for pagination.
            per_page: Number of coins per page.
            order: Ordering criteria (default: market_cap_desc).

        Returns:
            Dict[str, Any]: List of coins with market data.

        Raises:
            Exception: If API request fails.
        """
        try:
            url = f"{self.base_url}/coins/markets"
            params = {
                "vs_currency": "usd,inr,cad",
                "order": order,
                "per_page": per_page,
                "page": page,
                "sparkline": False,
            }

            if self.api_key:
                params["x_cg_pro_api_key"] = self.api_key

            data = await HTTPClient.get(url, params=params)
            logger.info(f"Successfully fetched coins page {page}")
            return data
        except Exception as e:
            logger.error(f"Failed to fetch coins: {str(e)}")
            raise

    async def get_coin_by_id(self, coin_id: str) -> Dict[str, Any]:
        """
        Fetch detailed information for a specific coin.

        Args:
            coin_id: CoinGecko coin ID (e.g., "bitcoin", "ethereum").

        Returns:
            Dict[str, Any]: Detailed coin information with market data.

        Raises:
            Exception: If API request fails.
        """
        try:
            url = f"{self.base_url}/coins/{coin_id}"
            params = {
                "localization": False,
                "tickers": False,
                "market_data": True,
                "community_data": False,
                "developer_data": False,
            }

            if self.api_key:
                params["x_cg_pro_api_key"] = self.api_key

            data = await HTTPClient.get(url, params=params)
            logger.info(f"Successfully fetched coin: {coin_id}")
            return data
        except Exception as e:
            logger.error(f"Failed to fetch coin {coin_id}: {str(e)}")
            raise

    async def get_categories(self) -> List[Dict[str, Any]]:
        """
        Fetch all cryptocurrency categories.

        Returns:
            List[Dict[str, Any]]: List of cryptocurrency categories.

        Raises:
            Exception: If API request fails.
        """
        try:
            url = f"{self.base_url}/coins/categories"
            params = {}

            if self.api_key:
                params["x_cg_pro_api_key"] = self.api_key

            data = await HTTPClient.get(url, params=params)
            logger.info("Successfully fetched categories")
            return data
        except Exception as e:
            logger.error(f"Failed to fetch categories: {str(e)}")
            raise

    async def get_category_by_id(self, category_id: str) -> Dict[str, Any]:
        """
        Fetch coins in a specific category.

        Args:
            category_id: Category ID (e.g., "decentralized-exchange").

        Returns:
            Dict[str, Any]: Category with associated coins.

        Raises:
            Exception: If API request fails.
        """
        try:
            url = f"{self.base_url}/coins/categories/{category_id}"
            params = {}

            if self.api_key:
                params["x_cg_pro_api_key"] = self.api_key

            data = await HTTPClient.get(url, params=params)
            logger.info(f"Successfully fetched category: {category_id}")
            return data
        except Exception as e:
            logger.error(f"Failed to fetch category {category_id}: {str(e)}")
            raise

    async def search_coins(self, query: str) -> Dict[str, Any]:
        """
        Search for coins by name or symbol.

        Args:
            query: Search query string.

        Returns:
            Dict[str, Any]: Search results.

        Raises:
            Exception: If API request fails.
        """
        try:
            url = f"{self.base_url}/search"
            params = {"query": query}

            if self.api_key:
                params["x_cg_pro_api_key"] = self.api_key

            data = await HTTPClient.get(url, params=params)
            logger.info(f"Successfully searched for: {query}")
            return data
        except Exception as e:
            logger.error(f"Failed to search coins: {str(e)}")
            raise
