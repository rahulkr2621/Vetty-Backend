"""
Application configuration and settings management.
Uses environment variables with sensible defaults.
"""

from typing import List
from functools import lru_cache
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    This class defines all configuration parameters for the Deliverease Crypto API.
    Settings can be overridden via .env file or environment variables.
    """

    # Application
    app_name: str = Field(default="Deliverease Crypto API")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")

    # Server
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    # JWT
    jwt_secret_key: str = Field(
        default="your-super-secret-jwt-key-change-in-production-min-32-chars"
    )
    jwt_algorithm: str = Field(default="HS256")
    jwt_expiration_hours: int = Field(default=24)

    # CoinGecko API
    coingecko_api_url: str = Field(default="https://api.coingecko.com/api/v3")
    coingecko_api_key: str = Field(default="")

    # Pagination
    default_page_num: int = Field(default=1)
    default_per_page: int = Field(default=10)
    max_per_page: int = Field(default=100)

    # CORS
    allowed_origins: List[str] = Field(default=["http://localhost:3000", "http://localhost:8000"])

    # Database
    database_url: str = Field(default="sqlite:///./deliverease.db")

    # Health Check
    health_check_timeout: int = Field(default=5)

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v):
        """Parse allowed origins from comma-separated string."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Returns:
        Settings: Application settings singleton instance.
    """
    return Settings()
