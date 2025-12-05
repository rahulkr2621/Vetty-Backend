"""
Coins API router for cryptocurrency data endpoints.

Provides endpoints for fetching and filtering cryptocurrency coin data.
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from app.services import CoinGeckoService
from app.utils import PaginationParams, PaginatedResponse, PaginationHelper
from app.auth import verify_jwt
from app.utils.logger import logger

router = APIRouter(prefix="/v1/coins", tags=["coins"], dependencies=[Depends(verify_jwt)])


@router.get("", response_model=PaginatedResponse)
async def list_coins(
    page_num: int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=10, ge=1, le=100, description="Items per page"),
    order: str = Query(default="market_cap_desc", description="Ordering criteria"),
) -> PaginatedResponse:
    """
    List all cryptocurrency coins with pagination.

    Returns coins with market data in USD, INR, and CAD currencies.

    Query Parameters:
        - page_num: Page number (default: 1)
        - per_page: Items per page (default: 10, max: 100)
        - order: Sort order (default: market_cap_desc)

    Returns:
        PaginatedResponse: Paginated list of coins with market data.
    """
    try:
        pagination = PaginationParams(page_num=page_num, per_page=per_page)
        service = CoinGeckoService()

        coins_data = await service.get_all_coins(
            page=pagination.page_num, per_page=pagination.per_page, order=order
        )

        # Format response with essential market data
        formatted_coins = [
            {
                "id": coin.get("id"),
                "name": coin.get("name"),
                "symbol": coin.get("symbol").upper() if coin.get("symbol") else None,
                "market_cap_rank": coin.get("market_cap_rank"),
                "current_price": {
                    "usd": coin.get("current_price", {})
                    if isinstance(coin.get("current_price"), dict)
                    else coin.get("current_price"),
                    "inr": coin.get("current_price"),
                    "cad": coin.get("current_price"),
                },
                "market_cap": coin.get("market_cap"),
                "market_cap_change_24h": coin.get("market_cap_change_24h"),
            }
            for coin in coins_data
        ]

        logger.info(f"Retrieved {len(formatted_coins)} coins for page {pagination.page_num}")

        return PaginatedResponse.create(
            data=formatted_coins,
            total=len(formatted_coins),
            page_num=pagination.page_num,
            per_page=pagination.per_page,
        )
    except Exception as e:
        logger.error(f"Error listing coins: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch coins"
        )


@router.get("/filter", response_model=dict)
async def filter_coins(
    id: Optional[str] = Query(None, description="Coin ID to fetch"),
    category: Optional[str] = Query(None, description="Category to filter by"),
) -> dict:
    """
    Filter coins by ID or category.

    Query Parameters:
        - id: Specific coin ID (e.g., "bitcoin", "ethereum")
        - category: Category ID (e.g., "decentralized-exchange")

    Returns:
        dict: Filtered coin or category data with market information.
    """
    try:
        service = CoinGeckoService()

        if id:
            coin_data = await service.get_coin_by_id(id)
            logger.info(f"Filtered coin by ID: {id}")
            return {
                "id": coin_data.get("id"),
                "name": coin_data.get("name"),
                "symbol": coin_data.get("symbol", "").upper(),
                "description": coin_data.get("description", {}),
                "market_data": coin_data.get("market_data", {}),
                "links": coin_data.get("links", {}),
            }

        elif category:
            category_data = await service.get_category_by_id(category)
            logger.info(f"Filtered coins by category: {category}")
            return category_data

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either 'id' or 'category' parameter must be provided",
            )

    except Exception as e:
        logger.error(f"Error filtering coins: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to filter coins"
        )
