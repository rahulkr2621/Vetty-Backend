"""
Categories API router for cryptocurrency categories.

Provides endpoints for fetching cryptocurrency categories and related coins.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.services import CoinGeckoService
from app.auth import verify_jwt
from app.utils.logger import logger

router = APIRouter(prefix="/v1/categories", tags=["categories"], dependencies=[Depends(verify_jwt)])


@router.get("", response_model=list)
async def list_categories() -> list:
    """
    List all cryptocurrency categories.

    Returns:
        list: List of cryptocurrency categories with IDs and names.
    """
    try:
        service = CoinGeckoService()
        categories = await service.get_categories()

        # Format categories response
        formatted_categories = [
            {
                "category_id": cat.get("category_id"),
                "name": cat.get("name"),
                "market_cap_1h_change": cat.get("market_cap_1h_change"),
                "market_cap_24h_change": cat.get("market_cap_24h_change"),
                "market_cap_7d_change": cat.get("market_cap_7d_change"),
                "market_cap": cat.get("market_cap"),
            }
            for cat in categories
        ]

        logger.info(f"Retrieved {len(formatted_categories)} categories")
        return formatted_categories

    except Exception as e:
        logger.error(f"Error listing categories: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch categories"
        )
