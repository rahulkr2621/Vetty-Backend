"""
Pagination utilities for handling paginated API responses.

Provides pagination helpers with validation and response formatting.
"""

from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel, Field
from app.config import get_settings

T = TypeVar("T")


class PaginationParams(BaseModel):
    """
    Pagination query parameters.

    Attributes:
        page_num: Page number (1-indexed), minimum 1.
        per_page: Items per page, validated against max_per_page setting.
    """

    page_num: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    per_page: int = Field(default=10, ge=1, le=100, description="Items per page")

    def __init__(self, page_num: int = None, per_page: int = None, **data):
        """Initialize pagination with defaults and validation."""
        settings = get_settings()

        if page_num is None:
            page_num = settings.default_page_num
        if per_page is None:
            per_page = settings.default_per_page

        # Cap per_page at max allowed
        per_page = min(per_page, settings.max_per_page)

        super().__init__(page_num=page_num, per_page=per_page, **data)

    def get_offset(self) -> int:
        """
        Calculate database offset for pagination.

        Returns:
            int: Offset value for SQL queries.
        """
        return (self.page_num - 1) * self.per_page


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Generic paginated API response wrapper.

    Attributes:
        data: List of items for current page.
        total: Total number of items across all pages.
        page_num: Current page number.
        per_page: Items per page.
        total_pages: Total number of pages.
    """

    data: List[T]
    total: int
    page_num: int
    per_page: int
    total_pages: int

    @classmethod
    def create(
        cls, data: List[T], total: int, page_num: int, per_page: int
    ) -> "PaginatedResponse[T]":
        """
        Create paginated response with calculated total pages.

        Args:
            data: List of items for current page.
            total: Total number of items.
            page_num: Current page number.
            per_page: Items per page.

        Returns:
            PaginatedResponse: Formatted paginated response.
        """
        total_pages = (total + per_page - 1) // per_page  # Ceiling division
        return cls(
            data=data, total=total, page_num=page_num, per_page=per_page, total_pages=total_pages
        )


class PaginationHelper:
    """Helper methods for pagination operations."""

    @staticmethod
    def paginate_list(items: List[T], page_num: int, per_page: int) -> tuple[List[T], int]:
        """
        Paginate a list of items in-memory.

        Args:
            items: Complete list to paginate.
            page_num: Desired page number.
            per_page: Items per page.

        Returns:
            tuple: (paginated_items, total_count)
        """
        total = len(items)
        offset = (page_num - 1) * per_page
        end = offset + per_page
        paginated = items[offset:end]
        return paginated, total
